from pathlib import Path
import numpy as np,wave,subprocess,json
R=Path(__file__).resolve().parents[1];A=R/'OpenFilm工程/assets';fs=48000
starts=[.18,3.18,7.18,11.12,15.25];durs=[2.481625,3.072,3.186938,3.578750,4.179594]
def run(args):subprocess.run(['ffmpeg','-v','error','-y',*map(str,args)],check=True)
for i in range(1,6):
 run(['-i',R/'素材'/f'vo{i}.mp3','-af','loudnorm=I=-17:TP=-2:LRA=7,afade=t=in:d=0.025','-ar',fs,'-ac',1,A/f'vo{i}.wav'])
# Original designed paper and air movement, deterministic and very quiet under narration.
rng=np.random.default_rng(783);sound=np.zeros((20*fs,2))
def filt(x,lo,hi):
 z=np.fft.rfft(x);f=np.fft.rfftfreq(len(x),1/fs);z*=np.minimum(1,np.maximum(0,(f-lo)/250))*np.minimum(1,np.maximum(0,(hi-f)/700));return np.fft.irfft(z,len(x))
def put(x,at,gain,pan=0):
 n=int(at*fs);x=x[:len(sound)-n]*gain;sound[n:n+len(x),0]+=x*(1-pan*.45);sound[n:n+len(x),1]+=x*(1+pan*.45)
for i,at in enumerate([2.72,6.72,10.72,14.72]):
 n=int(.64*fs);t=np.linspace(0,1,n);x=filt(rng.normal(0,1,n),300,3500)*np.sin(np.pi*t)**2;put(x,at,.038,(-1)**i*.6)
for at in [.22,3.22,7.22,11.22,15.3]:
 t=np.arange(int(.16*fs))/fs;x=(np.sin(2*np.pi*280*t)*np.exp(-t*45)+filt(rng.normal(0,.25,len(t)),100,1500)*np.exp(-t*35))*np.minimum(t/.003,1);put(x,at,.022)
with wave.open(str(A/'foley.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(fs);w.writeframes((np.clip(sound,-1,1)*32767).astype('<i2').tobytes())
run(['-i',R.parent/'Vox拼贴风格测试/素材/music.mp3','-t',20,'-af','loudnorm=I=-24:TP=-5:LRA=9,afade=t=in:d=0.25,afade=t=out:st=18.8:d=1.2','-ar',fs,'-ac',2,A/'music.wav'])
# Film contains real separate tracks, each voice line at its editorial time.
f=R/'OpenFilm工程/film.html';text=f.read_text();tracks='<section id="narration">'+''.join(f'<audio id="vo-{i+1}" src="assets/vo{i+1}.wav" at="{t}" volume="1"></audio>' for i,t in enumerate(starts))+'</section><section id="music"><audio id="score" src="assets/music.wav#t=0,20" volume="1"></audio></section><section id="foley"><audio id="paper-air" src="assets/foley.wav#t=0,20" volume="1"></audio></section>'
if 'id="narration"' not in text:f.write_text(text.replace('</body>',tracks+'</body>'))
(R/'制作文件/audio-timing.json').write_text(json.dumps({'starts':starts,'durations':durs,'music':'-24 LUFS, 1.2s tail fade','voice':'-17 LUFS'},indent=2))
print('Audio tracks ready')
