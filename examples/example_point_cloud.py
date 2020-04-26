import numpy as np
import pyviz3d.visualizer as viz


def main():

    # First, we set up a visualizer
    v = viz.Visualizer()

    # Random point clouds.
    for j in range(5):
        i = j + 1
        name = 'Points_'+str(i)
        num_points = 3
        point_positions = np.random.random(size=[num_points, 3])
        point_colors = (np.random.random(size=[num_points, 3]) * 255).astype(np.uint8)
        point_size = 0.1 * i

        # Here we add point clouds to the visualizer
        v.add_points(name, point_positions, point_colors, point_size)

    # Sample point clouds from the ScanNet dataset.
    for scene_name in ['scene0140_01', 'scene0451_01']:
        scene = np.load('examples/' + scene_name + '.npy')
        point_positions = scene[:, 0:3]
        point_colors = scene[:, 3:6]
        point_size = 0.03

        # Add more point clouds
        v.add_points(scene_name, point_positions, point_colors, point_size)

    # When we added everything we need to the visualizer, we save it.
    v.save('test')


if __name__ == '__main__':
    main()
