import bpy
from pathlib import Path
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'blender/pump.blend'))
s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.render.resolution_percentage=100;s.frame_start=1;s.frame_end=3
print('EEVEE',s.eevee.bl_rna.properties.keys(),flush=True)
s.eevee.taa_render_samples=16
s.render.filepath=str(R/'renders/eeveetest_');bpy.ops.render.render(animation=True)
