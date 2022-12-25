"""Labels class e.g. to visualize the labels of instances."""
import numpy as np


class Labels:
    """Set of labels."""

    def __init__(self, labels, positions, colors, visible):
        self.labels = labels
        self.positions = positions
        self.colors = colors
        self.visible = visible

    def get_properties(self, binary_filename):
        """ Get arrow properties, they are written into json and interpreted by javascript.
        :return: A dict conteining object properties.
        """

        positions = np.array(self.positions)
        colors = np.array(self.colors)

        json_dict = {
            'type': 'labels',
            'labels': self.labels,
            'positions': positions.tolist(),
            'colors': colors.tolist(),
            'visible': self.visible,
        }
        return json_dict

    def write_binary(self, path):
        """Write lines to binary file."""
        return
