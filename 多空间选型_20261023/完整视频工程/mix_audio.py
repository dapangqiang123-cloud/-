from pathlib import Path
import json,subprocess,re
import numpy as np
import wave
class PCM:
    @staticmethod
    def read(p,**kwargs):
        with wave.open(str(p),'rb') as f:
            return np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').reshape(-1,f.getnchannels()).astype(np.float32)/32768,f.getframerate()
    @staticmethod
    def write(p,a,sr):
        with wave.open(str(p),'wb') as f:
            f.setnchannels(a.shape[1]);f.setsampwidth(2);f.setframerate(sr);f.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
sf=PCM()
R=Path(__file__).parent; F='/opt/homebrew/bin/ffmpeg'; P='/opt/homebrew/bin/ffprobe'
rows=json.loads((R/'script.json').read_text()); sr=48000
voice=np.zeros((84*sr,2),np.float32); caps=[];log=[]
for r in rows:
    src=R/'audio_words'/(r['id']+'.mp3')
    duration=float(subprocess.check_output([P,'-v','quiet','-show_entries','format=duration','-of','csv=p=0',str(src)]))
    window=r['end']-r['start']; speed=max(1,duration/(window-.42))
    if speed>1.16:raise ValueError(f"Speech too fast: {r['id']}: {speed}")
    dst=R/'audio'/(r['id']+'_timed.wav')
    subprocess.run([F,'-y','-loglevel','error','-i',str(src),'-af',f'atempo={speed:.7f},loudnorm=I=-18:TP=-2:LRA=7','-ar',str(sr),'-ac','2',str(dst)],check=True)
    data,_=sf.read(dst,dtype='float32',always_2d=True);start=r['start']+.2;offset=round(start*sr)
    voice[offset:offset+len(data)]+=data
    words=json.loads((R/'audio_words'/(r['id']+'.json')).read_text())
    # Group provider word timestamps into short natural clauses. No estimated per-character alignment.
    groups=[]; g=[]
    for w in words:
        if g:
            gap=(w['offset']-(g[-1]['offset']+g[-1]['duration']))/1e7
            if len(''.join(v['text'] for v in g))+len(w['text'])>18 or gap>.18:
                groups.append(g);g=[]
        g.append(w)
    if g:groups.append(g)
    for i,g in enumerate(groups):
        text=''.join(w['text'] for w in g)
        a=start+g[0]['offset']/1e7/speed;b=start+(g[-1]['offset']+g[-1]['duration'])/1e7/speed+.1
        if i+1<len(groups):b=min(b,start+groups[i+1][0]['offset']/1e7/speed-.025)
        caps.append({'start':round(a,3),'end':round(min(b,r['end']-.06),3),'text':text})
    log.append({'id':r['id'],'raw_seconds':duration,'speed':speed,'audio_start':start,'audio_end':start+len(data)/sr,'scene_end':r['end']})
sf.write(R/'audio/voice.wav',voice,sr)
subprocess.run([F,'-y','-loglevel','error','-i',str(R/'assets/music.mp3'),'-i',str(R/'assets/music.mp3'),'-i',str(R/'assets/music.mp3'),'-filter_complex','[0:a][1:a]acrossfade=d=3:c1=tri:c2=tri[m];[m][2:a]acrossfade=d=3:c1=tri:c2=tri,loudnorm=I=-29:TP=-9:LRA=5,afade=t=in:d=1,afade=t=out:st=81:d=3[music]','-map','[music]','-t','84','-ar',str(sr),'-ac','2',str(R/'audio/music.wav')],check=True)
music,_=sf.read(R/'audio/music.wav',dtype='float32',always_2d=True);mix=voice.copy();mix[:min(len(mix),len(music))]+=music[:len(mix)]
sf.write(R/'audio/premix.wav',mix,sr)
subprocess.run([F,'-y','-loglevel','error','-i',str(R/'audio/premix.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=7','-ar',str(sr),'-c:a','pcm_s16le',str(R/'audio/mix.wav')],check=True)
(R/'captions.json').write_text(json.dumps(caps,ensure_ascii=False,indent=2));(R/'audio/timing.json').write_text(json.dumps(log,ensure_ascii=False,indent=2))
def ts(t):
    ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(R.parent/'璀璨多空间选型_字幕.srt').write_text('\n\n'.join(f'{i+1}\n{ts(c["start"])} --> {ts(c["end"])}\n{c["text"]}' for i,c in enumerate(caps))+'\n')
print('Mixed 84s; subtitles',len(caps),'max speed',max(x['speed'] for x in log))
