from pathlib import Path
import numpy as np,wave,subprocess,json
def filt(x,low,high):
 f=np.fft.rfftfreq(len(x),1/48000);z=np.fft.rfft(x);z*=((f>low)&(f<high));return np.fft.irfft(z,n=len(x))
b=Path.cwd()/'多空间选型_20261023';o=b/'升级制作/剪映交付素材';o.mkdir(exist_ok=True);fs=48000;rng=np.random.default_rng(20261023);sound=np.zeros((84*fs,2),np.float32)
def put(x,at,gain=.1,pan=0):
 n=int(at*fs);x=x[:len(sound)-n]*gain;sound[n:n+len(x),0]+=x*(1-pan*.3);sound[n:n+len(x),1]+=x*(1+pan*.3)
def air(at,d=.6,gain=.025):
 n=int(d*fs);t=np.linspace(0,1,n);x=filt(rng.normal(0,1,n),300,2200);put(x*np.sin(np.pi*t)**2,at,gain)
for at in [4.75,22.75,40.75,59.75]:air(at,.6,.035)
for at in [16.1,32.1,51.1,71.1]:
 t=np.arange(int(.7*fs))/fs;x=(np.sin(2*np.pi*520*t)+.35*np.sin(2*np.pi*1040*t))*np.exp(-t*8)*np.minimum(t/.012,1);put(x,at,.016)
air(13.2,2.4,.014);air(27.2,2.8,.01);air(68.2,2.5,.012)
t=np.arange(int(.22*fs))/fs;x=np.sin(2*np.pi*180*t)*np.exp(-t*30)+filt(rng.normal(0,.25,len(t)),0,1600)*np.exp(-t*42);put(x,63.1,.045)
t=np.arange(int(2*fs))/fs;put((np.sin(2*np.pi*659.25*t)+.5*np.sin(2*np.pi*987.77*t))*np.exp(-t*2.8)*np.minimum(t/.02,1),80,.012)
with wave.open(str(o/'03_音效.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(fs);w.writeframes((np.clip(sound,-1,1)*32767).astype('<i2').tobytes())
def run(args):subprocess.run(['ffmpeg','-v','error','-y',*args],check=True)
run(['-i',str(b/'完整视频工程/audio/voice.wav'),'-af','volume=2.11dB,alimiter=limit=0.84:level=false','-ar','48000',str(o/'01_女声配音.wav')])
run(['-i',str(b/'升级制作/即梦生成素材/M01.mp3'),'-i',str(o/'01_女声配音.wav'),'-filter_complex','[0:a]volume=-14.8dB,afade=t=in:d=0.8,afade=t=out:st=80:d=4[m];[m][1:a]sidechaincompress=threshold=0.04:ratio=3:attack=80:release=450[out]','-map','[out]','-t','84','-ar','48000',str(o/'02_配乐.wav')])
run(['-i',str(o/'01_女声配音.wav'),'-i',str(o/'02_配乐.wav'),'-i',str(o/'03_音效.wav'),'-filter_complex','[0:a][1:a][2:a]amix=inputs=3:normalize=0,alimiter=limit=0.84:level=false[out]','-map','[out]','-t','84',str(o/'审片混音.wav')])
print('三条独立音轨与审片混音已生成')
