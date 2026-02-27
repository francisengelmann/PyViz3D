## Version 0.6.0 (February 27, 2026)
 - **New Feature**: Spline-based camera trajectories for Blender animations
   - Added `animation_spline_control_points` parameter to `BlenderConfig`
   - Smooth Bezier curve interpolation through custom control points
   - Full backward compatibility with circular trajectories
   - Support for looping trajectories and variable height profiles
 - New examples: `example_spline_camera_trajectory.py` and updated `example_superquadrics.py` with `--spline` flag
 - Comprehensive documentation in `docs/spline_camera_trajectory.md`

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
 
