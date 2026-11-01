"""只读取源目录的文件名、路径与 stat 元数据；不复制、修改或解码素材。"""
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import csv
import os

PROJECT = Path(__file__).resolve().parents[1]
BASE = Path('/Users/weipeilong/Desktop/璀璨中央空调/资料&客户提供/视频:达人素材')
ROOTS = {
    '达人视频': BASE / '达人视频家居图素材/达人视频素材参考',
    '达人家居图': BASE / '达人视频家居图素材/达人家居美图素材参考',
    '产品视频': BASE / '产品视频',
    '日常产品素材': BASE / 'ai产品视频',
}
OUT = PROJECT / 'memory/projects'
IMAGES = {'.jpg', '.jpeg', '.png', '.heic', '.webp', '.tif', '.tiff'}
VIDEOS = {'.mp4', '.mov', '.m4v', '.avi', '.mkv'}


def scan():
    rows, errors, skipped = [], [], Counter()
    for category, root in ROOTS.items():
        if not root.is_dir():
            errors.append(f'目录不存在或不可访问：{root}')
            continue
        for folder, dirs, files in os.walk(root, followlinks=False, onerror=lambda e: errors.append(str(e))):
            skipped[category] += sum(d.startswith('.') for d in dirs)
            dirs[:] = sorted(d for d in dirs if not d.startswith('.'))
            for name in sorted(files):
                if name.startswith('.'):
                    skipped[category] += 1
                    continue
                path = Path(folder) / name
                rel = path.relative_to(root)
                try:
                    stat = path.stat()
                except OSError as error:
                    errors.append(f'{path}: {error}')
                    continue
                ext = path.suffix.lower()
                kind = '图片' if ext in IMAGES else '视频' if ext in VIDEOS else '文档/其他'
                status = '待使用时检查内容'
                priority = '按任务选用'
                if category == '产品视频':
                    priority = '优先：产品宣传/片段；具体内容使用前核对'
                    if '口播小视频-成片' in rel.parts:
                        priority = '低：口播成片不重要'
                    elif '安装视频-成片' in rel.parts or '操作视频' in name or '安装视频' in name:
                        priority = '按需：安装/操作'
                elif category == '日常产品素材':
                    priority = '低：日常整理补充'
                if ext in {'.downloading', '.part', '.crdownload'}:
                    kind, status, priority = '未完成下载', '不可作为可用素材', '排除'
                elif stat.st_size == 0:
                    status, priority = '空文件', '排除'
                if '草稿素材，非指定不使用' in rel.parts:
                    priority = '目录标注：非指定不使用'
                if '网络素材仅供璀璨风格参考' in rel.parts:
                    priority = '目录标注：仅风格参考'
                rows.append(dict(类别=category, 分组=rel.parts[0] if len(rel.parts) > 1 else '根目录', 类型=kind,
                                 调用优先级=priority, 状态=status, 文件名=name, 相对路径=str(rel),
                                 绝对路径=str(path), 字节数=stat.st_size,
                                 修改时间UTC=datetime.fromtimestamp(stat.st_mtime, ZoneInfo('UTC')).isoformat()))
    # 扫描失败时保留之前的有效索引，避免把读取失败误记为文件删除。
    if errors:
        raise SystemExit('\n'.join(errors))
    rows.sort(key=lambda r: (r['类别'], r['相对路径']))
    OUT.mkdir(parents=True, exist_ok=True)
    csv_path = OUT / 'tresor-assets-files.csv'
    fields = ['类别', '分组', '类型', '调用优先级', '状态', '文件名', '相对路径', '绝对路径', '字节数', '修改时间UTC']
    with csv_path.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    stamp = datetime.now(ZoneInfo('America/New_York')).isoformat(timespec='seconds')
    lines = ['# 璀璨素材目录扫描快照', '', f'扫描时间：{stamp}（America/New_York）', '',
             '本快照只核对文件路径、名称、类型、大小和修改时间；未逐张审图或逐条看片，不代表内容、清晰度或完整性审核通过。隐藏文件/目录未纳入，未复制素材。', '',
             '| 类别 | 文件数 | 类型数量 | 总大小 GiB |', '| --- | ---: | --- | ---: |']
    for category in ROOTS:
        subset = [r for r in rows if r['类别'] == category]
        kinds = Counter(r['类型'] for r in subset)
        lines.append(f"| {category} | {len(subset)} | {'、'.join(f'{k} {v}' for k, v in sorted(kinds.items()))} | {sum(r['字节数'] for r in subset)/1024**3:.2f} |")
    lines += ['', f'合计：{len(rows)} 个非隐藏文件。路径与文件名以同目录 `tresor-assets-files.csv` 为准。', '', '## 分组', '']
    for category in ROOTS:
        lines += [f'### {category}', '', f'源目录：`{ROOTS[category]}`', '', '| 分组 | 文件数 |', '| --- | ---: |']
        groups = Counter(r['分组'] for r in rows if r['类别'] == category)
        lines += [f'| {group} | {count} |' for group, count in sorted(groups.items())]
        if category in {'达人视频', '产品视频'}:
            lines += ['', '根目录文件：', '']
            lines += [f"- `{r['文件名']}`" for r in rows if r['类别'] == category and r['分组'] == '根目录']
        lines += ['']
    lines += ['## 未完成下载或空文件', '']
    flagged = [r for r in rows if r['状态'] in {'不可作为可用素材', '空文件'}]
    lines += [f"- {r['状态']}：`{r['绝对路径']}`" for r in flagged] or ['无。']
    (OUT / 'tresor-assets-snapshot.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'已索引 {len(rows)} 个文件；异常读取 0；未完成下载/空文件 {len(flagged)}；未复制素材。')


if __name__ == '__main__':
    scan()
