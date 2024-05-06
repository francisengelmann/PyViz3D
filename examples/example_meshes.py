import pyviz3d.visualizer as viz
import numpy as np
import open3d as o3d


def main():
    v = viz.Visualizer(position=[5, 5, 1])

    v.add_mesh('Plane',
        path='examples/data/plane.obj',
        scale=np.array([0.5, 0.5, 0.5]),
        translation=np.array([1.0, -0.6, -0.7]),
        rotation=viz.euler_to_quaternion(-np.pi / 2.0, -np.pi, np.pi / 2.0),
        color=np.array([100, 170, 255]))

    v.add_mesh('Motorbike',
        path='examples/data/motorbike.obj',
        rotation=viz.euler_to_quaternion(np.pi / 2.0, -np.pi / 15.0, 0.0),
        scale=np.array([2, 2, 2]),
        translation=np.array([0.0, 0.0, -0.95]),
        color=np.array([50, 225, 50]))

    v.add_mesh('Room', path='examples/data/office_chairs.ply')

    for i in range(3):
        ii = i / 3.0
        pos_x = np.cos(ii) * 2.0
        pos_y = np.sin(ii) * 2.0
        v.add_mesh('Chairs;'+str(i),
                   path='examples/data/chair_model.obj',
                   color=np.array([255, i * 30, 0]),
                   translation=np.array([pos_x, pos_y, -1.0]),
                   rotation=viz.euler_to_quaternion(np.pi / 2.0, 0.0, np.pi / 4.0 * i))

    blender_args = {'output_prefix': './',
                    'executable_path': '/Applications/Blender.app/Contents/MacOS/Blender'}
    v.save('example_meshes', blender_args=blender_args)

if __name__ == '__main__':
    main()
