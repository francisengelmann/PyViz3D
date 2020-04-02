# Points class i.e. point cloud.
import numpy as np


class Points:
    def __init__(self, positions, colors, point_size=5):
        self.positions = positions.astype(np.float32)
        self.colors = colors.astype(np.uint8)
        self.point_size = point_size

    def get_properties(self, binary_filename):
        """
        :return: A dict conteining object properties. They are written into json and interpreted by javascript.
        """
        json_dict = {}
        json_dict['type'] = 'points'
        json_dict['point_size'] = self.point_size
        json_dict['num_points'] = self.positions.shape[0]
        json_dict['binary_filename'] = binary_filename
        return json_dict

    def write_binary(self, path):
        bin_positions = self.positions.tobytes()
        bin_colors = self.colors.tobytes()
        with open(path, "wb") as f:
            f.write(bin_positions)
            f.write(bin_colors)

