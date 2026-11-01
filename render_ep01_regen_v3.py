from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import html
import json


ROOT = Path("/Users/weipeilong/Desktop/Aaaaaaa/AI工作台/06_codex项目/璀璨codex任务")
V3 = ROOT / "output/EP01_regen_v3"
BASE_DIR = V3 / "01_base"
FINAL_DIR = V3 / "02_final"
CONTACT_DIR = V3 / "03_contact"

COFFEE = "#3B2F2C"
GOLD = "#B8952A"
FOG = "#F0EDE8"
MUTED = "#C9BFB6"
ZH_FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
LATIN_FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"


def font(path, size):
    return ImageFont.truetype(path, size=size)


def centered(draw, xy, text, fnt, fill, stroke_width=0, stroke_fill=None):
    x, y = xy
    box = draw.textbbox((0, 0), text, font=fnt, stroke_width=stroke_width)
    width = box[2] - box[0]
    height = box[3] - box[1]
    draw.text(
        (x - width / 2, y - height / 2 - box[1]),
        text,
        font=fnt,
        fill=fill,
        stroke_width=stroke_width,
        stroke_fill=stroke_fill,
    )


def save(image, path):
    image.convert("RGB").save(path, "PNG", optimize=True)


def ending_withtext():
    """Create withtext strictly from the accepted v3 clean base."""
    source = BASE_DIR / "EP01_07_scene_grand_ending_clean.png"
    target = FINAL_DIR / "EP01_07_scene_grand_ending_withtext.png"
    image = Image.open(source).convert("RGB")
    w, h = image.size
    draw = ImageDraw.Draw(image)
    title_font = font(ZH_FONT, max(58, round(w * 0.073)))
    sub_font = font(ZH_FONT, max(34, round(w * 0.043)))
    shadow = "#241B18"
    centered(draw, (w / 2, h * 0.785), "璀璨家的空气答案", title_font, GOLD, 2, shadow)
    draw.line((w * 0.34, h * 0.822, w * 0.66, h * 0.822), fill=GOLD, width=max(2, round(w * 0.002)))
    centered(draw, (w / 2, h * 0.855), "懂空气，也懂家的尺度", sub_font, FOG, 2, shadow)
    save(image, target)


ASSETS = [
    ("EP01_00_card_Q_layengao_clean.png", "Q卡片头 · clean", "沿用 / 双版"),
    ("EP01_00_card_Q_layengao_withtext.png", "Q卡片头 · withtext", "沿用 / 双版"),
    ("EP01_01_scene_livingroom_heightscale_clean.png", "镜01 客厅层高底图", "全新生成 / 风口锁定"),
    ("EP01_02_scene_livingroom_clean.png", "镜02 客餐厅空镜", "全新生成 / 风口锁定"),
    ("EP01_03_diagram_biandiao_section_clean.png", "镜03 局部边吊 · clean", "沿用 / 双版"),
    ("EP01_03_diagram_biandiao_section_withtext.png", "镜03 局部边吊 · withtext", "同底叠字"),
    ("EP01_05_scene_finished_open_livingdining_clean.png", "镜05 完工客餐厅", "全新生成 / 风口锁定"),
    ("EP01_06_card_maidian_190mm_clean.png", "镜06 190mm卡 · clean", "沿用 / 双版"),
    ("EP01_06_card_maidian_190mm_withtext.png", "镜06 190mm卡 · withtext", "沿用 / 双版"),
    ("EP01_07_scene_grand_ending_clean.png", "镜07 片尾空间 · clean", "全新生成 / 风口锁定 / 双版"),
    ("EP01_07_scene_grand_ending_withtext.png", "镜07 片尾空间 · withtext", "同一v3底图叠字"),
]


def contact_png():
    width, height = 1920, 1760
    sheet = Image.new("RGB", (width, height), FOG)
    draw = ImageDraw.Draw(sheet)
    draw.rectangle((0, 0, width, 212), fill=COFFEE)
    draw.text((70, 38), "璀璨家的空气答案 · EP01 家居全量重生 v3", font=font(ZH_FONT, 52), fill=FOG)
    draw.text(
        (72, 121),
        "共11张｜家居重生：01 / 02 / 05 / 07｜风口：吊顶立面横长条＋纯横向细百叶｜片尾双版同底",
        font=font(ZH_FONT, 27),
        fill=GOLD,
    )

    cols = 4
    tile_w, tile_h = 430, 478
    start_x, start_y = 55, 246
    gap_x, gap_y = 33, 28
    thumb_w, thumb_h = 204, 363
    title_f = font(ZH_FONT, 23)
    meta_f = font(ZH_FONT, 18)

    for i, (filename, label, tag) in enumerate(ASSETS):
        row, col = divmod(i, cols)
        x = start_x + col * (tile_w + gap_x)
        y = start_y + row * (tile_h + gap_y)
        draw.rounded_rectangle((x, y, x + tile_w, y + tile_h), radius=22, fill="#FFFFFF", outline=MUTED, width=2)
        source = Image.open(FINAL_DIR / filename).convert("RGB")
        thumb = source.copy()
        thumb.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        tx = x + (tile_w - thumb.width) // 2
        ty = y + 18
        draw.rounded_rectangle((tx - 4, ty - 4, tx + thumb.width + 4, ty + thumb.height + 4), radius=8, fill=COFFEE)
        sheet.paste(thumb, (tx, ty))
        centered(draw, (x + tile_w / 2, y + 400), label, title_f, COFFEE)
        centered(draw, (x + tile_w / 2, y + 438), tag, meta_f, GOLD)
        short = filename.replace("EP01_", "")
        if len(short) > 44:
            short = short[:41] + "…"
        centered(draw, (x + tile_w / 2, y + 464), short, font(LATIN_FONT, 13), "#756A65")
    save(sheet, CONTACT_DIR / "contact_sheet_regen_v3.png")


def contact_html():
    cards = []
    for filename, label, tag in ASSETS:
        cards.append(
            f'''<article class="card"><img src="../02_final/{html.escape(filename)}" alt="{html.escape(label)}">
<h2>{html.escape(label)}</h2><p>{html.escape(tag)}</p><code>{html.escape(filename)}</code></article>'''
        )
    page = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>EP01 家居全量重生 v3</title><style>*{{box-sizing:border-box}}body{{margin:0;background:{FOG};color:{COFFEE};font-family:-apple-system,BlinkMacSystemFont,"Hiragino Sans GB",sans-serif}}header{{padding:28px 4vw 24px;background:{COFFEE};color:{FOG};border-top:6px solid {GOLD}}}h1{{margin:0 0 9px;font-size:30px}}header p{{color:{GOLD};margin:0}}main{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;padding:22px 3vw 34px}}.card{{background:#fff;border:1px solid {MUTED};border-radius:15px;padding:13px;text-align:center}}img{{height:38vh;max-height:390px;min-height:250px;max-width:100%;aspect-ratio:9/16;object-fit:contain;background:{COFFEE};border-radius:8px}}h2{{font-size:15px;margin:7px 0 5px}}.card p{{font-size:12px;color:{GOLD};margin:0 0 6px}}code{{display:block;color:#756a65;font-size:10px;overflow-wrap:anywhere}}@media(max-width:1000px){{main{{grid-template-columns:repeat(2,1fr)}}}}@media(max-width:560px){{main{{grid-template-columns:1fr}}}}</style></head>
<body><header><h1>璀璨家的空气答案 · EP01 家居全量重生 v3</h1><p>共11张｜01 / 02 / 05 / 07全新生成｜风口位于吊顶竖向立面，内部仅横向细百叶｜不复制参考户型与家具组合</p></header><main>{''.join(cards)}</main></body></html>'''
    (CONTACT_DIR / "contact_sheet_regen_v3.html").write_text(page, encoding="utf-8")


def report():
    data = {
        "version": "EP01_regen_v3",
        "final_png_count": len(ASSETS),
        "regenerated_home_assets": ["EP01_01", "EP01_02", "EP01_05", "EP01_07"],
        "vent_spec": "靠墙局部吊顶的竖向立面；横向细长矩形；内部仅沿长边贯通的均匀细密横百叶；无竖格、方格、单黑缝。",
        "style_direction": "参考暖白矿物墙面、暖木、中古现代混搭、人字拼地板、自然侧光和真实居住感；所有户型与家具组合重新设计。",
        "vent_qc": {
            "EP01_01": "通过；单风口，吊顶立面，横向细百叶。",
            "EP01_02": "通过；单风口，吊顶立面，横向细百叶。",
            "EP01_05": "通过；单风口，吊顶立面，横向细百叶。",
            "EP01_07": "首轮出现疑似第二风口，未收录；重跑1次后通过。",
        },
        "text_rule": "EP01_07 withtext由本轮接受的clean底图直接叠字，背景像素未独立生成。",
        "older_versions_preserved": ["output/EP01", "output/EP01_grille_v2"],
        "files": [name for name, _, _ in ASSETS],
    }
    (CONTACT_DIR / "revision_report_regen_v3.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    for directory in (BASE_DIR, FINAL_DIR, CONTACT_DIR):
        directory.mkdir(parents=True, exist_ok=True)
    ending_withtext()
    contact_png()
    contact_html()
    report()
