# Points class i.e. point cloud.
import numpy as np


class Points:
    def __init__(self, positions, colors, normals, point_size=25, visible=True, alpha=1.0):
        self.positions = positions.astype(np.float32)
        self.colors = colors.astype(np.uint8)
        self.normals = normals.astype(np.float32)
        self.point_size = point_size
        self.visible = visible
        self.alpha = alpha

    def get_properties(self, binary_filename):
        """
        :return: A dict conteining object properties. They are written into json and interpreted by javascript.
        """
        json_dict = {}
        json_dict['type'] = 'points'
        json_dict['visible'] = self.visible
        json_dict['alpha'] = self.alpha
        json_dict['point_size'] = self.point_size
        json_dict['num_points'] = self.positions.shape[0]
        json_dict['binary_filename'] = binary_filename
        return json_dict

    def write_binary(self, path):
        bin_positions = self.positions.tobytes()
        bin_normals = self.normals.tobytes()
        bin_colors = self.colors.tobytes()
        with open(path, "wb") as f:
            f.write(bin_positions)
            f.write(bin_normals)
            f.write(bin_colors)

