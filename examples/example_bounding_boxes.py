import pyviz3d.visualizer as viz
import numpy as np
import quaternion as q
import math


def main():
    v = viz.Visualizer()

    v.add_bounding_box('Box_1', position=np.array([0.0, 0.0, 1.0]), size=np.array([1, 1, 2]))
    v.add_bounding_box('Box_2',
                       position=np.array([1, 0, 0.05]),
                       size=np.array([2, 1, 0.1]),
                       orientation=np.array([math.pi/6.0, 0.0, 0.0, 1.0]),
                       color=np.array([0, 0, 255]), alpha=0.5, edge_width=0.01)
    v.add_bounding_box('Box_3',
                       position=np.array([-1, 1, 0]),
                       size=np.array([1, 2, 1]),
                       orientation=np.array([math.pi/3.0, 0.0, 0.0, 1.0]),
                       color=np.array([30, 255, 50]), edge_width=0.01)
    for i in range(4):
        v.add_bounding_box(f'Box;_{i}',
                           position=np.array([1, 1, 0]),
                           size=np.array([1, 2, 1]),
                           orientation=q.as_float_array(q.from_euler_angles(0.0, 0.0, i * math.pi/4.0)).tolist(),
                           color=np.array([130, 155, 50]), edge_width=0.02)
    v.save('example_bounding_boxes')


if __name__ == '__main__':
    main()
