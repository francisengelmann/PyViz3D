"""2D circle annotations anchored in 3D space."""
import numpy as np


class Circles2D:
    """A set of 2D circles with labels projected in the scene."""

    def __init__(self, labels, positions, border_colors, fill_colors, visible):
        """Initialize 2D circles.

        Args:
            labels: List of label strings.
            positions: Nx3 positions in world coordinates.
            border_colors: Nx3 RGB colors for borders.
            fill_colors: Nx3 RGB colors for fills.
            visible: Whether circles are visible.
        """
        self.labels = labels
        self.positions = positions
        self.border_colors = border_colors
        self.fill_colors = fill_colors
        self.visible = visible

    def get_properties(self, binary_filename):
        """Return JSON-serializable properties for this element.

        Args:
            binary_filename: Name of the binary data file (unused for circles).

        Returns:
            A dict of properties for the web viewer.
        """

        positions = np.array(self.positions)
        border_colors = np.array(self.border_colors)
        fill_colors = np.array(self.fill_colors)

        json_dict = {
            'type': 'circles_2d',
            'labels': self.labels,
            'positions': positions.tolist(),
            'border_colors': border_colors.tolist(),
            'fill_colors': fill_colors.tolist(),
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