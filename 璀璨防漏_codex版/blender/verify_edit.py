import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'edit/双重防漏_完整分轨剪辑备份.blend'))
s=bpy.context.scene;e=s.sequence_editor;coverage=[0]*1950;rows=[]
for x in e.strips:
 row={'name':x.name,'type':x.type,'channel':x.channel,'start':x.frame_final_start,'end':x.frame_final_end}
 if x.type=='MOVIE':
  assert Path(bpy.path.abspath(x.filepath)).exists(),x.filepath
  for i in range(x.frame_final_start-1,x.frame_final_end-1):coverage[i]+=1
 elif x.type=='SOUND':assert Path(bpy.path.abspath(x.sound.filepath)).exists(),x.sound.filepath
 rows.append(row)
assert len(rows)==15 and all(v==1 for v in coverage)
assert [(s.render.resolution_x,s.render.resolution_y),s.render.fps,s.frame_end]==[(1080,1920),30,1950]
assert sorted(x['channel'] for x in rows if x['type']=='SOUND')==[3,4]
(R/'logs/可编辑备份核验.json').write_text(json.dumps({'frame_coverage':'1950 frames exactly once','strips':rows,'channels':[{ 'number':c.number,'name':c.name} for c in e.channels if c.number in [1,2,3,4]]},ensure_ascii=False,indent=2))
print('PASS: 13 video strips, 2 separate audio strips, exact 65-second coverage, all source files exist.')
