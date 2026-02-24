"""Labels class e.g. to visualize the labels of instances."""
import numpy as np


class Labels:
    """Set of labels."""

    def __init__(self, labels, positions, colors, visible):
        """Initialize labels.

        Args:
            labels: List of label strings.
            positions: Nx3 positions in world coordinates.
            colors: Nx3 RGB colors for each label.
            visible: Whether labels are visible.
        """
        self.labels = labels
        self.positions = positions
        self.colors = colors
        self.visible = visible

    def get_properties(self, binary_filename):
        """Return JSON-serializable properties for this element.

        Args:
            binary_filename: Name of the binary data file (unused for labels).

        Returns:
            A dict of properties for the web viewer.
        """

        positions = np.array(self.positions)
        colors = np.array(self.colors)

        json_dict = {
            'type': 'labels',
            'labels': self.labels,
            'positions': positions.tolist(),
            'colors': colors.tolist(),
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