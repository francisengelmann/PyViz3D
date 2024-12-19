from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class BlenderConfig:
    blender_path: str 
    render: bool = True  # Whether or not to render in blender
    render_resolution: List[int] = field(default_factory=lambda: [800, 600])
    render_film_transparent: bool = True
    output_prefix: str = 'out'
    animation: bool = False  # If true, renders a video sequence.
    animation_length: int = 60  # Number of frames in the animation.
    animation_circle_radius: float = 5.0  # Radius of cirlce on which the camera moves around the center
    animation_circle_center: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    cycles_samples: int = 10  # Number of cycles samples
    file_format: str = 'PNG'

    # color_mode='RGBA'
    address: Dict[str, str] = field(default_factory=lambda: {"city": "Unknown", "state": "Unknown"})

    def to_dict(self):
        return self.__dict__