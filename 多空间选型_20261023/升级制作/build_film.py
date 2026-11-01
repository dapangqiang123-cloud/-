from pathlib import Path
import json,shutil,os,html
root=Path.cwd();b=root/'多空间选型_20261023';u=b/'升级制作';p=b/'品牌科普升级样片_OpenFilm';a=p/'assets';a.mkdir(exist_ok=True)
idx={x['id']:x for x in json.loads((u/'达人选片/index.json').read_text())}
for i in [6,11,15,17,20]:
 src=Path(idx[i]['path']);dst=a/f'talent{i}{src.suffix.lower()}'
 if not dst.exists():shutil.copy2(src,dst)
for k in ['A02','A03','P01','P02','P03','P04']:
 dst=a/f'{k}.mp4'
 if not dst.exists():os.link(u/f'即梦生成素材/{k}.mp4',dst)
for k in ['logo.png','mini.png','body.woff2','title.woff2']:
 shutil.copy2(b/f'完整视频工程/assets/{k}',a/k)
# at,duration,source,in,description,title,subtitle,footnote
shots=[
(0,2,'talent17.mov',8,'客餐厅开场','','',''),
(2,3,'talent11.mov',88,'系列片头','家的空气答案','四个问题，选对全屋舒适',''),
(5,5,'talent17.mov',14.6,'第一问','大客餐厅，怎么选？','01  /  空间与送风',''),
(10,3,'talent17.mov',51.2,'真实送风口','看风量，也看距离','',''),
(13,3,'talent15.mp4',54,'送风原理','','舒适，需要覆盖到位','气流效果示意'),
(16,7,'P01.mp4',0,'C2产品','璀璨 C2 艺境','18 m  超远送风','送风距离与内机型号、安装及实际工况有关'),
(23,4,'talent11.mov',88,'第二问','全屋都想装，怎么选？','02  /  多房间与稳定性',''),
(27,5,'A02.mp4',1,'空间剖切','多房间，一起舒适','','空间覆盖概念示意，非安装设计图'),
(32,3,'P02.mp4',0,'C3微距','璀璨 C3 多联机','',''),
(35,2,'talent20.mp4',66,'压缩机','日系压缩机','','技术效果示意'),
(37,2,'talent15.mp4',73.1,'液冷','液冷科技','高温稳定运行','技术效果示意'),
(39,2,'P02.mp4',5,'C3全貌','','稳定，才是舒适的底气',''),
(41,3,'talent11.mov',118,'第三问','家有老人孩子，怎么选？','03  /  全家空气健康',''),
(44,2,'talent11.mov',14,'儿童特写','','把空气质量，放在心上',''),
(46,3,'talent15.mp4',48.2,'健康模块原理','关注空气净化','','健康模块原理示意'),
(49,2,'talent11.mov',16,'亲子呼吸','','甲醛 · 细菌 · 异味',''),
(51,7,'P03.mp4',0,'C3D产品','璀璨 C3D 多联机','Hi-nano Ultra 健康模块','净化效果受环境及使用条件影响'),
(58,2,'talent11.mov',119,'亲子阅读','','舒适，更关乎家人',''),
(60,2,'talent6.mp4',.2,'秋日窗外','关窗怕憋闷，怎么选？','04  /  新风与换气',''),
(62,3,'talent6.mp4',2.4,'关闭窗户','','不开窗，也能换新空气',''),
(65,3,'talent17.mov',66.4,'室内舒适','重点看新风换气','',''),
(68,3,'A03.mp4',2,'过滤微距','','让新鲜空气，经过层层过滤','过滤概念示意，非真实滤芯微观结构'),
(71,2,'P04.mp4',0,'Mini管口细节','璀璨 Mini 新风','',''),
(73,3,'mini',0,'Mini原始产品','350 m³/h','大新风量','产品示意；具体安装及性能以实物和说明书为准'),
(76,2,'A03.mp4',6,'洁净空气','','层层过滤，清新入室','过滤概念示意'),
(78,2,'talent11.mov',88,'生活收束','','让舒适，选得恰到好处',''),
(80,4,'talent17.mov',8,'品牌落版','璀璨中央空调','家的空气答案 · 多空间选型','')]
assert sum(x[1] for x in shots)==84
shared='''@font-face{font-family:Body;src:url(assets/body.woff2)}@font-face{font-family:Title;src:url(assets/title.woff2)}*{box-sizing:border-box}html,body{margin:0;width:720px;height:1280px;overflow:hidden;background:transparent;color:#fff;font-family:Body,"PingFang SC",sans-serif}.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,12,12,.23),transparent 29%,transparent 57%,rgba(10,12,12,.66))}.logo{position:absolute;left:42px;top:47px;width:168px;filter:drop-shadow(0 1px 3px #0007)}.series{position:absolute;right:42px;top:62px;font-size:18px;letter-spacing:3px;color:#f1e4d2}.copy{position:absolute;left:44px;right:38px;bottom:224px;text-shadow:0 2px 10px #0005}.eyebrow{font-size:20px;letter-spacing:4px;color:#ead5b7;margin-bottom:18px}.title{font-family:Title,Body,sans-serif;font-size:46px;line-height:1.3;letter-spacing:1px;font-weight:500}.sub{font-size:24px;line-height:1.6;margin-top:16px;letter-spacing:2px}.line{width:42px;height:2px;background:#dbc29a;margin-bottom:22px;transform-origin:left}.foot{position:absolute;left:44px;bottom:68px;right:42px;font-size:13px;line-height:1.6;color:#eee9df;opacity:.8}.end .copy{bottom:470px;left:40px;right:40px;text-align:center}.end .line{margin:0 auto 28px}.end .title{font-size:52px}.end .sub{font-size:22px}.end .shade{background:rgba(15,19,18,.57)}.hero{background:radial-gradient(ellipse at 55% 30%,#e3ded5,#b8b0a4)}.product{position:absolute;top:230px;left:30px;width:660px;mix-blend-mode:multiply}.hero .title{font-family:Body;font-size:64px;letter-spacing:1px}.hero .shade{background:linear-gradient(0deg,#27251fe6,transparent 47%)}'''
(p/'style.css').write_text(shared)
pages=[];vids=[];manifest=[]
for n,s in enumerate(shots,1):
 at,dur,src,inn,name,title,sub,foot=s; fn=f'shot{n:02}.html';isend=n==27;hero=src=='mini';q=n in [3,7,13,19]
 eye=sub if q else '';sub='' if q else sub
 markup=f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body class="{'end' if isend else 'hero' if hero else ''}">{'<img class="product" src="assets/mini.png">' if hero else ''}<div class="shade"></div><img class="logo" src="assets/logo.png"><div class="series">家的空气答案</div><div class="copy"><div class="line"></div><div class="eyebrow">{eye}</div><div class="title">{title}</div><div class="sub">{sub}</div></div><div class="foot">{foot}</div><script>const cp=document.querySelector('.copy');window.film={{duration:{dur},width:720,height:1280,ready:document.fonts.ready,frame(t){{let f=Math.max(0,Math.min(1,(t-.15)/.7));f=1-Math.pow(1-f,3);cp.style.opacity=f;cp.style.transform='translateY('+((1-f)*22)+'px)';document.querySelector('.line').style.transform='scaleX('+f+')';const im=document.querySelector('.product');if(im)im.style.transform='scale('+(1.015+.035*t/{dur})+')';}}}};</script></body></html>'''
 if not title and not sub:markup=markup.replace('<div class="line"></div>','')
 (p/fn).write_text(markup);pages.append(f'<iframe id="G{n:02}" src="{fn}" at="{at}"></iframe>')
 if not hero:vids.append(f'<video id="V{n:02}" src="assets/{src}#t={inn},{inn+dur}" at="{at}" muted style="object-fit:cover"></video>')
 manifest.append(dict(id=n,at=at,duration=dur,source=src,inPoint=inn,name=name))
film='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=720, height=1280"></head><body><section>'+''.join(pages)+'</section><section>'+''.join(vids)+'</section></body></html>'
(p/'film.html').write_text(film);(u/'剪辑镜头表.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print('84秒，27剪辑片段，已写入OpenFilm')
