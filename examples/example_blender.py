import numpy as np
import pyviz3d.visualizer as viz
import os
import open3d as o3d
import matplotlib as mpl

def main():

    prefix = '/Users/francis/Downloads/scannet_evaluation/bcd2436daf'
    name = 'iphone'
    path = os.path.join(prefix, name+'.ply')

    v = viz.Visualizer(position=[0.0, 5.0, 2.0], look_at=None, up=None)
    pcd = o3d.io.read_point_cloud(path)
    points = np.array(pcd.points)[::10]
    points -= np.mean(points, axis=0)
    colors = np.array(pcd.colors)[::10] * 255.0

    v.add_points(name, points, colors, point_size=20, visible=False)
    v.save(f'{name}', show_in_blender=True, blender_output_path=os.path.join(prefix, name+'.png'))

    return

    # First, we set up a visualizer
    prefix = '/Users/francis/Documents/Conferences/ECCV24/denoising/data/visuals'
    
    names = ['camel', 'duck', 'horse', 'kitten']
    models = ['clean', 'mag', 'noisy', 'p2sb', 'pdflow', 'sd']
    
    r=-3.1415/2.0
    rot_matrix = np.array(
        [[1.0, 0.0, 0.0],[0.0, np.cos(r), -np.sin(r)],[0, np.sin(r), np.cos(r)]])

    for name in names:
        for model in models:
            v = viz.Visualizer(position=[0.0, 5.0, 2.0], look_at=None, up=None)
            path = os.path.join(prefix, name, model+'.npy')
            data = np.load(path)
            points = data[:, 0:3] @ rot_matrix
            distances = 10 - data[:, -1] * 600.0
            print(np.min(distances), np.max(distances))
            cmap = mpl.colormaps['RdYlGn']
            colors = cmap(distances)[:, 0:3] * 255
            v.add_points(name, points, colors, point_size=15, visible=False)
            v.add_bounding_box('background', np.array([0.0, 0.0, np.min(points[:, 2])]), np.array([3, 3, 0.001]))
            v.save(f'{name}_{model}', show_in_blender=True, blender_output_path=os.path.join(prefix, name+"_png", model+'.png'))

if __name__ == '__main__':
    main()
