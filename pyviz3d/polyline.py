# Cuboid class e.g. a bounding box.


class Polyline:
    def __init__(self, positions,color, alpha, edge_width, visible):
        self.positions = positions
        self.color = color
        self.alpha = alpha
        self.edge_width = edge_width
        self.visible = visible

    def get_properties(self, binary_filename):
        """ Get line properties, they are written into json and interpreted by javascript.
        :return: A dict conteining object properties.
        """
        json_dict = {
            'type': 'polyline',
            'positions': self.positions.tolist(),
            'color': self.color.tolist(),
            'alpha': float(self.alpha),
            'edge_width': float(self.edge_width),
            'visible': self.visible,
        }
        return json_dict

    def write_binary(self, path):
        """Write lines to binary file."""
        return
