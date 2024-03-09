# blender experimental
# run with:
# blender myscene.blend --background --python myscript.py
# blender -b -P myscript.py

import bpy
import math
import mathutils
import numpy as np
import subprocess
import json

C = bpy.context
D = bpy.data

def clear_scene():
  for o in C.scene.objects:
    print(o)
    if o.type == 'MESH':
        o.select_set(True)
    else:
        o.select_set(False)
  bpy.ops.object.delete()


def render(path, file_format='PNG', color_mode='RGBA'):
  """
  :path: the file path of the rendered image
  :file_format: {PNG, JPEG}
  """
  C.scene.render.image_settings.file_format=file_format
  C.scene.render.filepath = path

  # C.scene.view_settings.view_transform = 'Standard'
  # D.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
  # bpy.context.scene.world.use_nodes = False
  # bpy.context.scene.world.color = (1, 1, 1)
  # C.scene.render.alpha_mode = 'SKY'
  bpy.ops.render.render(use_viewport=True, write_still=True)


def save_blender_scene(path):
  bpy.ops.wm.save_as_mainfile(filepath=f'/Users/francis/Programming/PyViz3D/{path}')


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


def create_video(input_dir, pattern, output_filepath):
  trans_to_white = "format=yuva444p,\
  geq=\
  'if(lte(alpha(X,Y),16),255,p(X,Y))':\
  'if(lte(alpha(X,Y),16),128,p(X,Y))':\
  'if(lte(alpha(X,Y),16),128,p(X,Y))'"

  # f = "color=white,format=rgb24[c];[c][0]scale2ref[c][i];[c][i]overlay=format=auto:shortest=1,setsar=1"
  # cmd = ["ffmpeg", "-i", pattern, '-filter_complex', f, '-y', output_filepath]
  # subprocess.run(cmd)

  import glob
  for fi in glob.glob(f'{input_dir}/output_*.png'):
    subprocess.run(["convert", "-flatten", fi, fi])
    # subprocess.run(["convert", fi, "-background", "white", "-alpha", "remove", "-flatten", "-alpha", "off", fi])
  # subprocess.run(["ffmpeg", "-i", pattern, '-y', output_filepath])
  subprocess.run(["ffmpeg", "-i", f'{input_dir}/{pattern}', "-vcodec", "libx264", "-vf", "format=yuv420p", "-y", output_filepath])
  # subprocess.run(["convert", "-delay", "1", "-loop", "0", "*.png", "myimage.gif"])


def init_scene():
  # render stuff
  C.scene.render.resolution_x = 16 * 40
  C.scene.render.resolution_y = 9 * 40
  D.scenes["Scene"].render.film_transparent = True
  C.scene.render.image_settings.color_mode = 'RGBA'
  C.scene.view_settings.look = 'AgX - Medium High Contrast'
  C.scene.render.engine = 'CYCLES'
  C.scene.cycles.device = 'GPU'
  C.scene.cycles.preview_samples = 100
  C.scene.cycles.samples = 150
  C.scene.frame_end = 60
  # lights
  C.scene.objects['Light'].data.shadow_soft_size = 1.0
  bpy.ops.object.light_add(type='POINT', radius=1, align='WORLD', location=(1, 1, 0), scale=(1, 1, 1))
  C.scene.objects['Point'].data.energy = 100.0


def main(scene_name, layer_name):
  clear_scene()
  init_scene()
  # bpy.ops.import_mesh.ply(filepath='examples/data/scene0106_02_vh_clean_2.ply')
  prefix = f'example_scenes/{scene_name}'
  bpy.ops.import_mesh.ply(filepath=f'{prefix}/{scene_name}.ply')
  obj = bpy.data.objects[scene_name]

  # loops = len(obj.data.loops)
  # verts = len(obj.data.vertices)
  # print(loops, verts, len(obj.data.vertex_colors['Col'].data))

  # Read vertex colors
  path_json = f'{prefix}/nodes.json'
  with open(path_json) as f:
    j = json.load(f)
  name = layer_name  # Color
  num_points = j[name]['num_points']
  binary_filename = j[name]['binary_filename']
  path_pointcloud = f'{prefix}/{binary_filename}'
  try:
    with open(path_pointcloud, 'rb') as f:
      data = f.read()
  except:
    print(f'Could not read: {path_pointcloud}')
  colors = data[24 * num_points:]
  print(len(colors))
  # try: 
  for i, d in enumerate(obj.data.vertex_colors['Col'].data):
    vertex_index = obj.data.loops[i].vertex_index
    for j in [0, 1, 2]:
      d.color[j] = float(colors[vertex_index * 3 + j]) / 255.0
  # except:
    # print(f'{name} not found: {path_pointcloud}')


    # look into each loop's vertex ? (need to filter out double entries)
    # visit = verts * [False]
    # colors = {}

    # for l in range(loops):
    # v = obj.data.loops[l].vertex_index
    # c = vcol.data[l].color
    # if not visit[v]:
    #         colors[v] = c
    #         visit[v] = True

    # sorted(colors)
    # print("Vertex-Colors of Layer:", vcol.name)
    # #print(colors)
    # for v, c in colors.items():
    #     print("Vertex {0} has Color {1}".format(v, (c[0], c[1], c[2])))

  # bpy.ops.material.new()
  # bpy.data.materials["Material.001"].use_backface_culling = True

  # bpy.ops.object.mode_set(mode='VERTEX_PAINT')

  def create_mat(obj):
      mat = bpy.data.materials.new(name="test")
      mat.use_backface_culling = True

      obj.data.materials.append(mat)
      mat.use_nodes = True
      mat.node_tree.nodes.new(type="ShaderNodeVertexColor")
      mat.node_tree.nodes["Color Attribute"].layer_name = "Col"
      mat.node_tree.links.new(
        mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"],
        mat.node_tree.nodes["Color Attribute"].outputs["Color"])

      mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0  # specular

  create_mat(obj)
  print(f'{prefix}/{name}.blend')
  
  save_blender_scene(path=f'{prefix}/{name}.blend')
  exit()
  for i in range(0, 2):
    a = i * 2 / 180.0 * math.pi
    radius = 2.0
    camera_position=mathutils.Vector(
      (math.cos(a) * radius, math.sin(a) * radius, 1.0 ))
    scene_center=compute_object_center(obj)
    scene_center.z = -0.3
    camera_position += scene_center
    look_at(D.objects['Camera'],
            eye=camera_position,
            at=scene_center)
    render(path=f'{prefix}/frames/output_{str(i).zfill(5)}', file_format='PNG')
  create_video(f'{prefix}/frames', 'output_%05d.png', f"{prefix}/{scene_name}_{name}.mp4")


if __name__ == "__main__":
  main(scene_name="cnb_103",
       layer_name="InstancesAll")  # Color, InstanceAll

  # matg = bpy.data.materials.new("Green")
  # matg.diffuse_color = (0,1,0,0.8)
  # obj.active_material = matg
  # obj.vertex_colors.new(name=vertex_colors_name)
  # color_layer = mesh.vertex_colors[vertex_colors_name]
  # print(len(obj.data.vertices))



    # loops = len(obj.data.loops)
    # verts = len(obj.data.vertices)
    # print(loops, verts, len(obj.data.vertex_colors['Col'].data))

    # Read vertex colors

    # name = 'PointClouds;1'  # Color
    # num_points = j[name]['num_points']
    # print(num_points)
    # binary_filename = j[name]['binary_filename']
    # path_pointcloud = f'{binary_filename}'
    # try:
    #     with open(path_pointcloud, 'rb') as f:
    #         data = f.read()
    # except:
    #     print(f'Could not read: {path_pointcloud}')
    #     points = data[:12 * num_points]
    #     normals = data[12 * num_points:24 * num_points]
    #     colors = data[24 * num_points:]

    # points = np.frombuffer(data[:12 * num_points], np.float32).reshape([-1, 3])
    # colors = np.frombuffer(data[24 * num_points:], np.uint8).reshape([-1, 3])

    # for i in range(num_points):
    #     bpy.ops.mesh.primitive_uv_sphere_add(segments=5,
    #                                         ring_count=5,
    #                                         radius=0.1,
    #                                         enter_editmode=False,
    #                                         location=points[i])



# try: 
#   for i, d in enumerate(obj.data.vertex_colors['Col'].data):
#     vertex_index = obj.data.loops[i].vertex_index
#      for j in [0, 1, 2]:
#       d.color[j] = float(colors[vertex_index * 3 + j]) / 255.0
# except:
# print(f'{name} not found: {path_pointcloud}')

# look into each loop's vertex ? (need to filter out double entries)
# visit = verts * [False]
# colors = {}

# for l in range(loops):
# v = obj.data.loops[l].vertex_index
# c = vcol.data[l].color
# if not visit[v]:
#         colors[v] = c
#         visit[v] = True

# sorted(colors)
# print("Vertex-Colors of Layer:", vcol.name)
# #print(colors)
# for v, c in colors.items():
#     print("Vertex {0} has Color {1}".format(v, (c[0], c[1], c[2])))

# bpy.ops.material.new()
# bpy.data.materials["Material.001"].use_backface_culling = True

# bpy.ops.object.mode_set(mode='VERTEX_PAINT')

#   create_mat(obj)
  
#   save_blender_scene(path=f'{name}.blend')
#   exit()
#   for i in range(0, 2):
#     a = i * 2 / 180.0 * math.pi
#     radius = 2.0
#     camera_position=mathutils.Vector(
#       (math.cos(a) * radius, math.sin(a) * radius, 1.0 ))
#     scene_center=compute_object_center(obj)
#     scene_center.z = -0.3
#     camera_position += scene_center
#     look_at(D.objects['Camera'],
#             eye=camera_position,
#             at=scene_center)
#     render(path=f'{prefix}/frames/output_{str(i).zfill(5)}', file_format='PNG')
#   create_video(f'{prefix}/frames', 'output_%05d.png', f"{prefix}/{scene_name}_{name}.mp4")


# if __name__ == "__main__":
#   main(scene_name="cnb_103",
#        layer_name="InstancesAll")  # Color, InstanceAll

# matg = bpy.data.materials.new("Green")
# matg.diffuse_color = (0,1,0,0.8)
# obj.active_material = matg
# obj.vertex_colors.new(name=vertex_colors_name)
# color_layer = mesh.vertex_colors[vertex_colors_name]
# print(len(obj.data.vertices))