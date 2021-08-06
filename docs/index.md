![Screenshot](https://raw.githubusercontent.com/francisengelmann/pyviz3d/master/docs/img/pyviz3d-logo.png)

### Examples

- Draw meshes.
 [[Demo]](https://francisengelmann.github.io/pyviz3d_examples/meshes/index.html)
 [[Code]](https://github.com/francisengelmann/PyViz3D/blob/master/examples/example_meshes.py)

- Draw normals using lines.
 [[Demo]](https://francisengelmann.github.io/pyviz3d_examples/normals/index.html)
 [[Code]](https://github.com/francisengelmann/pyviz3d/blob/master/examples/example_normals.py)

### Installation
Intall the latest stable PyViz3D via pip: `pip install pyviz3d`

### Getting Started
In this simple example we will display multiple point clouds. [Show example](https://francisengelmann.github.io/pyviz3d_examples/example/index.html).

```python
import numpy as np
import pyviz3d.visualizer as viz


def main():

    # First, we set up a visualizer
    v = viz.Visualizer()

    # Random point clouds.
    for j in range(5):
        i = j + 1
        name = 'Points;'+str(i)
        num_points = 3
        point_positions = np.random.random(size=[num_points, 3])
        point_colors = (np.random.random(size=[num_points, 3]) * 255).astype(np.uint8)
        point_size = 25 * i

        # Here we add point clouds to the visualizer
        v.add_points(name, point_positions, point_colors, point_size=point_size, visible=False)

    # Sample point clouds from the ScanNet dataset.
    for scene_name in ['scene0140_01', 'scene0451_01']:
        scene = np.load('examples/' + scene_name + '.npy')
        point_positions = scene[:, 0:3]
        point_colors = scene[:, 3:6]
        point_size = 25.0

        # Add more point clouds
        v.add_points(scene_name, point_positions, point_colors, point_size=point_size)

    # When we added everything we need to the visualizer, we save it.
    v.save('test')


if __name__ == '__main__':
    main()


```
