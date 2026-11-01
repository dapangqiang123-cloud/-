"""Editable video-sequencer backup. Does not write the user's Jianying drafts."""
import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.name='家的空气答案06_双重防漏_65秒'
s.render.resolution_x=1080;s.render.resolution_y=1920;s.render.resolution_percentage=100;s.render.fps=30;s.frame_start=1;s.frame_end=1950
s.view_settings.view_transform='Standard'
e=s.sequence_editor_create()
items=json.loads((R/'edit/剪辑清单.json').read_text())
for item in items:
 f=Path(item['file']);assert f.exists() and f.stat().st_size>1000,f
 channel=2 if item['kind']=='BlenderEEVEE' else 1
 st=e.strips.new_movie(item['description'],str(f),channel=channel,frame_start=int(item['start']*30)+1,fit_method='FIT')
 st.frame_final_duration=round(item['duration']*30)
for n,f,ch in [('临时配音_剪映新闻女声','临时配音_剪映新闻女声_65秒.wav',3),('BGM_Warm_Luxury_Lounge','BGM_剪映曲库_Warm_Luxury_Lounge_65秒.wav',4)]:
 st=e.strips.new_sound(n,str(R/'assets/audio'/f),channel=ch,frame_start=1);st.frame_final_duration=1950
for ch,n in [(1,'视频主轨_生活与官方'),(2,'3D原理段'),(3,'临时配音'),(4,'BGM')]:
 if ch<len(e.channels):e.channels[ch].name=n
for item in items:s.timeline_markers.new(item['description'],frame=item['start']*30+1)
s.frame_set(1)
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   area.type='SEQUENCE_EDITOR'
# Original resources remain linked; all media paths are within this deliverable folder.
bpy.ops.wm.save_as_mainfile(filepath=str(R/'edit/双重防漏_完整分轨剪辑备份.blend'))
print('Editable 65-second timeline saved; video and audio sources remain separate.')
