#!/usr/bin/env python3
"""Generate VO via edge-tts and mix light bed + sfx placeholders."""
import asyncio, os, subprocess, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
AUD=ROOT/'assets'/'audio'
AUD.mkdir(parents=True, exist_ok=True)
LINES=[
 (1,"关着窗，空气怎么进出？"),
 (2,"墙里，藏着一条换气通道。"),
 (3,"两股气流交错，热量在芯里交换。"),
 (4,"脏的留下，干净的进来。"),
 (5,"璀璨 Mini 全热交换新风。"),
]
# timing anchors (start sec)
STARTS=[0.3,3.6,7.6,12.0,16.0]

async def synth():
  try:
    import edge_tts
  except ImportError:
    subprocess.check_call(['pip3','install','-q','edge-tts'])
    import edge_tts
  voice='zh-CN-YunxiNeural'
  for i,text in LINES:
    out=AUD/f'vo{i}.mp3'
    communicate=edge_tts.Communicate(text,voice,rate='-5%')
    await communicate.save(str(out))
    print('vo',out)
  # concat with delays using ffmpeg adelay
  # Build filter
  inputs=[]
  filters=[]
  for idx,(i,_) in enumerate(LINES):
    inputs+=['-i',str(AUD/f'vo{i}.mp3')]
    delay=int(STARTS[idx]*1000)
    filters.append(f'[{idx}]adelay={delay}|{delay}[v{idx}]')
  mix=''.join(f'[v{i}]' for i in range(len(LINES)))+f'amix=inputs={len(LINES)}:normalize=0[aout]'
  fc=';'.join(filters)+';'+mix
  vo_all=AUD/'vo_all.mp3'
  cmd=['ffmpeg','-y',*inputs,'-filter_complex',fc,'-map','[aout]','-t','20',str(vo_all)]
  subprocess.check_call(cmd)
  print('wrote',vo_all)
  # simple soft bed: sine pads via ffmpeg
  bed=AUD/'bed.mp3'
  subprocess.check_call(['ffmpeg','-y','-f','lavfi','-i','sine=frequency=196:duration=20','-f','lavfi','-i','sine=frequency=294:duration=20','-filter_complex','[0]volume=0.03[a];[1]volume=0.02[b];[a][b]amix=inputs=2,afade=t=in:st=0:d=1,afade=t=out:st=18:d=2','-t','20',str(bed)])
  # paper sfx-ish noise bursts
  sfx=AUD/'sfx.mp3'
  subprocess.check_call(['ffmpeg','-y','-f','lavfi','-i','anoisesrc=color=pink:duration=20:amplitude=0.015','-af','volume=0.4,afade=t=in:st=3.4:d=0.15,afade=t=out:st=4.2:d=0.4','-t','20',str(sfx)])
  mix_out=AUD/'mix.mp3'
  subprocess.check_call(['ffmpeg','-y','-i',str(vo_all),'-i',str(bed),'-i',str(sfx),
    '-filter_complex','[0]volume=1.0[v];[1]volume=0.7[b];[2]volume=0.35[s];[v][b][s]amix=inputs=3:duration=first:normalize=0','-t','20',str(mix_out)])
  print('mix',mix_out)
  (AUD/'timing.json').write_text(json.dumps({'starts':STARTS,'lines':[t for _,t in LINES]},ensure_ascii=False,indent=2))

asyncio.run(synth())
