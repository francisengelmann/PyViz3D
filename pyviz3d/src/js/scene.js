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

function get_lines(){
	var lines_material = new THREE.LineBasicMaterial({color: 0x00ff00, linewidth: 5});
	var lines_geometry = new THREE.Geometry();
	lines_geometry.vertices.push(new THREE.Vector3( -2, 0, 0) );
	lines_geometry.vertices.push(new THREE.Vector3( 0, 2, 0) );
	lines_geometry.vertices.push(new THREE.Vector3( 2, 0, 0) );
	return new THREE.Line(lines_geometry, lines_material);
}

function get_cube(){
	let cube_geometry = new THREE.BoxGeometry(1, 5, 1);
	let cube_material = new THREE.MeshPhongMaterial({color: 0x00ffff});
	cube_material.wireframe = false;
	cube_material.wireframeLinewidth = 5;
	let cube = new THREE.Mesh(cube_geometry, cube_material);
	return cube
}

function get_points(properties){
	// Add points
	// https://github.com/mrdoob/three.js/blob/master/examples/webgl_buffergeometry_points.html
	let positions = [];
	let particles = properties['num_points'];
	let geometry = new THREE.BufferGeometry();
	let binary_filename = properties['binary_filename'];

	fetch(binary_filename)
	    .then(response => response.arrayBuffer())
		.then(buffer => {
			positions = new Float32Array(buffer, 0, 3 * particles);
		    let colors_uint8 = new Uint8Array(buffer, (3 * particles) * 4, 3 * particles);
		    let colors_float32 = Float32Array.from(colors_uint8);
		    for(let i=0; i<colors_float32.length; i++) {
			    colors_float32[i] /= 255;
			}
		    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
			geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors_float32, 3));
		})
        .then(render);

	let material = new THREE.PointsMaterial({size: properties['point_size'], vertexColors: THREE.VertexColors});
	let points = new THREE.Points(geometry, material);
	points.frustumCulled = false;
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
	//let fol = gui.addFolder(`Objects`)
	for (const [key, value] of Object.entries(objects)){
		gui.add(value, 'visible').name(key).onChange(render);
	}
	//fol.open = true
}

function render() {
    renderer.render(scene, camera);
}

function init(){
	scene.background = new THREE.Color(0xffffff);
	camera.position.set(5, 5, 5);
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

function create_threejs_objects(properties){
	for (const [key, value] of Object.entries(properties)) {
		if (properties['type'] = 'points'){
			threejs_objects[key] = get_points(value);
    		render();
		}
		threejs_objects[key].visible = value['visible']
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

let domElement = document.body.appendChild(renderer.domElement);
domElement.addEventListener("dblclick", onDoubleClick);

// dict(?) containing all objects of the scene
let threejs_objects = {};

init();

// Load nodes.json and perform one after the other the following commands:
fetch('nodes.json')
    .then(response => {return response.json();})
    .then(json_response => {console.log(json_response); return json_response})
    .then(json_response => create_threejs_objects(json_response))
    .then(() => add_threejs_objects_to_scene(threejs_objects))
    .then(() => init_gui(threejs_objects))
    .then(render);
