"""Arrow scene element."""


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
        """Write a Blender-friendly asset for this element (no-op)."""
        return