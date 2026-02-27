"""Configuration for Blender rendering."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class BlenderConfig:
    """Settings used when exporting and rendering with Blender."""
    blender_path: str 
    render: bool = True  # Whether or not to render in blender
    render_resolution: List[int] = field(default_factory=lambda: [800, 600])
    render_film_transparent: bool = True
    output_prefix: str = 'out'
    animation: bool = False  # If true, renders a video sequence.
    animation_length: int = 60  # Number of frames in the animation.
    animation_circle_radius: float = 5.0  # Radius of cirlce on which the camera moves around the center
    animation_circle_center: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    animation_circle_rotation: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    animation_look_at_target: Optional[List[float]] = field(default_factory=lambda: None)  # Camera look-at point (defaults to animation_circle_center if None)
    animation_spline_control_points: Optional[List[List[float]]] = field(default_factory=lambda: None)  # Control points for spline-based camera trajectory
    cycles_samples: int = 10  # Number of cycles samples
    file_format: str = 'PNG'

    # color_mode='RGBA'
    address: Dict[str, str] = field(default_factory=lambda: {"city": "Unknown", "state": "Unknown"})

    def to_dict(self):
        """Return a JSON-serializable representation of the config."""
        return self.__dict__