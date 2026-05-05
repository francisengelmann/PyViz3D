import numpy as np
import pyviz3d as viz


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

    angles = np.linspace(0.0, 2.0 * np.pi, 8, endpoint=False)
    camera_path = [
        [5.0 * np.cos(angle), 5.0 * np.sin(angle), 1.5]
        for angle in angles
    ]

    # Save everything
    blender_config = viz.BlenderConfig(
        animation=True,
        animation_length=10,
        animation_camera_path=camera_path,
        animation_look_at_path=[[0.0, 0.0, 0.0]],
        cycles_samples=10,
        render_resolution=[800, 600],
        render_film_transparent=False,
        output_prefix='horse/horse_',
        blender_path='/Applications/Blender.app/Contents/MacOS/Blender')
    v.save('examples_output/example_blender', blender_config=blender_config)

if __name__ == '__main__':
    main()
