<p align="center"><img width="40%" src="docs/img/pyviz3d-logo.png" /></p>

----
PyViz3D is a python package to visualize 3D scenes directly in your browser.

#### Links

- Install: ```pip install pyviz3d```
- [Documentation](https://francisengelmann.github.io/PyViz3D/)
- [Examples](https://github.com/francisengelmann/PyViz3D/tree/master/examples)

### Examples
Scene graph example, including blender rendering.
[[Show Code]](https://github.com/francisengelmann/PyViz3D/blob/master/examples/example_graph.py)
[[Show Demo]](https://francisengelmann.github.io/pyviz3d_examples/graph/index.html)
<p align="center">
  <img width="45%" src="docs/img/example_graph.png" />
  <img width="45%" src="docs/img/example_graph_blender.png" />
</p>

Polygon meshes example.
[[Show Code]](https://github.com/francisengelmann/PyViz3D/blob/master/examples/example_meshes.py)
[[Show Demo]](https://francisengelmann.github.io/pyviz3d_examples/meshes/index.html)
[<p align="center"><img width="60%" src="docs/img/example_meshes.png" /></p>](https://francisengelmann.github.io/pyviz3d_examples/meshes/index.html)

Bounding boxes example.
[[Show Code]](https://github.com/francisengelmann/PyViz3D/blob/master/examples/example_bounding_boxes.py)
[[Show Demo]](https://francisengelmann.github.io/pyviz3d_examples/bounding_boxes/index.html)
[<p align="center"><img width="60%" src="docs/img/example_bounding_boxes.png" /></p>](https://francisengelmann.github.io/pyviz3d_examples/bounding_boxes/index.html)

Polyline example.
[[Show Code]](https://github.com/francisengelmann/PyViz3D/blob/master/examples/example_polylines.py)
[[Show Demo]](https://francisengelmann.github.io/pyviz3d_examples/polylines/index.html)
[<p align="center"><img width="60%" src="docs/img/example_polylines.png" /></p>](https://francisengelmann.github.io/pyviz3d_examples/polylines/index.html)

Arrow example.
[[Show Code]](https://github.com/francisengelmann/PyViz3D/blob/master/examples/example_arrows.py)
[[Show Demo]](https://francisengelmann.github.io/pyviz3d_examples/arrows/index.html)
[<p align="center"><img width="60%" src="docs/img/example_arrows.png" /></p>](https://francisengelmann.github.io/pyviz3d_examples/arrows/index.html)

Point clouds and segments example.
[[Show Code]](https://github.com/francisengelmann/PyViz3D/blob/master/examples/example_normals.py)
[[Show Demo]](https://francisengelmann.github.io/pyviz3d_examples/normals/index.html)
[<p align="center"><img width="60%" src="docs/img/example.png" /></p>](https://francisengelmann.github.io/pyviz3d_examples/normals/index.html)

# Blender

1. Install Blender (from https://www.blender.org/)
2. Set up alias in you ~/.bashrc or ~/.zshrc etc.
`alias blender="/Applications/Blender.app/Contents/MacOS/Blender"`
then `source ~/.zshrc`
3. `blender myscene.blend --background --python blender.py`
currently there is no myscene.blend to remove that: `blender --background --python blender.py`
4. This creates a .blend file. Open it in blender.  
Select camera: View/Cameras/Active Camera    
Lock camera to view:  
Press N to show sidebar.  
Under View, lock camera to view.  
Control the camera with the small coordinate frame on the top right.
5. This will render an `output.png`
6. The scene can also be opened in blender `bunny.blend`
7. Need to install ffmpeg and convert (on mac via brew)  
brew install ffmpeg