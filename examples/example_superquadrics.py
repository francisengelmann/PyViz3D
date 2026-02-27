"""Test the new Superquadric class."""
import pyviz3d as viz
import numpy as np
import os


def generate_ncolors(n, saturation=0.65, value=0.9):
    """Generate n visually distinct RGB colors as uint8 in [0, 255]."""
    if n <= 0:
        return np.zeros((0, 3), dtype=np.uint8)
    from colorsys import hsv_to_rgb
    hues = np.linspace(0.0, 1.0, n, endpoint=False)
    colors = [hsv_to_rgb(h, saturation, value) for h in hues]
    return (np.array(colors) * 255).astype(np.uint8)


def main():
    v = viz.Visualizer()
    create_demo_superquadrics(v)

    # Load and visualize lamp superquadrics
    npz_path = os.path.join(os.path.dirname(__file__), 'data', 'lamp_superquadrics.npz')
    data = np.load(npz_path, allow_pickle=True)
    sample_index = 0
    P = data['scale'].shape[1]
    colors = generate_ncolors(P)
    rot_x = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, 1.0, 0.0]])
    
    scale = data['scale']
    rotation = data['rotation']
    translation = data['translation']
    exponents = data['exponents']
    exist = data['exist']
    tapering = data.get('tapering', np.zeros((scale.shape[0], scale.shape[1], 2)))
    bending = data.get('bending', np.zeros((scale.shape[0], scale.shape[1], 6)))

    for p in range(P):
        if exist[sample_index, p] > 0.5:
            rotation_mat = rot_x @ rotation[sample_index, p]
            exponents_3d = np.array([
                exponents[sample_index, p, 0],
                exponents[sample_index, p, 1],
                exponents[sample_index, p, 0],
            ])
            
            v.add_superquadric_direct(
                name=f"lamp_sq;{p}",
                scalings=scale[sample_index, p],
                exponents=exponents_3d,
                translation=rot_x @ translation[sample_index, p],
                rotation=np.array([0.0, 0.0, 0.0, 1.0]),
                rotation_matrix=rotation_mat,
                color=colors[p],
                tapering=tapering[sample_index, p],
                bending=bending[sample_index, p],
                resolution=300,
                alpha=1.0,
                wireframe=True,
            )

    v.add_bounding_box('ground_plane', np.array([0.0, 0.0, -0.5]), np.array([5.0, 5.0, 0.001]))

    blender_config = viz.BlenderConfig(
        animation=True,
        animation_length=50,
        animation_circle_radius=3.0,
        animation_circle_center=[0.0, 0.0, 1.0],
        animation_circle_rotation=[np.pi/8, 0.0, 0.0],
        animation_look_at_target=[0.0, 0.0, 0.0],
        cycles_samples=50,
        render_resolution=[800, 600],
        render_film_transparent=False,
        output_prefix='video_lamp_',
        blender_path='/Applications/Blender.app/Contents/MacOS/Blender')
    v.save('examples_output/example_superquadrics', blender_config=blender_config)


def create_demo_superquadrics(v):
    """Create demo superquadrics for visualization."""
    v.add_superquadric_direct(
        'sq_direct_1',
        exponents=np.array([1.0, 1.0, 1.0]),
        scalings=np.array([0.25, 0.75, 0.25]),
        color=np.array([255, 0, 0]),
        translation=np.array([0.0, -1.25, 0.0]),
        resolution=100,
        wireframe=True,
    )

    v.add_superquadric_direct(
        'sq_direct_2',
        exponents=np.array([0.3, 0.3, 0.3]),
        scalings=np.array([0.5, 0.125, 0.75]),
        color=np.array([0, 255, 100]),
        translation=np.array([1.25, 0.0, 0.0]),
        tapering=np.array([0.5, 0.3]),
        resolution=300,
        alpha=0.8,
        wireframe=True,
    )

    v.add_superquadric_direct(
        'sq_direct_3',
        exponents=np.array([1.0, 1.0, 1.0]),
        scalings=np.array([0.25, 0.25, 0.5]),
        color=np.array([0, 100, 255]),
        translation=np.array([0.75, 1.25, 0.25]),
        bending=np.array([0.5, 0.0, 0.0, 0.0, 0.0, 0.0]),
        resolution=200,
        wireframe=True,
    )

    v.add_superquadric_direct(
        'sq_direct_4',
        exponents=np.array([0.2, 1.0, 0.2]),
        scalings=np.array([0.375, 0.375, 0.625]),
        color=np.array([255, 165, 0]),
        translation=np.array([-0.75, 0.0, 0.25]),
        tapering=np.array([0.3, 0.3]),
        bending=np.array([0.3, np.pi/4, 0.0, 0.0, 0.0, 0.0]),
        resolution=400,
        alpha=0.9,
        wireframe=True,
    )


if __name__ == '__main__':
    main()