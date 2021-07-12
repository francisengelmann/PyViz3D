"""Polygon mesh."""
from shutil import copyfile
import os

class Mesh:
    """Polygon mesh defined by .obj file and some solid color."""

    def __init__(self, filename, translation=None, rotation=None, scale=None, color=None, visible=True):
        self.filename = filename
        self.translation = translation
        self.rotation = rotation
        self.scale = scale
        self.color = color
        self.visible = visible

    def get_properties(self, filename):
        """
        :return: A dict conteining object properties. They are written into json and interpreted by javascript.
        """
        json_dict = {
            'type': 'obj',
            'filename': os.path.split(self.filename)[-1],
            'translation': self.translation,
            'rotation': self.rotation,
            'scale': self.scale,
            'color': self.color,
            'visible': self.visible,
            }
        return json_dict

    def write_binary(self, path):
        obj_file = os.path.split(self.filename)[-1]
        destination_dir = os.path.dirname(path)
        destination_path = os.path.join(destination_dir, obj_file)
        if not os.path.exists(destination_path):
            copyfile(self.filename, destination_path)
