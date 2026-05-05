## Version 0.5.1 (February 27, 2026)
 - **New Feature**: Path-based camera animation for Blender renders
   - Added `animation_camera_path` and `animation_look_at_path` to `BlenderConfig`
   - Smooth Bezier curve interpolation through custom path points
   - Support for looping trajectories and variable height profiles
 - **Enhanced Camera Control**:
   - Forward-facing mode: Camera automatically looks along the path direction when no look-at path is defined
   - Fixed look-at target: Camera focuses on a specific point via a one-point `animation_look_at_path`
   - Animated look-at path: Camera can animate both position and target using point paths
 - New examples: `example_spline_camera_trajectory.py` with three modes (fixed, forward-facing, look-at spline)

## Version 0.2
 - 0.3: Overall cleanup and support for blender renderings.
 - 0.2.32: Bug fixes.
 - 0.2.30: Add labels and include bootstrap files.
 - 0.2.27: Replaced euler angles with quaternions for objects.
 - 0.2.26: Specify camera up vector and bug fix.
 - 0.2.25: Bug fixes.
 - 0.2.24: Add arrows.
 - 0.2.23: Add segments.
 - 0.2.22: Add (oriented) bounding boxes.
 - 0.2.21: Add .obj meshes and other overall improvements.
 - 0.2.19: Add verbose flag to save function.
 - 0.2.18: Several smaller improvements, including colors for lines, alpha value for point clouds when no color is provided and assertions for shapes.
 - 0.2.12: Add alpha value to point clouds and folders to gui. Add progress bar while loading elements. Add camera object.
 - 0.2.11: Add phong shading to point clouds.
 - 0.2.10: Add lines primitives. Can for example be used to display normals.
 - 0.2.9: Add object parameter `visible` indicating wether the object is visible on default or not.
 
