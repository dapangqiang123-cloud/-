from pathlib import Path
import json, shutil, html, zipfile
from PIL import Image

root=Path(__file__).parent
records=json.loads((root/'生成记录.json').read_text())
if not records:
    raise SystemExit('暂无已完成批次，等待生成后再整理。')
cards=[]
for r in records:
    dest=root/'分镜图'/f"{r['id']}_{r['title']}_无字.png"
    shutil.copy2(r['source'],dest)
    with Image.open(dest) as im: im.verify()
    with Image.open(dest) as im: r['size']=list(im.size)
    r['file']=str(dest.relative_to(root))
    cards.append(f'''<article><a href="{html.escape(r['file'])}" target="_blank"><img src="{html.escape(r['file'])}" alt="分镜{r['id']}"></a><div><span>{r['id']} · {html.escape(r['time'])}</span><h2>{html.escape(r['title'])}</h2></div></article>''')
(root/'无文字分镜总览.html').write_text('''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>第六期 · 无文字分镜图</title><style>*{box-sizing:border-box}body{margin:0;background:#eeeae2;color:#332c26;font:15px -apple-system,"PingFang SC",sans-serif}header{padding:36px 4vw}h1{font-size:30px;margin:10px 0}header p{color:#766a5f}main{padding:0 4vw 44px;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:22px}article{background:#faf8f3;overflow:hidden;border-radius:4px}article div{padding:16px}img{display:block;width:100%;height:auto}span{font-size:12px;color:#8b7865}h2{font-size:16px;margin:7px 0}a{color:inherit}@media(max-width:1000px){main{grid-template-columns:repeat(3,1fr)}}@media(max-width:700px){main{grid-template-columns:repeat(2,1fr)}}@media(max-width:440px){main{grid-template-columns:1fr}}</style><header><p>家的空气答案 / 第六期</p><h1>多空间选型 · 无文字版</h1><p>14张独立原图 · 保留气流与空间示意 · 点击查看原图</p></header><main>'''+''.join(cards)+'</main></html>',encoding='utf-8')
(root/'生成记录.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'生成提示词.md').write_text('# 无文字版本\n\n工具：内置 image_gen。以第一版清晰分镜图为编辑目标，逐张删除文字。\n\n'+'\n\n'.join(dict.fromkeys(r['prompt'] for r in records)),encoding='utf-8')
if len(records)==14:
    with zipfile.ZipFile(root/'第六期_14张无文字分镜图.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted((root/'分镜图').glob('*.png')): z.write(p,p.relative_to(root))
        z.write(root/'无文字分镜总览.html','无文字分镜总览.html')
        z.write(root/'生成提示词.md','生成提示词.md')
print('已保存',len(records),'张；尺寸',sorted({tuple(r['size']) for r in records}))
