import numpy as np
import pyviz3d.visualizer as viz


def main():
    # Load point cloud
    data = np.load('examples/data/horse.npy')
    r=-3.1415/2.0
    rot_matrix = np.array(
        [[1.0, 0.0, 0.0],[0.0, np.cos(r), -np.sin(r)],[0, np.sin(r), np.cos(r)]])
    points = data[:, 0:3] @ rot_matrix
    colors = np.ones_like(points) * 100
    colors[:, 1] = 200
    
    # Setting up the visualizer, including the camera parameters
    v = viz.Visualizer(
            position=np.array([0.0, 5.0, 2.0]),
            look_at=np.array([0.0, 0.0, 0.0]),
            up=np.array([0.0, 0.0, 1.0]),
            focal_length=45.0)
    
    # Add the point cloud
    v.add_points('Horse', points, colors, point_size=15, visible=True)

    # Add a white thin box below the point cloud for the shadow
    v.add_bounding_box('background', np.array([0.0, 0.0, np.min(points[:, 2])]), np.array([3, 3, 0.001]))

    # Save everything
    v.save(f'example_blender',
           show_in_blender=True, # Should we use blender?
           blender_output_path='horse.png',  # Where to save the rendering, if None don't render
           blender_executable_path='/Applications/Blender.app/Contents/MacOS/Blender')  # Path to blender executable

if __name__ == '__main__':
    main()
