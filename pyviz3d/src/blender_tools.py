import bpy
import math
import mathutils
import numpy as np
import subprocess
import json
import os

C = bpy.context
D = bpy.data

import sys
argv = sys.argv
try:
    argv = argv[argv.index("--") + 1:]  # get all args after "--"
except ValueError:
   argv = []

def clear_scene():
  # Remove all meshes from the scene, keep the light and camera
  for o in C.scene.objects:
    print(o)
    if o.type == 'MESH':
        o.select_set(True)
    else:
        o.select_set(False)
  bpy.ops.object.delete()


def render(output_prefix, configuration):
  """
  :path: the file path of the rendered image
  :file_format: {PNG, JPEG}
  """
  
  # C.scene.view_settings.view_transform = 'Standard'
  # D.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
  # bpy.context.scene.world.use_nodes = False
  # bpy.context.scene.world.color = (1, 1, 1)
  # C.scene.render.alpha_mode = 'SKY'
  
  if configuration['animation']:
    print(configuration['animation_circle_center'])
    bpy.ops.curve.primitive_bezier_circle_add(
       radius=configuration['animation_circle_radius'], enter_editmode=False, align='WORLD',
       location=configuration['animation_circle_center'],
       rotation=configuration['animation_circle_rotation'],
       scale=(1, 1, 1))
    bezier_circle = C.object
    bpy.context.object.data.path_duration = configuration['animation_length']
    bpy.context.scene.frame_end = configuration['animation_length']
    bpy.context.scene.cycles.samples = configuration['cycles_samples']
    bpy.data.scenes['Scene'].render.ffmpeg.codec = 'H264'

    cam = C.scene.objects['Camera']
    cam.select_set(True)
    bpy.context.view_layer.objects.active = cam
    cam.matrix_world = mathutils.Matrix(np.eye(4))
    cam.location = [0.0, 0.0, 0.5]
    bpy.ops.object.constraint_add(type='FOLLOW_PATH')
    cam.constraints["Follow Path"].target = bezier_circle
    bpy.ops.object.constraint_add(type='TRACK_TO')
    empty = bpy.data.objects.new("TrackTarget", None)
    look_at = configuration.get('animation_look_at_target') or configuration['animation_circle_center']
    empty.location = look_at
    bpy.context.scene.collection.objects.link(empty)
    cam.constraints["Track To"].target = empty
    bpy.ops.constraint.followpath_path_animate(constraint="Follow Path", owner='OBJECT')

  bpy.ops.render.render(use_viewport=True, animation=configuration['animation'], write_still=True)

  # Combine individual frames into video using ffmpeg
  if configuration['animation']:
    output_filepath = output_prefix + '.mp4'
    subprocess.run(["ffmpeg", "-y", "-i", f'{output_prefix}%04d.png',
                     "-vcodec", "libx264", "-crf", "18", "-preset", "slow",
                     "-vf", "format=yuv420p", output_filepath])
    subprocess.run(["ffmpeg", "-y", "-i", output_filepath, "-pix_fmt", "rgb24", output_filepath[:-3]+'gif'])


def save_blender_scene(path: str) -> None:
  bpy.ops.wm.save_as_mainfile(filepath=path)


def compute_object_center(object):
  local_bbox_center = 0.125 * sum((mathutils.Vector(b) for b in object.bound_box),
                                   mathutils.Vector())
  return object.matrix_world @ local_bbox_center


def look_at(camera,
            eye=mathutils.Vector((13.0, 13.0, 13.0)),
            at=mathutils.Vector((0.0, 0.0, 3.0)),
            up=mathutils.Vector((0.0, 0.0, 1.0))):
  d = (eye - at).normalized()
  r = up.cross(d).normalized()
  u = d.cross(r).normalized()
  camera.matrix_world = mathutils.Matrix(((r.x, u.x, d.x, eye.x),
                                          (r.y, u.y, d.y, eye.y),
                                          (r.z, u.z, d.z, eye.z),
                                          (0.0, 0.0, 0.0, 1.0)))


def init_scene(configuration):
  # render stuff
  C.scene.render.resolution_x = configuration['render_resolution'][0]
  C.scene.render.resolution_y = configuration['render_resolution'][1]
  C.scene.render.film_transparent = configuration['render_film_transparent']
  if configuration['render_film_transparent']:
    C.scene.render.image_settings.color_mode = 'RGBA'
  else:
    C.scene.render.image_settings.color_mode = 'RGB'
  C.scene.render.image_settings.file_format=configuration['file_format']
  C.scene.render.filepath = configuration['output_prefix']
  C.scene.view_settings.look = 'AgX - Medium High Contrast'
  C.scene.view_settings.view_transform = 'Standard'
  C.scene.render.engine = 'CYCLES'
  C.scene.cycles.device = 'GPU'
  C.scene.cycles.preview_samples = 50
  C.scene.cycles.samples = 50

  bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
  bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 1

  # Add lights
  # C.scene.objects['Light'].data.shadow_soft_size = 1.0
  # C.scene.objects['Light'].data.cycles.cast_shadow = False
  # C.scene.objects['Light'].data.energy = 1000.0
  # C.scene.objects['Light'].data.use_shadow = False

  # bpy.ops.object.light_add(type='POINT', radius=1, align='WORLD', location=(-1, 1, 10), scale=(1, 1, 1))
  # C.scene.objects['Point'].data.energy = 3000.0
  # C.scene.objects['Point'].data.shadow_soft_size = 3

  # for i in range(4):
  #   bpy.ops.object.light_add(type='POINT', radius=0.1, align='WORLD', location=(i%2, i//2, 1), scale=(1, 1, 1))
  #   C.scene.objects[f'Point.{str(i+1).zfill(3)}'].data.energy = 5.0
  #   C.scene.objects[f'Point.{str(i+1).zfill(3)}'].data.shadow_soft_size = 0.1
  #   C.scene.objects[f'Point.{str(i+1).zfill(3)}'].data.color = (1, 0.795182, 0.375358)


def create_mat(obj, color=None, alpha=1.0):
    mat = bpy.data.materials.new(name="material")
    mat.use_backface_culling = True
    obj.data.materials.append(mat)
    mat.use_nodes = True
    mat.node_tree.nodes.new(type="ShaderNodeVertexColor")
    bsdf = mat.node_tree.nodes["Principled BSDF"]

    # Subtle specular + controlled roughness for soft highlights
    bsdf.inputs["Specular IOR Level"].default_value = 0.35
    bsdf.inputs["Roughness"].default_value = 0.45
    bsdf.inputs["Metallic"].default_value = 0.0

    # Light clearcoat layer for extra depth / edge sheen
    bsdf.inputs["Coat Weight"].default_value = 0.15
    bsdf.inputs["Coat Roughness"].default_value = 0.3

    # Faint sheen gives a soft velvet-like rim on curved surfaces
    bsdf.inputs["Sheen Weight"].default_value = 0.05
    bsdf.inputs["Sheen Roughness"].default_value = 0.4

    if color:
      print('mesh color', color)
      bsdf.inputs["Base Color"].default_value = (color[0]/255.0, color[1]/255.0, color[2]/255.0, 1.0)
      bsdf.inputs["Alpha"].default_value = alpha
    else:
      mat.node_tree.nodes["Color Attribute"].layer_name = "Col"
      mat.node_tree.links.new(
        bsdf.inputs["Base Color"],
        mat.node_tree.nodes["Color Attribute"].outputs["Color"])


def cylinder_between(x1, y1, z1, x2, y2, z2, r, color, alpha):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1    
    dist = math.sqrt(dx**2 + dy**2 + dz**2)
    bpy.ops.mesh.primitive_cylinder_add(
        radius = r, 
        depth = dist,
        location = (dx/2 + x1, dy/2 + y1, dz/2 + z1)   
    ) 
    phi = math.atan2(dy, dx) 
    theta = math.acos(dz/dist) 
    C.object.rotation_euler[1] = theta 
    C.object.rotation_euler[2] = phi

    mat = bpy.data.materials.new(name="test")
    mat.use_backface_culling = True
    C.object.data.materials.append(mat)
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0  # specular
    mat.node_tree.nodes["Principled BSDF"].inputs[12].default_value = 0  #
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (color[0]/255.0, color[1]/255.0, color[2]/255.0, 1.0)
    mat.node_tree.nodes["Principled BSDF"].inputs[4].default_value = alpha
    return C.object   


def main():
    
    with open('nodes.json') as f:
        nodes_dict = json.load(f)    
    with open('blender_config.json', 'r') as f:
        configuration = json.load(f)

    clear_scene()
    init_scene(configuration)

    for name, properties in nodes_dict.items():
        print(name, properties)

        if properties['type'] == 'points':
           bpy.ops.wm.ply_import(filepath=name+'.ply')
           bpy.ops.object.shade_smooth()
           obj = bpy.data.objects[name]
           create_mat(obj)

        if properties['type'] == 'camera':
           eye = mathutils.Vector(properties['position'])
           at = mathutils.Vector(properties['look_at'])
           up = mathutils.Vector(properties['up'])
           look_at(C.scene.objects['Camera'], eye, at, up)
           C.scene.objects['Camera'].data.lens = properties['focal_length']

        if properties['type'] == 'cuboid':
           obj = bpy.ops.mesh.primitive_cube_add(
              size=1, enter_editmode=False, align='WORLD',
              location=mathutils.Vector(properties['position']),
              scale=mathutils.Vector(properties['size']))

        if properties['type'] == 'polyline':
            if len(properties['positions']) <= 1:
                continue
            for i in range(len(properties['positions']) - 1):
                x1, y1, z1 = properties['positions'][i]
                x2, y2, z2 = properties['positions'][i + 1]
                obj = cylinder_between(
                   x1, y1, z1,
                   x2, y2, z2,
                   properties['edge_width'],
                   properties['color'],
                   properties['alpha'])
            for i in range(len(properties['positions'])):
                x, y, z = properties['positions'][i]
                bpy.ops.mesh.primitive_uv_sphere_add(
                    radius=properties['edge_width'],
                    location=(x, y, z),
                    segments=16,
                    ring_count=8
                )
                sphere = bpy.context.active_object
                # Reuse cylinder material if available
                if getattr(obj, "active_material", None) is not None:
                    sphere.active_material = obj.active_material

                # mat = bpy.data.materials.new(name="test")
                # mat.use_backface_culling = True
                # C.object.data.materials.append(mat)
                # mat.use_nodes = True
                # mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (color[0]/255.0, color[1]/255.0, color[2]/255.0, alpha)


        if properties['type'] == 'arrow':
            start = mathutils.Vector(properties['start'])
            end   = mathutils.Vector(properties['end'])
            color = properties['color']
            alpha = float(properties['alpha'])
            r_shaft = float(properties['stroke_width'])
            r_head  = float(properties['head_width'])
            visible = bool(properties['visible'])

            d = end - start
            L = d.length
            if L <= 1e-9:
                return None, None
            n = d.normalized()
            head_h  = 2.0 * r_head
            shaft_h = max(1e-6, L - head_h)

            # Material
            mat = bpy.data.materials.new(name="ArrowMat")
            mat.use_nodes = True

            #bpy.ops.node.add_node(use_transform=True, type="ShaderNodeBsdfDiffuse")

            bsdf = mat.node_tree.nodes["Principled BSDF"]
            bsdf.inputs["Base Color"].default_value = (color[0], color[1], color[2], 1.0)
            bsdf.inputs["Alpha"].default_value = alpha
            # match old Diffuse-style look
            bsdf.inputs["Metallic"].default_value = 0.0
            bsdf.inputs["Specular"].default_value = 0.0
            bsdf.inputs["Roughness"].default_value = 1.0

            # make sure it's not glowing
            bsdf.inputs["Emission"].default_value = (0.0, 0.0, 0.0, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 0.0
            bsdf.inputs["Clearcoat"].default_value = 0.0
            bsdf.inputs["Sheen"].default_value = 0.0
            mat.blend_method = 'BLEND'
            mat.shadow_method = 'HASHED'

            # Rotation: +Z -> direction
            rot = mathutils.Vector((0,0,1)).rotation_difference(n)

            # Shaft: cylinder along +Z, centered at start + n * (shaft_h/2)
            bpy.ops.mesh.primitive_cylinder_add(radius=r_shaft, depth=shaft_h, location=(0,0,0))
            shaft = bpy.context.active_object
            shaft.rotation_mode = 'QUATERNION'
            shaft.rotation_quaternion = rot
            shaft.location = start + n * (shaft_h * 0.5)
            shaft.data.materials.append(mat)

            # Head: cone along +Z, centered at end - n * (head_h/2)
            bpy.ops.mesh.primitive_cone_add(radius1=r_head, radius2=0.0, depth=head_h, location=(0,0,0))
            head = bpy.context.active_object
            head.rotation_mode = 'QUATERNION'
            head.rotation_quaternion = rot
            head.location = end - n * (head_h * 0.5)
            head.data.materials.append(mat)

            # Visibility
            for obj in (shaft, head):
                obj.hide_set(not visible)
                obj.hide_render = not visible


        if properties['type'] == 'mesh':
          if properties['filename'].split('.')[-1] == 'ply':
            bpy.ops.wm.ply_import(filepath=properties['filename'], forward_axis='Y', up_axis='Z')
          if properties['filename'].split('.')[-1] == 'obj':
            bpy.ops.wm.obj_import(filepath=properties['filename'], forward_axis='Y', up_axis='Z')          
          bpy.ops.object.shade_smooth()
          obj = bpy.context.view_layer.objects.active
          obj.scale = [properties['scale'][0], properties['scale'][1], properties['scale'][2]]
          obj.rotation_mode = 'QUATERNION'  # blender quats are WXYZ
          obj.rotation_quaternion = [properties['rotation'][3], properties['rotation'][0], properties['rotation'][1], properties['rotation'][2]]
          obj.location = [properties['translation'][0], properties['translation'][1], properties['translation'][2]]
          try:
            create_mat(obj, properties['color'])
          except KeyError:
            create_mat(obj)

        if properties['type'] == 'superquadric':
          bpy.ops.wm.ply_import(filepath=name + '.ply', forward_axis='Y', up_axis='Z')
          bpy.ops.object.shade_smooth()
          obj = bpy.context.view_layer.objects.active
          try:
            create_mat(obj, properties['color'], properties.get('alpha', 1.0))
          except KeyError:
            create_mat(obj)

    # Render if output filename is provided
    if configuration['render']:
        render(os.path.abspath(argv[0]), configuration)

    output_blender_file = os.path.abspath('blender_scene.blend')
    save_blender_scene(output_blender_file)
    print('Saved blender file to:', output_blender_file)

# def create_video(input_dir, pattern, output_filepath):
#   trans_to_white = "format=yuva444p,\
#   geq=\
#   'if(lte(alpha(X,Y),16),255,p(X,Y))':\
#   'if(lte(alpha(X,Y),16),128,p(X,Y))':\
#   'if(lte(alpha(X,Y),16),128,p(X,Y))'"

#   # f = "color=white,format=rgb24[c];[c][0]scale2ref[c][i];[c][i]overlay=format=auto:shortest=1,setsar=1"
#   # cmd = ["ffmpeg", "-i", pattern, '-filter_complex', f, '-y', output_filepath]
#   # subprocess.run(cmd)

#   import glob
#   for fi in glob.glob(f'{input_dir}/output_*.png'):
#     subprocess.run(["convert", "-flatten", fi, fi])
#     # subprocess.run(["convert", fi, "-background", "white", "-alpha", "remove", "-flatten", "-alpha", "off", fi])
#   # subprocess.run(["ffmpeg", "-i", pattern, '-y', output_filepath])
#   subprocess.run(["ffmpeg", "-i", f'{input_dir}/{pattern}', "-vcodec", "libx264", "-vf", "format=yuv420p", "-y", output_filepath])
#   # subprocess.run(["convert", "-delay", "1", "-loop", "0", "*.png", "myimage.gif"])
