import numpy as np
import pyviz3d.visualizer as viz
import plyfile  # pip3 install plyfile
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

    v = viz.Visualizer(position=np.array([-0.265198, -0.411423, 7.11054]), focal_length=28.0, animation=False)

    # Read input scene
    prefix = 'examples/data/'
    name = 'office_chairs_instances'
    scene = o3d.io.read_point_cloud(os.path.join(prefix, name+".ply"))
    scene_meta_data = read_ply_data(os.path.join(prefix, name+".ply"))
    scene.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

    # Preapre for visualization
    point_normals = np.asarray(scene.normals)
    point_positions = np.asarray(scene.points)
    point_positions -= np.mean(point_positions, axis=0)
    point_colors = np.asarray(scene.colors)

    # Cut off ceiling so we can look inside the scene from the top
    mask = point_positions[:, 2] < 0.8
    point_positions = point_positions[mask]
    point_normals = point_normals[mask]
    point_colors = point_colors[mask]

    # Find instance centers and corresponding colors
    objectIds = scene_meta_data['objectId'][mask]
    unique_objectIds = np.unique(objectIds)
    obj_centers = []
    obj_colors = []
    for obj_id in unique_objectIds:
        obj_center = np.mean(point_positions[objectIds == obj_id], axis=0)
        obj_color = point_colors[objectIds == obj_id][0, :]
        obj_centers.append(obj_center)
        obj_colors.append(obj_color)
    obj_centers = np.concatenate(obj_centers).reshape(-1, 3)
    obj_colors = np.concatenate(obj_colors).reshape(-1, 3) * 0.5  # make them a bit darker

    # Compute edges nearest-neighbor graph
    nbrs = NearestNeighbors(n_neighbors=5, algorithm='ball_tree').fit(obj_centers)
    distances, indices = nbrs.kneighbors(obj_centers)
    for i in range(indices.shape[0]):
        for jj, j in enumerate(indices[i].tolist()):
            if distances[i][jj] < 2.0 and distances[i][jj] > 0.001:
                edges = []
                edges.append(obj_centers[i])
                edges.append(obj_centers[j])
                v.add_polyline(f'polyline{i}{j}', np.array(edges), color=np.array([100.0, 100.0, 100.0]), edge_width=0.02, alpha=0.5)

    v.add_points('RGB Color', point_positions, point_colors * 255, point_normals, point_size=50, visible=True)
    v.add_points('Instances', obj_centers, obj_colors * 255, point_size=200, resolution=15, visible=True)

    # Vsualize the scene and its graph in the browser and also in blender
    render_path =f'~/{name}.png'
    blender_path = '/Applications/Blender.app/Contents/MacOS/Blender'

    blender_args = {'output_prefix': render_path,
                    'executable_path': blender_path}
    v.save('example_graph', blender_args=blender_args)


if __name__ == '__main__':
    main()
