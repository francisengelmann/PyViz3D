"""Polyline element."""


class Polyline:
    """A connected series of line segments."""

    def __init__(self, positions, color, alpha, edge_width, visible):
        """Initialize a polyline.

        Args:
            positions: Nx3 positions along the polyline.
            color: RGB color array-like in 0-255.
            alpha: Transparency value in [0, 1].
            edge_width: Line width.
            visible: Whether the polyline is visible.
        """
        self.positions = positions
        self.color = color
        self.alpha = alpha
        self.edge_width = edge_width
        self.visible = visible

    def get_properties(self, binary_filename):
        """Return JSON-serializable properties for this element.

        Args:
            binary_filename: Name of the binary data file (unused for polylines).

        Returns:
            A dict of properties for the web viewer.
        """
        json_dict = {
            'type': 'polyline',
            'positions': self.positions.tolist(),
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
        """Write a Blender-friendly asset for this element (no-op)."""
        return