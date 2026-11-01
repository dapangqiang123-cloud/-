import asyncio, json, os, sys
from pathlib import Path
sys.path.insert(0,'/private/tmp/tresor-video-tts')
import edge_tts
ROOT=Path(__file__).parent
rows=json.loads((ROOT/'script.json').read_text())
out=ROOT/'audio_words'
out.mkdir(exist_ok=True)
async def main():
    for row in rows:
        target=out/(row['id']+'.mp3')
        if target.exists() and target.stat().st_size>1000:
            continue
        proxy=os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
        c=edge_tts.Communicate(row['voice'], 'zh-CN-XiaoxiaoNeural',rate='+0%',pitch='-2Hz',boundary='WordBoundary',proxy=proxy)
        subs=edge_tts.SubMaker()
        words=[]
        with target.open('wb') as f:
            async for chunk in c.stream():
                if chunk['type']=='audio': f.write(chunk['data'])
                elif chunk['type']=='WordBoundary':
                    subs.feed(chunk)
                    words.append(chunk)
        (out/(row['id']+'.srt')).write_text(subs.get_srt())
        (out/(row['id']+'.json')).write_text(json.dumps(words,ensure_ascii=False,indent=2))
        print(row['id'],'done',flush=True)
asyncio.run(main())
