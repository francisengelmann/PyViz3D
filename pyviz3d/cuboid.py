"""Cuboid (bounding box) scene element."""


class Cuboid:
    """An oriented 3D bounding box."""

    def __init__(self, position, size, rotation, color, alpha, edge_width, visible):
        """Initialize a cuboid.

        Args:
            position: Center position (3,).
            size: Box dimensions (3,).
            rotation: Orientation as quaternion (4,).
            color: RGB color array-like in 0-255.
            alpha: Transparency value in [0, 1].
            edge_width: Edge line width.
            visible: Whether the cuboid is visible.
        """
        self.position = position
        self.size = size
        self.rotation = rotation
        self.color = color
        self.alpha = alpha
        self.edge_width = edge_width
        self.visible = visible

    def get_properties(self, binary_filename):
        """Return JSON-serializable properties for this cuboid.

        Args:
            binary_filename: Name of the binary data file (unused for cuboids).

        Returns:
            A dict of properties for the web viewer.
        """
        json_dict = {
            'type': 'cuboid',
            'position': self.position.tolist(),
            'size': self.size.tolist(),
            'orientation': self.rotation.tolist(),
            'color': self.color.tolist(),
            'alpha': float(self.alpha),
            'edge_width': float(self.edge_width),
            'visible': self.visible,
        }
        return json_dict

    def write_binary(self, path):
        """Write binary payload for this element (no-op)."""
        return

    def write_blender(self, path):
        """Write a Blender-friendly asset for this element (not implemented)."""
        print(type(self).__name__ + '.write_blender() not yet implemented.')
        return