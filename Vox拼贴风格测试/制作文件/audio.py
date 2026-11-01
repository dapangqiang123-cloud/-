from pathlib import Path
import numpy as np,wave,subprocess,json
R=Path(__file__).resolve().parents[1];A=R/'OpenFilm工程/assets';fs=48000
starts=[.35,4.45,8.05,12.5,16.9,21.65];durs=[3.291406,3.004063,3.709375,2.377125,3.787750,3.186938]
def run(args):subprocess.run(['ffmpeg','-v','error','-y',*map(str,args)],check=True)
for i in range(1,7):
 run(['-i',R/'素材'/f'vo{i}.mp3','-af','loudnorm=I=-17:TP=-2:LRA=7,afade=t=in:d=0.025','-ar',fs,'-ac',1,A/f'vo{i}.wav'])
# Original designed paper and air movement, deterministic and very quiet under narration.
rng=np.random.default_rng(783);sound=np.zeros((25*fs,2))
def filt(x,lo,hi):
 z=np.fft.rfft(x);f=np.fft.rfftfreq(len(x),1/fs);z*=np.minimum(1,np.maximum(0,(f-lo)/250))*np.minimum(1,np.maximum(0,(hi-f)/700));return np.fft.irfft(z,len(x))
def put(x,at,gain,pan=0):
 n=int(at*fs);x=x[:len(sound)-n]*gain;sound[n:n+len(x),0]+=x*(1-pan*.45);sound[n:n+len(x),1]+=x*(1+pan*.45)
for i,at in enumerate([3.9,7.5,11.7,16.2,21.2]):
 n=int(.64*fs);t=np.linspace(0,1,n);x=filt(rng.normal(0,1,n),300,3500)*np.sin(np.pi*t)**2;put(x,at,.038,(-1)**i*.6)
for at in [.25,4.5,8,12.5,17,21.8]:
 t=np.arange(int(.16*fs))/fs;x=(np.sin(2*np.pi*280*t)*np.exp(-t*45)+filt(rng.normal(0,.25,len(t)),100,1500)*np.exp(-t*35))*np.minimum(t/.003,1);put(x,at,.022)
with wave.open(str(A/'foley.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(fs);w.writeframes((np.clip(sound,-1,1)*32767).astype('<i2').tobytes())
run(['-i',R/'素材/music.mp3','-t',25,'-af','loudnorm=I=-24:TP=-5:LRA=9,afade=t=in:d=0.25,afade=t=out:st=23.8:d=1.2','-ar',fs,'-ac',2,A/'music.wav'])
# Film contains real separate tracks, each voice line at its editorial time.
f=R/'OpenFilm工程/film.html';text=f.read_text();tracks='<section id="narration">'+''.join(f'<audio id="vo-{i+1}" src="assets/vo{i+1}.wav" at="{t}" volume="1"></audio>' for i,t in enumerate(starts))+'</section><section id="music"><audio id="score" src="assets/music.wav#t=0,25" volume="1"></audio></section><section id="foley"><audio id="paper-air" src="assets/foley.wav#t=0,25" volume="1"></audio></section>'
if 'id="narration"' not in text:f.write_text(text.replace('</body>',tracks+'</body>'))
(R/'制作文件/audio-timing.json').write_text(json.dumps({'starts':starts,'durations':durs,'music':'-24 LUFS, 1.2s tail fade','voice':'-17 LUFS'},indent=2))
print('Audio tracks ready')
