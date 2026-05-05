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
    animation_camera_path: Optional[List[List[float]]] = field(default_factory=lambda: None)  # Camera path points; Blender interpolates between them.
    animation_look_at_path: Optional[List[List[float]]] = field(default_factory=lambda: None)  # Look-at path points; use one point for a fixed target.
    cycles_samples: int = 10  # Number of cycles samples
    file_format: str = 'PNG'

    # color_mode='RGBA'
    address: Dict[str, str] = field(default_factory=lambda: {"city": "Unknown", "state": "Unknown"})

    def to_dict(self):
        """Return a JSON-serializable representation of the config."""
        return self.__dict__