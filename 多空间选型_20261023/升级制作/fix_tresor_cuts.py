from pathlib import Path
import re,json,os,subprocess,concurrent.futures
b=Path.cwd()/'多空间选型_20261023';p=b/'品牌科普升级样片_OpenFilm';u=b/'升级制作';out=u/'剪映交付素材/正式镜头';out.mkdir(exist_ok=True)
f=p/'film.html';s=f.read_text()
fix={3:('talent17.mov',67.2,70.2,.6,''),7:('talent11.mov',88,91,.75,''),11:('talent15.mp4',73.6,74.8,.6,'object-position:80% center;'),15:('talent15.mp4',48.2,50.6,.8,''),19:('talent6.mp4',.1,1.6,.75,''),21:('talent17.mov',67.2,70.2,1,''),14:('talent11.mov',14,15.6,.8,''),16:('talent11.mov',16,17.7,.85,'')}
shots=json.loads((u/'剪辑镜头表.json').read_text())
for n,(src,i,e,speed,style) in fix.items():
 s=re.sub(fr'<video id="V{n:02}"[^>]*></video>',f'<video id="V{n:02}" src="assets/{src}#t={i},{e}" at="{shots[n-1]["at"]}" speed="{speed}" muted style="object-fit:cover;{style}"></video>',s)
 shots[n-1].update(inPoint=i,outPoint=e,speed=speed)
f.write_text(s);(u/'剪辑镜头表.json').write_text(json.dumps(shots,ensure_ascii=False,indent=2))
# Render corrected visual ranges without audio/subtitle; restore full film after all renders.
audio=re.findall(r'<section><audio.*?</section>',s);visual=re.sub(r'<section><audio.*?</section>','',s);f.write_text(visual)
env=os.environ.copy();env.update(PLAYWRIGHT_BROWSERS_PATH='/Applications/OpenFilm.app/Contents/Resources/runtime/ms-playwright',OPENFILM_HOME='/tmp/tresor-openfilm-runtime',OPENFILM_NO_BROWSER='1')
cli='/Applications/OpenFilm.app/Contents/Resources/app.asar.unpacked/node_modules/openfilm/bin/openfilm.mjs'
def job(n):
 st=shots[n-1];dest=out/f'F{n:02}.mp4';res=subprocess.run(['node',cli,'render',f'{st["at"]}-{st["at"]+st["duration"]}','--out',str(dest),'--fps','30','--scale','1.5','--workers','1'],cwd=p,env=env,capture_output=True,text=True)
 print(n,res.returncode,res.stdout[-300:],res.stderr[-300:],flush=True);assert res.returncode==0
try:
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(job,fix))
 for n in range(1,28):
  if n not in fix:
   dest=out/f'F{n:02}.mp4'
   if not dest.exists():os.link(u/f'剪映交付素材/视频片段/V{n:02}.mp4',dest)
finally:f.write_text(s)
print('修正完成',flush=True)
