"""Example demonstrating spline-based camera trajectory for Blender animation."""
import pyviz3d as viz
import numpy as np


def main():

  # Load point cloud as example scene
  scene_name = 'scene0000_00_vh_clean_2'
  scene = np.load('examples/data/' + scene_name + '.npy')
  point_positions = scene[:, 0:3] - np.mean(scene[:, 0:3], axis=0)
  point_colors = scene[:, 3:6]
  point_normals = scene[:, 6:9]

  # Set up visualizer and add point cloud
  v = viz.Visualizer()
  v.add_points(
      'point_cloud',
      positions=point_positions,
      colors=point_colors,
      normals=point_normals,
      point_size=35,
  )
  
  # Camera path points; Blender interpolates a smooth trajectory between them.
  camera_path = [
      [1.8, 1.2, 1.5],
      [1.6, -1.4, 1.4],
      [-1.2, -1.8, 1.5],
      [-1.8, 0.8, 1.45],
  ]

  look_at_path = [
      [0.5, 0.3, 1.2],
      [0.4, -0.6, 1.1],
      [-0.5, -0.7, 1.2],
      [-0.6, 0.2, 1.15],
  ]
  
  # Example 1: Camera follows spline with fixed look-at target
  print("Creating example with fixed look-at target...")
  config1 = viz.BlenderConfig(
      animation=True,
      animation_length=25,
      animation_look_at_path=[[0.0, 0.0, 0.0]],
      animation_camera_path=camera_path,
      cycles_samples=50,
      render_resolution=[800, 600],
      render_film_transparent=False,
      output_prefix='video_spline_fixed_lookat_',
      blender_path='/Applications/Blender.app/Contents/MacOS/Blender'
  )
  v.save('examples_output/example_spline_camera_trajectory_fixed', blender_config=config1)

  # Example 2: Camera follows spline while forward-facing (no look-at specified)
  print("Creating example with forward-facing camera...")
  config2 = viz.BlenderConfig(
      animation=True,
      animation_length=15,
      animation_camera_path=camera_path,
      cycles_samples=50,
      render_resolution=[800, 600],
      render_film_transparent=False,
      output_prefix='video_spline_forward_facing_',
      blender_path='/Applications/Blender.app/Contents/MacOS/Blender'
  )
  v.save('examples_output/example_spline_camera_trajectory_forward', blender_config=config2)
  
  # Example 3: Camera path and look-at path are both animated.
  print("Creating example with look-at spline trajectory...")
  config3 = viz.BlenderConfig(
      animation=True,
      animation_length=25,
      animation_look_at_path=look_at_path,
      animation_camera_path=camera_path,
      cycles_samples=50,
      render_resolution=[800, 600],
      render_film_transparent=False,
      output_prefix='video_spline_look_at_spline_',
      blender_path='/Applications/Blender.app/Contents/MacOS/Blender'
  )
  v.save('examples_output/example_spline_camera_trajectory_look_at', blender_config=config3)

if __name__ == '__main__':
    main()
