from pathlib import Path
import subprocess,json,shutil
R=Path(__file__).resolve().parent;A=R/'assets/audio';A.mkdir(exist_ok=True)
P=Path('/Users/weipeilong/Downloads/JianyingPro Drafts/家的空气答案系列/textReading')
ids=['2b6cdeea-9861-464f-b1b0-6531b8dd0e66','f9866b64-b2dd-487e-b662-ca72d595dd78','d4c2cb46-5738-4214-9d69-a1d62ac2bbc2','9cab880f-e1cd-48f3-8b75-e2f09301efc1','1a3d3fbf-5d6d-4ff3-b428-f20d2ac2aa47','9180383a-76d0-4b38-985e-abb80e3e7d89','b8d665d4-981c-4583-b199-5ec6b2996f01','8bd682a0-4998-42b1-bb64-c5b1213bc7dc','3e6e188a-47a1-4eac-be04-7eec7cd0ba03','0f4162e3-00f3-4656-a7d8-502db16c83bd']
lines=json.loads((R/'edit/VO.json').read_text());records=[]
def run(args):subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',*map(str,args)],check=True)
for i,((start,end,text),id) in enumerate(zip(lines,ids)):
 src=next(P.glob('*'+id+'.wav'));raw=A/f'VO_{i+1:02}_剪映新闻女声原始.mp3';shutil.copy2(src,raw)
 dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(raw)]))
 length=end-start;speed=max(1,dur/(length-.16))
 out=A/f'VO_{i+1:02}_对齐.wav'
 run(['-i',raw,'-af',f'atempo={speed:.6f},apad,atrim=duration={length},afade=t=out:st={length-.04}:d=0.04','-ar',48000,'-ac',1,out])
 records.append({'index':i+1,'source':str(src),'start':start,'duration':length,'source_duration':dur,'speed':round(speed,6),'text':text,'aligned':str(out)})
(R/'logs/VO时间对齐.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
concat=A/'vo_concat.txt';concat.write_text('\n'.join("file '"+r['aligned']+"'" for r in records))
run(['-f','concat','-safe','0','-i',concat,'-af','loudnorm=I=-16:TP=-2:LRA=8','-ar',48000,'-ac',2,A/'临时配音_剪映新闻女声_65秒.wav'])
B=Path('/Users/weipeilong/Movies/JianyingPro/User Data/Cache/music/2ff45f7103783bab27d266b82d228e57.mp3');shutil.copy2(B,A/'BGM_剪映曲库_Warm_Luxury_Lounge_原始.m4a')
run(['-i',B,'-t',65,'-af','loudnorm=I=-30:TP=-8:LRA=8,afade=t=in:d=1,afade=t=out:st=61:d=4','-ar',48000,'-ac',2,A/'BGM_剪映曲库_Warm_Luxury_Lounge_65秒.wav'])
run(['-i',A/'临时配音_剪映新闻女声_65秒.wav','-i',A/'BGM_剪映曲库_Warm_Luxury_Lounge_65秒.wav','-filter_complex','[0:a][1:a]amix=inputs=2:normalize=0,alimiter=limit=0.89[a]','-map','[a]','-t',65,A/'成片混音_65秒.wav'])
print(json.dumps(records,ensure_ascii=False,indent=2))
