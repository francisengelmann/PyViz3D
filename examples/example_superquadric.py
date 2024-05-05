import pyviz3d.visualizer as viz
import numpy as np


def main():
    v = viz.Visualizer(position=np.array([15.0, 15.0, 5.0]))
    v.add_superquadric('sq_1',
                       exponents=np.array([3.0, 4.0, 5.0]),
                       scalings=np.array([1.0, 3.0, 1.0]),
                       color=np.array([255, 0, 0]),
                       resolution=100)
    v.add_superquadric('sq_2',
                       exponents=np.array([2.0, 4.0, 8.0]),
                       scalings=np.array([2.0, 0.5, 3.0]),
                       color=np.array([0.0, 255.0, 100.0]),
                       resolution=100)
    v.add_superquadric('sq_3',
                       exponents=np.array([0.5, 2.0, 0.5]),
                       scalings=np.array([1.0, 1.0, 1.0]),
                       color=np.array([0.0, 100.0, 255.0]),
                       translation=np.array([3.0, 2.0, 1.0]),
                       rotation=viz.euler_to_quaternion(0.0, 0.0, np.pi/3.0),
                       resolution=100)
    v.save('example_superquadric',
            show_in_blender=True,
            blender_output_path='~/superquadric',
            blender_executable_path='/Applications/Blender.app/Contents/MacOS/Blender')

if __name__ == '__main__':
    main()
