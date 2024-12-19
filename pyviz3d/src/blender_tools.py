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
       location=configuration['animation_circle_center'], scale=(1, 1, 1))
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
    empty.location = configuration['animation_circle_center']
    bpy.context.scene.collection.objects.link(empty)
    cam.constraints["Track To"].target = empty
    bpy.ops.constraint.followpath_path_animate(constraint="Follow Path", owner='OBJECT')

  bpy.ops.render.render(use_viewport=True, animation=configuration['animation'], write_still=True)

  # Combine individual frames into video using ffmpeg
  if configuration['animation']:
    output_filepath = output_prefix + '.mp4'
    subprocess.run(["ffmpeg", "-y", "-i", f'{output_prefix}%04d.png', "-vcodec", "libx264", "-vf", "format=yuv420p", "-y", output_filepath])
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
  C.scene.render.image_settings.color_mode = 'RGBA'
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
    mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0  # specular
    mat.node_tree.nodes["Principled BSDF"].inputs[12].default_value = 0  #
    if color:
      print('mesh color', color)
      mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (color[0]/255.0, color[1]/255.0, color[2]/255.0, 1.0)
      mat.node_tree.nodes["Principled BSDF"].inputs[4].default_value = alpha
    else:
      mat.node_tree.nodes["Color Attribute"].layer_name = "Col"
      mat.node_tree.links.new(
        mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"],
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
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (color[0]/255.0, color[1]/255.0, color[2]/255.0, alpha)
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
                x1 = properties['positions'][i][0]
                y1 = properties['positions'][i][1]
                z1 = properties['positions'][i][2]
                x2 = properties['positions'][i + 1][0]
                y2 = properties['positions'][i + 1][1]
                z2 = properties['positions'][i + 1][2]
                obj = cylinder_between(x1, y1, z1, x2, y2, z2, properties['edge_width'] * 2, properties['color'], properties['alpha'])
        
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
