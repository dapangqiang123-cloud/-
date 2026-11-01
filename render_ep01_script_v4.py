from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import json
import math


ROOT = Path("/Users/weipeilong/Desktop/Aaaaaaa/AI工作台/06_codex项目/璀璨codex任务")
V4 = ROOT / "output/EP01_script_v4"
GEN = V4 / "01_generated"
FINAL = V4 / "02_final"
PREVIEW = V4 / "03_preview"

COFFEE = "#3B2F2C"
COFFEE_RGBA = (59, 47, 44, 226)
GOLD = "#B8952A"
GOLD_RGBA = (184, 149, 42, 235)
FOG = "#F0EDE8"
FOG_RGBA = (240, 237, 232, 245)
MUTED = "#C9BFB6"
RED = "#B54A3A"
ZH_FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
ZH_LIGHT = "/System/Library/Fonts/STHeiti Light.ttc"
LATIN_FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"


def font(path, size):
    return ImageFont.truetype(path, size=max(12, int(size)))


def save(image, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(path, "PNG", optimize=True)


def text_bbox(draw, text, fnt, stroke_width=0):
    b = draw.textbbox((0, 0), text, font=fnt, stroke_width=stroke_width)
    return b, b[2] - b[0], b[3] - b[1]


def centered(draw, xy, text, fnt, fill, stroke_width=0, stroke_fill=None):
    b, tw, th = text_bbox(draw, text, fnt, stroke_width)
    draw.text(
        (xy[0] - tw / 2 - b[0], xy[1] - th / 2 - b[1]),
        text,
        font=fnt,
        fill=fill,
        stroke_width=stroke_width,
        stroke_fill=stroke_fill,
    )


def rounded_label(image, center, lines, width_ratio=0.82, y_pad=24, fill=COFFEE_RGBA, title_gold=False):
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = image.size
    title_f = font(ZH_FONT, w * 0.054)
    line_f = font(ZH_LIGHT, w * 0.041)
    fonts = [title_f] + [line_f] * (len(lines) - 1)
    heights = []
    for line, fnt in zip(lines, fonts):
        _, _, th = text_bbox(draw, line, fnt, 1)
        heights.append(th)
    box_w = int(w * width_ratio)
    box_h = sum(heights) + y_pad * 2 + int(w * 0.025) * (len(lines) - 1)
    x1 = int(center[0] - box_w / 2)
    y1 = int(center[1] - box_h / 2)
    x2, y2 = x1 + box_w, y1 + box_h
    draw.rounded_rectangle((x1, y1, x2, y2), radius=int(w * 0.025), fill=fill, outline=GOLD_RGBA, width=max(2, int(w * 0.0025)))
    y = y1 + y_pad
    for i, (line, fnt, th) in enumerate(zip(lines, fonts, heights)):
        color = GOLD if title_gold and i == 0 else FOG
        centered(draw, (w / 2, y + th / 2), line, fnt, color, 1, "#261C19")
        y += th + int(w * 0.025)
    return Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")


def shot01():
    source = GEN / "EP01_01_scene_height_pain_clean.png"
    image = Image.open(source).convert("RGB")
    w, h = image.size
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    x = int(w * 0.12)
    y_top, y_bottom = int(h * 0.18), int(h * 0.89)
    d.line((x, y_top, x, y_bottom), fill=GOLD_RGBA, width=max(4, int(w * 0.005)))
    for yy in (y_top, int(y_top + (y_bottom - y_top) * 0.46), y_bottom):
        d.line((x - int(w * 0.026), yy, x + int(w * 0.026), yy), fill=GOLD_RGBA, width=max(3, int(w * 0.004)))
    pill_f = font(LATIN_FONT, w * 0.045)
    for yy, txt in ((int(y_top + (y_bottom - y_top) * 0.12), "2.7m"), (int(y_top + (y_bottom - y_top) * 0.56), "2.6m")):
        b, tw, th = text_bbox(d, txt, pill_f)
        px = x + int(w * 0.035)
        d.rounded_rectangle((px, yy - th, px + tw + 26, yy + 14), radius=14, fill=COFFEE_RGBA, outline=GOLD_RGBA, width=2)
        d.text((px + 13 - b[0], yy - th - b[1] + 6), txt, font=pill_f, fill=GOLD)
    image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    image = rounded_label(image, (w / 2, h * 0.91), ["装中央空调，", "层高多少够用？"], width_ratio=0.72, title_gold=True)
    save(image, FINAL / "EP01_01_scene_height_pain_withtext.png")


def shot02():
    source = GEN / "EP01_02_compare_270_260_clean.png"
    image = Image.open(source).convert("RGB")
    w, h = image.size
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    head_f = font(ZH_FONT, w * 0.041)
    sub_f = font(ZH_LIGHT, w * 0.028)
    for cx, title, sub, accent in (
        (w * 0.25, "2.7m+", "安装更从容", GOLD),
        (w * 0.75, "2.6–2.7m", "机器选型很关键", FOG),
    ):
        bw = int(w * 0.43)
        d.rounded_rectangle((cx - bw / 2, h * 0.045, cx + bw / 2, h * 0.142), radius=int(w * 0.02), fill=COFFEE_RGBA, outline=GOLD_RGBA, width=2)
        centered(d, (cx, h * 0.079), title, head_f, accent, 1, "#251B18")
        centered(d, (cx, h * 0.12), sub, sub_f, FOG, 1, "#251B18")
    final = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    save(final, FINAL / "EP01_02_compare_270_260_withtext.png")


def shot03():
    source = GEN / "EP01_03_diagram_thick_unit_clean.png"
    image = Image.open(source).convert("RGB")
    w, h = image.size
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    title_f = font(ZH_FONT, w * 0.052)
    label_f = font(ZH_FONT, w * 0.036)
    small_f = font(ZH_LIGHT, w * 0.030)
    d.rounded_rectangle((w * 0.08, h * 0.045, w * 0.92, h * 0.13), radius=int(w * 0.025), fill=COFFEE_RGBA, outline=GOLD_RGBA, width=2)
    centered(d, (w * 0.5, h * 0.087), "普通机型：占用 20–30cm 层高", title_f, FOG, 1, "#251B18")
    labels = [
        (w * 0.18, h * 0.245, "普通厚内机", w * 0.35, h * 0.35),
        (w * 0.20, h * 0.335, "管线空间", w * 0.64, h * 0.305),
        (w * 0.19, h * 0.455, "局部边吊", w * 0.34, h * 0.445),
    ]
    for lx, ly, txt, tx, ty in labels:
        b, tw, th = text_bbox(d, txt, label_f)
        d.rounded_rectangle((lx - 12, ly - th / 2 - 9, lx + tw + 20, ly + th / 2 + 9), radius=12, fill=COFFEE_RGBA)
        d.text((lx - b[0], ly - th / 2 - b[1]), txt, font=label_f, fill=GOLD)
        d.line((lx + tw + 24, ly, tx, ty), fill=GOLD_RGBA, width=3)
        d.ellipse((tx - 6, ty - 6, tx + 6, ty + 6), fill=GOLD_RGBA)
    centered(d, (w * 0.5, h * 0.945), "璀璨内机侧面特写：请替换真实宣传片", small_f, FOG, 1, "#251B18")
    final = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    save(final, FINAL / "EP01_03_diagram_thick_unit_withtext.png")


def shot04():
    source = GEN / "EP01_04_scene_190mm_finish_clean.png"
    image = Image.open(source).convert("RGB")
    w, h = image.size
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rounded_rectangle((w * 0.055, h * 0.64, w * 0.56, h * 0.86), radius=int(w * 0.03), fill=COFFEE_RGBA, outline=GOLD_RGBA, width=3)
    brand_f = font(ZH_LIGHT, w * 0.032)
    number_f = font(LATIN_FONT, w * 0.126)
    unit_f = font(LATIN_FONT, w * 0.045)
    sub_f = font(ZH_FONT, w * 0.039)
    d.text((w * 0.09, h * 0.675), "璀璨中央空调｜薄至", font=brand_f, fill=FOG)
    d.text((w * 0.085, h * 0.715), "190", font=number_f, fill=GOLD)
    d.text((w * 0.39, h * 0.765), "mm", font=unit_f, fill=GOLD)
    d.line((w * 0.09, h * 0.81, w * 0.50, h * 0.81), fill=GOLD_RGBA, width=2)
    d.text((w * 0.09, h * 0.825), "大幅减少吊顶压迫感", font=sub_f, fill=FOG)
    final = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    save(final, FINAL / "EP01_04_scene_190mm_finish_withtext.png")


def shot05():
    source = GEN / "EP01_05_diagram_perimeter_soffit_clean.png"
    image = Image.open(source).convert("RGB")
    w, h = image.size
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    label_f = font(ZH_FONT, w * 0.038)
    sub_f = font(ZH_LIGHT, w * 0.031)
    tags = [
        (w * 0.06, h * 0.095, "原顶保留", w * 0.42, h * 0.24),
        (w * 0.60, h * 0.12, "超薄内机", w * 0.67, h * 0.28),
        (w * 0.63, h * 0.39, "局部边吊", w * 0.61, h * 0.38),
    ]
    for lx, ly, txt, tx, ty in tags:
        b, tw, th = text_bbox(d, txt, label_f)
        d.rounded_rectangle((lx, ly, lx + tw + 30, ly + th + 24), radius=14, fill=COFFEE_RGBA, outline=GOLD_RGBA, width=2)
        d.text((lx + 15 - b[0], ly + 12 - b[1]), txt, font=label_f, fill=GOLD)
        d.line((lx + (tw + 30) / 2, ly + th + 24, tx, ty), fill=GOLD_RGBA, width=3)
        d.ellipse((tx - 6, ty - 6, tx + 6, ty + 6), fill=GOLD_RGBA)
    d.rounded_rectangle((w * 0.10, h * 0.865, w * 0.90, h * 0.955), radius=int(w * 0.025), fill=COFFEE_RGBA, outline=GOLD_RGBA, width=2)
    centered(d, (w * 0.50, h * 0.895), "局部边吊 + 超薄内机", label_f, GOLD, 1, "#251B18")
    centered(d, (w * 0.50, h * 0.93), "守住家中开阔感", sub_f, FOG, 1, "#251B18")
    final = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    save(final, FINAL / "EP01_05_diagram_perimeter_soffit_withtext.png")


def shot06():
    source = GEN / "EP01_06_scene_mansion_air_clean.png"
    image = Image.open(source).convert("RGB")
    w, h = image.size
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    # Restrained airflow curves originating from the single grille.
    for offset, alpha in ((0, 150), (18, 110), (36, 80)):
        points = []
        for i in range(70):
            t = i / 69
            x = w * (0.44 + 0.27 * t)
            y = h * (0.37 + 0.13 * t + 0.035 * math.sin(math.pi * t)) + offset
            points.append((x, y))
        d.line(points, fill=(184, 149, 42, alpha), width=max(2, int(w * 0.003)))
    final = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    final = rounded_label(final, (w / 2, h * 0.90), ["不牺牲层高，", "也有大宅空气感"], width_ratio=0.66, title_gold=True)
    save(final, FINAL / "EP01_06_scene_mansion_air_withtext.png")


def shot07():
    base = Image.new("RGB", (1080, 1920), COFFEE)
    d = ImageDraw.Draw(base)
    d.rectangle((0, 0, 1080, 10), fill=GOLD)
    d.line((165, 735, 915, 735), fill=GOLD, width=2)
    d.rounded_rectangle((390, 1620, 690, 1688), radius=34, outline=GOLD, width=2)
    save(base, GEN / "EP01_07_card_brand_clean.png")
    save(base, FINAL / "EP01_07_card_brand_clean.png")

    image = base.copy()
    d = ImageDraw.Draw(image)
    mark_f = font(LATIN_FONT, 48)
    title_f = font(ZH_FONT, 72)
    sub_f = font(ZH_LIGHT, 46)
    brand_f = font(LATIN_FONT, 30)
    centered(d, (540, 600), "AIR ANSWERS · EP01", mark_f, GOLD)
    centered(d, (540, 855), "璀璨家的空气答案", title_f, FOG)
    centered(d, (540, 978), "懂空气，也懂家的尺度", sub_f, GOLD)
    centered(d, (540, 1654), "璀璨  TRÉSOR", brand_f, GOLD)
    save(image, FINAL / "EP01_07_card_brand_withtext.png")


ASSETS = [
    ("EP01_01_scene_height_pain_clean.png", "镜01 痛点客厅 · clean", "AI底图 / 标尺留白"),
    ("EP01_01_scene_height_pain_withtext.png", "镜01 痛点客厅 · withtext", "2.6m / 2.7m标尺"),
    ("EP01_02_compare_270_260_clean.png", "镜02 户型对比 · clean", "左右分屏"),
    ("EP01_02_compare_270_260_withtext.png", "镜02 户型对比 · withtext", "新版脚本字幕"),
    ("EP01_03_diagram_thick_unit_clean.png", "镜03 普通机型拆解 · clean", "通用机型 / 非品牌"),
    ("EP01_03_diagram_thick_unit_withtext.png", "镜03 普通机型拆解 · withtext", "20–30cm标注"),
    ("EP01_04_scene_190mm_finish_clean.png", "镜04 轻薄完工空间 · clean", "产品实拍另替换"),
    ("EP01_04_scene_190mm_finish_withtext.png", "镜04 轻薄完工空间 · withtext", "190mm卖点"),
    ("EP01_05_diagram_perimeter_soffit_clean.png", "镜05 局部边吊方案 · clean", "超薄机组示意"),
    ("EP01_05_diagram_perimeter_soffit_withtext.png", "镜05 局部边吊方案 · withtext", "同底标注"),
    ("EP01_06_scene_mansion_air_clean.png", "镜06 大宅空气感 · clean", "纯实景"),
    ("EP01_06_scene_mansion_air_withtext.png", "镜06 大宅空气感 · withtext", "柔和气流线"),
    ("EP01_07_card_brand_clean.png", "镜07 品牌收尾 · clean", "品牌母版"),
    ("EP01_07_card_brand_withtext.png", "镜07 品牌收尾 · withtext", "栏目slogan"),
]


def preview_sheet():
    width, height = 2200, 2180
    sheet = Image.new("RGB", (width, height), FOG)
    d = ImageDraw.Draw(sheet)
    d.rectangle((0, 0, width, 250), fill=COFFEE)
    d.text((72, 45), "璀璨家的空气答案 · 层高篇｜新版脚本素材预览 v4", font=font(ZH_FONT, 58), fill=FOG)
    d.text((74, 137), "7镜 · 38秒｜14张 clean / withtext｜镜4产品机身请替换真实宣传片｜全片9:16", font=font(ZH_LIGHT, 30), fill=GOLD)
    d.text((74, 188), "风口锁定：吊顶竖向立面横长条＋纯横向细百叶｜装修参考只取调性，不复制户型与家具组合", font=font(ZH_LIGHT, 26), fill=MUTED)

    cols = 4
    tile_w, tile_h = 500, 590
    sx, sy, gx, gy = 58, 292, 28, 28
    thumb_w, thumb_h = 250, 444
    title_f = font(ZH_FONT, 24)
    meta_f = font(ZH_LIGHT, 19)
    for i, (filename, label, meta) in enumerate(ASSETS):
        row, col = divmod(i, cols)
        x, y = sx + col * (tile_w + gx), sy + row * (tile_h + gy)
        d.rounded_rectangle((x, y, x + tile_w, y + tile_h), radius=24, fill="#FFFFFF", outline=MUTED, width=2)
        source = Image.open(FINAL / filename).convert("RGB")
        thumb = source.copy()
        thumb.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        tx, ty = x + (tile_w - thumb.width) // 2, y + 20
        d.rounded_rectangle((tx - 5, ty - 5, tx + thumb.width + 5, ty + thumb.height + 5), radius=10, fill=COFFEE)
        sheet.paste(thumb, (tx, ty))
        centered(d, (x + tile_w / 2, y + 495), label, title_f, COFFEE)
        centered(d, (x + tile_w / 2, y + 535), meta, meta_f, GOLD)
        short = filename.replace("EP01_", "")
        if len(short) > 46:
            short = short[:43] + "…"
        centered(d, (x + tile_w / 2, y + 568), short, font(LATIN_FONT, 14), "#756A65")
    save(sheet, PREVIEW / "EP01_v4_contact_sheet.png")


def storyboard_preview():
    width, height = 2400, 2050
    board = Image.new("RGB", (width, height), FOG)
    d = ImageDraw.Draw(board)
    d.rectangle((0, 0, width, 235), fill=COFFEE)
    d.text((72, 40), "璀璨家的空气答案 · 层高篇｜38秒分镜预览", font=font(ZH_FONT, 60), fill=FOG)
    d.text((74, 137), "按新版脚本顺序：痛点 → 户型对比 → 普通机型占高 → 190mm落点 → 局部边吊 → 大宅空气感 → 品牌收尾", font=font(ZH_LIGHT, 29), fill=GOLD)
    d.text((74, 186), "镜04前半段请插入真实璀璨内机侧面宣传片；以下AI图为后半段完工空间", font=font(ZH_LIGHT, 25), fill=MUTED)

    shots = [
        ("01", "0–4s｜黄金3秒痛点", "EP01_01_scene_height_pain_withtext.png", "装中央空调，层高不够怎么办？2米6还能不能装？"),
        ("02", "4–8s｜户型分屏", "EP01_02_compare_270_260_withtext.png", "层高2米7以上更从容；2.6–2.7m选对机器才是关键。"),
        ("03", "8–13s｜普通机型占高", "EP01_03_diagram_thick_unit_withtext.png", "普通内机加管线会占用20–30cm层高。"),
        ("04", "13–21s｜提前产品种草", "EP01_04_scene_190mm_finish_withtext.png", "真实产品特写后切完工空间：内机薄至190mm。"),
        ("05", "21–28s｜局部边吊方案", "EP01_05_diagram_perimeter_soffit_withtext.png", "把空调藏进局部边吊，保住主要活动区层高。"),
        ("06", "28–34s｜大宅空气感", "EP01_06_scene_mansion_air_withtext.png", "不为装空调牺牲层高，小户型也有大宅空气感。"),
        ("07", "34–38s｜品牌收尾", "EP01_07_card_brand_withtext.png", "璀璨家的空气答案，懂空气，更懂家的尺度。"),
    ]

    cols = 4
    tile_w, tile_h = 540, 790
    sx, sy, gx, gy = 62, 275, 38, 55
    thumb_w, thumb_h = 266, 473
    time_f = font(ZH_FONT, 25)
    vo_f = font(ZH_LIGHT, 21)
    shot_f = font(LATIN_FONT, 24)

    def wrap_cn(text, max_chars=22):
        return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]

    for i, (shot, timing, filename, vo) in enumerate(shots):
        row, col = divmod(i, cols)
        x, y = sx + col * (tile_w + gx), sy + row * (tile_h + gy)
        d.rounded_rectangle((x, y, x + tile_w, y + tile_h), radius=26, fill="#FFFFFF", outline=MUTED, width=2)
        d.rounded_rectangle((x + 20, y + 20, x + 92, y + 62), radius=18, fill=COFFEE)
        centered(d, (x + 56, y + 41), shot, shot_f, GOLD)
        image = Image.open(FINAL / filename).convert("RGB")
        thumb = image.copy()
        thumb.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        tx, ty = x + (tile_w - thumb.width) // 2, y + 78
        d.rounded_rectangle((tx - 5, ty - 5, tx + thumb.width + 5, ty + thumb.height + 5), radius=10, fill=COFFEE)
        board.paste(thumb, (tx, ty))
        centered(d, (x + tile_w / 2, y + 590), timing, time_f, COFFEE)
        yy = y + 630
        for line in wrap_cn(vo):
            centered(d, (x + tile_w / 2, yy), line, vo_f, "#6E625C")
            yy += 34
        if shot == "04":
            d.rounded_rectangle((x + 82, y + 724, x + tile_w - 82, y + 763), radius=16, fill="#F4E9C9")
            centered(d, (x + tile_w / 2, y + 744), "真实产品片替换位", font(ZH_FONT, 20), RED)
    save(board, PREVIEW / "EP01_v4_38s_storyboard.png")


def validation():
    rows = []
    for filename, _, _ in ASSETS:
        image = Image.open(FINAL / filename)
        w, h = image.size
        rows.append({"file": filename, "size": [w, h], "ratio": round(w / h, 6), "is_9_16": abs(w / h - 9 / 16) < 0.003})
    pair_checks = []
    for shot in range(1, 8):
        clean = next(name for name, _, _ in ASSETS if name.startswith(f"EP01_{shot:02d}_") and name.endswith("_clean.png"))
        text = next(name for name, _, _ in ASSETS if name.startswith(f"EP01_{shot:02d}_") and name.endswith("_withtext.png"))
        a = Image.open(FINAL / clean).convert("RGB")
        b = Image.open(FINAL / text).convert("RGB")
        pair_checks.append({"shot": f"{shot:02d}", "same_size": a.size == b.size, "different_pixels_bbox": ImageChops.difference(a, b).getbbox()})
    data = {
        "final_count": len(rows),
        "all_9_16": all(row["is_9_16"] for row in rows),
        "files": rows,
        "clean_withtext_pairs": pair_checks,
        "vent_qc": {
            "01": "通过",
            "02": "通过，左右两侧均为纯横百叶",
            "03": "通过",
            "04": "首轮出现转角第二格栅，淘汰；重跑通过",
            "05": "通过",
            "06": "通过",
        },
    }
    (PREVIEW / "validation_v4.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def prompt_notes():
    text = """# EP01 新版脚本 v4 · 生成与使用说明

## 脚本依据

唯一内容依据：`璀璨家的空气答案_层高篇脚本 (1).xlsx`，共7镜、38秒。

## 素材结构

- 每镜一张 clean 和一张 withtext，共14张。
- withtext 均由同镜 clean 底图确定性叠字，不独立生成背景。
- 镜01的标尺可在剪映中按2.6m / 2.7m做数字跳动动画。
- 镜02可做左右推拉或中线擦除转场。
- 镜03可对普通厚内机、管线、20–30cm尺寸括号依次做弹出动画。
- 镜04先放真实璀璨内机侧面宣传片，再切AI完工空间；AI图不虚构产品机身。
- 镜05可对金色边线和三个标注做逐层揭示。
- 镜06 clean适合后期自制送风动画；withtext已提供克制的静态气流线。
- 镜07直接使用withtext品牌收尾。

## 风口自查

镜01、02、03、04、05、06均使用吊顶竖向立面的横长条风口，内部仅横向细百叶。镜04首轮因右上角出现转角第二格栅而淘汰，重跑版通过。

## 装修参考边界

只提取暖白、暖木、人字拼、自然侧光、中古现代混搭与真实居住感；所有空间、家具组合、机位与陈设均重新设计。
"""
    (PREVIEW / "使用说明.md").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    for directory in (GEN, FINAL, PREVIEW):
        directory.mkdir(parents=True, exist_ok=True)
    shot01()
    shot02()
    shot03()
    shot04()
    shot05()
    shot06()
    shot07()
    preview_sheet()
    storyboard_preview()
    validation()
    prompt_notes()
