import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { OBJLoader } from     'three/addons/loaders/OBJLoader.js';
import { PLYLoader } from 'three/addons/loaders/PLYLoader.js';
import { GUI } from           'three/addons/libs/lil-gui.module.min.js';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';

let num_objects_curr = 0;
let num_objects = 100;


const layers = {
	'Toggle Name': function () {
		console.log('toggle')
		camera.layers.toggle(0);
	}
}

function onDoubleClick(event) {
	mouse.x = ( event.clientX / window.innerWidth ) * 2 - 1;
	mouse.y = - ( event.clientY / window.innerHeight ) * 2 + 1;
	raycaster.setFromCamera( mouse, camera );
	let intersections = raycaster.intersectObjects( [ threejs_objects['scene0451_01'] ] );
	intersection = ( intersections.length ) > 0 ? intersections[ 0 ] : null;
	console.log(intersections);
}

function get_lines(properties){
    var geometry = new THREE.BufferGeometry();
    let binary_filename = properties['binary_filename'];
    var positions = [];
    let num_lines = properties['num_lines'];

    fetch(binary_filename)
    .then(response => response.arrayBuffer())
    .then(buffer => {
        positions = new Float32Array(buffer, 0, 3 * num_lines * 2);
        let colors_uint8 = new Uint8Array(buffer, (3 * num_lines * 2) * 4, 3 * num_lines * 2);
        let colors_float32 = Float32Array.from(colors_uint8);
        for (let i=0; i<colors_float32.length; i++) {
         	colors_float32[i] /= 255.0;
        }
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors_float32, 3));
    }).then(step_progress_bar).then(render);
	var material = new THREE.LineBasicMaterial({color: 0xFFFFFF, vertexColors: true});
	return new THREE.LineSegments( geometry, material );
}

function get_cube(){
	let cube_geometry = new THREE.BoxGeometry(1, 5, 1);
	let cube_material = new THREE.MeshPhongMaterial({color: 0x00ffff});
	cube_material.wireframe = false;
	cube_material.wireframeLinewidth = 5;
	let cube = new THREE.Mesh(cube_geometry, cube_material);
	return cube
}

function add_progress_bar(){
    let gProgressElement = document.createElement("div");
    const html_code = '<div class="progress">\n' +
		'<div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 0%" id="progress_bar"></div>\n' +
		'</div>';
    gProgressElement.innerHTML = html_code;
    gProgressElement.id = "progress_bar_id"
    gProgressElement.style.left = "20%";
    gProgressElement.style.right = "20%";
    gProgressElement.style.position = "fixed";
    gProgressElement.style.top = "50%";
    document.body.appendChild(gProgressElement);
}

function step_progress_bar(){
	num_objects_curr += 1.0
	let progress_int = parseInt(num_objects_curr / num_objects * 100.0)
	let width_string = String(progress_int)+'%';
	document.getElementById('progress_bar').style.width = width_string;
	document.getElementById('progress_bar').innerText = width_string;

	if (progress_int==100) {
		document.getElementById( 'progress_bar_id' ).innerHTML = "";
	}
}

function add_watermark(){
	let watermark = document.createElement("div");
    const html_code = '<a href="https://francisengelmann.github.io/pyviz3d/" target="_blank"><b>PyViz3D</b></a>';
    watermark.innerHTML = html_code;
    watermark.id = "watermark"
    watermark.style.right = "5px";
    watermark.style.position = "fixed";
    watermark.style.bottom = "5px";
    watermark.style.color = "#999";
    watermark.style.fontSize = "7ox";
    document.body.appendChild(watermark);
}

function set_camera_properties(properties){
	camera.setFocalLength(properties['focal_length']);
	console.log(camera.getFocalLength);
	camera.up.set(properties['up'][0],
		          properties['up'][1],
				  properties['up'][2]);
	camera.position.set(properties['position'][0],
						properties['position'][1],
						properties['position'][2]);
	update_controls();
	controls.update();
	controls.target = new THREE.Vector3(properties['look_at'][0],
	 	                                properties['look_at'][1],
	 						    		properties['look_at'][2]);
	camera.updateProjectionMatrix();
	controls.update();
}

function get_points(properties){
	// Add points
	// https://github.com/mrdoob/three.js/blob/master/examples/webgl_buffergeometry_points.html
	let positions = [];
	let normals = [];
	let num_points = properties['num_points'];
	let geometry = new THREE.BufferGeometry();
	let binary_filename = properties['binary_filename'];

	fetch(binary_filename)
	    .then(response => response.arrayBuffer())
		.then(buffer => {
			positions = new Float32Array(buffer, 0, 3 * num_points);
			normals = new Float32Array(buffer, (3 * num_points) * 4, 3 * num_points);
		    let colors_uint8 = new Uint8Array(buffer, (3 * num_points) * 8, 3 * num_points);
		    let colors_float32 = Float32Array.from(colors_uint8);
		    for(let i=0; i<colors_float32.length; i++) {
			    colors_float32[i] /= 255.0;
			}
		    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
			geometry.setAttribute('normal', new THREE.Float32BufferAttribute(normals, 3));
			geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors_float32, 3));
		})
		.then(step_progress_bar)
        .then(render);

	 let uniforms = {
        pointSize: { value: properties['point_size'] },
		alpha: {value: properties['alpha']},
		shading_type: {value: properties['shading_type']},
     };

	 let material = new THREE.ShaderMaterial( {
		uniforms:       uniforms,
        vertexShader:   document.getElementById( 'vertexshader' ).textContent,
        fragmentShader: document.getElementById( 'fragmentshader' ).textContent,
        transparent:    true});

	let points = new THREE.Points(geometry, material);
	return points
}

function get_labels(properties){
	const labels = new THREE.Group();
	labels.name = "labels"
	for (let i=0; i<properties['labels'].length; i++){
		const labelDiv = document.createElement('div');
		labelDiv.className = 'label';
		labelDiv.style.color = "rgb("+properties['colors'][i][0]+", "+properties['colors'][i][1]+", "+properties['colors'][i][2]+")"; 
		labelDiv.textContent = properties['labels'][i];
	
		const label_2d = new CSS2DObject(labelDiv);
		label_2d.position.set(properties['positions'][i][0], properties['positions'][i][1], properties['positions'][i][2]);
		labels.add(label_2d);
	}
	return labels
}

function get_circles_2d(properties){
	const labels = new THREE.Group();
	labels.name = "labels"
	for (let i=0; i<properties['labels'].length; i++){
		const border_color = "rgb("+properties['border_colors'][i][0]+", "+properties['border_colors'][i][1]+", "+properties['border_colors'][i][2]+")";
		const fill_color = "rgb("+properties['fill_colors'][i][0]+", "+properties['fill_colors'][i][1]+", "+properties['fill_colors'][i][2]+")";
		const labelDiv = document.createElement('div');
		labelDiv.className = 'label';
		labelDiv.textContent = properties['labels'][i];
		labelDiv.style.border = '3px solid '+border_color;
		labelDiv.style.backgroundColor = fill_color;
		labelDiv.style.borderRadius = '30px';
		const label_2d = new CSS2DObject(labelDiv);
		label_2d.position.set(properties['positions'][i][0], properties['positions'][i][1], properties['positions'][i][2]);
		labels.add(label_2d);
	}
	return labels
}

function get_mesh(properties){
	var container = new THREE.Object3D();
	function loadModel(geometry) {
		let object;
		let r = properties['color'][0]
		let g = properties['color'][1]
		let b = properties['color'][2]
		let colorString = "rgb("+r+","+g+", "+b+")"
		if (geometry.isObject3D) {  // obj
			object = geometry;
			object.traverse(
				function(child) {
					if (child.isMesh) {
						child.material.color.set(new THREE.Color(colorString));
					}
				});
		} else {  // ply
			const materialShader = (geometry.hasAttribute('normal')) ? THREE.MeshPhongMaterial : THREE.MeshBasicMaterial
			const material = new materialShader({vertexColors: geometry.hasAttribute('color')})
			if (!geometry.hasAttribute){
				material.color.set(new THREE.Color(colorString));
			}
			object = new THREE.Mesh(geometry, material);
		}

		object.scale.set(properties['scale'][0], properties['scale'][1], properties['scale'][2])
		object.setRotationFromQuaternion(new THREE.Quaternion(properties['rotation'][0], properties['rotation'][1], properties['rotation'][2], properties['rotation'][3]))
		object.position.set(properties['translation'][0], properties['translation'][1], properties['translation'][2])
		container.add(object)
		step_progress_bar();
		render();
	}
	const filename_extension = properties['filename'].split('.').pop()
	console.log(filename_extension)

	let loader;
	if (filename_extension === 'ply'){
		loader = new PLYLoader();
	} else if (filename_extension === 'obj'){
		loader = new OBJLoader();
	} else {
		console.log( 'Unknown mesh extension: ' + filename_extension);
	}
	loader.load(properties['filename'], loadModel,
				function (xhr){ // called when loading is in progresses
					console.log( ( xhr.loaded / xhr.total * 100 ) + '% loaded' );
				},
				function (error){ // called when loading has errors
					console.log( 'An error happened: ' + error );
				});
	return container
}

function get_superquadric(properties){
	// Generate superquadric mesh procedurally from parameters
	let geometry = new THREE.BufferGeometry();
	let scalings = properties['scalings'];
	let exponents = properties['exponents'];
	let resolution = properties['resolution'];
	let tapering = properties['tapering'];
	let bending = properties['bending'];

	// Helper functions for superquadric surface
	function f(o, m) {
		let sin_o = Math.sin(o);
		return Math.sign(sin_o) * Math.pow(Math.abs(sin_o), m);
	}

	function g(o, m) {
		let cos_o = Math.cos(o);
		return Math.sign(cos_o) * Math.pow(Math.abs(cos_o), m);
	}

	// Helper function for bending transformation
	function apply_bending_axis(x, y, z, val_kb, val_alpha, axis) {
		if (Math.abs(val_kb) < 1e-3) return {x: x, y: y, z: z};
		
		let u, v_coord, w;
		if (axis === 'z') {
			u = x; v_coord = y; w = z;
		} else if (axis === 'x') {
			u = y; v_coord = z; w = x;
		} else if (axis === 'y') {
			u = z; v_coord = x; w = y;
		}
		
		let sin_alpha = Math.sin(val_alpha);
		let cos_alpha = Math.cos(val_alpha);
		
		let beta = Math.atan2(v_coord, u);
		let r = Math.sqrt(u*u + v_coord*v_coord) * Math.cos(val_alpha - beta);
		
		// Clamp kb (simplified version - proper clamping would need array operations)
		let inv_kb = 1.0 / val_kb;
		let gamma = w * val_kb;
		let rho = inv_kb - r;
		let R = inv_kb - rho * Math.cos(gamma);
		
		let expr = (R - r);
		u = u + expr * cos_alpha;
		v_coord = v_coord + expr * sin_alpha;
		w = rho * Math.sin(gamma);
		
		if (axis === 'z') {
			return {x: u, y: v_coord, z: w};
		} else if (axis === 'x') {
			return {x: w, y: u, z: v_coord};
		} else if (axis === 'y') {
			return {x: v_coord, y: w, z: u};
		}
	}

	// Generate vertices using simple uniform sampling
	let positions = [];
	let indices = [];
	let A = scalings[0], B = scalings[1], C = scalings[2];
	let r = exponents[0], s = exponents[1], t = exponents[2];
	let N = Math.max(10, Math.min(Math.round((resolution || 30) * 0.8), 50));

	function deform_vertex(x, y, z) {
		// Apply tapering
		if (tapering && (Math.abs(tapering[0]) > 1e-6 || Math.abs(tapering[1]) > 1e-6)) {
			let z_norm = z / C;
			let fx = tapering[0] * z_norm + 1.0;
			let fy = tapering[1] * z_norm + 1.0;
			x = x * fx;
			y = y * fy;
		}

		// Apply bending (y-axis, then x-axis, then z-axis)
		if (bending) {
			let result = apply_bending_axis(x, y, z, bending[4], bending[5], 'y');
			x = result.x; y = result.y; z = result.z;
			result = apply_bending_axis(x, y, z, bending[2], bending[3], 'x');
			x = result.x; y = result.y; z = result.z;
			result = apply_bending_axis(x, y, z, bending[0], bending[1], 'z');
			x = result.x; y = result.y; z = result.z;
		}

		// Apply rotation matrix if provided
		if (properties['rotation_matrix']) {
			let R = properties['rotation_matrix'];
			let x_rot = R[0][0] * x + R[0][1] * y + R[0][2] * z;
			let y_rot = R[1][0] * x + R[1][1] * y + R[1][2] * z;
			let z_rot = R[2][0] * x + R[2][1] * y + R[2][2] * z;
			x = x_rot;
			y = y_rot;
			z = z_rot;
		}

		return {x: x, y: y, z: z};
	}

	// Arc-length parameterization: find parameter values that produce
	// equally-spaced points on the actual 3D surface curve.
	function arc_length_sample(param_start, param_end, n_out, eval_fn) {
		// 1. Densely sample the curve to approximate arc length
		let n_dense = 500;
		let dense_params = new Array(n_dense);
		let dense_pts = new Array(n_dense);
		for (let i = 0; i < n_dense; i++) {
			let t = param_start + (param_end - param_start) * i / (n_dense - 1);
			dense_params[i] = t;
			dense_pts[i] = eval_fn(t);
		}

		// 2. Compute cumulative chord lengths
		let cum_len = new Array(n_dense);
		cum_len[0] = 0;
		for (let i = 1; i < n_dense; i++) {
			let dx = dense_pts[i][0] - dense_pts[i - 1][0];
			let dy = dense_pts[i][1] - dense_pts[i - 1][1];
			let dz = dense_pts[i][2] - dense_pts[i - 1][2];
			cum_len[i] = cum_len[i - 1] + Math.sqrt(dx * dx + dy * dy + dz * dz);
		}

		let total_len = cum_len[n_dense - 1];
		if (total_len < 1e-12) {
			// Degenerate curve, fall back to uniform
			let result = new Array(n_out);
			for (let i = 0; i < n_out; i++) {
				result[i] = param_start + (param_end - param_start) * i / (n_out - 1);
			}
			return result;
		}

		// 3. Invert: for each desired equal arc-length, find corresponding parameter
		let result = new Array(n_out);
		result[0] = param_start;
		result[n_out - 1] = param_end;
		let j = 0;
		for (let i = 1; i < n_out - 1; i++) {
			let target_len = total_len * i / (n_out - 1);
			// Advance j until we bracket the target
			while (j < n_dense - 2 && cum_len[j + 1] < target_len) j++;
			// Linear interpolation between dense_params[j] and dense_params[j+1]
			let seg_len = cum_len[j + 1] - cum_len[j];
			let frac = seg_len > 1e-15 ? (target_len - cum_len[j]) / seg_len : 0;
			result[i] = dense_params[j] + frac * (dense_params[j + 1] - dense_params[j]);
		}
		return result;
	}

	// Sample u at the equator (v=0) for arc-length parameterization
	let u_samples = arc_length_sample(-Math.PI, Math.PI, N, function(u) {
		let x = A * g(0, r) * g(u, s);
		let y = B * g(0, r) * f(u, s);
		let z = C * f(0, t);
		return [x, y, z];
	});

	// Sample v at the prime meridian (u=0) for arc-length parameterization
	let v_samples = arc_length_sample(-Math.PI * 0.5, Math.PI * 0.5, N, function(v) {
		let x = A * g(v, r) * g(0, s);
		let y = B * g(v, r) * f(0, s);
		let z = C * f(v, t);
		return [x, y, z];
	});

	function build_mesh(u_samp, v_samp) {
		let pos = [];
		let idx = [];
		let pMap = new Map();
		let cnt = 0;
		let nu = u_samp.length;
		let nv = v_samp.length;
		
		for (let j = 0; j < nv; j++) {
			for (let i = 0; i < nu; i++) {
				let u = u_samp[i % nu];
				let v = v_samp[j % nv];
				let x = A * g(v, r) * g(u, s);
				let y = B * g(v, r) * f(u, s);
				let z = C * f(v, t);
				let p = deform_vertex(x, y, z);
				pos.push(p.x, p.y, p.z);
				pMap.set(i + ',' + j, cnt++);
			}
		}
		
		for (let j = 0; j < nv - 1; j++) {
			for (let i = 0; i < nu - 1; i++) {
				let i00 = pMap.get(i + ',' + j);
				let i10 = pMap.get((i + 1) + ',' + j);
				let i11 = pMap.get((i + 1) + ',' + (j + 1));
				let i01 = pMap.get(i + ',' + (j + 1));
				idx.push(i00, i10, i11, i00, i11, i01);
			}
			// Connect seam
			let iLast = nu - 1;
			let i00 = pMap.get(iLast + ',' + j);
			let i10 = pMap.get(0 + ',' + j);
			let i11 = pMap.get(0 + ',' + (j + 1));
			let i01 = pMap.get(iLast + ',' + (j + 1));
			idx.push(i00, i10, i11, i00, i11, i01);
		}
		return {pos: pos, idx: idx};
	}

	// Resample the grid so all edges are equal length on the actual 3D surface.
	// For each v-row, compute arc lengths along u, then redistribute u params equally.
	// Then for each u-column, compute arc lengths along v, redistribute v params equally.
	function resample_grid(u_samp, v_samp) {
		let nu = u_samp.length;
		let nv = v_samp.length;

		// Evaluate a surface point (before deformation, since we parameterize pre-deform)
		function eval_pt(u, v) {
			let x = A * g(v, r) * g(u, s);
			let y = B * g(v, r) * f(u, s);
			let z = C * f(v, t);
			let p = deform_vertex(x, y, z);
			return [p.x, p.y, p.z];
		}

		function dist3(a, b) {
			let dx = a[0]-b[0], dy = a[1]-b[1], dz = a[2]-b[2];
			return Math.sqrt(dx*dx + dy*dy + dz*dz);
		}

		// Step 1: For each v value, resample u by arc length
		// Average the arc-length distributions across all v-rows
		let u_cum = new Float64Array(nu); // averaged cumulative arc lengths
		for (let j = 0; j < nv; j++) {
			let v = v_samp[j];
			let prev = eval_pt(u_samp[0], v);
			let row_cum = 0;
			for (let i = 1; i < nu; i++) {
				let cur = eval_pt(u_samp[i], v);
				row_cum += dist3(prev, cur);
				u_cum[i] += row_cum;
				prev = cur;
			}
		}
		for (let i = 0; i < nu; i++) u_cum[i] /= nv;

		let u_total = u_cum[nu - 1];
		let new_u = new Array(nu);
		new_u[0] = u_samp[0];
		new_u[nu - 1] = u_samp[nu - 1];
		if (u_total > 1e-12) {
			let k = 0;
			for (let i = 1; i < nu - 1; i++) {
				let target = u_total * i / (nu - 1);
				while (k < nu - 2 && u_cum[k + 1] < target) k++;
				let seg = u_cum[k + 1] - u_cum[k];
				let frac = seg > 1e-15 ? (target - u_cum[k]) / seg : 0;
				new_u[i] = u_samp[k] + frac * (u_samp[k + 1] - u_samp[k]);
			}
		} else {
			new_u = u_samp.slice();
		}

		// Step 2: For each u value, resample v by arc length
		let v_cum = new Float64Array(nv);
		for (let i = 0; i < nu; i++) {
			let u = new_u[i];
			let prev = eval_pt(u, v_samp[0]);
			let col_cum = 0;
			for (let j = 1; j < nv; j++) {
				let cur = eval_pt(u, v_samp[j]);
				col_cum += dist3(prev, cur);
				v_cum[j] += col_cum;
				prev = cur;
			}
		}
		for (let j = 0; j < nv; j++) v_cum[j] /= nu;

		let v_total = v_cum[nv - 1];
		let new_v = new Array(nv);
		new_v[0] = v_samp[0];
		new_v[nv - 1] = v_samp[nv - 1];
		if (v_total > 1e-12) {
			let k = 0;
			for (let j = 1; j < nv - 1; j++) {
				let target = v_total * j / (nv - 1);
				while (k < nv - 2 && v_cum[k + 1] < target) k++;
				let seg = v_cum[k + 1] - v_cum[k];
				let frac = seg > 1e-15 ? (target - v_cum[k]) / seg : 0;
				new_v[j] = v_samp[k] + frac * (v_samp[k + 1] - v_samp[k]);
			}
		} else {
			new_v = v_samp.slice();
		}

		return {u: new_u, v: new_v};
	}

	// Subdivide in high-curvature areas by inserting midpoints where
	// normals change direction rapidly between adjacent grid cells
	function subdivide_high_curvature(u_samp, v_samp) {
		let nu = u_samp.length;
		let nv = v_samp.length;

		function eval_pt(u, v) {
			let x = A * g(v, r) * g(u, s);
			let y = B * g(v, r) * f(u, s);
			let z = C * f(v, t);
			let p = deform_vertex(x, y, z);
			return [p.x, p.y, p.z];
		}

		// Compute normals at each grid point via central differences
		let normals = new Array(nu * nv);
		let eps = 1e-4;
		for (let j = 0; j < nv; j++) {
			for (let i = 0; i < nu; i++) {
				let u = u_samp[i], v = v_samp[j];
				let du_p = eval_pt(u + eps, v), du_m = eval_pt(u - eps, v);
				let dv_p = eval_pt(u, v + eps), dv_m = eval_pt(u, v - eps);
				let tu = [(du_p[0]-du_m[0]), (du_p[1]-du_m[1]), (du_p[2]-du_m[2])];
				let tv = [(dv_p[0]-dv_m[0]), (dv_p[1]-dv_m[1]), (dv_p[2]-dv_m[2])];
				// Cross product tu x tv
				let nx = tu[1]*tv[2] - tu[2]*tv[1];
				let ny = tu[2]*tv[0] - tu[0]*tv[2];
				let nz = tu[0]*tv[1] - tu[1]*tv[0];
				let len = Math.sqrt(nx*nx + ny*ny + nz*nz);
				if (len > 1e-12) { nx /= len; ny /= len; nz /= len; }
				normals[j * nu + i] = [nx, ny, nz];
			}
		}

		// For each grid edge, compute dot product of adjacent normals.
		// Small dot product = high curvature = insert midpoint.
		let u_set = new Set(u_samp);
		let v_set = new Set(v_samp);

		// Check u-edges (along rows)
		for (let j = 0; j < nv; j++) {
			for (let i = 0; i < nu - 1; i++) {
				let n1 = normals[j * nu + i];
				let n2 = normals[j * nu + i + 1];
				let dot = n1[0]*n2[0] + n1[1]*n2[1] + n1[2]*n2[2];
				if (dot < 0.95) { // normal changes by > ~18 degrees
					u_set.add((u_samp[i] + u_samp[i + 1]) * 0.5);
				}
			}
		}

		// Check v-edges (along columns)
		for (let i = 0; i < nu; i++) {
			for (let j = 0; j < nv - 1; j++) {
				let n1 = normals[j * nu + i];
				let n2 = normals[(j + 1) * nu + i];
				let dot = n1[0]*n2[0] + n1[1]*n2[1] + n1[2]*n2[2];
				if (dot < 0.95) {
					v_set.add((v_samp[j] + v_samp[j + 1]) * 0.5);
				}
			}
		}

		return {
			u: Array.from(u_set).sort((a, b) => a - b),
			v: Array.from(v_set).sort((a, b) => a - b)
		};
	}

	// Iteratively resample to converge on equal-edge-length grid
	let cur_u = u_samples;
	let cur_v = v_samples;
	for (let iter = 0; iter < 5; iter++) {
		let resampled = resample_grid(cur_u, cur_v);
		cur_u = resampled.u;
		cur_v = resampled.v;
	}

	// Subdivide high-curvature regions, then re-equalize
	let subdiv = subdivide_high_curvature(cur_u, cur_v);
	cur_u = subdiv.u;
	cur_v = subdiv.v;
	for (let iter = 0; iter < 3; iter++) {
		let resampled = resample_grid(cur_u, cur_v);
		cur_u = resampled.u;
		cur_v = resampled.v;
	}

	let final_mesh = build_mesh(cur_u, cur_v);
	positions = final_mesh.pos;
	indices = final_mesh.idx;

	geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
	geometry.setIndex(indices);
	geometry.computeVertexNormals();

	// Set vertex colors
	let r_color = Math.fround(properties['color'][0] / 255.0);
	let g_color = Math.fround(properties['color'][1] / 255.0);
	let b_color = Math.fround(properties['color'][2] / 255.0);
	let num_vertices = positions.length / 3;
	let colors = new Float32Array(num_vertices * 3);
	for (let i = 0; i < num_vertices; i++){
		colors[3 * i + 0] = r_color;
		colors[3 * i + 1] = g_color;
		colors[3 * i + 2] = b_color;
	}
	geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

	let uniforms = {
		alpha: {value: properties['alpha']},
		shading_type: {value: 1},
	};
	let material = new THREE.ShaderMaterial({
		uniforms:       uniforms,
		vertexShader:   document.getElementById('vertexshader').textContent,
		fragmentShader: document.getElementById('fragmentshader').textContent,
		transparent:    true,
		side: THREE.DoubleSide,
	});

	let mesh = new THREE.Mesh(geometry, material);
	mesh.setRotationFromQuaternion(new THREE.Quaternion(
		properties['rotation'][0],
		properties['rotation'][1],
		properties['rotation'][2],
		properties['rotation'][3]
	));
	mesh.position.set(properties['translation'][0], properties['translation'][1], properties['translation'][2]);

	// Add wireframe if requested
	if (properties['wireframe']) {
		let wireframeGeometry = new THREE.WireframeGeometry(geometry);
		let wireframeMaterial = new THREE.LineBasicMaterial({ 
			color: 0x000000,
			linewidth: 1,
			opacity: 0.5,
			transparent: true
		});
		let wireframe = new THREE.LineSegments(wireframeGeometry, wireframeMaterial);
		mesh.add(wireframe);
	}

	step_progress_bar();
	render();

	return mesh;
}


function get_material(alpha){
	let uniforms = {
		alpha: {value: alpha},
		shading_type: {value: 1},
	};
	let material = new THREE.ShaderMaterial({
		uniforms:       uniforms,
		vertexShader:   document.getElementById('vertexshader').textContent,
		fragmentShader: document.getElementById('fragmentshader').textContent,
		transparent:    true,
    });
    return material;
}

function set_geometry_vertex_color(geometry, color){
	const r = Math.fround(color[0] / 255.0);
	const g = Math.fround(color[1] / 255.0);
	const b = Math.fround(color[2] / 255.0);
	const num_vertices = geometry.getAttribute('position').count;
	const colors = new Float32Array(num_vertices * 3);
	for (let i = 0; i < num_vertices; i++){
		colors[3 * i + 0] = r;
		colors[3 * i + 1] = g;
		colors[3 * i + 2] = b;
	}
	geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
}

function get_cylinder_geometry(radius_top, radius_bottom, height, radial_segments, color){
	let geometry = new THREE.CylinderGeometry(radius_top, radius_bottom, height, radial_segments);
	set_geometry_vertex_color(geometry, color)
	return geometry;
}

function get_sphere_geometry(radius, widthSegments, heightSegments, color){
	const geometry = new THREE.SphereGeometry(radius, widthSegments, heightSegments);
	set_geometry_vertex_color(geometry, color);
	return geometry;
}

function get_cuboid(properties){
	const radius_top = properties['edge_width'];
	const radius_bottom = properties['edge_width'];
	const radial_segments = 30;
	const height = 1;
	
	let geometry = get_cylinder_geometry(
		radius_top, radius_bottom, height, radial_segments,
		properties['color']);
	let material = get_material(properties['alpha']);

	const cylinder_x = new THREE.Mesh(geometry, material);
	cylinder_x.scale.set(1.0, properties['size'][0], 1.0)
	cylinder_x.rotateZ(3.1415/2.0)
	const cylinder_00 = cylinder_x.clone()
	cylinder_00.position.set(0, -properties['size'][1]/2.0, -properties['size'][2]/2.0)
	const cylinder_01 = cylinder_x.clone()
	cylinder_01.position.set(0, properties['size'][1]/2.0, -properties['size'][2]/2.0)
	const cylinder_20 = cylinder_x.clone()
	cylinder_20.position.set(0, -properties['size'][1]/2.0, properties['size'][2]/2.0)
	const cylinder_21 = cylinder_x.clone()
	cylinder_21.position.set(0, properties['size'][1]/2.0, properties['size'][2]/2.0)

	const cylinder_y = new THREE.Mesh(geometry, material);
	cylinder_y.scale.set(1.0, properties['size'][1], 1.0)
	const cylinder_02 = cylinder_y.clone()
	cylinder_02.position.set(-properties['size'][0]/2.0, 0, -properties['size'][2]/2.0)
	const cylinder_03 = cylinder_y.clone()
	cylinder_03.position.set(properties['size'][0]/2.0, 0, -properties['size'][2]/2.0)
	const cylinder_22 = cylinder_y.clone()
	cylinder_22.position.set(-properties['size'][0]/2.0, 0, properties['size'][2]/2.0)
	const cylinder_23 = cylinder_y.clone()
	cylinder_23.position.set(properties['size'][0]/2.0, 0, properties['size'][2]/2.0)

	const cylinder_z = new THREE.Mesh(geometry, material);
	cylinder_z.scale.set(1.0, properties['size'][2], 1.0)
	cylinder_z.rotateX(3.1415/2.0)
	const cylinder_10 = cylinder_z.clone()
	cylinder_10.position.set(-properties['size'][0]/2.0, -properties['size'][1]/2.0, 0.0)
	const cylinder_11 = cylinder_z.clone()
	cylinder_11.position.set(properties['size'][0]/2.0, -properties['size'][1]/2.0, 0.0)
	const cylinder_12 = cylinder_z.clone()
	cylinder_12.position.set(-properties['size'][0]/2.0, properties['size'][1]/2.0, 0.0)
	const cylinder_13 = cylinder_z.clone()
	cylinder_13.position.set(properties['size'][0]/2.0, properties['size'][1]/2.0, 0.0)

	let corner_geometry = get_sphere_geometry(properties['edge_width'], 30, 30, properties['color']);

	const sphere = new THREE.Mesh(corner_geometry, material);
	const corner_00 = sphere.clone()
	corner_00.position.set(-properties['size'][0]/2.0, -properties['size'][1]/2.0, -properties['size'][2]/2.0)
	const corner_01 = sphere.clone()
	corner_01.position.set(properties['size'][0]/2.0, -properties['size'][1]/2.0, -properties['size'][2]/2.0)
	const corner_02 = sphere.clone()
	corner_02.position.set(-properties['size'][0]/2.0, properties['size'][1]/2.0, -properties['size'][2]/2.0)
	const corner_03 = sphere.clone()
	corner_03.position.set(properties['size'][0]/2.0, properties['size'][1]/2.0, -properties['size'][2]/2.0)
	const corner_10 = sphere.clone()
	corner_10.position.set(-properties['size'][0]/2.0, -properties['size'][1]/2.0, properties['size'][2]/2.0)
	const corner_11 = sphere.clone()
	corner_11.position.set(properties['size'][0]/2.0, -properties['size'][1]/2.0, properties['size'][2]/2.0)
	const corner_12 = sphere.clone()
	corner_12.position.set(-properties['size'][0]/2.0, properties['size'][1]/2.0, properties['size'][2]/2.0)
	const corner_13 = sphere.clone()
	corner_13.position.set(properties['size'][0]/2.0, properties['size'][1]/2.0, properties['size'][2]/2.0)

	const cuboid = new THREE.Group();
	cuboid.position.set(properties['position'][0], properties['position'][1], properties['position'][2])
	cuboid.add(cylinder_00)
	cuboid.add(cylinder_01)
	cuboid.add(cylinder_20)
	cuboid.add(cylinder_21)
	cuboid.add(cylinder_02)
	cuboid.add(cylinder_03)
	cuboid.add(cylinder_22)
	cuboid.add(cylinder_23)
	cuboid.add(cylinder_10)
	cuboid.add(cylinder_11)
	cuboid.add(cylinder_12)
	cuboid.add(cylinder_13)

	cuboid.add(corner_00)
	cuboid.add(corner_01)
	cuboid.add(corner_02)
	cuboid.add(corner_03)
	cuboid.add(corner_10)
	cuboid.add(corner_11)
	cuboid.add(corner_12)
	cuboid.add(corner_13)

	const q = new THREE.Quaternion(
			properties['orientation'][0],
			properties['orientation'][1],
			properties['orientation'][2],
			properties['orientation'][3])
	cuboid.setRotationFromQuaternion(q)
	cuboid.position.set(properties['position'][0], properties['position'][1], properties['position'][2])
	return cuboid
}

function get_polyline(properties){
	const radius_top = properties['edge_width']
	const radius_bottom = properties['edge_width']
	const radial_segments = 5;
	const height = 1;
	let material = get_material(properties['alpha']);
	let geometry = get_cylinder_geometry(radius_top, radius_bottom, height, radial_segments, properties['color']);
	const cylinder = new THREE.Mesh(geometry, material);
	let corner_geometry = get_sphere_geometry(properties['edge_width'], radial_segments, radial_segments, properties['color']);
	const sphere = new THREE.Mesh(corner_geometry, material);
	const polyline = new THREE.Group();

	// Add first corner to the polyline
	const corner_0 = sphere.clone()
	corner_0.position.set(properties['positions'][0][0], properties['positions'][0][1], properties['positions'][0][2])
	polyline.add(corner_0)

	for (var i=1; i < properties['positions'].length; i++){
		// Put the sphere the make a nice round corner
		const corner_i = sphere.clone()
		corner_i.position.set(properties['positions'][i][0],
			                  properties['positions'][i][1],
			                  properties['positions'][i][2])

		// Put a segment connecting the two last points
		const cylinder_i = cylinder.clone()
		var dist_x = properties['positions'][i][0] - properties['positions'][i-1][0]
		var dist_y = properties['positions'][i][1] - properties['positions'][i-1][1]
		var dist_z = properties['positions'][i][2] - properties['positions'][i-1][2]
		var cylinder_length = Math.sqrt(dist_x*dist_x + dist_y*dist_y + dist_z*dist_z)
		cylinder_i.scale.set(1.0, cylinder_length, 1.0)
		cylinder_i.lookAt(properties['positions'][i][0] - properties['positions'][i-1][0],
	                      properties['positions'][i][1] - properties['positions'][i-1][1],
	                      properties['positions'][i][2] - properties['positions'][i-1][2])
		cylinder_i.rotateX(3.1415/2.0)
		cylinder_i.position.set(properties['positions'][i-1][0],
			                    properties['positions'][i-1][1],
		                        properties['positions'][i-1][2])
		cylinder_i.translateY(cylinder_length/2.0)
		polyline.add(cylinder_i)
	}

	return polyline
}

function get_arrow(properties){
	const radius_top = 0.0;
	const radius_bottom = properties['head_width'];
	const radial_segments = 15;
	const height = radius_bottom * 2.0;

	var dist_x = properties['end'][0] - properties['start'][0]
	var dist_y = properties['end'][1] - properties['start'][1]
	var dist_z = properties['end'][2] - properties['start'][2]
	var margnitude = Math.sqrt(dist_x*dist_x + dist_y*dist_y + dist_z*dist_z)

	let material = get_material(properties['alpha']);
	let geometry = get_cylinder_geometry(radius_top, radius_bottom, height, radial_segments, properties['color']);
	let geometry_stroke = get_cylinder_geometry(properties['stroke_width'], properties['stroke_width'], margnitude - height, radial_segments, properties['color']);

	const arrow_head = new THREE.Mesh(geometry, material);
	arrow_head.translateY(margnitude - height / 2.0)
	const arrow_stroke = new THREE.Mesh(geometry_stroke, material);
	arrow_stroke.translateY(margnitude / 2.0 - height / 2.0)

	const arrow = new THREE.Group();
	arrow.add(arrow_head);
	arrow.add(arrow_stroke);

	arrow.lookAt(properties['end'][0] - properties['start'][0],
		              properties['end'][1] - properties['start'][1],
		              properties['end'][2] - properties['start'][2])
	arrow.rotateX(3.1415/2.0)
	arrow.position.set(properties['start'][0], properties['start'][1], properties['start'][2] )
	return arrow;
}

function get_three_color(color) {
	if (color[0] > 1. || color[1] > 1. || color[2] > 1. ) {
		color[0] = color[0] / 255.
		color[1] = color[1] / 255.
		color[2] = color[2] / 255.
	}

	return new THREE.Color( color[0], color[1], color[2] )
}

function vector3ToArray(vector) {
	return [vector.x, vector.y, vector.z];
}

function threejsColorToArray(vector) {
	return [vector.r*255, vector.g*255, vector.b*255];
}

function get_motion(properties) {
	var motion_type = properties['motion_type']
	var motion_origin_pos_temp = properties['motion_origin_pos']
	var motion_origin_pos = new THREE.Vector3(motion_origin_pos_temp[0], motion_origin_pos_temp[1], motion_origin_pos_temp[2]);
	var motion_direction_temp = properties['motion_direction']
	var motion_direction = new THREE.Vector3(motion_direction_temp[0], motion_direction_temp[1], motion_direction_temp[2]);
	var motion_viz_orient = properties['motion_viz_orient']
	var motion_dir_color = get_three_color(properties['motion_dir_color'])
	var motion_origin_color = get_three_color(properties['motion_origin_color'])
	let annotation_motion_group = new THREE.Group();
	
	let motion_origin_pos_ = new THREE.Vector3(motion_origin_pos.x, motion_origin_pos.y, motion_origin_pos.z);
	let motion_direction_ = motion_direction.clone()
	motion_direction_.normalize()

	let arrow_len = 0.5;
	let originSphereRadius = 0.02;

	const originGeometry = new THREE.SphereGeometry( originSphereRadius, 16); 
	const originMaterial = new THREE.MeshBasicMaterial( { color: motion_origin_color } ); 
	const originSphere = new THREE.Mesh( originGeometry, originMaterial ); 
	originSphere.position.copy(motion_origin_pos_);

	annotation_motion_group.add(originSphere)

	let torusPos;
	if (motion_type === "rot") {
		let torusDir = motion_direction_.clone()
		torusDir.multiplyScalar(arrow_len/2)

		torusPos = new THREE.Vector3();
		torusPos.addVectors(motion_origin_pos_, torusDir);
	}

	let pseudoOrigin = motion_origin_pos_.clone()
	if (motion_viz_orient === "inwards") {
		let arrowDirection = motion_direction_.clone()
		pseudoOrigin.addScaledVector(arrowDirection, -arrow_len);

		if (motion_type === "rot") {
			torusPos.addScaledVector(arrowDirection, -arrow_len);
		}
	}

	if (motion_type === "rot") {
		const geometry = new THREE.TorusGeometry( 0.04, 0.008, 16, 100 ); 
		const material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } ); 
		const torus = new THREE.Mesh( geometry, material ); 

		const normal = new THREE.Vector3(0, 0, 1); // The normal vector in the direction you want the ring's normal to point (z-axis in this case)

		const quaternion = new THREE.Quaternion();
		quaternion.setFromUnitVectors(normal, motion_direction_);
		torus.setRotationFromQuaternion(quaternion);
		torus.position.copy(torusPos);
		annotation_motion_group.add(torus)
	}

	let arrow_start = motion_origin_pos.clone()
	
	let arrow_end = motion_origin_pos.clone()
	if (motion_viz_orient === "inwards") {
		arrow_start.addScaledVector(motion_direction_, -(0.5+0.02));

		arrow_end.addScaledVector(motion_direction_, -(0.02));
	}
    else {
		arrow_start.addScaledVector(motion_direction_, (0.02));

		arrow_end.addScaledVector(motion_direction_, (0.5+0.02));
	}

	const arrow_properties = {
		'start': vector3ToArray(arrow_start),
		'end': vector3ToArray(arrow_end),
		'color': threejsColorToArray(motion_dir_color),
		'alpha': 0.85,
		'stroke_width': 0.04*0.25,
		'head_width': 0.2*0.2,
	}
	const arrow = get_arrow(arrow_properties)
	annotation_motion_group.add(arrow)

	return annotation_motion_group
}

function get_ground(){
	let mesh = new THREE.Mesh(new THREE.PlaneBufferGeometry(2000, 2000),
							  new THREE.MeshPhongMaterial({ color: 0x999999, depthWrite: true}));
	mesh.rotation.x = -Math.PI / 2;
	mesh.position.set(0, -5, 0);
	mesh.receiveShadow = true;
	return mesh;
}



function init_gui(objects){
	let menuMap = new Map();
	for (const [name, value] of Object.entries(objects)){
		let splits = name.split(';');
		if (splits.length > 1) {
			let folder_name = splits[0];
			if (!menuMap.has(folder_name)) {
				menuMap.set(folder_name, gui.addFolder(folder_name));
			}
			let fol = menuMap.get(folder_name);
			fol.add(value, 'visible').name(splits[1]).onChange(render);
			fol.open();
		} else {
			if (value.name.localeCompare('labels') != 0) {
				gui.add(value, 'visible').name(name).onChange(render);
			}
		}
	}
}

function render() {
    renderer.render(scene, camera);
	labelRenderer.render(scene, camera);
}

function init(){
	scene.background = new THREE.Color(0xffffff);
	renderer.setSize(window.innerWidth, window.innerHeight);
	labelRenderer.setSize(window.innerWidth, window.innerHeight);

	let hemiLight = new THREE.HemisphereLight( 0xffffff, 0x444444 );
	hemiLight.position.set(0, 20, 0);
	//scene.add(hemiLight);

	let dirLight = new THREE.DirectionalLight( 0xffffff );
	dirLight.position.set(-10, 10, - 10);
	dirLight.castShadow = true;
	dirLight.shadow.camera.top = 2;
	dirLight.shadow.camera.bottom = - 2;
	dirLight.shadow.camera.left = - 2;
	dirLight.shadow.camera.right = 2;
	dirLight.shadow.camera.near = 0.1;
	dirLight.shadow.camera.far = 40;
	//scene.add(dirLight);

	let intensity = 0.5;
	let color = 0xffffff;
	const spotLight1 = new THREE.SpotLight(color, intensity);
	spotLight1.position.set(100, 1000, 0);
	scene.add(spotLight1);
	const spotLight2 = new THREE.SpotLight(color, intensity/3.0);
	spotLight2.position.set(100, -1000, 0);
	scene.add(spotLight2);
	const spotLight3 = new THREE.SpotLight(color, intensity);
	spotLight3.position.set(0, 100, 1000);
	scene.add(spotLight3);
	const spotLight4 = new THREE.SpotLight(color, intensity/3.0);
	spotLight4.position.set(0, 100, -1000);
	scene.add(spotLight4);
	const spotLight5 = new THREE.SpotLight(color, intensity);
	spotLight5.position.set(1000, 0, 100);
	scene.add(spotLight5);
	const spotLight6 = new THREE.SpotLight(color, intensity/3.0);
	spotLight6.position.set(-1000, 0, 100);
	scene.add(spotLight6);

	raycaster = new THREE.Raycaster();
	raycaster.params.Points.threshold = 1.0;
}

function create_threejs_objects(properties){

	num_objects_curr = 0.0;
	num_objects = parseFloat(Object.entries(properties).length);

	for (const [object_name, object_properties] of Object.entries(properties)) {
		if (String(object_properties['type']).localeCompare('camera') == 0){
			set_camera_properties(object_properties);
			render();
    		step_progress_bar();
    		continue;
		}
		if (String(object_properties['type']).localeCompare('points') == 0){
			threejs_objects[object_name] = get_points(object_properties);
    		render();
		}
		if (String(object_properties['type']).localeCompare('labels') == 0){
			threejs_objects[object_name] = get_labels(object_properties);
			step_progress_bar();
			render();
		}
		if (String(object_properties['type']).localeCompare('circles_2d') == 0){
			threejs_objects[object_name] = get_circles_2d(object_properties);
			step_progress_bar();
			render();
		}
		if (String(object_properties['type']).localeCompare('lines') == 0){
			threejs_objects[object_name] = get_lines(object_properties);
    		render();
		}
		if (String(object_properties['type']).localeCompare('obj') == 0){
			threejs_objects[object_name] = get_obj(object_properties);
		}
		if (String(object_properties['type']).localeCompare('ply') == 0){
			threejs_objects[object_name] = get_ply(object_properties);
		}
		if (String(object_properties['type']).localeCompare('mesh') == 0){
			threejs_objects[object_name] = get_mesh(object_properties);
		}
		if (String(object_properties['type']).localeCompare('cuboid') == 0){
			threejs_objects[object_name] = get_cuboid(object_properties);
			step_progress_bar();
			render();
		}
		if (String(object_properties['type']).localeCompare('polyline') == 0){
			threejs_objects[object_name] = get_polyline(object_properties);
			step_progress_bar();
			render();
		}
		if (String(object_properties['type']).localeCompare('arrow') == 0){
			threejs_objects[object_name] = get_arrow(object_properties);
			step_progress_bar();
			render();
		}
		if (String(object_properties['type']).localeCompare('motion') == 0){
			threejs_objects[object_name] = get_motion(object_properties);
			step_progress_bar();
			render();
		}
		if (String(object_properties['type']).localeCompare('superquadric') == 0){
			threejs_objects[object_name] = get_superquadric(object_properties);
			render();
		}
		threejs_objects[object_name].visible = object_properties['visible'];
		threejs_objects[object_name].frustumCulled = false;
	}
	
	// Add axis helper
	threejs_objects['Axis'] = new THREE.AxesHelper(1);

	render();
}

function add_threejs_objects_to_scene(threejs_objects){
	for (const [key, value] of Object.entries(threejs_objects)) {
		scene.add(value);
	}
}

function onWindowResize(){
    const innerWidth = window.innerWidth
    const innerHeight = window.innerHeight;
    renderer.setSize(innerWidth, innerHeight);
    labelRenderer.setSize(innerWidth, innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    render();
}

function update_controls(){
	controls = new OrbitControls(camera, labelRenderer.domElement);
	controls.addEventListener("change", render);
	controls.enableKeys = true;
	controls.enablePan = true; // enable dragging
}

const scene = new THREE.Scene();

const renderer = new THREE.WebGLRenderer({antialias: true});
document.getElementById('render_container').appendChild(renderer.domElement)

var camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.01, 1000);
var controls = '';

let labelRenderer = new CSS2DRenderer();
labelRenderer.setSize( window.innerWidth, window.innerHeight );
labelRenderer.domElement.style.position = 'absolute';
labelRenderer.domElement.style.top = '0px';
document.getElementById('render_container').appendChild(labelRenderer.domElement)

window.addEventListener('resize', onWindowResize, false);

let raycaster;
let intersection = null;
let mouse = new THREE.Vector2();

const gui = new GUI({autoPlace: true, width: 120});

// dict containing all objects of the scene
let threejs_objects = {};

init();

// Load nodes.json and perform one after the other the following commands:
fetch('nodes.json')
	.then(response => {add_progress_bar(); return response;})
    .then(response => {return response.json();})
    // .then(json_response => {console.log(json_response); return json_response})
    .then(json_response => create_threejs_objects(json_response))
    .then(() => add_threejs_objects_to_scene(threejs_objects))
    .then(() => init_gui(threejs_objects))
	.then(() => console.log('Done'))
	.then(render);