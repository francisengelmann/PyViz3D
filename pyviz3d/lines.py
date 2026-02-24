"""Lines class e.g. to visualize normals."""
import numpy as np


class Lines:
    """Set of line segments defined by start and end points."""

    def __init__(self, lines_start, lines_end, colors_start, colors_end, visible):
        """Initialize line segments.

        Args:
            lines_start: Nx3 array of start points.
            lines_end: Nx3 array of end points.
            colors_start: Nx3 RGB colors for start vertices.
            colors_end: Nx3 RGB colors for end vertices.
            visible: Whether lines are visible.
        """
        # Interleave start and end positions for WebGL.
        self.num_lines = lines_start.shape[0]
        self.positions = np.empty((self.num_lines * 2, 3), dtype=lines_start.dtype)
        self.positions[0::2] = lines_start
        self.positions[1::2] = lines_end
        self.colors = np.empty((self.num_lines * 2, 3), dtype=np.uint8)
        self.colors[0::2] = colors_start
        self.colors[1::2] = colors_end
        self.visible = visible

    def get_properties(self, binary_filename):
        """Return JSON-serializable properties for this element.

        Args:
            binary_filename: Name of the binary data file containing line data.

        Returns:
            A dict of properties for the web viewer.
        """
        json_dict = {
            'type': 'lines',
            'visible': self.visible,
            'num_lines': self.num_lines,
            'binary_filename': binary_filename}
        return json_dict

    def write_binary(self, path):
        """Write interleaved line positions and colors to binary file."""

        bin_positions = self.positions.tobytes()
        bin_colors = self.colors.tobytes()
        with open(path, "wb") as f:
            f.write(bin_positions)
            f.write(bin_colors)

    def write_blender(self, path):
        """Write a Blender-friendly asset for this element (not implemented)."""
        print(type(self).__name__ + '.write_blender() not yet implemented.')
        return