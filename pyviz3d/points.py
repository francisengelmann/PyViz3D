"""Points class i.e. point cloud."""
import numpy as np
import trimesh

_SPHERE_CACHE = {}

class Points:
    """Set of points defined by positions, colors, normals and more."""

    def __init__(self, positions, colors, normals, point_size, resolution, visible, alpha, shading_type=1):
        """Initialize point cloud data.

        Args:
            positions: Nx3 float32 positions.
            colors: Nx3 uint8 RGB colors.
            normals: Nx3 float32 normals.
            point_size: Point size in viewer units.
            resolution: Blender sphere resolution.
            visible: Whether points are visible.
            alpha: Transparency in [0, 1].
            shading_type: 0 for uniform, 1 for Phong.
        """
        self.positions = positions
        self.colors = colors
        self.normals = normals
        self.point_size = point_size
        self.resolution = resolution
        self.visible = visible
        self.alpha = alpha
        self.shading_type = shading_type

    def get_properties(self, binary_filename):
        """Return JSON-serializable properties for this element.

        Args:
            binary_filename: Name of the binary data file containing point data.

        Returns:
            A dict of properties for the web viewer.
        """
        json_dict = {
            'type': 'points',
            'visible': self.visible,
            'alpha': self.alpha,
            'shading_type': self.shading_type,
            'point_size': self.point_size,
            'num_points': self.positions.shape[0],
            'binary_filename': binary_filename}
        return json_dict

    def write_binary(self, path):
        """Write positions, normals, and colors to a binary file."""
        bin_positions = self.positions.tobytes()
        bin_normals = self.normals.tobytes()
        bin_colors = self.colors.tobytes()
        with open(path, "wb") as f:
            f.write(bin_positions)
            f.write(bin_normals)
            f.write(bin_colors)

    def write_blender(self, path):
        """Write a Blender-friendly mesh for the points using Open3D."""
        import open3d as o3d
        pcd_combined = o3d.geometry.TriangleMesh()

        def _create_sphere_at_xyz(xyz, colors, radius, resolution):
            sphere = o3d.geometry.TriangleMesh.create_sphere(radius=radius, resolution=resolution)
            sphere.compute_vertex_normals()
            sphere.paint_uniform_color(colors)
            sphere = sphere.translate(xyz)
            return sphere

        for i in range(self.positions.shape[0]):
            pcd_combined += _create_sphere_at_xyz(self.positions[i],
                                                  self.colors[i] / 255.0,
                                                  self.point_size / 1000.0,
                                                  resolution=self.resolution)

        o3d.io.write_triangle_mesh(path, pcd_combined)