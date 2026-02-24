"""The visualizer class is used to show 3d scenes."""

from .points import Points
from .labels import Labels
from .lines import Lines
from .mesh import Mesh
from .camera import Camera
from .cuboid import Cuboid
from .polyline import Polyline
from .arrow import Arrow
from .circles_2d import Circles2D
from .motion import Motion
from .blender_config import BlenderConfig

import os
import sys
import shutil
import json
import numpy as np

def euler_to_quaternion(x: float, y: float, z: float):
    """Convert Euler angles (radians) to a quaternion.

    Args:
        x: Rotation around X in radians.
        y: Rotation around Y in radians.
        z: Rotation around Z in radians.

    Returns:
        Quaternion as array [x, y, z, w].
    """
    cr = np.cos(x * 0.5)
    sr = np.sin(x * 0.5)
    cp = np.cos(y * 0.5)
    sp = np.sin(y * 0.5)
    cy = np.cos(z * 0.5)
    sy = np.sin(z * 0.5)
    q = np.zeros([4])
    q[0] = sr * cp * cy - cr * sp * sy  # x
    q[1] = cr * sp * cy + sr * cp * sy  # y
    q[2] = cr * cp * sy - sr * sp * cy  # z
    q[3] = cr * cp * cy + sr * sp * sy  # w
    return q

class Visualizer:
    """Scene builder and exporter for PyViz3D visualizations."""

    def __init__(self,
                 position: np.array = np.array([3.0, 3.0, 3.0]),
                 look_at: np.array = np.array([0.0, 0.0, 0.0]),
                 up: np.array = np.array([0.0, 0.0, 1.0]),
                 focal_length: float = 28.0):
        """Initialize a visualizer with a default camera.

        Args:
            position: Camera position (3,).
            look_at: Camera look-at point (3,).
            up: Camera up vector (3,).
            focal_length: Camera focal length in mm.
        """

        self.camera = Camera(
            position=np.array(position),
            look_at=np.array(look_at),
            up=np.array(up),
            focal_length=focal_length,
        )
        self.elements = {"Camera_0": self.camera}

    def __parse_name(self,
                     name: str) -> str:
        """Return a sanitized element name safe for use in filenames.

        Args:
            name: Element name.

        Returns:
            Sanitized name string.
        """
        return name.replace(':', ';')

    def save(self,
            path: str,
            port: int=6008,
            blender_config: BlenderConfig=None,
            verbose: bool=True) -> None:
        """Creates the visualization and displays the link to it.

        Args:
            path: Destination directory for the visualization.
            port: Port used in the printed local server command.
            blender_config: Optional Blender render configuration.
            verbose: Whether to print the web-server message.
        """

        # Delete destination directory if it exists already
        directory_destination = os.path.abspath(path)
        if os.path.isdir(directory_destination):
            shutil.rmtree(directory_destination)

        # Copy website directory
        directory_source = os.path.realpath(os.path.join(os.path.dirname(__file__), "src"))
        shutil.copytree(directory_source, directory_destination)

        # Assemble binary data files
        nodes_dict = {}
        for name, e in self.elements.items():
            binary_file_path = os.path.join(directory_destination, name + ".bin")
            nodes_dict[name] = e.get_properties(name + ".bin")
            e.write_binary(binary_file_path)
            if blender_config:
                blender_file_path = os.path.join(directory_destination, name + ".ply")
                e.write_blender(blender_file_path)

        # Write json file containing all scene elements
        json_file = os.path.join(directory_destination, "nodes.json")
        with open(json_file, "w") as outfile:
            json.dump(nodes_dict, outfile)

        # Display link
        if verbose:
          http_server_string = "python -m SimpleHTTPServer " + str(port)
          if sys.version[0] == "3":
              http_server_string = "python -m http.server " + str(port)
          print("")
          print(
              "************************************************************************"
          )
          print("1) Start local server:")
          print("    cd " + directory_destination + "; " + http_server_string)
          print("2) Open in browser:")
          print("    http://localhost:" + str(port))
          print(
              "************************************************************************"
          )

        # Render in blender if arguments are not None
        if blender_config:
            self.show_in_blender(path, blender_config, verbose)

    def show_in_blender(self,
                        path: str,
                        blender_config: BlenderConfig,
                        verbose: bool=True):
        """Generate Blender scripts and optionally render a scene.

        Args:
            path: Destination directory with scene files.
            blender_config: Blender render configuration.
            verbose: Whether to print Blender instructions.
        """

        directory_destination = os.path.abspath(path)
        blender_script_path = os.path.join(directory_destination, "blender_script.py")
        blender_config_path = os.path.join(directory_destination, "blender_config.json")
        with open(blender_config_path, 'w') as json_file:
          json.dump(blender_config.to_dict(), json_file, indent=2)
          
        with open(blender_script_path, "w") as outfile:
            outfile.write(
"import bpy\nimport os\n\
import sys\n\
sys.path.append(os.getcwd())\n\
import blender_tools\n\
blender_tools.main()")

        cmd = "cd " + directory_destination + "; " + blender_config.blender_path + " --background --python blender_script.py"
        if blender_config.render:
            cmd = cmd + " -- " + blender_config.output_prefix
        os.system(cmd)

        if verbose:
            print("")
            print("************************************************************************")
            print("Blender instructions")
            print(cmd)
            print("************************************************************************")
        
    def add_points(
        self,
        name: str,
        positions: np.array,
        colors: np.array=None,
        normals: np.array=None,
        point_size: int=25,
        resolution: int=3,
        visible: bool=True,
        alpha: float=1.0,
    ):
        """Add points to the visualizer.

        Args:
            name: Element name. Use ';' to create sub-layers.
            positions: Nx3 point positions.
            colors: Optional Nx3 RGB colors.
            normals: Optional Nx3 normals.
            point_size: Point size in viewer units.
            resolution: Blender sphere resolution.
            visible: Whether points are visible.
            alpha: Transparency in [0, 1].
        """

        assert positions.shape[1] == 3
        assert colors is None or positions.shape == colors.shape
        assert normals is None or positions.shape == normals.shape

        shading_type = 1  # Phong shading
        if colors is None:
            colors = np.ones(positions.shape, dtype=np.uint8) * 50  # gray
        if normals is None:
            normals = np.ones(positions.shape, dtype=np.float32)
            shading_type = 0  # Uniform shading when no normals are available

        positions = positions.astype(np.float32)
        colors = colors.astype(np.uint8)
        normals = normals.astype(np.float32)

        alpha = min(max(alpha, 0.0), 1.0)  # cap alpha to [0..1]

        self.elements[self.__parse_name(name)] = Points(
            positions, colors, normals, point_size, resolution, visible, alpha, shading_type
        )

    def add_labels(self,
                   name: str,
                   labels: list,
                   positions: np.array,
                   colors: np.array,
                   visible: bool=True):
        """Add labels to the visualizer.
        
        Args:
            name: Element name.
            labels: List of label strings.
            positions: Nx3 label positions.
            colors: Nx3 RGB colors for labels.
            visible: Whether labels are visible.
        """
        self.elements[self.__parse_name(name)] = Labels(labels, positions, colors, visible)

    def add_circles_2d(self,
                       name: str,
                       labels: list,
                       positions: np.array,
                       border_colors: np.array,
                       fill_colors: np.array,
                       visible: bool=True):
        """Add node to the visualizer.
        
        Args:
            name: Element name.
            labels: List of label strings.
            positions: Nx3 circle positions.
            border_colors: Nx3 RGB border colors.
            fill_colors: Nx3 RGB fill colors.
            visible: Whether circles are visible.
        """
        self.elements[self.__parse_name(name)] = Circles2D(labels, positions, border_colors, fill_colors, visible)

    def add_lines(self,
                  name: str,
                  lines_start: np.array,
                  lines_end: np.array,
                  colors: np.array=None,
                  visible: bool=True):
        """Add lines to the visualizer.

        Args:
            name: Element name.
            lines_start: Nx3 start points.
            lines_end: Nx3 end points.
            colors: Optional Nx3 RGB colors.
            visible: Whether lines are visible.
        """

        assert lines_start.shape[1] == 3
        assert lines_start.shape == lines_end.shape
        assert colors is None or lines_start.shape == colors.shape

        if colors is None:
            colors = np.ones(lines_start.shape, dtype=np.uint8) * 50  # gray

        colors = colors.astype(np.uint8)
        lines_start = lines_start.astype(np.float32)
        lines_end = lines_end.astype(np.float32)
        self.elements[self.__parse_name(name)] = Lines(lines_start, lines_end, colors, colors, visible)

    def add_bounding_box(self,
                         name: str,
                         position: np.array,
                         size: np.array,
                         rotation: np.array=np.array([0.0, 0.0, 0.0, 1.0]),
                         color: np.array=np.array([255, 0, 0]),
                         alpha: float=1.0,
                         edge_width: float=0.01,
                         visible: bool=True):
        """Add an oriented 3D bounding box."""
        rotation /= np.linalg.norm(rotation)  # normalize the orientation
        self.elements[self.__parse_name(name)] = Cuboid(position, size, rotation, color, alpha, edge_width, visible)

    def add_mesh(self,
                 name: str,
                 path: str,
                 translation: np.array=np.array([0.0, 0.0, 0.0]),
                 rotation: np.array=np.array([0.0, 0.0, 0.0, 1.0]),  # [x, y, z, w] - rotate w degrees rad around the axis xyz
                 scale: np.array=np.array([1, 1, 1]),
                 color: np.array=np.array([200, 200, 200]),
                 visible: bool=True):
                """Add a polygon mesh to the scene.

                Args:
                        name: Element name.
                        path: Path to an .obj mesh file.
                        translation: Translation vector.
                        rotation: Quaternion rotation.
                        scale: Scale vector.
                        color: RGB color array-like in 0-255.
                        visible: Whether the mesh is visible.
                """
        rotation /= np.linalg.norm(rotation)  # normalize the orientation
        self.elements[self.__parse_name(name)] = Mesh(path, translation=translation, rotation=rotation, scale=scale, color=color, visible=visible)

    def add_polyline(self,
                     name: str,
                     positions: np.array,
                     color: np.array=np.array([255, 0, 0]),
                     alpha: float=1.0,
                     edge_width: float=0.01,
                     visible: bool=True):
        """Add polyline.

        Args:
            name: Element name.
            positions: Nx3 positions along the polyline.
            color: RGB color array-like in 0-255.
            alpha: Transparency in [0, 1].
            edge_width: Line width.
            visible: Whether the polyline is visible.
        """

        self.elements[self.__parse_name(name)] = Polyline(positions, color, alpha, edge_width, visible)

    def add_superquadric(self,
        name: str,
        scalings: np.array=np.array([1.0, 1.0, 1.0]),
        exponents: np.array=np.array([2.0, 2.0, 2.0]),
        translation: np.array=np.array([0.0, 0.0, 0.0]),
        rotation: np.array=np.array([1.0, 0.0, 0.0, 0.0]),
        color: np.array=np.array([255, 255, 255]),
        resolution: int=30,
        visible: bool=True):
        """Add a superquadric mesh to the scene."""

        def create_superquadric_mesh(A, B, C, r, s, t, N):
            def f(o, m):
                return np.sign(np.sin(o)) * np.abs(np.sin(o))**m
            def g(o, m):
                return np.sign(np.cos(o)) * np.abs(np.cos(o))**m
            u = np.linspace(-np.pi, np.pi, N, endpoint=True)
            v = np.linspace(-np.pi/2.0, np.pi/2.0, N, endpoint=True)
            u = np.tile(u, N)
            v = np.repeat(v, N)
            triangles = []

            x = A * g(v, 2.0 / r) * g(u, 2.0 / r)
            y = B * g(v, 2.0 / s) * f(u, 2.0 / s)
            z = C * f(v, 2.0 / t)
            vertices =  np.concatenate([np.expand_dims(x, 1),
                                        np.expand_dims(y, 1),
                                        np.expand_dims(z, 1)], axis=1)
            triangles = []
            for i in range(N-1):
                for j in range(N-1):
                    triangles.append([i*N+j, (i+1)*N+j+1, (i+1)*N+j])
                    triangles.append([i*N+j, i*N+(j+1), (i+1)*N+(j+1)])
            return vertices, triangles

        vertices, triangles = create_superquadric_mesh(scalings[0], scalings[1], scalings[2],
                                                       exponents[0], exponents[1], exponents[2],
                                                       resolution)
        import open3d as o3d
        mesh_sq = o3d.geometry.TriangleMesh()
        mesh_sq.vertices = o3d.utility.Vector3dVector(vertices)
        mesh_sq.triangles = o3d.utility.Vector3iVector(triangles)
        o3d.io.write_triangle_mesh(f"{name}.obj", mesh_sq, write_ascii=True, compressed=False, write_vertex_normals=False, write_vertex_colors=False, write_triangle_uvs=False, print_progress=False)

        rotation /= np.linalg.norm(rotation)  # normalize the orientation
        scale = np.array([1.0, 1.0, 1.0])
        self.elements[self.__parse_name(name)] = Mesh(f"{name}.obj", translation=translation, rotation=rotation, scale=scale, color=color, visible=visible)

    def add_superquadric_rot_mat(self,
        name: str,
        scalings: np.array=np.array([1.0, 1.0, 1.0]),
        exponents: np.array=np.array([2.0, 2.0, 2.0]),
        translation: np.array=np.array([0.0, 0.0, 0.0]),
        rotation: np.array=np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0],[0.0, 0.0,1.0]]),
        color: np.array=np.array([255, 255, 255]),
        resolution: int=30,
        visible: bool=True):
        """Add a superquadric mesh using a rotation matrix."""

        def create_superquadric_mesh(A, B, C, r, s, t, N):
            def f(o, m):
                return np.sign(np.sin(o)) * np.abs(np.sin(o))**m
            def g(o, m):
                return np.sign(np.cos(o)) * np.abs(np.cos(o))**m
            u = np.linspace(-np.pi, np.pi, N, endpoint=True)
            v = np.linspace(-np.pi/2.0, np.pi/2.0, N, endpoint=True)
            u = np.tile(u, N)
            v = np.repeat(v, N)
            triangles = []

            x = A * g(v, 2.0 / r) * g(u, 2.0 / r)
            y = B * g(v, 2.0 / s) * f(u, 2.0 / s)
            z = C * f(v, 2.0 / t)
            vertices =  np.concatenate([np.expand_dims(x, 1),
                                        np.expand_dims(y, 1),
                                        np.expand_dims(z, 1)], axis=1)
            vertices = vertices @ rotation # apply rotation 

            triangles = []
            for i in range(N-1):
                for j in range(N-1):
                    triangles.append([i*N+j, (i+1)*N+j+1, (i+1)*N+j])
                    triangles.append([i*N+j, i*N+(j+1), (i+1)*N+(j+1)])
            return vertices, triangles

        vertices, triangles = create_superquadric_mesh(scalings[0], scalings[1], scalings[2],
                                                    exponents[0], exponents[1], exponents[2],
                                                    resolution)
        import open3d as o3d
        mesh_sq = o3d.geometry.TriangleMesh()
        mesh_sq.vertices = o3d.utility.Vector3dVector(vertices)
        mesh_sq.triangles = o3d.utility.Vector3iVector(triangles)
        if not os.path.exists("objs"):
            os.makedirs("objs")
        o3d.io.write_triangle_mesh(f"objs/{name}.obj", mesh_sq, write_ascii=True, compressed=False, write_vertex_normals=False, write_vertex_colors=False, write_triangle_uvs=False, print_progress=False)
        
        id_rot_quat = np.array([1,0,0,0])
        scale = np.array([1.0, 1.0, 1.0])
        self.elements[self.__parse_name(name)] = Mesh(f"objs/{name}.obj", translation=translation, rotation=id_rot_quat, scale=scale, color=color, visible=visible)

    def add_arrow(self,
                  name:str,
                  start: np.array,
                  end: np.array,
                  color: np.array=np.array([255, 0, 0]),
                  alpha: float=1.0,
                  stroke_width: float=0.01,
                  head_width: float=0.03,
                  visible: bool=True):
        """Add an arrow element."""

        self.elements[self.__parse_name(name)] = Arrow(start, end, color, alpha, stroke_width, head_width, visible)

    def add_motion(self, 
                   name: str, 
                   motion_type: str, 
                   motion_direction: np.array, 
                   motion_origin_pos: np.array,
                   motion_viz_orient: str, 
                   motion_dir_color: np.array=np.array([0, 255, 0]), 
                   motion_origin_color: np.array=np.array([0, 255, 0]), 
                   visible: bool=True):
        """Add a motion vector to the visualizer.

        Args:
            name: Element name.
            motion_type: "trans" for translation or "rot" for rotation.
            motion_direction: 3D direction vector.
            motion_origin_pos: 3D origin position.
            motion_viz_orient: "outwards" or "inwards".
            motion_dir_color: RGB color for the motion vector.
            motion_origin_color: RGB color for the origin marker.
            visible: Whether the motion vector is visible.

        Raises:
            AssertionError: If motion options are invalid.
        """
        assert motion_type in ["trans", "rot"], f"Unknown motion_type option {motion_type}"
        assert motion_viz_orient in ["outwards", "inwards"], f"Unknown motion_viz_orient option {motion_viz_orient}"

        self.elements[self.__parse_name(name)] = Motion(motion_type, motion_direction, motion_origin_pos, motion_viz_orient, motion_dir_color, motion_origin_color, visible)
