import numpy as np
import pyviz3d.visualizer as viz
import plyfile
import open3d as o3d
import os
from sklearn.neighbors import NearestNeighbors

def read_ply_data(filename):
    filename_in = filename
    file = open(filename_in, 'rb')
    ply_data = plyfile.PlyData.read(file)
    file.close()
    x = ply_data['vertex']['x']
    y = ply_data['vertex']['y']
    z = ply_data['vertex']['z']
    red = ply_data['vertex']['red']
    green = ply_data['vertex']['green']
    blue = ply_data['vertex']['blue']
    object_id = ply_data['vertex']['objectId']
    global_id = ply_data['vertex']['globalId']
    nyu40_id = ply_data['vertex']['NYU40']
    eigen13_id = ply_data['vertex']['Eigen13']
    rio27_id = ply_data['vertex']['RIO27']
 
    vertices = np.empty(len(x), dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4'),  ('red', 'u1'), ('green', 'u1'), ('blue', 'u1'),
                                                     ('objectId', 'h'), ('globalId', 'h'), ('NYU40', 'u1'), ('Eigen13', 'u1'), ('RIO27', 'u1')])
    
    vertices['x'] = x.astype('f4')
    vertices['y'] = y.astype('f4')
    vertices['z'] = z.astype('f4')
    vertices['red'] = red.astype('u1')
    vertices['green'] = green.astype('u1')
    vertices['blue'] = blue.astype('u1')
    vertices['objectId'] = object_id.astype('h')
    vertices['globalId'] = global_id.astype('h')
    vertices['NYU40'] = nyu40_id.astype('u1')
    vertices['Eigen13'] = eigen13_id.astype('u1')
    vertices['RIO27'] = rio27_id.astype('u1')
    return vertices


def main():

    # First, we set up a visualizer
    v = viz.Visualizer(position=np.array([-0.265198, -0.411423, 7.11054]), focal_length=28.0)
    
    # name = 'labels.instances.align.annotated.v2.ply'
    name = 'labels.instances.align.annotated.v2_neg_office.ply'

    prefix = '/Users/francis/Materials/graphloc/office_chair_moves/'
    # rooms = ['office_chair_move1', 'office_chair_move2', 'office_chair_moves3'] 
    rooms = ['office_chair_move1']  #, 'office_chair_move2', 'office_chair_moves3'] 

    for name in rooms:

        scene = o3d.io.read_point_cloud(os.path.join(prefix, name+".ply"))

        scene_meta = read_ply_data(os.path.join(prefix, name+".ply"))

        scene.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

        point_normals = np.asarray(scene.normals)
        point_positions = np.asarray(scene.points)
        point_positions -= np.mean(point_positions, axis=0)
        point_colors = np.asarray(scene.colors)

        # Find instance centers and colors
        objectIds = scene_meta['objectId']
        unique_objectIds = np.unique(objectIds)
        obj_centers = []
        obj_colors = []
        for obj_id in unique_objectIds:
            obj_center = np.mean(point_positions[objectIds == obj_id], axis=0)
            obj_color = point_colors[objectIds == obj_id][0, :]
            obj_centers.append(obj_center)
            obj_colors.append(obj_color)
        obj_centers = np.concatenate(obj_centers).reshape(-1, 3)
        obj_colors = np.concatenate(obj_colors).reshape(-1, 3)

        mask = obj_centers[:, 2] < 0.8
        obj_centers = obj_centers[mask]
        obj_colors = obj_colors[mask]

        nbrs = NearestNeighbors(n_neighbors=5, algorithm='ball_tree').fit(obj_centers)
        distances, indices = nbrs.kneighbors(obj_centers)
        for i in range(indices.shape[0]):
            for jj, j in enumerate(indices[i].tolist()):
                if distances[i][jj] < 2.0 and distances[i][jj] > 0.001:
                    edges = []
                    edges.append(obj_centers[i])
                    edges.append(obj_centers[j])
                    v.add_polyline(f'polyline{i}{j}', np.array(edges), color=np.array([100.0, 100.0, 100.0]), edge_width=0.02, alpha=0.5)

        mask = point_positions[:,2] < 0.8
        v.add_points('RGB Color', point_positions[mask], point_colors[mask] * 255, point_normals[mask], point_size=50, visible=True)
        v.add_points('centers', obj_centers, obj_colors * 255, point_size=200, resolution=15, visible=True)    
        # v.add_circles_2d('Labels',
        #              ['x', 'y', 'z']
        #              [np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]), np.array([0.0, 0.0, 1.0])],
        #              [np.array([255.0, 0.0, 0.0]), np.array([0.0, 255.0, 0.0]), np.array([0.0, 0.0, 255.0])],
        #              [np.array([255.0, 130.0, 130.0]), np.array([130.0, 255.0, 130.0]), np.array([130.0, 130.0, 255.0])],
        #              visible=False)
        # When we added everything we need to the visualizer, we save it.
        v.save('example_text', show_in_blender=True, blender_output_path=os.path.join(prefix, name+".png"), blender_path='/Applications/Blender.app/Contents/MacOS/Blender')


if __name__ == '__main__':
    main()
