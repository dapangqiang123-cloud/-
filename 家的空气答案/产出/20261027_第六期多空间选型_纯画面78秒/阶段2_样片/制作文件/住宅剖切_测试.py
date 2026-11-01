"""Original procedural architectural previs. No generated images, audio or product internals."""
import bpy, math, random, sys, argparse
from mathutils import Vector
from pathlib import Path
random.seed(213)
p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--samples',type=int,default=64);p.add_argument('--frame',type=int,default=52);p.add_argument('--width',type=int,default=1080);p.add_argument('--height',type=int,default=1920);p.add_argument('--animate',action='store_true');p.add_argument('--engine',default='CYCLES');args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
S=bpy.context.scene;S.render.engine=args.engine;S.render.resolution_x=args.width;S.render.resolution_y=args.height;S.render.resolution_percentage=100;S.render.fps=30;S.frame_start=1;S.frame_end=105
S.render.image_settings.file_format='PNG';S.render.image_settings.color_mode='RGB';S.render.image_settings.color_depth='8';S.render.film_transparent=False
S.view_settings.view_transform='AgX';S.view_settings.look='AgX - Medium High Contrast';S.view_settings.exposure=0
S.world.use_nodes=True;S.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.62,.67,.72,1);S.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.22
if args.engine=='CYCLES':
 S.cycles.samples=args.samples;S.cycles.use_denoising=True;S.cycles.max_bounces=8;S.cycles.diffuse_bounces=4;S.cycles.glossy_bounces=4;S.cycles.transparent_max_bounces=8
 try:
  pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='METAL';pref.get_devices()
  for d in pref.devices:d.use=d.type=='METAL'
  S.cycles.device='GPU'
 except Exception as e:print('GPU_SETUP',e)

def mat(name,c,rough=.5,metal=0):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes.get('Principled BSDF');n.inputs['Base Color'].default_value=(*c,1);n.inputs['Roughness'].default_value=rough;n.inputs['Metallic'].default_value=metal;return m
plaster=mat('暖石灰抹墙',(.68,.63,.55),.83);edge=mat('切面石膏',(.81,.77,.68),.75);coffee=mat('咖色金属',(.067,.049,.038),.34,.7);gold=mat('暗香槟金',(.32,.22,.10),.3,.72);olive=mat('低饱和橄榄',(.22,.25,.14),.75);ceramic=mat('米白陶瓷',(.74,.71,.64),.28);paper=mat('无字纸张',(.72,.69,.60),.9);glass=mat('玻璃',(.65,.74,.73),.12);glass.node_tree.nodes['Principled BSDF'].inputs['Transmission Weight'].default_value=.95;glass.node_tree.nodes['Principled BSDF'].inputs['IOR'].default_value=1.46

def wood(name,c):
 m=mat(name,c,.43);nt=m.node_tree;n=nt.nodes;tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=3.0;tex.inputs['Detail'].default_value=3;tc=n.new('ShaderNodeTexCoord');v=n.new('ShaderNodeVectorMath');v.operation='MULTIPLY';v.inputs[1].default_value=(1.8,38,14);nt.links.new(tc.outputs['Generated'],v.inputs[0]);nt.links.new(v.outputs[0],tex.inputs['Vector']);r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].position=.22;r.color_ramp.elements[0].color=(*(x*.6 for x in c),1);r.color_ramp.elements[1].position=.78;r.color_ramp.elements[1].color=(*(min(x*1.32,1) for x in c),1);nt.links.new(tex.outputs['Fac'],r.inputs[0]);nt.links.new(r.outputs['Color'],n.get('Principled BSDF').inputs['Base Color']);b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.12;b.inputs['Distance'].default_value=.012;nt.links.new(tex.outputs['Fac'],b.inputs['Height']);nt.links.new(b.outputs[0],n.get('Principled BSDF').inputs['Normal']);return m
walnut=wood('烟熏胡桃木',(.062,.033,.019));oak=[wood('橡木_%02d'%i,(.235+random.uniform(-.020,.020),.173+random.uniform(-.015,.015),.115+random.uniform(-.010,.010))) for i in range(7)]
def fabric(name,c):
 m=mat(name,c,.88);nt=m.node_tree;n=nt.nodes;t=n.new('ShaderNodeTexNoise');t.inputs['Scale'].default_value=180;t.inputs['Detail'].default_value=2;b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.24;b.inputs['Distance'].default_value=.004;nt.links.new(t.outputs['Fac'],b.inputs['Height']);nt.links.new(b.outputs[0],n.get('Principled BSDF').inputs['Normal']);n.get('Principled BSDF').inputs['Sheen Weight'].default_value=.22;return m
linen=fabric('米白亚麻',(.67,.63,.55));white=fabric('被褥棉麻',(.79,.76,.69));rugmat=fabric('手织羊毛地毯',(.43,.40,.34));greenfab=fabric('橄榄织物',(.23,.25,.16));stone=mat('深咖洞石',(.13,.105,.082),.36)
nt=stone.node_tree;n=nt.nodes;t=n.new('ShaderNodeTexNoise');t.inputs['Scale'].default_value=5;t.inputs['Roughness'].default_value=.8;r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(.05,.038,.027,1);r.color_ramp.elements[1].color=(.22,.19,.14,1);nt.links.new(t.outputs['Fac'],r.inputs[0]);nt.links.new(r.outputs[0],n.get('Principled BSDF').inputs['Base Color'])

pn=plaster.node_tree.nodes;pt=pn.new('ShaderNodeTexNoise');pt.inputs['Scale'].default_value=95;pb=pn.new('ShaderNodeBump');pb.inputs['Strength'].default_value=.13;pb.inputs['Distance'].default_value=.005;plaster.node_tree.links.new(pt.outputs['Fac'],pb.inputs['Height']);plaster.node_tree.links.new(pb.outputs[0],pn.get('Principled BSDF').inputs['Normal'])
ROOT=None

def bind(ob,material=None):
 if material:ob.data.materials.append(material)
 if ROOT:ob.parent=ROOT
 return ob

def cube(name,loc,dim,material,bevel=.02):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);ob=bpy.context.object;ob.name=name;ob.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);bind(ob,material)
 if bevel:
  m=ob.modifiers.new('实体圆角','BEVEL');m.width=bevel;m.segments=3
  m=ob.modifiers.new('加权法线','WEIGHTED_NORMAL')
 return ob

def cylinder(name,loc,r,depth,material,vertices=40):
 bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=depth,location=loc);o=bpy.context.object;o.name=name;bind(o,material);m=o.modifiers.new('边缘圆润','BEVEL');m.width=min(.012,r*.12);m.segments=3
 for f in o.data.polygons:f.use_smooth=True
 return o

def ball(name,loc,dim,material):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,radius=1,location=loc);o=bpy.context.object;o.name=name;o.scale=dim;bind(o,material)
 for f in o.data.polygons:f.use_smooth=True
 return o

def curve(name,pts,rad,material,cyclic=False):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.resolution_u=16;c.bevel_depth=rad;c.bevel_resolution=3;s=c.splines.new('BEZIER');s.bezier_points.add(len(pts)-1)
 for b,pt in zip(s.bezier_points,pts):b.co=pt;b.handle_left_type='AUTO';b.handle_right_type='AUTO'
 s.use_cyclic_u=cyclic;o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);bind(o,material);return o

def chair(x,y,angle=0):
 parent=bpy.data.objects.new('曲木餐椅',None);bpy.context.collection.objects.link(parent);parent.parent=ROOT;parent.location=(x,y,0);parent.rotation_euler.z=angle
 objects=[]
 objects.append(cube('椅座',(0,0,.48),(.49,.48,.07),walnut,.065))
 for a in [-1,1]:
  for b in [-1,1]:objects.append(curve('餐椅渐收椅腿',[(a*.18,b*.17,.48),(a*.22,b*.23,.06)],.022,walnut))
 verts=[];faces=[]
 for i in range(19):
  t=-1+i/9;xx=t*.27;yy=.19+.065*(1-t*t)
  for z in [.60,.82]:verts.append((xx,yy,z))
 for i in range(18):faces.append((2*i,2*i+2,2*i+3,2*i+1))
 me=bpy.data.meshes.new('弯曲椅背');me.from_pydata(verts,[],faces);ob=bpy.data.objects.new('弧面胡桃椅背',me);bpy.context.collection.objects.link(ob);bind(ob,walnut);m=ob.modifiers.new('曲木厚度','SOLIDIFY');m.thickness=.035;m=ob.modifiers.new('椅背圆角','BEVEL');m.width=.025;m.segments=3;objects.append(ob)
 for ob in objects:ob.parent=parent
 return parent

def plant(x,y,z=0,size=1):
 cylinder('粗陶花盆',(x,y,z+.23*size),.20*size,.46*size,ceramic)
 for i in range(14):
  a=i*2.399;zz=z+(.70+i*.045)*size;ex=x+math.cos(a)*(.2+(i%4)*.04)*size;ey=y+math.sin(a)*(.2+(i%4)*.04)*size
  curve('细植物枝',[(x,y,z+.35*size),(x+math.cos(a)*.1*size,y+math.sin(a)*.1*size,zz-.15*size),(ex,ey,zz)],.008*size,olive)
  ob=ball('有厚度的橄榄叶',(ex,ey,zz),(.17*size,.048*size,.009*size),olive);ob.rotation_euler=(random.uniform(-.4,.4),random.uniform(-.4,.4),a)

def curtain(x,y,width=2,height=2.4):
 verts=[];faces=[];nx=60;nz=22
 for j in range(nz+1):
  z=.14+height*j/nz
  for i in range(nx+1):
   xx=x+width*i/nx;yy=y+.075*math.cos(i/nx*math.pi*16)+.02*math.sin(j/nz*5+i*.2);verts.append((xx,yy,z))
 for j in range(nz):
  for i in range(nx):
   a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1))
 me=bpy.data.meshes.new('亚麻褶皱曲面');me.from_pydata(verts,[],faces);ob=bpy.data.objects.new('落地窗纱',me);bpy.context.collection.objects.link(ob);bind(ob,linen);m=ob.modifiers.new('轻薄布料厚度','SOLIDIFY');m.thickness=.003
 for f in me.polygons:f.use_smooth=True


def bed(x,y,w=1.6,length=2.1,accent=greenfab):
 cube('木床框',(x,y,.27),(w+.12,length+.12,.32),walnut,.055);cube('床垫',(x,y,.50),(w,length,.28),white,.11)
 cube('软包床头',(x,y+length/2,.78),(w+.14,.15,.94),linen,.09)
 # Duvet is a wrinkled, draped mesh rather than a rigid box.
 vs=[];fs=[];nx=32;ny=40
 for j in range(ny+1):
  yy=-length/2-.07+(length-.27)*j/ny
  for i in range(nx+1):
   xx=-w/2-.08+(w+.16)*i/nx;fall=max(0,abs(xx)-w*.44)*1.5+max(0,-yy-length*.43)*1.2
   zz=.68-fall+.014*math.sin(xx*22+yy*4)+.008*math.sin(yy*31+xx*7);vs.append((x+xx,y+yy,zz))
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;fs.append((a,a+1,a+nx+2,a+nx+1))
 me=bpy.data.meshes.new('棉麻被褥褶皱');me.from_pydata(vs,[],fs);ob=bpy.data.objects.new('自然起伏的被褥',me);bpy.context.collection.objects.link(ob);bind(ob,white);m=ob.modifiers.new('被沿厚度','SOLIDIFY');m.thickness=.028
 for f in me.polygons:f.use_smooth=True
 for xx in [-w*.25,w*.25]:
  o=cube('柔软枕头',(x+xx,y+length*.32,.73),(w*.43,.48,.15),linen,.12);o.rotation_euler.z=random.uniform(-.05,.05)
 cube('床尾织物',(x,y-length*.33,.71),(w+.02,.48,.045),accent,.025)
 cylinder('床边圆几',(x+w*.5+.32,y+length*.32,.29),.22,.55,walnut)
 ball('床边陶灯',(x+w*.5+.32,y+length*.32,.68),(.10,.10,.17),ceramic)

def window_west(y0,y1):
 # True opening between solid sill and head, with glazing and mullions.
 x=-5.68;cube('外墙窗台',(x,(y0+y1)/2,.34),(.18,y1-y0,.20),edge,.015);cube('窗上梁',(x,(y0+y1)/2,2.57),(.18,y1-y0,.23),edge,.015)
 for y in [y0,(y0+y1)/2,y1]:cube('细金属窗框',(x,y,1.45),(.075,.045,2.13),coffee,.004)
 for z in [.43,2.45]:cube('窗横框',(x,(y0+y1)/2,z),(.075,y1-y0,.035),coffee,.003)
 cube('透明窗玻璃',(x,(y0+y1)/2,1.44),(.009,y1-y0,2.0),glass,.0)


def apartment(variant=3):
 global ROOT
 ROOT=bpy.data.objects.new('住宅_%s房'%variant,None);bpy.context.collection.objects.link(ROOT);root=ROOT
 cube('建筑楼板',(0,0,-.17),(11.6,8.8,.30),edge,.035)
 # Actual staggered planks, individual bevels and subtle hue variation.
 for j in range(28):
  y=-4.2+j*.3
  for i in range(-1,7):
   x=-5.6+i*1.9+(j%2)*.95
   left=max(-5.6,x);right=min(5.6,x+1.89)
   if right>left:cube('错缝实木地板',((left+right)/2,y+.147,.007),(right-left,.293,.025),random.choice(oak),.003)
 # Two far facade walls; front/right intentionally section-cut.
 cube('北面实体外墙',(0,4.27,1.36),(11.5,.18,2.75),plaster,.015)
 cube('西南实体墙',(-5.68,-4.02,1.35),(.18,.38,2.72),plaster,.014)
 cube('西北实体墙',(-5.68,2.63,1.35),(.18,3.18,2.72),plaster,.014)
 window_west(-3.82,1.0)
 cube('南外墙剖面',(0,-4.28,.18),(11.5,.18,.35),edge,.008);cube('东外墙剖面',(5.68,0,.18),(.18,8.4,.35),edge,.008)
 for y in [-4.15,4.15]:cube('木踢脚线',(0,y,.055),(11.2,.035,.085),walnut,.005)
 # Living walnut battens / soffit with one horizontal slot. No cassette or crossed grille.
 for i in range(47):cube('细胡桃护墙条',(-5.555,-3.75+i*.1,1.15),(.06,.034,1.65),walnut,.006)
 cube('隐藏式吊顶短边',(-5.36,-1.40,2.38),(.52,4.70,.24),edge,.015)
 cube('唯一水平线性风口',(-5.09,-1.40,2.37),(.008,3.70,.038),coffee,.004)
 # Sofa with separate rounded cushions, back pillows, proper shadow gap and slim base.
 cube('羊毛地毯',(-2.70,-1.85,.048),(4.10,3.55,.043),rugmat,.07)
 cube('沙发低底座',(-3.75,-1.6,.19),(1.12,3.05,.24),walnut,.05)
 cube('沙发左靠背',(-4.20,-1.6,.68),(.27,3.08,.79),linen,.11)
 for j in range(3):
  yy=-2.58+j*.96;cube('沙发独立坐垫',(-3.69,yy,.46),(.94,.92,.31),linen,.115)
  o=cube('松弛靠枕',(-4.02,yy,.86),(.27,.77,.56),linen,.12);o.rotation_euler.y=-.16
  if j==0:o=cube('橄榄抱枕',(-3.83,yy-.17,.76),(.22,.49,.46),greenfab,.095);o.rotation_euler=(.11,-.25,.12)
 cube('沙发端扶手',(-3.76,-3.08,.55),(1.13,.20,.61),linen,.07);cube('沙发端扶手',(-3.76,-.12,.55),(1.13,.20,.61),linen,.07)
 cube('石材茶几',(-1.97,-1.64,.36),(1.45,.86,.11),stone,.055)
 for xx in [-2.45,-1.5]:cube('茶几支脚',(xx,-1.64,.20),(.10,.60,.31),coffee,.02)
 cylinder('无字陶茶杯',(-2.13,-1.69,.48),.068,.12,ceramic);cylinder('木茶托',(-2.13,-1.69,.422),.12,.012,walnut)
 cube('无字画册',(-1.68,-1.48,.435),(.35,.27,.035),paper,.007)
 cylinder('陶花瓶',(-1.92,-1.44,.55),.075,.23,ceramic);curve('花瓶枝条',[(-1.92,-1.44,.66),(-1.88,-1.41,.90),(-1.72,-1.42,1.06)],.008,olive)
 for xx,yy,zz in [(-1.78,-1.42,.98),(-1.91,-1.41,.86),(-1.84,-1.41,.94)]:ball('小叶',(xx,yy,zz),(.09,.025,.007),olive)
 cylinder('圆形脚凳',(-1.02,-3.06,.30),.39,.48,linen);plant(-4.95,-3.45,size=.88)
 # Dining room / kitchen, no text, scales or screen UI.
 table=cube('实木餐桌',(-2.75,1.80,.79),(2.10,.95,.10),walnut,.13)
 for xx in [-3.52,-1.98]:cube('餐桌板脚',(xx,1.80,.43),(.11,.65,.70),walnut,.022)
 for xx in [-3.44,-2.70,-1.96]:chair(xx,1.12,math.pi);chair(xx,2.48,0)
 ball('餐桌陶器',(-2.7,1.8,.91),(.19,.14,.07),ceramic)
 for i in range(5):cube('厨房下柜',(-4.86+i*.91,3.73,.47),(.895,.72,.90),walnut,.015)
 cube('浅石材台面',(-3.04,3.71,.97),(4.61,.82,.065),stone,.018)
 for i in range(5):
  cube('厨房上柜',(-4.86+i*.91,4.0,1.99),(.89,.36,.77),walnut,.014)
  cube('柜体暗金拉手',(-4.51+i*.91,3.807,1.90),(.012,.018,.18),gold,.005)
 cube('水槽浅凹面',(-4.55,3.65,1.007),(.62,.43,.016),coffee,.04);curve('水龙头',[(-4.6,3.92,1.01),(-4.6,3.92,1.31),(-4.6,3.68,1.32),(-4.6,3.66,1.24)],.022,gold)
 # Master and secondary rooms. Doorways are real voids, not drawn lines.
 if variant>=3:
  cube('主卧低剖切分隔',(3.03,.83,.61),(5.1,.16,1.22),edge,.012)
  cube('纵向隔墙前段',(.48,-2.97,.61),(.16,2.45,1.22),edge,.012)
  cube('纵向隔墙中段',(.48,.10,.61),(.16,1.70,1.22),edge,.012)
  cube('纵向隔墙后段',(.48,3.30,1.35),(.16,1.72,2.70),plaster,.012)
  bed(3.25,2.65,1.72,2.05)
  cube('主卧地毯',(3.25,2.4,.045),(3.45,3.0,.035),rugmat,.04)
  # rug rendered slightly above flooring but under bed (no intersection with cloth).
  cube('书房分隔',(3.12,-2.0,.61),(.16,4.25,1.22),edge,.012)
  bed(4.38,-2.43,1.02,1.90,accent=linen)
  cube('儿童房衣柜',(4.75,-.15,.94),(1.38,.49,1.84),edge,.035)
  for i in range(3):cylinder('小木积木',(4.05+i*.15,-.90,.10),.08,.14,walnut if i%2 else olive,vertices=16)
  cube('书桌',(1.75,-3.65,.78),(1.72,.66,.065),walnut,.025)
  for x in [1.02,2.48]:cube('桌腿',(x,-3.65,.40),(.055,.48,.75),walnut,.01)
  chair(1.72,-2.93,0)
  for j in range(4):cube('无字书本',(1.36+j*.13,-3.65,.91),(.09,.27,.22),paper if j%2 else greenfab,.005)
  cylinder('桌灯灯座',(2.32,-3.70,.85),.12,.035,gold);curve('桌灯细杆',[(2.32,-3.7,.86),(2.32,-3.7,1.25),(2.2,-3.58,1.30)],.012,gold);ball('桌灯灯罩',(2.16,-3.57,1.30),(.14,.12,.07),ceramic)
  if variant==4:
   cube('四房中部分隔',(1.78,-1.21,.61),(2.43,.14,1.22),edge,.012);bed(1.77,-.1,1.03,1.36,accent=linen)
 else:
  # Large flat: enlarged continuous living-dining; one enclosed sleeping suite.
  cube('大平层卧室分隔',(2.2,.5,.60),(.15,5.2,1.2),edge,.015);bed(4.02,2.65,1.80,2.10)
  cube('平层长餐边柜',(1.4,-2.3,.45),(.65,2.8,.85),walnut,.025);plant(3.9,-2.6,size=1.1)
 # Wall-mounted horizontal concealed vent for north bedroom, no vertical division.
 cube('北面隐蔽吊顶',(3.2,4.08,2.45),(4.65,.33,.28),edge,.014)
 cube('主卧唯一横缝',(3.2,3.905,2.43),(3.75,.009,.04),coffee,.003)
 # Floor lamp as a designed object with readable silhouette.
 cylinder('阅读灯底座',(-4.55,-.16,.07),.17,.06,stone)
 curve('阅读弧形细杆',[(-4.55,-.16,.1),(-4.55,-.16,1.4),(-4.40,-.16,1.72),(-4.16,-.16,1.60)],.014,gold)
 ball('阅读灯罩',(-4.12,-.16,1.58),(.17,.17,.08),ceramic)
 ROOT=None
 return root

# Ground is architectural presentation context, not a product pedestal.
cube('暖咖灰地面',(0,0,-.50),(200,200,.2),mat('哑光石灰地',(.42,.37,.31),.95),.0)
root=apartment(3)
# Small warm emission motivated by a strip recessed in north wall.
def light(name,loc,power,color,size,target,kind='AREA'):
 d=bpy.data.lights.new(name,kind);d.energy=power;d.color=color
 if kind=='AREA':d.shape='DISK';d.size=size
 o=bpy.data.objects.new(name,d);bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o
light('窗侧大面积日光',(-8,-4,10),850,(1,.90,.78),6,(0,0,0));light('自然天光反射',(5,-2,8),430,(.81,.88,1),8,(0,0,0));light('北面墙反射',(0,7,9),650,(1,.95,.86),6,(0,0,0))
sun=light('傍晚斜日',(-8,-4,11),3.0,(1,.90,.77),1,(0,0,0),kind='SUN');sun.data.angle=.08
bpy.ops.object.camera_add(location=(13.5,-17,17.5));cam=bpy.context.object;cam.name='等轴测建筑相机';S.camera=cam;target=Vector((0,0,.25));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=26.6;cam.data.lens=50;cam.data.clip_end=300
# Test frame first. Only render the animation after visual gate.
S.frame_set(args.frame)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'住宅剖切_质量测试.blend'))
S.render.filepath=str(out/'SH02_质量测试.png');bpy.ops.render.render(write_still=True)
print('QUALITY_STILL_READY',S.render.filepath,flush=True)
