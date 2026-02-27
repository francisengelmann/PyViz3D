"""Arrow scene element."""

import numpy as np


class Arrow:
    """A 3D arrow defined by start and end points."""

    def __init__(self, start, end, color, alpha, stroke_width, head_width, visible):
        """Initialize an arrow element.

        Args:
            start: 3D start position array-like.
            end: 3D end position array-like.
            color: RGB color array-like in 0-255.
            alpha: Transparency value in [0, 1].
            stroke_width: Width of the arrow shaft.
            head_width: Width of the arrow head.
            visible: Whether the arrow is visible.
        """
        self.start = start
        self.end = end
        self.color = color
        self.alpha = alpha
        self.stroke_width = stroke_width
        self.head_width = head_width
        self.visible = visible

    def get_properties(self, binary_filename):
        """Return JSON-serializable properties for this arrow.

        Args:
            binary_filename: Name of the binary data file (unused for arrows).

        Returns:
            A dict of properties for the web viewer.
        """
        json_dict = {
            'type': 'arrow',
            'start': self.start.tolist(),
            'end': self.end.tolist(),
            'color': self.color.tolist(),
            'alpha': float(self.alpha),
            'stroke_width': float(self.stroke_width),
            'head_width': float(self.head_width),
            'visible': self.visible,
        }
        return json_dict

    def write_binary(self, path):
        """Write binary payload for this element (no-op)."""
        return

    def write_blender(self, path):
        """Write a Blender-friendly mesh for the arrow using Open3D."""
        import open3d as o3d
        
        # Calculate arrow direction and length
        direction = self.end - self.start
        arrow_length = np.linalg.norm(direction)
        if arrow_length == 0:
            return
        
        direction_normalized = direction / arrow_length
        
        # Proportions: shaft takes up most of the arrow, cone is at the tip
        cone_height = min(self.head_width * 2, arrow_length * 0.3)
        shaft_length = arrow_length - cone_height
        
        # Create cylinder for the shaft
        if shaft_length > 0:
            cylinder = o3d.geometry.TriangleMesh.create_cylinder(
                radius=self.stroke_width / 2,
                height=shaft_length
            )
            cylinder.compute_vertex_normals()
            cylinder.paint_uniform_color(self.color / 255.0)
        else:
            cylinder = o3d.geometry.TriangleMesh()
        
        # Create cone for the arrow head
        cone = o3d.geometry.TriangleMesh.create_cone(
            radius=self.head_width / 2,
            height=cone_height
        )
        cone.compute_vertex_normals()
        cone.paint_uniform_color(self.color / 255.0)
        
        # Translate cone to the end of the cylinder
        cone.translate([0, 0, shaft_length / 2 + cone_height / 2])
        
        # Translate cylinder to be centered at origin along shaft
        cylinder.translate([0, 0, shaft_length / 2])
        
        # Combine meshes
        arrow_mesh = cylinder + cone
        
        # Rotate arrow to align with direction
        # Default arrow points along +Z, we need to rotate it to point along direction
        z_axis = np.array([0, 0, 1])
        
        if not np.allclose(direction_normalized, z_axis):
            if np.allclose(direction_normalized, -z_axis):
                # Special case: arrow points in -Z direction
                rotation_axis = np.array([1, 0, 0])
                rotation_angle = np.pi
            else:
                rotation_axis = np.cross(z_axis, direction_normalized)
                rotation_axis = rotation_axis / np.linalg.norm(rotation_axis)
                rotation_angle = np.arccos(np.clip(np.dot(z_axis, direction_normalized), -1.0, 1.0))
            
            # Create rotation matrix from axis-angle
            R = o3d.geometry.get_rotation_matrix_from_axis_angle(rotation_axis * rotation_angle)
            arrow_mesh.rotate(R, center=[0, 0, 0])
        
        # Translate arrow to start position
        arrow_mesh.translate(self.start)
        
        o3d.io.write_triangle_mesh(path, arrow_mesh)