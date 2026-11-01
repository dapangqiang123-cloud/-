# Standalone, unbranded, generic blower shutdown insert. Not a TRESOR assembly position drawing.
import bpy,math,sys
from mathutils import Vector
from pathlib import Path
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=16;s.render.resolution_x=1080;s.render.resolution_y=1920;s.render.resolution_percentage=100;s.render.fps=30;s.frame_start=1;s.frame_end=60
s.world=bpy.data.worlds.new('Warm');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.14,.09,.055,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.5
s.view_settings.view_transform='AgX'
def mat(n,c,metal):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=.28;return m
metal=mat('Unbranded aluminium',(.5,.5,.46),.7);dark=mat('Warm graphite',(.075,.055,.04),.35)
root=bpy.data.objects.new('Generic rotating blower',None);bpy.context.collection.objects.link(root)
for side in [-.55,.55]:
 bpy.ops.mesh.primitive_torus_add(major_radius=.62,minor_radius=.025,major_segments=64,minor_segments=12,location=(0,side,0),rotation=(math.pi/2,0,0));o=bpy.context.object;o.parent=root;o.data.materials.append(metal)
 for i in range(4):
  a=i*math.pi/2;bpy.ops.mesh.primitive_cube_add(size=1);o=bpy.context.object;o.dimensions=(.64,.035,.045);o.location=(.31*math.cos(a),side,.31*math.sin(a));o.rotation_euler[1]=-a;o.parent=root;o.data.materials.append(metal)
for i in range(28):
 a=i*math.tau/28;bpy.ops.mesh.primitive_cube_add(size=1);o=bpy.context.object;o.dimensions=(.03,1.1,.10);o.location=(.60*math.cos(a),0,.60*math.sin(a));o.rotation_euler[1]=-a+.22;o.parent=root;o.data.materials.append(metal)
bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=.08,depth=1.45,rotation=(math.pi/2,0,0));bpy.context.object.data.materials.append(dark)
# visible support bearing, no electric internals
for side in [-.75,.75]:
 bpy.ops.mesh.primitive_cube_add(size=1,location=(0,side,-.6));o=bpy.context.object;o.dimensions=(.3,.16,1.1);o.data.materials.append(dark)
# studio ground
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-1.2));bpy.context.object.data.materials.append(dark)
for loc,power,size in [((-3,-4,6),1000,5),((4,2,3),1200,4)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.size=size;o.data.color=(1,.8,.6);o.rotation_euler=(-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(3.5,-5,2.2));s.camera=bpy.context.object;s.camera.rotation_euler=(Vector((0,0,0))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.lens=51
for f in range(1,61):
 t=(f-1)/30;theta=12*(min(t,1.4)-min(t,1.4)**2/2.8);root.rotation_euler=(0,theta,0);root.keyframe_insert(data_path='rotation_euler',frame=f)
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.compression=15
p=R/'renders/fan';p.mkdir(exist_ok=True);s.render.filepath=str(p/'f_');bpy.ops.wm.save_as_mainfile(filepath=str(R/'blender/fan.blend'));
if 'preview' in sys.argv:
 s.render.resolution_percentage=50;s.frame_set(1);s.render.filepath=str(p/'preview.png');bpy.ops.render.render(write_still=True)
else:bpy.ops.render.render(animation=True)
