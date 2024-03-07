"""Labels class e.g. to visualize the labels of instances."""
import numpy as np


class Circles2D:
    """Set of labels."""

    def __init__(self, labels, positions, border_colors, fill_colors, visible):
        self.labels = labels
        self.positions = positions
        self.border_colors = border_colors
        self.fill_colors = fill_colors
        self.visible = visible

    def get_properties(self, binary_filename):
        """ Get arrow properties, they are written into json and interpreted by javascript.
        :return: A dict conteining object properties.
        """

        positions = np.array(self.positions)
        border_colors = np.array(self.border_colors)
        fill_colors = np.array(self.fill_colors)

        json_dict = {
            'type': 'circles_2d',
            'labels': self.labels,
            'positions': positions.tolist(),
            'border_colors': border_colors.tolist(),
            'fill_colors': fill_colors.tolist(),
            'visible': self.visible,
        }
        return json_dict

    def write_binary(self, path):
        """Write lines to binary file."""
        return

    def write_blender(self, path):
        print(type(self).__name__+'.write_blender() not yet implemented.' )
        return