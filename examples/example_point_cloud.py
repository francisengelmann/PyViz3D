import numpy as np
import pyviz3d.visualizer as viz


def main():

    v = viz.Visualizer()

    for j in range(5):
        i = j + 1
        name = 'Points_'+str(i)
        num_points = 3
        point_positions = np.random.random(size=[num_points, 3])
        point_colors = (np.random.random(size=[num_points, 3]) * 255).astype(np.uint8)
        point_size = 0.1 * i
        v.add_points(name, point_positions, point_colors, point_size)

    for scene_name in ['scene0140_01', 'scene0451_01']:
        scene = np.load('examples/' + scene_name + '.npy')
        v.add_points(scene_name, scene[:, 0:3], scene[:, 3:6], 0.03)
        
    v.show('test')


if __name__ == '__main__':
    main()
