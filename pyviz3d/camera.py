# Points class i.e. point cloud.
import numpy as np


class Camera:
    def __init__(self, position, look_at):
        self.position = position.astype(np.float32)
        self.look_at = look_at.astype(np.float32)

    def get_properties(self, binary_filename):
        """
        :return: A dict conteining object properties. They are written into json and interpreted by javascript.
        """
        json_dict = {}
        json_dict['type'] = 'camera'
        json_dict['position'] = self.position.tolist()
        json_dict['look_at'] = self.look_at.tolist()
        return json_dict

    def write_binary(self, path):
        bin_position = self.position.tobytes()
        with open(path, "wb") as f:
            f.write(bin_position)
