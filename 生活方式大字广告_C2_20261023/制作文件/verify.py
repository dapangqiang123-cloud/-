from pathlib import Path
import subprocess,json

ROOT=Path(__file__).resolve().parents[1]
movie=ROOT/'成片/璀璨C2_尽兴相聚_24秒测试片_V1.mp4'
out=ROOT/'检查'
facts=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(movie)]))
v=next(s for s in facts['streams'] if s['codec_type']=='video')
a=next(s for s in facts['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'])==(1080,1440)
assert abs(float(facts['format']['duration'])-24)<0.08
assert v['r_frame_rate']=='30/1'
assert float(a['duration'])>=23.9
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(movie),'-vf',"select='not(mod(n,60))',scale=324:-1,drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:text='%{pts\\:hms}':fontsize=15:fontcolor=white:box=1:boxcolor=black@0.7:x=7:y=7,tile=4x3",'-frames:v','1',str(out/'成片每2秒检查.jpg')],check=True)
for name,start,length in [('横移',4.8,1.6),('两厅拉远',10.8,1.6),('产品转场',16.5,1.6),('片尾拉远',20.7,1.6)]:
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(start),'-t',str(length),'-i',str(movie),'-vf','fps=5,scale=270:-1,tile=4x2','-frames:v','1',str(out/(name+'_过程检查.jpg'))],check=True)
metrics=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(movie),'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True,check=True)
(out/'音轨检查.txt').write_text(metrics.stderr)
report={'file':str(movie),'duration':float(facts['format']['duration']),'dimensions':[v['width'],v['height']],'fps':v['r_frame_rate'],'videoCodec':v['codec_name'],'audioCodec':a['codec_name'],'audioDuration':float(a['duration']),'bytes':int(facts['format']['size']),'imageChecks':['成片每2秒检查.jpg','横移_过程检查.jpg','两厅拉远_过程检查.jpg','产品转场_过程检查.jpg','片尾拉远_过程检查.jpg'],'audioReview':'Audio track decoded successfully and measured; no claim of auditory audition.'}
(out/'成片参数与验收.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False))
