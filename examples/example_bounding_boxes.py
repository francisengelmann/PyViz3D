import pyviz3d.visualizer as viz
import numpy as np
import quaternion as q  # install with `pip install numpy-quaternion'
import math


def main():
    v = viz.Visualizer()
    # Add a bounding box with specified position and size.
    v.add_bounding_box('Box_1',
                       position=np.array([0.0, 0.0, 1.0]),
                       size=np.array([1.0, 1.0, 2.0]))
    
    # Add another bounding box specifying the orientation (using quaternions) and color.
    v.add_bounding_box('Box_2',
                       position=np.array([-1, 1, 0]),
                       size=np.array([1, 2, 1]),
                       orientation=np.array([math.pi/3.0, 0.0, 0.0, 1.0]),
                       color=np.array([30, 255, 50]), edge_width=0.01)
    
    # Add a semi transparent bounding box.
    v.add_bounding_box('Box_3',
                       position=np.array([1, 0, 0.05]),
                       size=np.array([2, 1, 0.1]),
                       orientation=np.array([math.pi/6.0, 0.0, 0.0, 1.0]),
                       color=np.array([0, 0, 255]),
                       alpha=0.5,
                       edge_width=0.01)
    
    # Add an oriented bounding boxes via euler angles.
    for i in range(4):
        euler_x, euler_y, euler_z = 0.0, 0.0, i * math.pi/4.0
        orientation = q.as_float_array(q.from_euler_angles(euler_x, euler_y, euler_z))
        v.add_bounding_box(f'Box;_{i}',
                           position=np.array([1.0, 1.0, 0]),
                           size=np.array([1.0, 2.0, 0.5]),
                           orientation=orientation,
                           color=np.array([255, 255, 0]),
                           alpha=0.1,
                           edge_width=0.02)
    v.save('example_bounding_boxes')


if __name__ == '__main__':
    main()
