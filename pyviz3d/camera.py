"""Camera related functionality."""
import numpy as np


class Camera:
    """Camera class looking at the scene"""

    def __init__(self, position, look_at):
        self.position = position.astype(np.float32)
        self.look_at = look_at.astype(np.float32)

    def get_properties(self, binary_filename):
        """Get the camera properties, they are written into json and interpreted by javascript.

        :return: A dict conteining object properties.
        """
        json_dict = {
            'type': 'camera',
            'position': self.position.tolist(),
            'look_at': self.look_at.tolist()}
        return json_dict

    def write_binary(self, path):
        """Write camera to binary file."""
        bin_position = self.position.tobytes()
        with open(path, "wb") as f:
            f.write(bin_position)
