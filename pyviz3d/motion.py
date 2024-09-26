# Motion class.


class Motion:
    def __init__(self, motion_type, motion_direction, motion_origin_pos, motion_viz_orient, motion_dir_color, motion_origin_color, visible):
        self.motion_type = motion_type
        self.motion_direction = motion_direction
        self.motion_origin_pos = motion_origin_pos
        self.motion_viz_orient = motion_viz_orient
        self.motion_dir_color = motion_dir_color
        self.motion_origin_color = motion_origin_color
        self.visible = visible
    
    def get_properties(self, binary_filename):
        """ 
        :return: A dict containing object properties. They are written into json and interpreted by javascript.
        """
        json_dict = {
            'type': 'motion',
            'motion_type': self.motion_type,
            'motion_direction': self.motion_direction.tolist(),
            'motion_origin_pos': self.motion_origin_pos.tolist(),
            'motion_viz_orient': self.motion_viz_orient,
            'motion_dir_color': self.motion_dir_color.tolist(),
            'motion_origin_color': self.motion_origin_color.tolist(),
            'visible': self.visible,
        }
        return json_dict

    def write_binary(self, path):
        """Write lines to binary file."""
        return
