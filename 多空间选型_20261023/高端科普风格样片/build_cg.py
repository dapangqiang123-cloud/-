import bpy, math, random, sys, os
from mathutils import Vector
from pathlib import Path
root=Path(__file__).resolve().parent
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
mode=args[0] if args else 'room'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
sc=bpy.context.scene
sc.render.engine='CYCLES';sc.cycles.samples=24;sc.cycles.use_denoising=True
try:
 prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
 for d in prefs.devices:d.use=d.type=='METAL'
 sc.cycles.device='GPU'
except:pass
sc.render.resolution_x=1080;sc.render.resolution_y=1920;sc.render.resolution_percentage=50
sc.render.image_settings.file_format='PNG';sc.render.fps=24
sc.frame_start=1;sc.frame_end=120
sc.world.color=(.35,.35,.35)
w=sc.world;w.use_nodes=True;w.node_tree.nodes['Background'].inputs['Color'].default_value=(.83,.84,.86,1);w.node_tree.nodes['Background'].inputs['Strength'].default_value=.45
sc.view_settings.view_transform='AgX'
def mat(name,col,rough=.5,metal=0,noise=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*col,1);m.use_nodes=True;m.node_tree.nodes.clear();p=m.node_tree.nodes.new('ShaderNodeBsdfPrincipled');p.name='Principled BSDF';out=m.node_tree.nodes.new('ShaderNodeOutputMaterial');m.node_tree.links.new(p.outputs['BSDF'],out.inputs['Surface']);p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 if noise:
  n=m.node_tree.nodes.new('ShaderNodeTexNoise');n.inputs['Scale'].default_value=110;n.inputs['Roughness'].default_value=.7;b=m.node_tree.nodes.new('ShaderNodeBump');b.inputs['Strength'].default_value=noise;b.inputs['Distance'].default_value=.04;m.node_tree.links.new(n.outputs['Fac'],b.inputs['Height']);m.node_tree.links.new(b.outputs['Normal'],p.inputs['Normal'])
 return m
ivory=mat('Warm mineral plaster',(.79,.77,.71),.7,noise=.12)
cream=mat('Linen woven upholstery',(.67,.62,.52),.86,noise=.42)
white=mat('Warm white lacquer',(.86,.85,.8),.32)
wood=mat('Natural oak',(.41,.29,.16),.48,noise=.13)
bronze=mat('Brushed champagne metal',(.44,.33,.19),.3,.7)
dark=mat('Shadow bronze',(.065,.058,.047),.5,.4)
flowmat=mat('Pearlescent air',(.52,.70,.72),.21,.3)
p=flowmat.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(.4,.6,.62,1);p.inputs['Emission Strength'].default_value=.4
particlemat=mat('Air light tracer',(.73,.80,.77),.25,.25)
ground=mat('Studio seamless',(.74,.72,.67),.78)
def cube(name,loc,dim,m,bev=.04):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m)
 if bev:
  b=o.modifiers.new('Hand finished edges','BEVEL');b.width=bev;b.segments=3
  o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
 return o
def sphere(name,loc,scale,m):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;o.data.materials.append(m)
 for p in o.data.polygons:p.use_smooth=True
 return o
def cyl(name,loc,r,depth,m):
 bpy.ops.mesh.primitive_cylinder_add(vertices=40,radius=r,depth=depth,location=loc);o=bpy.context.object;o.name=name;o.data.materials.append(m)
 b=o.modifiers.new('Edge finish','BEVEL');b.width=.025;b.segments=3;o.modifiers.new('Normals','WEIGHTED_NORMAL');return o
def curve(name,pts,r,m):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=16;cu.bevel_depth=r;cu.bevel_resolution=3;s=cu.splines.new('BEZIER');s.bezier_points.add(len(pts)-1)
 for b,co in zip(s.bezier_points,pts):b.co=co;b.handle_left_type='AUTO';b.handle_right_type='AUTO'
 ob=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(ob);ob.data.materials.append(m);return ob

def light(name,loc,power,size,target):
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
light('Large softbox',(-4,-3,9),1500,7,(0,0,0));light('Window light',(3,5,7),1100,5,(0,0,0));light('Warm edge',(5,-1,4),650,4,(0,0,1))
cube('Infinite seamless',(0,0,-.33),(200,200,.2),ground,.0)
if mode=='room':
 cube('Architecture plinth',(0,0,-.12),(5.5,8.5,.25),ivory,.07)
 for i in range(18):
  mm=mat('Oak tonal '+str(i),(.43+.018*math.sin(i*2),.34+.015*math.sin(i*2),.23+.013*math.sin(i*2)),.54)
  cube('Oak plank',(i*.285-2.42,0,.025),(.28,8,.06),mm,.008)
 cube('Left gallery wall',(-2.6,0,1.45),(.16,8.3,2.9),ivory)
 cube('Rear wall',(0,4.08,1.45),(5.35,.16,2.9),ivory)
 # Window surround and sheer translucent glazing
 glass=mat('Frosted daylight',(.9,.92,.91),.4)
 cube('Window recess',(-2.49,.65,1.65),(.05,4.35,1.8),dark,.01)
 for i in range(3):cube('Window light pane',(-2.45,-.78+i*1.42,1.65),(.055,1.36,1.68),glass,.005)
 # very slim soffit with vent
 cube('Ceiling cove',(0,3.82,2.75),(5.18,.5,.25),white)
 cube('Linear AC outlet',(0,3.548,2.72),(2.8,.03,.095),dark,.005)
 for z in [2.699,2.724,2.749]:cube('Outlet louvre',(0,3.523,z),(2.76,.016,.007),bronze,.001)
 # Living area sofa, modular low rounded cushions
 cube('Sofa shadow base',(-1.48,-1.65,.17),(1.45,2.65,.24),dark,.06)
 cube('Sofa body',(-1.48,-1.65,.43),(1.5,2.75,.52),cream,.18)
 cube('Sofa back',(-2.03,-1.65,.83),(.33,2.7,.72),cream,.15)
 for y in [-2.25,-1.05]:cube('Seat cushion',(-1.35,y,.73),(1.06,1.15,.2),cream,.1)
 for y in [-3,-.3]:cube('Sofa arm',(-1.45,y,.71),(1.45,.23,.52),cream,.1)
 rug=mat('Natural wool rug',(.61,.58,.51),.95,noise=.7)
 cube('Wool rug',(.38,-1.45,.083),(3,3.4,.028),rug,.09)
 cyl('Stone coffee table',(.4,-1.65,.43),.69,.15,ivory);cyl('Coffee base',(.4,-1.65,.25),.26,.38,wood)
 cube('Book',(.35,-1.65,.53),(.42,.3,.045),white,.01)
 # Dining table long ovoid slab
 table=cube('Oak dining table',(.1,1.6,.87),(2.85,1.15,.13),wood,.22)
 for x in [-.85,1.05]:cube('Pedestal table leg',(x,1.6,.46),(.18,.78,.78),wood,.04)
 for x in [-.8,.25,1.2]:
  for y in [.57,2.63]:
   cube('Dining seat',(x,y,.47),(.6,.57,.16),cream,.09)
   cube('Chair back',(x,y+(.22 if y>1 else -.22),.83),(.62,.13,.65),wood,.08)
   for dx in [-.2,.2]:
    for dy in [-.19,.19]:cube('Chair leg',(x+dx,y+dy,.23),(.055,.055,.46),wood,.012)
 cyl('Ceramic vase',(.05,1.6,1.08),.12,.28,white)
 # airflow paths roll gently down through occupied space; clearly conceptual
 for i in range(9):
  x=(i-4)*.28
  pts=[(x,3.48,2.72),(x*1.1,2.5,2.62),(x*1.28,.6,2.35),(x*1.4,-1.3,2.05),(x*1.45,-3.55,1.52)]
  cu=curve('Continuous air strand',pts,.009,flowmat)
  cu.data.bevel_factor_end=.05;cu.data.keyframe_insert(data_path='bevel_factor_end',frame=1)
  cu.data.bevel_factor_end=1;cu.data.keyframe_insert(data_path='bevel_factor_end',frame=65)
  for j in range(3):
   ob=sphere('Flow tracer',(0,0,0),(.025,.05,.025),particlemat)
   for f in range(1,122,4):
    u=((f-1)/100+j/3)%1
    ob.location=(x*(1+.45*u),3.48-7.03*u,2.72-1.2*u*u);ob.keyframe_insert(data_path='location',frame=f)
 start=(11,-15,11);end=(10,-13.5,10.3);target=(0,.25,1.0);lens=50
else:
 # Macro conceptual layer assembly, oriented along X and floating above studio floor
 # outer frames lie in YZ planes. open corners with careful material thickness
 def frame(name,x,m):
  for y in [-1.04,1.04]:cube(name,(x,y,1.65),(.13,.08,2.18),m,.018)
  for z in [.56,2.74]:cube(name,(x,0,z),(.13,2.16,.08),m,.018)
 frame('Fine mesh perimeter',-1.8,bronze)
 for i in range(23):
  p=-1+i*.091
  curve('Woven pre-filter strand',[(-1.8,p,.6),(-1.8,p,2.7)],.009,bronze)
  curve('Woven cross strand',[(-1.81,-1,1.65+p),(-1.81,1,1.65+p)],.009,bronze)
 frame('Pleated fibre perimeter',0,white)
 # folded HEPA medium, real folds and side-raking texture
 verts=[];faces=[]
 for i in range(45):
  y=-1+i/22; x=.16 if i%2 else -.16
  verts.extend([(x,y,.6),(x,y,2.7)])
  if i:faces.append((2*i-2,2*i,2*i+1,2*i-1))
 mesh=bpy.data.meshes.new('Folded fibre mesh');mesh.from_pydata(verts,[],faces);mesh.update();ob=bpy.data.objects.new('Pleated fibre medium',mesh);bpy.context.collection.objects.link(ob);ob.data.materials.append(mat('Matte fibrous paper',(.78,.78,.71),.92,noise=.7));sol=ob.modifiers.new('Paper thickness','SOLIDIFY');sol.thickness=.01
 # Heat exchange stack distinct from filter paper
 frame('Heat exchange core surround',1.85,ivory)
 for i in range(24):
  z=.64+i*.087
  cube('Heat exchanger lamella',(1.85,0,z),(.65,2,.022),white,.004)
  for j in range(10):cube('Core channels',(1.85,-.9+j*.2,z+.035),(.65,.015,.06),ivory,.002)
 # gentle continuous airflow + intercepted warm particles
 for i in range(7):
  y=-.8+i*.26;z=1.65+.35*math.sin(i*2)
  curve('Air through layers',[(-3.3,y,z),(-1.9,y,z),(-.4,y,z),(1.5,y,z),(3.25,y,z)],.009,flowmat)
 rng=random.Random(11)
 dust=mat('Illustrative suspended particles',(.32,.21,.105),.5,.1)
 for i in range(50):
  yy=rng.uniform(-.95,.95);zz=rng.uniform(.7,2.6);xx=rng.uniform(-3.5,-2)
  o=sphere('Particle captured at prefilter',(xx,yy,zz),(.022,.022,.022),dust)
  o.keyframe_insert(data_path='location',frame=1);o.location.x=-1.86 if i%3 else -.19;o.keyframe_insert(data_path='location',frame=65+i%30)
 for i in range(20):
  o=sphere('Clean airflow indicator',(0,0,0),(.025,.025,.025),particlemat)
  y=rng.uniform(-.9,.9);z=rng.uniform(.8,2.5)
  for f in range(1,122,4):
   u=((f-1)/115+i/20)%1;o.location=(-3.4+6.8*u,y,z);o.keyframe_insert(data_path='location',frame=f)
 start=(10,-15,7.8);end=(9,-14,7.1);target=(0,0,1.6);lens=62
bpy.ops.object.camera_add(location=start);cam=bpy.context.object;sc.camera=cam;cam.data.lens=lens
for f,pos in [(1,start),(120,end)]:cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.keyframe_insert(data_path='location',frame=f);cam.keyframe_insert(data_path='rotation_euler',frame=f)
cam.data.dof.use_dof=True;cam.data.dof.focus_distance=(Vector(target)-cam.location).length;cam.data.dof.aperture_fstop=9 if mode=='room' else 7
sc.render.filepath=str(root/'frames'/f'{mode}_')
bpy.ops.wm.save_as_mainfile(filepath=str(root/f'{mode}.blend'))
sc.frame_set(72);sc.render.filepath=str(root/f'{mode}_preview.png');bpy.ops.render.render(write_still=True)
