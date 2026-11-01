from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import html
import json


ROOT = Path("/Users/weipeilong/Desktop/Aaaaaaa/AI工作台/06_codex项目/璀璨codex任务")
V2 = ROOT / "output/EP01_grille_v2"
BASE_DIR = V2 / "01_base"
FINAL_DIR = V2 / "02_final"
CONTACT_DIR = V2 / "03_contact"

COFFEE = "#3B2F2C"
COFFEE_ALT = "#433538"
GOLD = "#B8952A"
FOG = "#F0EDE8"
MUTED = "#C9BFB6"
ZH_FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
LATIN_FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"


def font(path, size):
    return ImageFont.truetype(path, size=size)


def centered(draw, xy, text, fnt, fill):
    x, y = xy
    box = draw.textbbox((0, 0), text, font=fnt)
    width = box[2] - box[0]
    height = box[3] - box[1]
    draw.text((x - width / 2, y - height / 2 - box[1]), text, font=fnt, fill=fill)


def save(image, path):
    image.convert("RGB").save(path, "PNG", optimize=True)


def diagram_withtext():
    image = Image.open(BASE_DIR / "EP01_03_diagram_biandiao_section_clean.png").convert("RGB")
    w, h = image.size
    d = ImageDraw.Draw(image)
    label_font = font(ZH_FONT, max(42, round(w * 0.058)))
    small_font = font(ZH_FONT, max(36, round(w * 0.047)))

    d.rounded_rectangle((50, 220, 320, 306), radius=20, fill=COFFEE_ALT)
    centered(d, (185, 263), "局部边吊", label_font, GOLD)
    d.line((320, 264, 500, 790), fill=GOLD, width=3)
    d.ellipse((492, 782, 508, 798), fill=GOLD)

    d.rounded_rectangle((390, 300, 678, 390), radius=22, fill=COFFEE_ALT)
    centered(d, (534, 345), "原顶保留", label_font, FOG)
    d.line((534, 390, 632, 590), fill=GOLD, width=3)
    d.ellipse((624, 582, 640, 598), fill=GOLD)

    x = w - 74
    y1, y2 = 570, 1260
    d.line((x, y1, x, y2), fill=GOLD, width=3)
    d.line((x - 22, y1, x + 22, y1), fill=GOLD, width=3)
    d.line((x - 22, y2, x + 22, y2), fill=GOLD, width=3)
    label = "层高线"
    box = d.textbbox((0, 0), label, font=small_font)
    tw, th = box[2] - box[0], box[3] - box[1]
    tag = Image.new("RGBA", (tw + 32, th + 22), (59, 47, 44, 230))
    td = ImageDraw.Draw(tag)
    td.text((16 - box[0], 11 - box[1]), label, font=small_font, fill=GOLD)
    tag = tag.rotate(90, expand=True, resample=Image.Resampling.BICUBIC)
    image.paste(tag, (x - tag.width - 20, round((y1 + y2 - tag.height) / 2)), tag)
    save(image, FINAL_DIR / "EP01_03_diagram_biandiao_section_withtext.png")


def ending_withtext():
    image = Image.open(BASE_DIR / "EP01_07_scene_grand_ending_clean.png").convert("RGB")
    w, h = image.size
    d = ImageDraw.Draw(image)
    title_font = font(ZH_FONT, max(62, round(w * 0.078)))
    sub_font = font(ZH_FONT, max(38, round(w * 0.047)))
    centered(d, (w / 2, h * 0.78), "璀璨家的空气答案", title_font, GOLD)
    d.line((w * 0.34, h * 0.815, w * 0.66, h * 0.815), fill=GOLD, width=2)
    centered(d, (w / 2, h * 0.85), "懂空气，也懂家的尺度", sub_font, FOG)
    save(image, FINAL_DIR / "EP01_07_scene_grand_ending_withtext.png")


ASSETS = [
    ("EP01_00_card_Q_layengao_clean.png", "Q卡片头 · clean", "沿用 / 双版"),
    ("EP01_00_card_Q_layengao_withtext.png", "Q卡片头 · withtext", "沿用 / 双版"),
    ("EP01_01_scene_livingroom_heightscale_clean.png", "客厅＋层高标尺底图", "格栅修正"),
    ("EP01_02_scene_livingroom_clean.png", "客厅空镜 · 换机位", "格栅修正 / 重跑1次"),
    ("EP01_03_diagram_biandiao_section_clean.png", "局部边吊剖面 · clean", "格栅修正 / 双版"),
    ("EP01_03_diagram_biandiao_section_withtext.png", "局部边吊剖面 · withtext", "新clean叠字"),
    ("EP01_05_scene_finished_open_livingdining_clean.png", "完工客餐厅空镜", "格栅修正"),
    ("EP01_06_card_maidian_190mm_clean.png", "190mm卖点卡 · clean", "沿用 / 双版"),
    ("EP01_06_card_maidian_190mm_withtext.png", "190mm卖点卡 · withtext", "沿用 / 双版"),
    ("EP01_07_scene_grand_ending_clean.png", "大宅片尾 · clean", "格栅修正 / 双版"),
    ("EP01_07_scene_grand_ending_withtext.png", "大宅片尾 · withtext", "新clean叠字"),
]


def contact_png():
    width, height = 1920, 1760
    sheet = Image.new("RGB", (width, height), FOG)
    d = ImageDraw.Draw(sheet)
    d.rectangle((0, 0, width, 212), fill=COFFEE)
    d.text((70, 40), "璀璨家的空气答案 · EP01 格栅风口修正版", font=font(ZH_FONT, 54), fill=FOG)
    d.text((72, 122), "共11张｜修正：01 / 02 / 03 / 05 / 07｜横向细百叶｜无单黑缝｜原版另存未覆盖", font=font(ZH_FONT, 28), fill=GOLD)

    cols = 4
    tile_w, tile_h = 430, 478
    start_x, start_y = 55, 246
    gap_x, gap_y = 33, 28
    thumb_w, thumb_h = 204, 363
    title_f = font(ZH_FONT, 24)
    meta_f = font(ZH_FONT, 19)

    for i, (filename, label, tag) in enumerate(ASSETS):
        row, col = divmod(i, cols)
        x = start_x + col * (tile_w + gap_x)
        y = start_y + row * (tile_h + gap_y)
        d.rounded_rectangle((x, y, x + tile_w, y + tile_h), radius=22, fill="#FFFFFF", outline=MUTED, width=2)
        source = Image.open(FINAL_DIR / filename).convert("RGB")
        thumb = source.copy()
        thumb.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        tx = x + (tile_w - thumb.width) // 2
        ty = y + 18
        d.rounded_rectangle((tx - 4, ty - 4, tx + thumb.width + 4, ty + thumb.height + 4), radius=8, fill=COFFEE_ALT)
        sheet.paste(thumb, (tx, ty))
        centered(d, (x + tile_w / 2, y + 400), label, title_f, COFFEE)
        centered(d, (x + tile_w / 2, y + 438), tag, meta_f, GOLD)
        short = filename.replace("EP01_", "")
        if len(short) > 44:
            short = short[:41] + "…"
        centered(d, (x + tile_w / 2, y + 464), short, font(LATIN_FONT, 13), "#756A65")
    save(sheet, CONTACT_DIR / "contact_sheet_grille_v2.png")


def contact_html():
    cards = []
    for filename, label, tag in ASSETS:
        cards.append(f'''<article class="card"><img src="../02_final/{html.escape(filename)}" alt="{html.escape(label)}">
<h2>{html.escape(label)}</h2><p>{html.escape(tag)}</p><code>{html.escape(filename)}</code></article>''')
    page = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>EP01 格栅风口修正版</title><style>*{{box-sizing:border-box}}body{{margin:0;background:{FOG};color:{COFFEE};font-family:-apple-system,BlinkMacSystemFont,"Hiragino Sans GB",sans-serif}}header{{padding:28px 4vw 24px;background:{COFFEE};color:{FOG};border-top:6px solid {GOLD}}}h1{{margin:0 0 9px;font-size:30px}}header p{{color:{GOLD};margin:0}}main{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;padding:22px 3vw 34px}}.card{{background:#fff;border:1px solid {MUTED};border-radius:15px;padding:13px;text-align:center}}img{{height:38vh;max-height:390px;min-height:250px;max-width:100%;aspect-ratio:9/16;object-fit:contain;background:{COFFEE_ALT};border-radius:8px}}h2{{font-size:15px;margin:7px 0 5px}}.card p{{font-size:12px;color:{GOLD};margin:0 0 6px}}code{{display:block;color:#756a65;font-size:10px;overflow-wrap:anywhere}}@media(max-width:1000px){{main{{grid-template-columns:repeat(2,1fr)}}}}@media(max-width:560px){{main{{grid-template-columns:1fr}}}}</style></head>
<body><header><h1>璀璨家的空气答案 · EP01 格栅风口修正版</h1><p>共11张｜修正：01 / 02 / 03 / 05 / 07｜横向细百叶｜无单黑缝｜原版另存未覆盖</p></header><main>{''.join(cards)}</main></body></html>'''
    (CONTACT_DIR / "contact_sheet_grille_v2.html").write_text(page, encoding="utf-8")


def report():
    data = {
        "version": "EP01_grille_v2",
        "final_png_count": 11,
        "modified_assets": ["EP01_01", "EP01_02", "EP01_03", "EP01_05", "EP01_07"],
        "vent_spec": "吊顶内嵌横向长条格栅风口；细长矩形；内部均匀横向细百叶；无单黑线；无竖向格栅；无方形百叶。",
        "reference_policy": {
            "vent_images": "前4张只参考风口构造。",
            "decor_images": "第5至10张只提取暖白、木色、自然光、中古松弛感，不复制具体户型、家具组合或陈设。",
        },
        "retries": {
            "EP01_02": "首轮过疏，重跑1次后通过。",
            "EP01_07": "3次模型编辑仍过疏；最终仅在既有风口窄带内进行确定性9叶片局部绘制。",
        },
        "text_rule": "EP01_03与EP01_07的withtext均从修正后的clean重新叠字；未独立生成背景。",
        "original_preserved": "/output/EP01/ 保留未覆盖。",
        "files": [name for name, _, _ in ASSETS],
    }
    (CONTACT_DIR / "revision_report.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    for directory in (BASE_DIR, FINAL_DIR, CONTACT_DIR):
        directory.mkdir(parents=True, exist_ok=True)
    diagram_withtext()
    ending_withtext()
    contact_png()
    contact_html()
    report()
