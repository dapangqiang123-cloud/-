from pathlib import Path
from PIL import Image, ImageDraw
import json, shutil, html, zipfile
base = Path(__file__).resolve().parent
root = base.parent
records = json.loads((base / '生成记录.json').read_text())
(base / '分镜图').mkdir(exist_ok=True)
(base / '参考图').mkdir(exist_ok=True)
for x in records:
    shutil.copy2(x['source'], base / x['file'])
    with Image.open(base / x['file']) as im:
        x['size'] = list(im.size)
(base / '生成记录.json').write_text(json.dumps(records, ensure_ascii=False, indent=2))
refs = [
('/var/folders/nz/ln59_g0j4jz7dpl9yp1xqz5c0000gn/T/codex-clipboard-954e7a2c-1043-44ca-9a13-ce1f7e106fa6.png','图1_吊顶风口参考.png'),
('/var/folders/nz/ln59_g0j4jz7dpl9yp1xqz5c0000gn/T/codex-clipboard-36c05ab0-3c26-47e5-a48d-0f86613fcdee.png','图2_吊顶风口参考.png')]
for src,dst in refs:
    shutil.copy2(src, base / '参考图' / dst)
intro = """# 第六期 · 无文字风效修正版 V2

2026-10-27，使用内置 image_gen 图像生成工具，逐镜从清晰的初版原图重做。
修正 03、04、06、09、10、12、13 共 7 张。

用户要求：
- 风口统一为璀璨样式的吊顶侧面嵌入长条风口，连续横向格栅，无竖格栅。
- 蓝色风效统一改为淡白色、微带暖橙的流线型透明瀑布风幕。
- 延续无文字分镜要求。
- 保留各镜构图、人物、产品与关键建筑结构。

原有版本保留。本目录提供 7 张修正图，以及整合修正图后的 14 张总览。
第 12 张首轮风口位置不符合要求，已弃用并从清晰原图重新生成。
"""
(base / '生成提示词.md').write_text(intro + '\n\n' + '\n\n'.join('## '+x['id']+' '+x['title']+'\n\n'+x['prompt'] for x in records))
old = json.loads((root / '无文字版' / '生成记录.json').read_text())
fix = {x['id']: x for x in records}
full=[]
for x in old:
    if x['id'] in fix:
        n=fix[x['id']].copy()
        n['revised']=True
    else:
        n=x.copy()
        n['file']='../无文字版/'+x['file']
        n['revised']=False
    full.append(n)
def gallery(items,title,desc,name):
    cards=[]
    for x in items:
        src=html.escape(x['file'],quote=True)
        label=html.escape(x['id']+' · '+x['title'].replace('_',' '))
        badge='风效修正' if x.get('revised',True) else '保留画面'
        cards.append(f'<figure><a href="{src}" target="_blank"><img src="{src}" alt="{label}" loading="lazy"></a><figcaption><strong>{label}</strong><span>{x["time"]} · {badge}</span></figcaption></figure>')
    page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'''+title+'''</title><style>
*{box-sizing:border-box}body{margin:0;background:#171411;color:#eee6db;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif}header{max-width:1500px;margin:auto;padding:42px 24px 24px}h1{font-size:28px;margin:0 0 12px}p{color:#c9bcaa;line-height:1.8}nav{display:flex;gap:20px;flex-wrap:wrap}a{color:#e5c795}main{max-width:1500px;margin:auto;padding:14px 24px 50px;display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}figure{margin:0;background:#27211a;border-radius:12px;overflow:hidden}img{width:100%;display:block;aspect-ratio:9/16;object-fit:contain;background:#171411}figcaption{padding:16px;display:flex;flex-direction:column;gap:9px;font-size:14px}figcaption span{color:#b6a48f;font-size:12px}a:hover{filter:brightness(1.06)}</style><header><h1>'''+title+'</h1><p>'+desc+'''</p><nav><a href="风效修正7张总览.html">本次7张修正图</a><a href="整套14张无文字分镜V2.html">整套14张最新版本</a><a href="风效修正7张PNG.zip">下载7张PNG</a><a href="第六期14张无文字分镜V2.zip">下载整套14张</a></nav></header><main>'''+''.join(cards)+'</main></html>'
    (base / name).write_text(page)
gallery(records,'第六期 · 风效修正 7 张','璀璨吊顶长条风口 · 无竖格栅 · 淡白微暖橙透明瀑布风幕 · 无文字','风效修正7张总览.html')
gallery(full,'第六期 · 14 张无文字分镜 V2','已整合本次 7 张风口与风效修正，点击图片查看原图。','整套14张无文字分镜V2.html')
for name,items in [('风效修正7张PNG.zip',records),('第六期14张无文字分镜V2.zip',full)]:
    with zipfile.ZipFile(base / name, 'w', zipfile.ZIP_DEFLATED) as z:
        for x in items: z.write(base / x['file'],Path(x['file']).name)
out=Image.new('RGB',(7*282,540),'#211c17')
d=ImageDraw.Draw(out)
for i,x in enumerate(records):
    with Image.open(base / x['file']) as im:
        im.thumbnail((270,480))
        out.paste(im,(i*282+6,25))
    d.text((i*282+10,7),x['id'],fill='#e5c795')
out.save(base / '风效修正7张预览.jpg',quality=94)
print(json.dumps({'revised_count':len(records),'full_count':len(full),'sizes':[{'id':x['id'],'size':x['size']} for x in records],'gallery':str(base/'风效修正7张总览.html')},ensure_ascii=False,indent=2))

