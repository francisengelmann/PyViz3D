import os
import numpy as np
import pyviz3d.visualizer as viz


def create_color_palette():
    palette = np.array([
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
    ])
    return np.concatenate([palette, palette[1:, :] * 10, palette[1:, :] * 100])


def label_name(label_id):
        names = [
            'none',
            'wall',
            'floor',
            'cabinet',
            'bed',
            'chair',
            'sofa',
            'table',
            'door',
            'window',
            'bookshelf',
            'picture',
            'counter',
            'none',
            'desk',
            'none',
            'curtain',
            'none',
            'none',
            'none',
            'none',
            'none',
            'none',
            'none',
            'refrigerator',
            'none',
            'none',
            'none',
            'shower curtain',
            'none',
            'none',
            'none',
            'none',
            'toilet',
            'sink',
            'none',
            'bathtub',
            'none',
            'none',
            'otherfurn',
            'none'
        ]
        return names[label_id]

class Object:

    def __init__(self, name, points, semantic_colors, instance_colors, normals):
        self.name = name
        self.points = points
        self.semantic_colors = semantic_colors
        self.instance_colors = instance_colors
        self.normals = normals


def get_objects(scene, prediction_file):
    objects = []
    with open(prediction_file) as fp:
        line = fp.readline()
        while line:
            splits = line.strip().split(' ')
            semantic_id = int(splits[1])
            instance_id = len(objects)
            name = str(instance_id)+'_'+label_name(semantic_id)
            mask_file = os.path.join(os.path.dirname(prediction_file), splits[0])
            mask = np.loadtxt(mask_file).astype(int) == 1
            points = scene[mask, 0:3]
            semantic_colors = scene[mask, 3:6] * 0 + create_color_palette()[semantic_id]
            instance_colors = scene[mask, 3:6] * 0 + create_color_palette()[instance_id + 1]
            normals = scene[mask, 6:9]
            obj = Object(name, points, semantic_colors, instance_colors, normals)
            objects.append(obj)
            line = fp.readline()

    return objects


def main():

    data_path_normals = "/home/nekrasov/github/pc_aug/data/processed/scannet/test/"
    # data_path_instance = "/globalwork/data/3d_inst_sem_seg/scannet_francis/full/gt_instance/"

    # Get all names of test scenes
    test_scenes = []
    test_scenes_file = '/home/engelmann/benchmark/instances_pr_30-12-2019/'
    with open(test_scenes_file+'test_scenes.txt') as fp:
        line = fp.readline()
        while line:
            test_scenes.append(line.strip().split('.')[0])
            line = fp.readline()
    test_scenes = ['0801_00', '0747_00', '0793_00', '0708_00']
    test_scene_camera_positions = {'0801_00': [[-2, 0, 2], [1, 1, 0]],
                                   '0793_00': [[2, -0.35, 1.5], [0, 0, 0]],
                                   '0747_00': [[2, -2.2, 2], [0.5, -2, 0]],
                                   '0708_00': [[-1.3, -1.5, 1.3], [0, 0, 0]]}

    for scene_name in test_scenes:

        camera_positions = [5, 5, 5]
        camera_lookAt = [0, 0, 0]
        try:
            camera_positions = test_scene_camera_positions[scene_name][0]
            camera_lookAt = test_scene_camera_positions[scene_name][1]
        except:
            pass
        v = viz.Visualizer(camera_positions, camera_lookAt)

        # Read scene
        scene_normals = np.load(os.path.join(data_path_normals, scene_name+".npy"))  #, scene_name + '_vh_clean_2.npy'))
        # scene_instance = np.loadtxt(os.path.join(data_path_instance, scene_name+'.txt'))
        # scene_instance = (np.remainder(scene_instance, 1000)).astype(int)
        # scene = np.concatenate((scene_normals, np.reshape(scene_instance, [-1, 1])), axis=1)
        scene = scene_normals
        scene[:, 0:3] = scene[:, 0:3] - np.mean(scene[:, 0:3], axis=0)

        point_positions = scene[:, 0:3]
        point_colors = scene[:, 3:6]
        # point_instance_labels = scene[:, -1].astype(int)
        point_semantic_labels = scene[:, -2].astype(int)
        point_normals = scene[:, 6:9]
        # point_instance_colors_gt = create_color_palette()[point_instance_labels]
        point_semantic_colors_gt = create_color_palette()[point_semantic_labels]

        v.add_points('Input 3D Scene', point_positions, point_colors, point_normals, point_size=10, visible=True)
        # v.add_points('GT x`x`Semantics', point_positions, point_semantic_colors_gt, point_normals, point_size=point_size)
        # v.add_points('GT Instances', point_positions, point_instance_colors_gt, point_normals, point_size=point_size)
        # v.add_points('Pr Semantics', point_positions, point_semantic_colors_pr, point_normals, point_size=point_size)
        # v.add_points('Pr Instances', point_positions, point_instance_colors_pr, point_normals, point_size=point_size)
        # v.add_lines('Normals', point_positions, point_positions + point_normals/10, point_semantic_colors, visible=False)

        # Read predictions
        prediction_file = os.path.join(test_scenes_file, scene_name + '.txt')
        objects = get_objects(scene, prediction_file)

        object_points = np.concatenate([obj.points for obj in objects], axis=0)
        object_normals = np.concatenate([obj.normals for obj in objects], axis=0)
        object_semantic_points = np.concatenate([obj.semantic_colors for obj in objects], axis=0)
        object_instance_points = np.concatenate([obj.instance_colors for obj in objects], axis=0)

        v.add_points("Object Semantics", object_points, object_semantic_points, object_normals, point_size=10, visible=True)
        v.add_points("Object Instances", object_points, object_instance_points, object_normals, point_size=10, visible=True)

        # When we added everything we need to the visualizer, we save it.
        v.save('3D_MPA_scannet_test_scenes/'+scene_name+'/')


if __name__ == '__main__':
    main()
