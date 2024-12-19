import pyviz3d as viz
import numpy as np


def main():
    v = viz.Visualizer()
    # Add a bounding box with specified position and size.
    v.add_bounding_box('Box_1',
                       position=np.array([0.0, 0.0, 1.0]),
                       size=np.array([1.0, 1.0, 2.0]))
    
    # Add another bounding box specifying the orientation (using quaternions) and color.
    v.add_bounding_box('Box_2',
                       position=np.array([-1.0, 1.0, 0.0]),
                       size=np.array([1.0, 2.0, 1.0]),
                       rotation=viz.euler_to_quaternion(np.pi/3.0, 0.0, 0.0),
                       color=np.array([30, 255, 50]),
                       edge_width=0.01)
    
    # Add a semi transparent bounding box.
    v.add_bounding_box('Box_3',
                       position=np.array([1.0, 0.0, 0.0]),
                       size=np.array([2.0, 1.0, 0.1]),
                       rotation=viz.euler_to_quaternion(np.pi/6.0, 0.0, 0.0),
                       color=np.array([0, 0, 255]),
                       alpha=0.5,
                       edge_width=0.01)
    
    # Add an oriented bounding boxes via euler angles.
    for i in range(4):
        euler_x, euler_y, euler_z = 0.0, 0.0, i * np.pi/4.0
        v.add_bounding_box(f'Box;_{i}',
                           position=np.array([1.0, 1.0, 0]),
                           size=np.array([1.0, 2.0, 0.5]),
                           rotation=viz.euler_to_quaternion(euler_x, euler_y, euler_z),
                           color=np.array([255, 255, 0]),
                           alpha=0.1,
                           edge_width=0.02)
    v.save('example_bounding_boxes')


if __name__ == '__main__':
    main()
