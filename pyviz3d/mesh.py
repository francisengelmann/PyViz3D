"""Polygon mesh."""
from shutil import copyfile
import os

class Mesh:
    """Polygon mesh defined by .obj file and some solid color."""

    def __init__(self, filename, translation=None, rotation=None, scale=None, color=None, visible=True):
        self.filename_source = filename
        obj_file = os.path.split(filename)[-1]
        obj_file_name = obj_file.split('.')[0]
        obj_file_extension = obj_file.split('.')[1]
        obj_file_size = os.path.getsize(filename)
        self.filename_destination = obj_file_name + '_' + str(obj_file_size) + '.' + obj_file_extension
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
            'filename': self.filename_destination,
            'translation': self.translation,
            'rotation': self.rotation,
            'scale': self.scale,
            'color': self.color,
            'visible': self.visible,
            }
        return json_dict

    def write_binary(self, path):
        destination_dir = os.path.dirname(path)
        destination_path = os.path.join(destination_dir, self.filename_destination)
        if not os.path.exists(self.filename_destination):
            copyfile(self.filename_source, destination_path)
