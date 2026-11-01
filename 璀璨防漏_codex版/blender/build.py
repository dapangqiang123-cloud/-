import bpy,math,random,sys
from mathutils import Vector
from pathlib import Path
R=Path(__file__).resolve().parents[1]
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
shot=args[0] if args else 'pump'
preview='preview' in args
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=12;s.cycles.use_denoising=True
try:
 p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
 for d in p.devices:d.use=d.type=='METAL'
 s.cycles.device='GPU'
except:pass
s.render.resolution_x=1080;s.render.resolution_y=1920;s.render.resolution_percentage=50 if preview else 100
s.render.fps=30;s.world=bpy.data.worlds.new('Warm studio');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.09,.065,.045,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.45
s.view_settings.view_transform='AgX'
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.compression=15
s.render.film_transparent=False
random.seed(12)
def mat(n,c,metal=0,rough=.3,trans=0,emit=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;p.inputs['Transmission Weight'].default_value=trans;p.inputs['IOR'].default_value=1.333 if trans else 1.45
 if emit:p.inputs['Emission Color'].default_value=(*c,1);p.inputs['Emission Strength'].default_value=emit
 return m
silver=mat('Brushed aluminium',(.46,.48,.49),.8,.28);white=mat('Off-white polymer',(.82,.84,.81),.05,.27);black=mat('Black pump casing',(.018,.023,.026),.25,.25);copper=mat('Copper-colour visible path - illustrative material',(.48,.22,.115),.75,.23);gold=mat('Champagne highlight',(.83,.54,.22),.5,.25,emit=1.2);water=mat('Condensate water',(.35,.58,.62),.05,.09,.78);back=mat('Warm studio background',(.075,.044,.026),.1,.65);flow=mat('Water path glints',(.52,.77,.8),.12,.14,emit=1.2)
def cube(n,loc,scale,ma,bevel=.035):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel:mod=o.modifiers.new('Soft manufactured edge','BEVEL');mod.width=bevel;mod.segments=3
 o.data.materials.append(ma);return o
def cyl(n,loc,r,depth,ma):
 bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r,depth=depth,location=loc);o=bpy.context.object;o.name=n;o.data.materials.append(ma);b=o.modifiers.new('Rounded edge','BEVEL');b.width=.015;b.segments=3
 for poly in o.data.polygons:poly.use_smooth=True
 return o
def ball(n,loc,r,ma):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=r,location=loc);o=bpy.context.object;o.name=n;o.data.materials.append(ma)
 for p in o.data.polygons:p.use_smooth=True
 return o
def pipe(n,pts,r,ma):
 c=bpy.data.curves.new(n,'CURVE');c.dimensions='3D';c.resolution_u=16;c.bevel_depth=r;c.bevel_resolution=3;sp=c.splines.new('BEZIER');sp.bezier_points.add(len(pts)-1)
 for p,co in zip(sp.bezier_points,pts):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 o=bpy.data.objects.new(n,c);bpy.context.collection.objects.link(o);o.data.materials.append(ma);return o

def key(o,prop,frame,value):
 setattr(o,prop,value);o.keyframe_insert(data_path=prop,frame=frame)
def camera(loc,target,lens=48):
 bpy.ops.object.camera_add(location=loc);o=bpy.context.object;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();o.data.lens=lens;s.camera=o;return o

def light(loc,power,size,col):
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.data.color=col;o.rotation_euler=(Vector((0,0,.6))-o.location).to_track_quat('-Z','Y').to_euler();return o
cube('Infinite warm floor',(0,0,-.2),(200,200,.1),back)
light((-3,-4,6),750,5,(1,.86,.68));light((4,2,4),1000,4,(.72,.85,1));light((-3,3,2),600,3,(1,.64,.34))
N={'condense':240,'overflow':150,'pump':180,'float':330,'protect':90}.get(shot,180);s.frame_start=1;s.frame_end=N
# pan open at front as an intentional cutaway. No dimension or model claim.
width=3.5
cube('Drain pan base',(0,0,.02),(width,1.6,.12),silver)
cube('Rear pan wall',(0,.78,.32),(width,.07,.6),silver)
cube('Left pan wall',(-width/2,0,.32),(.07,1.6,.6),silver)
cube('Right pan wall',(width/2,0,.32),(.07,1.6,.6),silver)
cube('Cutaway front rim',(0,-.78,.11),(width,.06,.17),silver)
w=cube('Water volume',(0,0,.15),(width-.12,1.45,.14),water,.025)
# gentle optical ripple surface, kept below motor at every frame
tex=bpy.data.textures.new('Water gentle micro ripples',type='CLOUDS');tex.noise_scale=.13
bpy.ops.mesh.primitive_grid_add(x_subdivisions=65,y_subdivisions=33,size=2,location=(0,0,.225));surf=bpy.context.object;surf.name='Water meniscus';surf.scale=(1.68,.71,1);surf.data.materials.append(water)
disp=surf.modifiers.new('Small ripples','DISPLACE');disp.texture=tex;disp.strength=.006;disp.texture_coords='GLOBAL'
# Sweeping warm highlights are abstract editorial emphasis, not physical warning lamps.
if shot in ('pump','float','protect'):
 # pump at screen-left; separate float right; locked camera view throughout
 px=-.35;py=.04
 cyl('Lower water intake',(px,py,.22),.13,.25,black)
 cyl('Black pump lower bowl',(px,py,.43),.29,.23,black)
 cyl('Black pump rim',(px,py,.57),.32,.08,black)
 cyl('Motor lower cylinder above water',(px,py,1.04),.19,.33,white)
 cube('White motor body',(px,py,1.29),(.6,.48,.34),white,.07)
 cyl('White motor cap',(px,py,1.52),.16,.14,white)
 for dx in (-.25,.25):
  cyl('Exposed support post',(px+dx,py, .84),.023,.5,silver)
  cube('Motor side bracket',(px+dx*1.48,py+.09,1.26),(.055,.09,.65),silver,.015)
 cube('Top mounting bridge',(px,py+.11,1.62),(.89,.13,.07),silver,.02)
 cube('Rear mounting panel',(px,.5,1.25),(1.2,.045,1.0),silver,.025)
 # float is outside pump housing, in same collection area
 fx=.64;fy=-.02
 cyl('Float vertical guide rod',(fx,fy,.66),.025,.91,silver)
 cube('Float fixed top',(fx,fy,1.13),(.36,.3,.12),black,.025)
 fl=cyl('Independent white float',(fx,fy,.32),.19,.21,white)
 cyl('Float top flange',(fx,fy,1.21),.11,.045,white)
 path=[(-.59,.04,.46),(-1.02,.04,.46),(-1.22,.04,.64),(-1.22,.04,1.60),(-1.22,.04,1.96),(-1.5,.04,2.13),(-1.78,.04,1.96),(-1.78,.04,.92),(-1.87,.04,.6)]
 pipe('Visible inverted U drain route',path,.065,copper)
 # water intake and route explicit moving glints running from start in pump shot
 if shot=='pump':
  points=[(-.35,-.02,.1),(-.35,-.02,.32),(-.58,-.02,.46),(-1.02,-.02,.46),(-1.22,-.02,.64),(-1.22,-.02,1.6),(-1.22,-.02,1.96),(-1.5,-.02,2.13),(-1.78,-.02,1.96),(-1.78,-.02,.92),(-1.87,-.02,.6)]
  # glints on front surface signal direction without invented internal impeller
  for i in range(9):
   b=ball('Continuous active drainage glint '+str(i),points[0],.026,flow)
   for f in range(1,N+1,3):
    t=((f-1)/72+i/9)%1;v=t*(len(points)-1);k=int(v);a=Vector(points[k]);z=Vector(points[min(k+1,len(points)-1)]);loc=a.lerp(z,v-k);loc.y=-.035;key(b,'location',f,loc)
  halo=light((-.5,-1.5,2.6),95,1.5,(1,.65,.28))
 elif shot=='float':
  # blocked drainage: water rises then remains; no draining after trip
  for f,h in [(1,.225),(90,.30),(180,.50),(210,.54),(330,.54)]:
   key(surf,'location',f,(0,0,h));key(w,'location',f,(0,0,(h+.08)/2));key(w,'scale',f,(1,1,(h-.08)/.14));key(fl,'location',f,(fx,fy,h+.095))
  # visible centrifugal blower behind pan, decelerates to halt by trip
  root=bpy.data.objects.new('Blower rotation',None);bpy.context.collection.objects.link(root);root.location=(.92,.62,1.66);root.scale=(.78,.78,.78)
  for i in range(16):
   a=i*math.tau/16;o=cube('Blower blade', (0,0,0),(.035,.28,.12),silver,.008);o.parent=root;o.location=(.28*math.cos(a),0,.28*math.sin(a));o.rotation_euler[1]=-a
  for f,v in [(1,0),(110,28),(160,37),(205,40),(330,40)]:key(root,'rotation_euler',f,(0,v,0))
  warn=light((.7,-.7,1.2),0,.8,(1,.43,.18))
  for f,v in [(1,0),(185,0),(215,35),(240,8),(265,35),(290,8),(330,20)]:warn.data.energy=v;warn.data.keyframe_insert(data_path='energy',frame=f)
 elif shot=='protect':
  # Continue the previous abnormal-state level; never imply the float drains the pan.
  surf.location.z=.54;w.location.z=(.54+.08)/2;w.scale.z=(.54-.08)/.14;fl.location.z=.54+.095
  for x in (-.35,.64):
   ring=pipe('Abstract protection rim',[(x-.34,-.2,.1),(x-.42,-.2,1.65),(x+.42,-.2,1.65),(x+.34,-.2,.1)],.007,gold)
  line=pipe('Joining protection along pan edge',[(-1.7,-.81,.13),(0,-.81,.13),(1.7,-.81,.13),(1.7,.78,.6),(0,.78,.6),(-1.7,.78,.6)],.018,gold)
  
  for bp in line.data.splines[0].bezier_points:bp.handle_left_type='VECTOR';bp.handle_right_type='VECTOR'
  gold.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value=8
  line.data.bevel_factor_end=0;line.data.keyframe_insert(data_path='bevel_factor_end',frame=1);line.data.bevel_factor_end=1;line.data.keyframe_insert(data_path='bevel_factor_end',frame=N)
 cam=camera((3.1,-7,3.3),(-.1,0,.95),48)
 if shot=='protect':
  key(cam,'location',1,(3.1,-7,3.3));key(cam,'location',N,(3.8,-8.6,3.9))
 else:
  key(cam,'location',1,(3.1,-7,3.3));key(cam,'location',N,(2.9,-6.6,3.15))
elif shot=='condense':
 # a cropped unbranded heat exchanger over collection pan
 for i in range(45):
  x=-1.35+i*.06;cube('Aluminium cooling fin %02d'%i,(x,.2,1.22),(.018,.75,1.05),silver,.006)
 for z in (.95,1.45):
  pipe('Visible copper exchanger tube',[(-1.5,.19,z),(1.44,.19,z),(1.57,.35,z),(1.44,.5,z)],.045,copper)
 # condensate beads on fin front edge: growth, downward travel, drops, pan collection
 for i in range(55):
  x=random.uniform(-1.3,1.3);z=random.uniform(.78,1.7);start=random.randint(1,85)
  o=ball('Condensation bead %02d'%i,(x,-.195,z),.022,water)
  for f,sc in [(1,.18),(start,.35),(start+50,1.3),(start+85,1.45)]:key(o,'scale',f,(sc,sc*.7,sc))
  for f,zz in [(1,z),(start+40,z),(start+80,.71),(start+95,.25),(start+98,.24),(240,.24)]:key(o,'location',f,(x,-.195,zz))
 # pan collects towards right end (direction cue)
 for i in range(12):
  o=ball('Pan flow bead',(-1.2,0,.23),.018,flow)
  for f in range(120,241,4):
   x=-1.3+2.6*((f/100+i/12)%1);key(o,'location',f,(x,-.25,.24))
 cam=camera((3.7,-6.8,3.5),(0,0,.95),54);key(cam,'location',1,(2.2,-4.2,2.45));key(cam,'location',85,(2.4,-4.5,2.5));key(cam,'location',190,(3.7,-6.8,3.5));key(cam,'location',240,(3.7,-6.8,3.5))
elif shot=='overflow':
 # generic pan only: no branded/pump/float device
 cube('Generic obstructed outlet',(1.69,.0,.28),(.10,.28,.22),black,.04)
 for f,h in [(1,.225),(80,.57),(110,.62),(150,.62)]:
  key(surf,'location',f,(0,0,h));key(w,'location',f,(0,0,(h+.08)/2));key(w,'scale',f,(1,1,(h-.08)/.14))
 # small spill over right side, restrained thin rivulets
 for i in range(5):
  o=ball('Minor overflow bead',(1.81,-.35+i*.1,.6),.045,water)
  for f in range(1,151,3):
   sc=0 if f<92 else 1;key(o,'scale',f,(sc*.7,sc*.8,sc*1.9));key(o,'location',f,(1.81,-.35+i*.1,.61-((f+i*11)%43)/43*.48))
 cam=camera((4.8,-8.2,4.8),(0,0,.35),48)
 key(cam,'location',1,(4.8,-8.2,4.8));key(cam,'location',150,(4.65,-8.0,4.65))
if shot=='protect':
 for ob in bpy.data.objects:
  if ob.name.startswith('Abstract protection rim'):ob.hide_render=True
 for px in (-.35,.64):
  glow=light((px,-.8,1.7),100,.7,(1,.64,.28))
  for f,v in [(1,15),(30,100),(90,100)]:glow.data.energy=v;glow.data.keyframe_insert(data_path='energy',frame=f)
if shot=='float':
 for ob in bpy.data.objects:
  if ob.name.startswith('Blower blade'):ob.hide_render=True
# linear timing for flow and water rise
for o in bpy.data.objects:
 if o.animation_data and o.animation_data.action:
  try:
   for fc in o.animation_data.action.fcurves:
    for kp in fc.keyframe_points:kp.interpolation='LINEAR'
  except:pass
# smooth studio cyclorama, avoiding a black horizon band
verts=[]
profile=[(-30,-.26),(3,-.26),(4,-.15),(5,.35),(5.7,1.2),(6,2.5),(6,20)]
for y,z in profile:verts.extend([(-30,y,z),(30,y,z)])
faces=[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(profile)-1)]
me=bpy.data.meshes.new('Cyclorama');me.from_pydata(verts,[],faces);me.update();ob=bpy.data.objects.new('Seamless warm backdrop',me);bpy.context.collection.objects.link(ob);ob.data.materials.append(back)
sub=ob.modifiers.new('Smooth studio curve','SUBSURF');sub.levels=2
for po in me.polygons:po.use_smooth=True
if 'eevee' in args:
 s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=24;s.eevee.use_shadow_jitter_viewport=False
 water.node_tree.nodes['Principled BSDF'].inputs['Transmission Weight'].default_value=0
 water.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.20,.36,.38,1)
 water.node_tree.nodes['Principled BSDF'].inputs['Coat Weight'].default_value=.7
 water.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.16

s.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'blender'/f'{shot}.blend'))
out=R/'renders'/shot;out.mkdir(exist_ok=True)
if preview:
 s.frame_set(N if 'last' in args else N//2);s.render.filepath=str(out/'preview.png');bpy.ops.render.render(write_still=True)
else:
 s.render.filepath=str(out/'f_');bpy.ops.render.render(animation=True)
