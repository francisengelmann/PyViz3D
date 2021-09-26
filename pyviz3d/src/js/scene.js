import * as THREE from 'https://threejsfundamentals.org/threejs/resources/threejs/r112/build/three.module.js';
import {GUI} from 'https://threejsfundamentals.org/3rdparty/dat.gui.module.js';
import {OrbitControls} from 'https://threejsfundamentals.org/threejs/resources/threejs/r112/examples/jsm/controls/OrbitControls.js';
import {OBJLoader} from 'https://threejsfundamentals.org/threejs/resources/threejs/r127/examples/jsm/loaders/OBJLoader.js';

let num_objects_curr = 0;
let num_objects = 100;

function onDoubleClick(event) {
	//console.log(event);
	mouse.x = ( event.clientX / window.innerWidth ) * 2 - 1;
	mouse.y = - ( event.clientY / window.innerHeight ) * 2 + 1;
	raycaster.setFromCamera( mouse, camera );
	//let objs = Object.values(threejs_objects);
	let intersections = raycaster.intersectObjects( [ threejs_objects['scene0451_01'] ] );
	intersection = ( intersections.length ) > 0 ? intersections[ 0 ] : null;
	//console.log(objs);
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
        for(let i=0; i<colors_float32.length; i++) {
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
	camera.position.set(properties['position'][0],
						properties['position'][1],
						properties['position'][2]);
	controls.target = new THREE.Vector3(properties['look_at'][0],
	 	                                properties['look_at'][1],
	 						    		properties['look_at'][2]);
	camera.updateProjectionMatrix();
	controls.update()

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

function get_obj(properties){
	var container = new THREE.Object3D();
	function loadModel(object) {
		object.traverse(
		function(child) {
			if (child.isMesh) {
				console
				let r = properties['color'][0]
				let g = properties['color'][1]
				let b = properties['color'][2]
				let colorString = "rgb("+r+","+g+", "+b+")"
				child.material.color.set(new THREE.Color(colorString));
				console.log('setting colors ' + r + " " + g + " " + b)
			}
		});
		object.translateX(properties['translation'][0])
		object.translateY(properties['translation'][1])
		object.translateZ(properties['translation'][2])

		object.rotateX(properties['rotation'][0])
		object.rotateY(properties['rotation'][1])
		object.rotateZ(properties['rotation'][2])

		object.scale.set(properties['scale'][0], properties['scale'][1], properties['scale'][2])

		container.add(object)
		step_progress_bar();
		render();
	}

	const loader = new OBJLoader();
	loader.load(properties['filename'], loadModel,
				function (xhr){ // called when loading is in progresses
					console.log( ( xhr.loaded / xhr.total * 100 ) + '% loaded' );
				},
				function (error){ // called when loading has errors
					console.log( 'An error happened' );
				});
	return container
}

function get_cuboid(properties){
	const radius_top = properties['edge_width']
	const radius_bottom = properties['edge_width']
	const radial_segments = 30
	const height = 1
	let geometry = new THREE.CylinderGeometry(radius_top, radius_bottom, height, radial_segments);
	for (let i=0; i<geometry.faces.length; i++){
		const r = properties['color'][0]
		const g = properties['color'][1]
		const b = properties['color'][2]
		for (let j=0; j<3; j++){
			geometry.faces[i].vertexColors[j] = new THREE.Color("rgb("+r+", "+g+", "+b+")");
		}
	}

	let uniforms = {
		alpha: {value: properties['alpha']},
		shading_type: {value: 1},
	};
	let material = new THREE.ShaderMaterial( {
		 uniforms:       uniforms,
    	 vertexShader:   document.getElementById( 'vertexshader' ).textContent,
	     fragmentShader: document.getElementById( 'fragmentshader' ).textContent,
		 transparent:    true,
	 });

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

	const corner_geometry = new THREE.SphereGeometry(properties['edge_width'], 30, 30);
	for (let i=0; i<corner_geometry.faces.length; i++){
		const r = properties['color'][0]
		const g = properties['color'][1]
		const b = properties['color'][2]
		for (let j=0; j<3; j++){
			corner_geometry.faces[i].vertexColors[j] = new THREE.Color("rgb("+r+", "+g+", "+b+")");
		}
	}
	const sphere = new THREE.Mesh(corner_geometry, material)
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

	cuboid.rotateX(properties['orientation'][0])
	cuboid.rotateY(properties['orientation'][1])
	cuboid.rotateZ(properties['orientation'][2])
	cuboid.position.set(properties['position'][0], properties['position'][1], properties['position'][2])

	return cuboid

}

function get_ground(){
	let mesh = new THREE.Mesh(new THREE.PlaneBufferGeometry(2000, 2000),
							  new THREE.MeshPhongMaterial({ color: 0x999999, depthWrite: true}));
	mesh.rotation.x = -Math.PI / 2;
	mesh.position.set(0, -5, 0);
	mesh.receiveShadow = true;
	return mesh
}

function init_gui(objects){

	let menuMap = new Map();

	for (const [name, value] of Object.entries(objects)){
		let splits = name.split(';')
		if (splits.length > 1) {
			let folder_name = splits[0];
			if (!menuMap.has(folder_name)) {
				menuMap.set(folder_name, gui.addFolder(folder_name));
			}
			let fol = menuMap.get(folder_name);
			fol.add(value, 'visible').name(splits[1]).onChange(render);
			fol.open();

		} else {
			gui.add(value, 'visible').name(name).onChange(render);
		}
	}
}

function render() {
    renderer.render(scene, camera);
}

function init(){
	scene.background = new THREE.Color(0xffffff);
	controls.update()
	renderer.setSize(window.innerWidth, window.innerHeight);

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
		if (String(object_properties['type']).localeCompare('lines') == 0){
			threejs_objects[object_name] = get_lines(object_properties);
    		render();
		}
		if (String(object_properties['type']).localeCompare('obj') == 0){
			threejs_objects[object_name] = get_obj(object_properties);
		}
		if (String(object_properties['type']).localeCompare('cuboid') == 0){
			threejs_objects[object_name] = get_cuboid(object_properties);
			step_progress_bar();
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
		console.log('Adding '+key)
	}
}

function onWindowResize(){
    const innerWidth = window.innerWidth
    const innerHeight = window.innerHeight;
    renderer.setSize(innerWidth, innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    render();
}

const scene = new THREE.Scene();
const renderer = new THREE.WebGLRenderer({antialias: true});
var camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.01, 1000);
camera.up.set(0, 0, 1);

window.addEventListener('resize', onWindowResize, false);

//Orbit Control
const controls = new OrbitControls(camera, renderer.domElement);
controls.addEventListener("change", render);
controls.enableKeys = true;
controls.enablePan = true; // enable dragging

let raycaster;
let intersection = null;
let mouse = new THREE.Vector2();

const gui = new GUI({autoPlace: true, width: 120});

document.getElementById('render_container').appendChild(renderer.domElement)

// dict containing all objects of the scene
let threejs_objects = {};

init();

// Load nodes.json and perform one after the other the following commands:
fetch('nodes.json')
	.then(response => {add_progress_bar(); return response;})
    .then(response => {return response.json();})
    .then(json_response => {console.log(json_response); return json_response})
    .then(json_response => create_threejs_objects(json_response))
    .then(() => add_threejs_objects_to_scene(threejs_objects))
    .then(() => init_gui(threejs_objects))
	.then(() => console.log('done'))
	.then(render)
	.then(() => console.log('hiding progress bar'));
