from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import html
import json
import textwrap


ROOT = Path("/Users/weipeilong/Desktop/Aaaaaaa/AI工作台/06_codex项目/璀璨codex任务")
BASE_DIR = ROOT / "output/EP01/01_base"
FINAL_DIR = ROOT / "output/EP01/02_final"
CONTACT_DIR = ROOT / "output/EP01/03_contact"

COFFEE = "#3B2F2C"
COFFEE_ALT = "#433538"
GOLD = "#B8952A"
FOG = "#F0EDE8"
MUTED = "#C9BFB6"

ZH_FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
LATIN_FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
LATIN_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size=size)


def centered(draw, xy, text, fnt, fill, stroke_width=0, stroke_fill=None):
    x, y = xy
    box = draw.textbbox((0, 0), text, font=fnt, stroke_width=stroke_width)
    w = box[2] - box[0]
    h = box[3] - box[1]
    draw.text(
        (x - w / 2, y - h / 2 - box[1]),
        text,
        font=fnt,
        fill=fill,
        stroke_width=stroke_width,
        stroke_fill=stroke_fill,
    )


def save_png(image, path):
    image.convert("RGB").save(path, "PNG", optimize=True)


def make_q_card():
    clean = Image.new("RGB", (1080, 1920), COFFEE)
    draw = ImageDraw.Draw(clean)
    draw.rectangle((0, 0, 1080, 8), fill=GOLD)
    draw.line((176, 758, 904, 758), fill=GOLD, width=2)
    draw.rounded_rectangle((326, 1640, 754, 1744), radius=52, outline=GOLD, width=2)

    clean_path = BASE_DIR / "EP01_00_card_Q_layengao_clean.png"
    save_png(clean, clean_path)
    save_png(clean, FINAL_DIR / clean_path.name)

    withtext = clean.copy()
    d = ImageDraw.Draw(withtext)
    d.text((130, 310), "Q", font=font(LATIN_FONT, 200), fill=GOLD)
    centered(d, (540, 864), "装中央空调，", font(ZH_FONT, 96), FOG)
    centered(d, (540, 1018), "层高到底要多少？", font(ZH_FONT, 96), FOG)
    centered(d, (540, 1692), "璀璨 TRÉSOR", font(ZH_FONT, 44), GOLD)
    save_png(withtext, FINAL_DIR / "EP01_00_card_Q_layengao_withtext.png")


def make_190_card():
    clean = Image.new("RGB", (1080, 1920), COFFEE)
    draw = ImageDraw.Draw(clean)
    draw.line((276, 1000, 804, 1000), fill=GOLD, width=2)
    clean_path = BASE_DIR / "EP01_06_card_maidian_190mm_clean.png"
    save_png(clean, clean_path)
    save_png(clean, FINAL_DIR / clean_path.name)

    withtext = clean.copy()
    d = ImageDraw.Draw(withtext)
    centered(d, (540, 884), "薄至 190mm", font(ZH_FONT, 120), GOLD)
    centered(d, (540, 1090), "少占吊顶空间", font(ZH_FONT, 56), FOG)
    save_png(withtext, FINAL_DIR / "EP01_06_card_maidian_190mm_withtext.png")


def make_diagram_withtext():
    clean_path = BASE_DIR / "EP01_03_diagram_biandiao_section_clean.png"
    image = Image.open(clean_path).convert("RGB")
    w, h = image.size
    d = ImageDraw.Draw(image)

    # 局部边吊：标签在左上留白区，引导至右上方局部吊顶。
    label_font = font(ZH_FONT, max(42, round(w * 0.058)))
    small_font = font(ZH_FONT, max(36, round(w * 0.047)))
    d.rounded_rectangle((50, 220, 320, 306), radius=20, fill=COFFEE_ALT)
    centered(d, (185, 263), "局部边吊", label_font, GOLD)
    d.line((320, 264, 500, 790), fill=GOLD, width=3)
    d.ellipse((492, 782, 508, 798), fill=GOLD)

    # 原顶保留：雾白字置于深咖标签底，指向较高的中央原顶。
    d.rounded_rectangle((390, 300, 678, 390), radius=22, fill=COFFEE_ALT)
    centered(d, (534, 345), "原顶保留", label_font, FOG)
    d.line((534, 390, 632, 590), fill=GOLD, width=3)
    d.ellipse((624, 582, 640, 598), fill=GOLD)

    # 右侧层高线。
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

    save_png(image, FINAL_DIR / "EP01_03_diagram_biandiao_section_withtext.png")


def make_ending_withtext():
    clean_path = BASE_DIR / "EP01_07_scene_grand_ending_clean.png"
    image = Image.open(clean_path).convert("RGB")
    w, h = image.size
    d = ImageDraw.Draw(image)
    title_font = font(ZH_FONT, max(62, round(w * 0.078)))
    sub_font = font(ZH_FONT, max(38, round(w * 0.047)))
    centered(d, (w / 2, h * 0.78), "璀璨家的空气答案", title_font, GOLD)
    d.line((w * 0.34, h * 0.815, w * 0.66, h * 0.815), fill=GOLD, width=2)
    centered(d, (w / 2, h * 0.85), "懂空气，也懂家的尺度", sub_font, FOG)
    save_png(image, FINAL_DIR / "EP01_07_scene_grand_ending_withtext.png")


ASSETS = [
    ("EP01_00_card_Q_layengao_clean.png", "Q卡片头 · clean", "双版"),
    ("EP01_00_card_Q_layengao_withtext.png", "Q卡片头 · withtext", "双版"),
    ("EP01_01_scene_livingroom_heightscale_clean.png", "客厅＋层高标尺底图", "风口锁词"),
    ("EP01_02_scene_livingroom_clean.png", "客厅空镜 · 换机位", "风口锁词"),
    ("EP01_03_diagram_biandiao_section_clean.png", "局部边吊剖面 · clean", "双版 / 风口锁词 / 重跑1次"),
    ("EP01_03_diagram_biandiao_section_withtext.png", "局部边吊剖面 · withtext", "双版 / 风口锁词 / 重跑1次"),
    ("EP01_05_scene_finished_open_livingdining_clean.png", "完工客餐厅空镜", "风口锁词"),
    ("EP01_06_card_maidian_190mm_clean.png", "190mm卖点卡 · clean", "双版 / C2艺境"),
    ("EP01_06_card_maidian_190mm_withtext.png", "190mm卖点卡 · withtext", "双版 / C2艺境"),
    ("EP01_07_scene_grand_ending_clean.png", "大宅片尾 · clean", "双版 / 风口锁词"),
    ("EP01_07_scene_grand_ending_withtext.png", "大宅片尾 · withtext", "双版 / 风口锁词"),
]


def make_contact_png():
    width, height = 1920, 1760
    sheet = Image.new("RGB", (width, height), FOG)
    d = ImageDraw.Draw(sheet)
    d.rectangle((0, 0, width, 212), fill=COFFEE)
    d.text((70, 42), "璀璨家的空气答案 · EP01 资产总览", font=font(ZH_FONT, 58), fill=FOG)
    d.text((72, 124), "共11张｜双版：00 / 03 / 06 / 07｜风口锁词：01 / 02 / 03 / 05 / 07｜不合格重跑：镜03 × 1", font=font(ZH_FONT, 30), fill=GOLD)

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
        src = Image.open(FINAL_DIR / filename).convert("RGB")
        thumb = src.copy()
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

    save_png(sheet, CONTACT_DIR / "contact_sheet.png")


def make_contact_html():
    cards = []
    for filename, label, tag in ASSETS:
        cards.append(f'''<article class="card">
          <img src="../02_final/{html.escape(filename)}" alt="{html.escape(label)}">
          <h2>{html.escape(label)}</h2>
          <p class="tag">{html.escape(tag)}</p>
          <code>{html.escape(filename)}</code>
        </article>''')
    page = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>EP01 资产总览</title><style>
*{{box-sizing:border-box}} body{{margin:0;background:{FOG};color:{COFFEE};font-family:-apple-system,BlinkMacSystemFont,"Hiragino Sans GB","Microsoft YaHei",sans-serif}}
header{{padding:28px 4vw 24px;background:{COFFEE};color:{FOG};border-top:6px solid {GOLD}}}
h1{{margin:0 0 9px;font-size:30px}} .summary{{margin:0;color:{GOLD};font-size:15px}}
main{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;padding:22px 3vw 34px}}
.card{{min-width:0;background:#fff;border:1px solid {MUTED};border-radius:15px;padding:13px;text-align:center;box-shadow:0 7px 24px rgba(59,47,44,.08)}}
.card img{{display:block;height:38vh;max-height:390px;min-height:250px;max-width:100%;aspect-ratio:9/16;object-fit:contain;margin:0 auto 10px;background:{COFFEE_ALT};border-radius:8px}}
h2{{font-size:15px;margin:7px 0 5px}} .tag{{font-size:12px;color:{GOLD};margin:0 0 6px}} code{{display:block;color:#756a65;font-size:10px;overflow-wrap:anywhere}}
@media(max-width:1000px){{main{{grid-template-columns:repeat(2,1fr)}}}} @media(max-width:560px){{main{{grid-template-columns:1fr}}}}
</style></head><body><header><h1>璀璨家的空气答案 · EP01 资产总览</h1>
<p class="summary">共11张｜双版：00 / 03 / 06 / 07｜风口锁词：01 / 02 / 03 / 05 / 07｜不合格重跑：镜03 × 1</p></header>
<main>{''.join(cards)}</main></body></html>'''
    (CONTACT_DIR / "contact_sheet.html").write_text(page, encoding="utf-8")


def write_report():
    report = {
        "episode": "EP01",
        "final_png_count": len(ASSETS),
        "double_version_assets": ["EP01_00", "EP01_03", "EP01_06", "EP01_07"],
        "vent_lock_assets": ["EP01_01", "EP01_02", "EP01_03", "EP01_05", "EP01_07"],
        "vent_retries": {"EP01_03": 1},
        "vent_validation": "All accepted images show one continuous narrow slot without grille bars, square louvers, diffuser fins, or segmented modules.",
        "size_policy": "All deliverables are native portrait 9:16 assets. Generated scenes/diagram remain at built-in native portrait resolution; cards are 1080x1920.",
        "text_rule": "withtext files were composited locally from the corresponding clean pixels; no withtext background was independently generated.",
        "font_note": "assets/fonts/title_zh.otf was not supplied; STHeiti Medium was used as the consistent Chinese title fallback.",
        "source_manifest": "/Users/weipeilong/Downloads/assets_manifest.json",
        "files": [name for name, _, _ in ASSETS],
    }
    (CONTACT_DIR / "generation_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    for directory in (BASE_DIR, FINAL_DIR, CONTACT_DIR):
        directory.mkdir(parents=True, exist_ok=True)
    make_q_card()
    make_190_card()
    make_diagram_withtext()
    make_ending_withtext()
    make_contact_png()
    make_contact_html()
    write_report()
