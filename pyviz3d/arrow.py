# Arrow class.


class Arrow:
    def __init__(self, start, end, color, alpha, stroke_width, head_width, visible):
        self.start = start
        self.end = end
        self.color = color
        self.alpha = alpha
        self.stroke_width = stroke_width
        self.head_width = head_width
        self.visible = visible

    def get_properties(self, binary_filename):
        """ Get line properties, they are written into json and interpreted by javascript.
        :return: A dict conteining object properties.
        """
        json_dict = {
            'type': 'arrow',
            'start': self.start.tolist(),
            'end': self.end.tolist(),
            'color': self.color.tolist(),
            'alpha': float(self.alpha),
            'stroke_width': float(self.stroke_width),
            'head_width': float(self.head_width),
            'visible': self.visible,
        }
        return json_dict

    def write_binary(self, path):
        """Write lines to binary file."""
        return
