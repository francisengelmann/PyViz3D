import numpy as np
import pyviz3d as viz


def create_color_palette():
    return np.array([
       (0, 0, 0),
       (174, 199, 232),		# wall
       (152, 223, 138),		# floor
       (31, 119, 180), 		# cabinet
       (255, 187, 120),		# bed
       (188, 189, 34), 		# chair
       (140, 86, 75),  		# sofa
       (255, 152, 150),		# table
       (214, 39, 40),  		# door
       (197, 176, 213),		# window
       (148, 103, 189),		# bookshelf
       (196, 156, 148),		# picture
       (23, 190, 207), 		# counter
       (178, 76, 76),
       (247, 182, 210),		# desk
       (66, 188, 102),
       (219, 219, 141),		# curtain
       (140, 57, 197),
       (202, 185, 52),
       (51, 176, 203),
       (200, 54, 131),
       (92, 193, 61),
       (78, 71, 183),
       (172, 114, 82),
       (255, 127, 14), 		# refrigerator
       (91, 163, 138),
       (153, 98, 156),
       (140, 153, 101),
       (158, 218, 229),		# shower curtain
       (100, 125, 154),
       (178, 127, 135),
       (120, 185, 128),
       (146, 111, 194),
       (44, 160, 44),  		# toilet
       (112, 128, 144),		# sink
       (96, 207, 209),
       (227, 119, 194),		# bathtub
       (213, 92, 176),
       (94, 106, 211),
       (82, 84, 163),  		# otherfurn
       (100, 85, 144)
    ], dtype=np.uint8)


def main():

    # First, we set up a visualizer
    v = viz.Visualizer()

    # Example with normals
    scene_name = 'scene0000_00_vh_clean_2'
    scene = np.load('examples/data/' + scene_name + '.npy')
    point_positions = scene[:, 0:3] - np.mean(scene[:, 0:3], axis=0)
    point_colors = scene[:, 3:6]
    point_labels = scene[:, -1].astype(int)
    point_normals = scene[:, 6:9]
    point_semantic_colors = create_color_palette()[point_labels]
    point_size = 35.0

    v.add_points('RGB Color', point_positions, point_colors, point_normals, point_size=point_size, visible=False)
    v.add_points('Semantics', point_positions, point_semantic_colors, point_normals, point_size=point_size)
    v.add_lines('Normals', point_positions, point_positions + point_normals/10.0, visible=True)

    # When we added everything we need to the visualizer, we save it.
    v.save('example_normals')


if __name__ == '__main__':
    main()
