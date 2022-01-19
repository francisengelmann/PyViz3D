import pyviz3d.visualizer as viz
import math


def main():
    v = viz.Visualizer()
    v.add_mesh('Plane', path='examples/data/plane.obj',
               rotation=[math.pi/2, 0, -math.pi/3], scale=[5, 5, 5], translation=[-3, -1, 1], color=[100, 170, 255])
    v.add_mesh('Motorbike', path='examples/data/motorbike.obj',
               rotation=[math.pi/1.5, 0, 0], scale=[2, 2, 2], translation=[0, 0.5, 0.5], color=[50, 225, 50])
    for i in range(10):
        ii = i / 3.0
        pos_x = math.cos(ii) * ii
        pos_y = math.sin(ii) * ii
        v.add_mesh('Chairs;'+str(i), path='examples/data/chair_model.obj',
                   color=[255, i*30, 0],
                   translation=[pos_x, pos_y, 0.0],
                   rotation=[3.1415/2, ii, 0],
                   scale=[ii/2.0, ii/2.0, ii/2.0])
    v.save('example_meshes')


def main2():
    v = viz.Visualizer()
    v.add_mesh('Motorbike', path='examples/data/a/model.obj', color=[100, 170, 255])
    v.add_mesh('Chair', path='examples/data/b/model.obj', color=[50, 225, 50])
    v.save('example_meshes2')


if __name__ == '__main__':
    main2()
