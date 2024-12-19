"""Polygon mesh."""
from shutil import copyfile
import os

class Mesh:
    """Polygon mesh defined by .obj file and some solid color."""

    def __init__(self, filename, translation=None, rotation=None, scale=None, color=None, visible=True):
        self.filename_source = filename
        mesh_file = os.path.split(filename)[-1]
        mesh_file_name = mesh_file.split('.')[0]
        self.mesh_file_extension = mesh_file.split('.')[1]
        mesh_file_size = os.path.getsize(filename)
        self.filename_destination = mesh_file_name + '_' + str(mesh_file_size) + '.' + self.mesh_file_extension
        self.translation = translation.tolist()
        self.rotation = rotation.tolist()
        self.scale = scale.tolist()
        self.color = color.tolist()
        self.visible = visible

    def get_properties(self, filename):
        """
        :return: A dict containing object properties. They are written into json and interpreted by javascript.
        """
        json_dict = {
            'type': 'mesh',
            'filename': self.filename_destination,
            'translation': self.translation,
            'rotation': self.rotation,
            'scale': self.scale,
            'visible': self.visible,
            'color': self.color,
            }
        return json_dict

    def write_binary(self, path):
        destination_dir = os.path.dirname(path)
        destination_path = os.path.join(destination_dir, self.filename_destination)
        if not os.path.exists(self.filename_destination):
            copyfile(self.filename_source, destination_path)

    def write_blender(self, path):
        return