import pyviz3d.visualizer as viz
import numpy as np
import math


def main():
    v = viz.Visualizer()
    v.add_mesh('Plane',
               path='examples/data/plane.obj',
               rotation=np.array([math.pi/2, 0.0, -math.pi/3, 0.0]),
               scale=np.array([5, 5, 5]),
               translation=np.array([-3, -1, 1]),
               color=np.array([100, 170, 255]))
    
    v.add_mesh('Motorbike',
               path='examples/data/motorbike.obj',
               rotation=np.array([math.pi/1.5, 1.0, 0.0, 0.0]),
               scale=np.array([2, 2, 2]),
               translation=np.array([0, 0.5, 0.5]),
               color=np.array([50, 225, 50]))
    
    for i in range(10):
        ii = i / 3.0
        pos_x = math.cos(ii) * ii
        pos_y = math.sin(ii) * ii
        v.add_mesh('Chairs;'+str(i),
                   path='examples/data/chair_model.obj',
                   color=np.array([255, i * 30, 0]),
                   translation=np.array([pos_x, pos_y, 0.0]),
                   rotation=np.array([3.1415/2, ii, 0.0, 0.0]),
                   scale=np.array([ii/2.0, ii/2.0, ii/2.0]))
    v.save('example_meshes')


if __name__ == '__main__':
    main()
