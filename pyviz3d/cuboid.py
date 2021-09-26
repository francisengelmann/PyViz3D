# Cuboid class e.g. a bounding box.


class Cuboid:
    def __init__(self, position, size, orientation, color, alpha, edge_width, visible):
        self.position = position
        self.size = size
        self.orientation = orientation
        self.color = color
        self.alpha = alpha
        self.edge_width = edge_width
        self.visible = visible

    def get_properties(self, binary_filename):
        """ Get line properties, they are written into json and interpreted by javascript.
        :return: A dict conteining object properties.
        """
        json_dict = {
            'type': 'cuboid',
            'position': self.position.tolist(),
            'size': self.size.tolist(),
            'orientation': self.orientation.tolist(),
            'color': self.color.tolist(),
            'alpha': float(self.alpha),
            'edge_width': float(self.edge_width),
            'visible': self.visible,
        }
        return json_dict

    def write_binary(self, path):
        """Write lines to binary file."""
        return
