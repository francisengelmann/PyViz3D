"""Motion vector element."""


class Motion:
    """Visual representation of translational or rotational motion."""

    def __init__(self, motion_type, motion_direction, motion_origin_pos, motion_viz_orient, motion_dir_color, motion_origin_color, visible):
        """Initialize a motion vector element.

        Args:
            motion_type: "trans" or "rot".
            motion_direction: 3D direction vector.
            motion_origin_pos: 3D origin position.
            motion_viz_orient: "outwards" or "inwards".
            motion_dir_color: RGB color for the motion vector.
            motion_origin_color: RGB color for the origin marker.
            visible: Whether the motion vector is visible.
        """
        self.motion_type = motion_type
        self.motion_direction = motion_direction
        self.motion_origin_pos = motion_origin_pos
        self.motion_viz_orient = motion_viz_orient
        self.motion_dir_color = motion_dir_color
        self.motion_origin_color = motion_origin_color
        self.visible = visible
    
    def get_properties(self, binary_filename):
        """Return JSON-serializable properties for this element.

        Args:
            binary_filename: Name of the binary data file (unused for motion).

        Returns:
            A dict of properties for the web viewer.
        """
        json_dict = {
            'type': 'motion',
            'motion_type': self.motion_type,
            'motion_direction': self.motion_direction.tolist(),
            'motion_origin_pos': self.motion_origin_pos.tolist(),
            'motion_viz_orient': self.motion_viz_orient,
            'motion_dir_color': self.motion_dir_color.tolist(),
            'motion_origin_color': self.motion_origin_color.tolist(),
            'visible': self.visible,
        }
        return json_dict

    def write_binary(self, path):
        """Write binary payload for this element (no-op)."""
        return

    def write_blender(self, path):
        """Write a Blender-friendly asset for this element (no-op)."""
        return
