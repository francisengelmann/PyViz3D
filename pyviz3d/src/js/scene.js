import * as THREE from 'https://threejsfundamentals.org/threejs/resources/threejs/r112/build/three.module.js';
import {GUI} from 'https://threejsfundamentals.org/3rdparty/dat.gui.module.js';
import {OrbitControls} from 'https://threejsfundamentals.org/threejs/resources/threejs/r112/examples/jsm/controls/OrbitControls.js';


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
        positions = new Float32Array(buffer, 0, 3 * num_lines);
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    }).then(render);

    geometry.setAttribute( 'position', new THREE.Float32BufferAttribute( positions, 3 ));
	var material = new THREE.LineBasicMaterial({color: 0xff7700});
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
		'<div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 0%" id="progress_bar">Loading...</div>\n' +
		'</div>';
    gProgressElement.innerHTML = html_code;
    gProgressElement.id = "progress_bar_id"
    gProgressElement.style.left = "20%";
    gProgressElement.style.right = "20%";
    gProgressElement.style.position = "fixed";
    gProgressElement.style.top = "50%";
    document.body.appendChild(gProgressElement);
}

function hide_progress_bar(){
	document.getElementById( 'progress_bar_id' ).innerHTML = "";
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
        .then(render);

	 // var loader = new THREE.TextureLoader();
	 // var texture = loader.load( 'disc.png' );
	 // let material = new THREE.PointsMaterial({
     //     size: properties['point_size'],
	 //     map: texture,
	 //     alphaTest: 0.5,
     //     vertexColors: THREE.VertexColors,
     //     sizeAttenuation: true});


	 var uniforms = {
        pointSize: { value: properties['point_size'] },
		alpha: {value: properties['alpha']}
     };

	 var material = new THREE.ShaderMaterial( {
		uniforms:       uniforms,
        vertexShader:   document.getElementById( 'vertexshader' ).textContent,
        fragmentShader: document.getElementById( 'fragmentshader' ).textContent,
        transparent:    true

    } );

	var points = new THREE.Points(geometry, material);
	return points
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
	camera.position.set(3, 3, 3);
	camera.lookAt(0, 0 , 0);
	controls.update()
	renderer.setSize(window.innerWidth, window.innerHeight);

	let hemiLight = new THREE.HemisphereLight( 0xffffff, 0x444444 );
	hemiLight.position.set( 0, 20, 0 );
	scene.add(hemiLight);

	let dirLight = new THREE.DirectionalLight( 0xffffff );
	dirLight.position.set( -10, 10, - 10 );
	dirLight.castShadow = true;
	dirLight.shadow.camera.top = 2;
	dirLight.shadow.camera.bottom = - 2;
	dirLight.shadow.camera.left = - 2;
	dirLight.shadow.camera.right = 2;
	dirLight.shadow.camera.near = 0.1;
	dirLight.shadow.camera.far = 40;
	scene.add(dirLight);

	raycaster = new THREE.Raycaster();
	let threshold = 1.0;
	raycaster.params.Points.threshold = threshold;
}

async function create_threejs_objects(properties){

	let num_objects_curr = 0.0;
	let num_objects = parseFloat(Object.entries(properties).length);

	for (const [object_name, object_properties] of Object.entries(properties)) {
		if (String(object_properties['type']).localeCompare('points') == 0){
			threejs_objects[object_name] = get_points(object_properties);
    		render();
		}
		if (String(object_properties['type']).localeCompare('lines') == 0){
			threejs_objects[object_name] = get_lines(object_properties);
    		render();
		}
		threejs_objects[object_name].visible = object_properties['visible'];
		threejs_objects[object_name].frustumCulled = false;
		num_objects_curr += 1.0;
		let width_string = String(parseInt(num_objects_curr/num_objects*100.0))+'%';
		console.log(width_string);
		document.getElementById('progress_bar').style.width = width_string;
		document.getElementById('progress_bar').innerText = width_string;
		await new Promise(resolve => setTimeout(resolve, 500));
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

const scene = new THREE.Scene();
const renderer = new THREE.WebGLRenderer({antialias: true});
const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.01, 1000);
camera.up.set(0, 0, 1);

window.addEventListener('resize', onWindowResize, false);

function onWindowResize(){
    const innerWidth = window.innerWidth
    const innerHeight = window.innerHeight;
    renderer.setSize(innerWidth, innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    render();
}

//Orbit Control
const controls = new OrbitControls(camera, renderer.domElement);
controls.addEventListener("change", render);
window.addEventListener("resize", render)

controls.enableKeys = true;
controls.enablePan = true; // enable dragging

let raycaster;
let intersection = null;
let mouse = new THREE.Vector2();

const gui = new GUI();

//let container = document.getElementById('render_container');
//document.body.appendChild(container);
//container.appendChild(renderer.domElement);

document.getElementById('render_container').appendChild(renderer.domElement)

//let domElement = document.body.appendChild(renderer.domElement);
//domElement.addEventListener("dblclick", onDoubleClick);

// dict(?) containing all objects of the scene
let threejs_objects = {};

init();

// Load nodes.json and perform one after the other the following commands:
fetch('nodes.json')
	.then(response => {add_progress_bar(); return response;})
    .then(response => {return response.json();})
    //.then(json_response => {console.log(json_response); return json_response})
    .then(json_response => create_threejs_objects(json_response))
    .then(() => add_threejs_objects_to_scene(threejs_objects))
    .then(() => init_gui(threejs_objects))
	.then(() => hide_progress_bar())
	.then(render);
