import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=8
print('CYCLESDEV',bpy.context.preferences.addons['cycles'].preferences.get_devices())
bpy.ops.mesh.primitive_cube_add();bpy.ops.object.camera_add(location=(4,-6,3));cam=bpy.context.object
from mathutils import Vector
cam.rotation_euler=(Vector((0,0,0))-cam.location).to_track_quat('-Z','Y').to_euler();s.camera=cam
bpy.ops.object.light_add(type='AREA',location=(2,-2,5));bpy.context.object.data.energy=600
s.render.engine='CYCLES';s.render.resolution_x=270;s.render.resolution_y=480;s.render.resolution_percentage=100;s.render.filepath='璀璨防漏_codex版/renders/test.png'
bpy.ops.render.render(write_still=True)
