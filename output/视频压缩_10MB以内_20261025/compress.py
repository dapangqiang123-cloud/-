from pathlib import Path
import concurrent.futures
import json
import subprocess
import time

ROOT = Path(__file__).resolve().parent
SOURCE = Path('/Users/weipeilong/Desktop/璀璨中央空调/璀璨日常整理留存/10月/视频')
FILES = ['家的空气答案2 省电篇.mp4', '家的空气答案3 选多联机单元机.mp4', '家的空气答案50m²篇4.mp4']

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(path)]))

def run(args, log):
    with log.open('ab') as handle:
        subprocess.run(args, stdout=handle, stderr=handle, check=True)

def compress(item):
    i, name = item
    start = time.monotonic()
    src = SOURCE / name
    info = probe(src)
    duration = float(info['format']['duration'])
    bitrate = int((9_550_000 * 8 / duration - 96_000 - 12_000) / 1000) * 1000
    out = ROOT / (src.stem + '_10MB以内.mp4')
    temp = ROOT / (src.stem + '_处理中.mp4')
    if out.exists():
        raise RuntimeError(f'Output already exists: {out}')
    log = ROOT / f'encode_{i}.log'
    passlog = ROOT / f'pass_{i}'
    basic = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-nostdin', '-y', '-i', str(src)]
    video = ['-vf', 'fps=30,scale=720:-2:flags=lanczos', '-c:v', 'libx264', '-preset', 'slow', '-b:v', str(bitrate), '-pix_fmt', 'yuv420p', '-threads', '4', '-passlogfile', str(passlog)]
    print(f'START {i}: {name}, {duration:.2f}s, video {bitrate//1000} kbps', flush=True)
    run(basic + ['-map', '0:v:0'] + video + ['-pass', '1', '-an', '-f', 'null', '/dev/null'], log)
    print(f'PASS1 {i}: complete', flush=True)
    run(basic + ['-map', '0:v:0', '-map', '0:a:0?'] + video + ['-pass', '2', '-c:a', 'aac', '-b:a', '96000', '-movflags', '+faststart', '-map_metadata', '-1', str(temp)], log)
    result = probe(temp)
    size = temp.stat().st_size
    assert size < 10_000_000, (name, size)
    assert abs(float(result['format']['duration']) - duration) < 0.15
    assert any(s['codec_type'] == 'audio' for s in result['streams'])
    run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-xerror', '-nostdin', '-i', str(temp), '-f', 'null', '/dev/null'], log)
    temp.rename(out)
    v = next(s for s in result['streams'] if s['codec_type'] == 'video')
    record = {'source': str(src), 'output': str(out), 'source_bytes': src.stat().st_size, 'output_bytes': size, 'size_MB': round(size / 1_000_000, 3), 'duration': result['format']['duration'], 'width': v['width'], 'height': v['height'], 'fps': v['avg_frame_rate'], 'video_codec': v['codec_name'], 'audio_codec': next(s['codec_name'] for s in result['streams'] if s['codec_type'] == 'audio'), 'full_decode_check': 'passed', 'elapsed_seconds': round(time.monotonic() - start, 1)}
    print(f'DONE {i}: {size / 1_000_000:.3f} MB, {record["elapsed_seconds"]}s', flush=True)
    return record

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(compress, enumerate(FILES, 1)))
(ROOT / '压缩核验.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
print('ALL_DONE', flush=True)
