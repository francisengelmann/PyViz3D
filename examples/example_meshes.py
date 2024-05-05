import pyviz3d.visualizer as viz
import numpy as np
import open3d as o3d


def main():
    v = viz.Visualizer(position=[1, 1, 1], focal_length=18)

    v.add_mesh('Plane',
        path='examples/data/plane.obj',
        scale=np.array([0.5, 0.5, 0.5]),
        translation=np.array([1.0, -0.0, -0.85]),
        rotation=viz.euler_to_quaternion(-np.pi / 2.0, -np.pi, np.pi / 2.0),
        color=np.array([100, 170, 255]))
    
    v.add_mesh('Motorbike',
        path='examples/data/motorbike.obj',
        rotation=viz.euler_to_quaternion(np.pi / 2.0, -np.pi / 15.0, 0.0),
        scale=np.array([2, 2, 2]),
        translation=np.array([-2.2, -0.5, -0.95]),
        color=np.array([50, 225, 50]))

    for i in range(10):
        ii = i / 3.0
        pos_x = np.cos(ii) * ii
        pos_y = np.sin(ii) * ii
        v.add_mesh('Chairs;'+str(i),
                   path='examples/data/chair_model.obj',
                   color=np.array([255, i * 30, 0]),
                   translation=np.array([pos_x, pos_y, 0.0]),
                   rotation=np.array([1.0, 1.0, 0.0, ii]),
                   scale=np.array([ii/2.0, ii/2.0, ii/2.0]))

    v.save('example_meshes',
        show_in_blender=True,
        blender_output_path='./',
        blender_executable_path='/Applications/Blender.app/Contents/MacOS/Blender')

if __name__ == '__main__':
    main()
