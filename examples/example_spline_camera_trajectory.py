"""Example demonstrating spline-based camera trajectory for Blender animation."""
import pyviz3d as viz
import numpy as np
import os


def main():
    """Example with spline-based camera trajectory."""
    v = viz.Visualizer()
    
    # Create a simple scene
    # Add some points
    positions = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 1.0, 0.0],
        [-1.0, 1.0, 0.0],
        [0.5, -1.0, 0.0],
        [-0.5, -1.0, 0.0],
    ])
    colors = np.array([
        [255, 0, 0],
        [0, 255, 0],
        [0, 0, 255],
        [255, 255, 0],
        [255, 0, 255],
    ])
    
    v.add_points(
        'point_cloud',
        positions=positions,
        colors=colors,
        point_size=50,
    )
    
    # Add a bounding box
    v.add_bounding_box(
        'ground_plane',
        np.array([-2.0, -2.0, -0.5]),
        np.array([2.0, 2.0, 0.01])
    )
    
    # Define spline control points for the camera trajectory
    # The camera will move along a smooth curve through these points
    spline_control_points = [
        [3.0, 3.0, 1.5],    # Start position
        [2.0, -2.0, 1.2],   # Intermediate point
        [-3.0, -2.0, 1.5],  # Another intermediate point
        [-2.0, 3.0, 1.3],   # End position
    ]
    
    # Blender configuration with spline-based animation
    blender_config = viz.BlenderConfig(
        animation=True,
        animation_length=25,  # Number of frames
        animation_look_at_target=[0.0, 0.0, 0.0],  # Where camera looks at
        animation_spline_control_points=spline_control_points,  # Spline trajectory
        cycles_samples=50,
        render_resolution=[800, 600],
        render_film_transparent=False,
        output_prefix='video_spline_trajectory_',
        blender_path='/Applications/Blender.app/Contents/MacOS/Blender'
    )
    
    v.save('examples_output/example_spline_camera_trajectory', blender_config=blender_config)


if __name__ == '__main__':
    main()
