import bpy
from pathlib import Path
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'blender/pump.blend'))
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=12;s.cycles.device='GPU';p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
for d in p.devices:d.use=d.type=='METAL'
s.render.resolution_percentage=100;s.frame_end=5;s.render.filepath=str(R/'renders/pump/f_');bpy.ops.render.render(animation=True)
