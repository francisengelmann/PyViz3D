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


def render(output_prefix, file_format='PNG', color_mode='RGBA', animation=False):
  """
  :path: the file path of the rendered image
  :file_format: {PNG, JPEG}
  """
  C.scene.render.image_settings.file_format=file_format
  C.scene.render.filepath = output_prefix
  print('output_prefix:', output_prefix)
  
  # C.scene.view_settings.view_transform = 'Standard'
  # D.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
  # bpy.context.scene.world.use_nodes = False
  # bpy.context.scene.world.color = (1, 1, 1)
  # C.scene.render.alpha_mode = 'SKY'
  
  if animation:
    bpy.ops.curve.primitive_bezier_circle_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    bezier_circle = C.object
    animation_length = 60
    bpy.context.object.data.path_duration = animation_length
    bpy.context.scene.frame_end = animation_length
    bpy.context.scene.render.resolution_y = 406
    bpy.context.scene.render.resolution_x = 720
    bpy.context.scene.cycles.samples = 10
    bpy.data.scenes['Scene'].render.ffmpeg.codec = 'H264'

    light = C.scene.objects['Point']
    light.location = [0.0, 0.0, 0.0]
    light.data.energy = 60
    light.data.shadow_soft_size = 0.1

    cam = C.scene.objects['Camera']
    cam.select_set(True)
    bpy.context.view_layer.objects.active = cam
    cam.matrix_world = mathutils.Matrix(np.eye(4))
    cam.location = [0.0, 0.0, 0.5]
    bpy.ops.object.constraint_add(type='FOLLOW_PATH')
    cam.constraints["Follow Path"].target = bezier_circle
    bpy.ops.object.constraint_add(type='TRACK_TO')
    cam.constraints["Track To"].target = light
    bpy.ops.constraint.followpath_path_animate(constraint="Follow Path", owner='OBJECT')

  bpy.ops.render.render(use_viewport=True, animation=animation, write_still=True)

  if animation:
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


def init_scene(resolution_x=800, resolution_y=600):
  # render stuff
  C.scene.render.resolution_x = resolution_x
  C.scene.render.resolution_y = resolution_y
  D.scenes["Scene"].render.film_transparent = True
  C.scene.render.image_settings.color_mode = 'RGBA'
  C.scene.view_settings.look = 'AgX - Medium High Contrast'
  C.scene.view_settings.view_transform = 'Standard'
  C.scene.render.engine = 'CYCLES'
  C.scene.cycles.device = 'GPU'
  C.scene.cycles.preview_samples = 50
  C.scene.cycles.samples = 50

  # Add lights
  C.scene.objects['Light'].data.shadow_soft_size = 1.0
  C.scene.objects['Light'].data.cycles.cast_shadow = False
  bpy.ops.object.light_add(type='POINT', radius=1, align='WORLD', location=(-1, 1, 10), scale=(1, 1, 1))
  C.scene.objects['Point'].data.energy = 7000.0
  C.scene.objects['Point'].data.shadow_soft_size = 3

  for i in range(4):
    bpy.ops.object.light_add(type='POINT', radius=0.1, align='WORLD', location=(i%2, i//2, 1), scale=(1, 1, 1))
    C.scene.objects[f'Point.{str(i+1).zfill(3)}'].data.energy = 5.0
    C.scene.objects[f'Point.{str(i+1).zfill(3)}'].data.shadow_soft_size = 0.1
    C.scene.objects[f'Point.{str(i+1).zfill(3)}'].data.color = (1, 0.795182, 0.375358)


def create_mat(obj, color=None):
    mat = bpy.data.materials.new(name="test")
    mat.use_backface_culling = True
    obj.data.materials.append(mat)
    mat.use_nodes = True
    mat.node_tree.nodes.new(type="ShaderNodeVertexColor")
    mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0  # specular
    mat.node_tree.nodes["Principled BSDF"].inputs[12].default_value = 0  #
    if color:
      print('mesh color', color)
      mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (color[0]/255.0, color[1]/255.0, color[2]/255.0, 1.0)
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
    clear_scene()
    init_scene()

    path_json = f'nodes.json'
    with open(path_json) as f:
        nodes_dict = json.load(f)
    animation = False
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
           animation = properties['animation']
        
        if properties['type'] == 'cuboid':
           obj = bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD',
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
          obj = bpy.data.objects[properties['filename'].split('.')[0]]
          obj.scale = [properties['scale'][0], properties['scale'][1], properties['scale'][2]]
          obj.rotation_mode = 'QUATERNION'  # blender quats are WXYZ
          obj.rotation_quaternion = [properties['rotation'][3], properties['rotation'][0], properties['rotation'][1], properties['rotation'][2]]
          obj.location = [properties['translation'][0], properties['translation'][1], properties['translation'][2]]
          try:
            create_mat(obj, properties['color'])
          except KeyError:
            create_mat(obj)
        # somwhere here parse the blender parameters

    # Render if output filename is provided
    if len(argv) > 0:
        print(argv)
        render(os.path.abspath(argv[0]), animation=animation)

    output_blender_file = f'blender_scene.blend'
    output_blender_file = os.path.abspath(output_blender_file)
    save_blender_scene(output_blender_file)
    print('Saved blender file to:', output_blender_file)
