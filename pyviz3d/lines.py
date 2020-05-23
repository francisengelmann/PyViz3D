# Lines class i.e. normals.
import numpy as np


class Lines:
    def __init__(self, lines_start, lines_end, colors_start, colors_end, visible):
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
        """
        :return: A dict conteining object properties. They are written into json and interpreted by javascript.
        """
        json_dict = {}
        json_dict['type'] = 'lines'
        json_dict['visible'] = self.visible
        json_dict['num_lines'] = self.num_lines
        json_dict['binary_filename'] = binary_filename
        return json_dict

    def write_binary(self, path):
        bin_positions = self.positions.tobytes()
        bin_colors = self.colors.tobytes()
        with open(path, "wb") as f:
            f.write(bin_positions)
            f.write(bin_colors)
