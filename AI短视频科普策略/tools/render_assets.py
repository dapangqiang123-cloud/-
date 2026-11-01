from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "第二期_电费篇_批量生图"
PRODUCT = ROOT / "产品素材"
GENERATED_BACKGROUNDS = ROOT / "tools" / "generated_backgrounds"
TARGET = (2160, 3840)
FONT_MEDIUM = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_LIGHT = "/System/Library/Fonts/STHeiti Light.ttc"


def cover_resize(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    image = image.convert("RGB")
    src_ratio = image.width / image.height
    dst_ratio = size[0] / size[1]
    if src_ratio > dst_ratio:
        new_width = round(image.height * dst_ratio)
        left = (image.width - new_width) // 2
        image = image.crop((left, 0, left + new_width, image.height))
    elif src_ratio < dst_ratio:
        new_height = round(image.width / dst_ratio)
        top = (image.height - new_height) // 2
        image = image.crop((0, top, image.width, top + new_height))
    return image.resize(size, Image.Resampling.LANCZOS)


def rounded_panel(
    canvas: Image.Image,
    box: tuple[int, int, int, int],
    radius: int = 48,
    fill: tuple[int, int, int, int] = (67, 53, 56, 232),
    outline: tuple[int, int, int, int] = (200, 166, 106, 180),
    width: int = 3,
) -> ImageDraw.ImageDraw:
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)
    canvas.alpha_composite(overlay)
    return ImageDraw.Draw(canvas)


def draw_clean_energy_panel(canvas: Image.Image, variant: int) -> None:
    boxes = {
        1: (1530, 2730, 2070, 3290),
        2: (1430, 3090, 2090, 3690),
        3: (120, 1360, 660, 2050),
    }
    box = boxes[variant]
    draw = rounded_panel(canvas, box, radius=42, fill=(67, 53, 56, 238))
    x1, y1, x2, y2 = box
    gold = (200, 166, 106, 255)
    warm_white = (241, 236, 229, 255)
    muted = (210, 202, 193, 230)
    value_font = ImageFont.truetype(FONT_LIGHT, 76)
    unit_font = ImageFont.truetype(FONT_LIGHT, 34)
    small_font = ImageFont.truetype(FONT_LIGHT, 28)

    pad = 54
    chart_left = x1 + pad
    chart_right = x2 - pad
    chart_top = y1 + 110
    chart_bottom = y1 + 300
    points = [
        (chart_left, chart_bottom - 8),
        (chart_left + 86, chart_bottom - 58),
        (chart_left + 162, chart_bottom - 32),
        (chart_left + 246, chart_bottom - 118),
        (chart_left + 336, chart_bottom - 84),
        (chart_right, chart_top),
    ]
    draw.line(points, fill=gold, width=8, joint="curve")
    for px, py in points:
        draw.ellipse((px - 7, py - 7, px + 7, py + 7), fill=warm_white)
    draw.line((chart_left, chart_bottom + 20, chart_right, chart_bottom + 20), fill=(200, 166, 106, 90), width=2)

    values = {1: "18.62", 2: "0024866", 3: "3.27"}
    value = values[variant]
    value_y = chart_bottom + 88
    draw.text((chart_left, value_y), value, font=value_font, fill=warm_white)
    value_width = draw.textbbox((0, 0), value, font=value_font)[2]
    draw.text((chart_left + value_width + 22, value_y + 34), "kWh", font=unit_font, fill=muted)
    draw.text((chart_left, y2 - 72), "ENERGY", font=small_font, fill=(200, 166, 106, 210))


def draw_shot01_title(canvas: Image.Image) -> None:
    box = (150, 360, 1730, 760)
    draw = rounded_panel(canvas, box, radius=54, fill=(67, 53, 56, 214), outline=(200, 166, 106, 140), width=3)
    gold = (200, 166, 106, 255)
    warm_white = (241, 236, 229, 255)
    draw.rounded_rectangle((220, 445, 236, 675), radius=8, fill=gold)
    title_font = ImageFont.truetype(FONT_MEDIUM, 104)
    draw.text((300, 470), "中央空调＝“电老虎”？", font=title_font, fill=warm_white)


def draw_title_panel(canvas: Image.Image, lines: list[str], box: tuple[int, int, int, int], font_size: int = 88) -> None:
    draw = rounded_panel(canvas, box, radius=48, fill=(67, 53, 56, 216), outline=(200, 166, 106, 140), width=3)
    x1, y1, _, _ = box
    draw.rounded_rectangle((x1 + 62, y1 + 64, x1 + 78, y1 + 64 + max(116, 110 * len(lines))), radius=8, fill=(200, 166, 106, 255))
    font = ImageFont.truetype(FONT_MEDIUM, font_size)
    for index, line in enumerate(lines):
        draw.text((x1 + 142, y1 + 60 + index * (font_size + 34)), line, font=font, fill=(241, 236, 229, 255))


def draw_energy_badge(canvas: Image.Image, box: tuple[int, int, int, int], value: str) -> None:
    draw = rounded_panel(canvas, box, radius=42, fill=(67, 53, 56, 226), outline=(200, 166, 106, 170), width=3)
    x1, y1, x2, y2 = box
    value_font = ImageFont.truetype(FONT_LIGHT, 74)
    unit_font = ImageFont.truetype(FONT_LIGHT, 30)
    draw.text((x1 + 46, y1 + 42), value, font=value_font, fill=(241, 236, 229, 255))
    value_width = draw.textbbox((0, 0), value, font=value_font)[2]
    draw.text((x1 + 58 + value_width, y1 + 82), "kWh", font=unit_font, fill=(210, 202, 193, 235))
    draw.line((x1 + 48, y2 - 54, x2 - 48, y2 - 54), fill=(200, 166, 106, 190), width=4)


def draw_factor_label(canvas: Image.Image, box: tuple[int, int, int, int], text: str) -> None:
    draw = rounded_panel(canvas, box, radius=28, fill=(67, 53, 56, 226), outline=(200, 166, 106, 150), width=2)
    font = ImageFont.truetype(FONT_LIGHT, 48)
    x1, y1, x2, y2 = box
    bbox = draw.textbbox((0, 0), text, font=font)
    draw.text(((x1 + x2 - (bbox[2] - bbox[0])) / 2, (y1 + y2 - (bbox[3] - bbox[1])) / 2 - bbox[1]), text, font=font, fill=(241, 236, 229, 255))


def render_shot02() -> None:
    material_dir = OUTPUT / "02_电费差异" / "material"
    effect_dir = OUTPUT / "02_电费差异" / "effect"
    badge_boxes = {
        1: ((140, 3010, 860, 3315), (1300, 3010, 2020, 3315)),
        2: ((120, 2940, 840, 3245), (1310, 2940, 2030, 3245)),
        3: ((120, 3000, 840, 3305), (1310, 3000, 2030, 3305)),
    }
    for variant in range(1, 4):
        material_path = material_dir / f"shot02_material_{variant:02d}.png"
        effect_path = effect_dir / f"shot02_effect_{variant:02d}.png"
        material = cover_resize(Image.open(material_path), TARGET).convert("RGBA")
        left_box, right_box = badge_boxes[variant]
        draw_energy_badge(material, left_box, "86.4")
        draw_energy_badge(material, right_box, "53.1")
        material.convert("RGB").save(material_path, "PNG", optimize=True)

        effect = material.copy()
        draw_title_panel(effect, ["后期使用省电关键"], (120, 220, 1640, 610), font_size=92)
        draw_factor_label(effect, (160, 3360, 930, 3505), "空调使用习惯")
        draw_factor_label(effect, (1230, 3360, 2000, 3505), "自身省电能力")
        effect.convert("RGB").save(effect_path, "PNG", optimize=True)


def patch_temperature_screen(canvas: Image.Image, variant: int) -> None:
    boxes = {
        1: (620, 2470, 1180, 2840),
        2: (960, 2180, 1665, 2685),
    }
    if variant not in boxes:
        return
    box = boxes[variant]
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(box, radius=24, fill=(151, 159, 151, 255), outline=(100, 108, 102, 255), width=4)
    value_font = ImageFont.truetype(FONT_MEDIUM, 180)
    unit_font = ImageFont.truetype(FONT_LIGHT, 76)
    x1, y1, x2, y2 = box
    value = "18"
    bbox = draw.textbbox((0, 0), value, font=value_font)
    value_x = x1 + (x2 - x1 - (bbox[2] - bbox[0])) / 2 - 28
    value_y = y1 + (y2 - y1 - (bbox[3] - bbox[1])) / 2 - bbox[1]
    draw.text((value_x, value_y), value, font=value_font, fill=(20, 20, 20, 255))
    draw.text((x2 - 142, y1 + 92), "°C", font=unit_font, fill=(20, 20, 20, 255))


def desaturate_rounded_region(canvas: Image.Image, box: tuple[int, int, int, int], radius: int = 48, opacity: int = 170) -> None:
    x1, y1, x2, y2 = box
    crop = canvas.crop(box).convert("RGB")
    gray = ImageOps.grayscale(crop).convert("RGBA")
    gray.putalpha(opacity)
    mask = Image.new("L", crop.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, crop.width, crop.height), radius=radius, fill=255)
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    layer.paste(gray, (x1, y1), mask)
    canvas.alpha_composite(layer)


def draw_x_mark(canvas: Image.Image, center: tuple[int, int], size: int = 116) -> None:
    draw = ImageDraw.Draw(canvas)
    cx, cy = center
    draw.ellipse((cx - size, cy - size, cx + size, cy + size), fill=(67, 53, 56, 218), outline=(200, 166, 106, 220), width=6)
    inset = int(size * 0.45)
    draw.line((cx - inset, cy - inset, cx + inset, cy + inset), fill=(241, 236, 229, 255), width=18)
    draw.line((cx + inset, cy - inset, cx - inset, cy + inset), fill=(241, 236, 229, 255), width=18)


def render_shot03() -> None:
    material_dir = OUTPUT / "03_科学使用" / "material"
    effect_dir = OUTPUT / "03_科学使用" / "effect"
    regions = {
        1: ((850, 770, 2060, 2170), (210, 2130, 1520, 3440)),
        2: ((150, 780, 1130, 2010), (680, 1920, 1940, 3320)),
        3: ((150, 160, 1380, 1520), (450, 1640, 2010, 3710)),
    }
    for variant in range(1, 4):
        material_path = material_dir / f"shot03_material_{variant:02d}.png"
        effect_path = effect_dir / f"shot03_effect_{variant:02d}.png"
        material = cover_resize(Image.open(material_path), TARGET).convert("RGBA")
        patch_temperature_screen(material, variant)
        material.convert("RGB").save(material_path, "PNG", optimize=True)

        effect = material.copy()
        first, second = regions[variant]
        desaturate_rounded_region(effect, first)
        desaturate_rounded_region(effect, second)
        draw_x_mark(effect, (first[2] - 150, first[1] + 150), size=92)
        draw_x_mark(effect, (second[2] - 150, second[1] + 150), size=92)
        draw_title_panel(effect, ["科学使用更省电"], (110, 80, 1560, 430), font_size=88)
        draw_factor_label(effect, (100, 3540, 2060, 3710), "少频繁启停 / 合理设温 / 稳定运行")
        effect.convert("RGB").save(effect_path, "PNG", optimize=True)


def render_shot04() -> None:
    material_dir = OUTPUT / "04_科学使用加高效空调" / "material"
    effect_dir = OUTPUT / "04_科学使用加高效空调" / "effect"
    for variant in range(1, 4):
        material_path = material_dir / f"shot04_material_{variant:02d}.png"
        effect_path = effect_dir / f"shot04_effect_{variant:02d}.png"
        material = cover_resize(Image.open(material_path), TARGET).convert("RGBA")
        material.convert("RGB").save(material_path, "PNG", optimize=True)
        effect = material.copy()
        draw_title_panel(effect, ["省电＝科学使用 + 高效空调"], (120, 230, 2000, 640), font_size=82)
        effect.convert("RGB").save(effect_path, "PNG", optimize=True)


def composite_rgba_with_shadow(
    canvas: Image.Image,
    source_path: Path,
    target_width: int,
    xy: tuple[int, int],
    shadow_blur: int = 42,
    shadow_offset: tuple[int, int] = (0, 42),
) -> tuple[int, int, int, int]:
    product = Image.open(source_path).convert("RGBA")
    target_height = round(product.height * target_width / product.width)
    product = product.resize((target_width, target_height), Image.Resampling.LANCZOS)
    x, y = xy

    alpha = product.getchannel("A")
    shadow = Image.new("RGBA", product.size, (18, 15, 14, 0))
    shadow.putalpha(alpha.filter(ImageFilter.GaussianBlur(shadow_blur)).point(lambda p: int(p * 0.48)))
    canvas.alpha_composite(shadow, (x + shadow_offset[0], y + shadow_offset[1]))
    canvas.alpha_composite(product, (x, y))
    return (x, y, x + target_width, y + target_height)


def draw_lock_on(canvas: Image.Image, box: tuple[int, int, int, int]) -> None:
    draw = ImageDraw.Draw(canvas)
    x1, y1, x2, y2 = box
    pad = 54
    x1, y1, x2, y2 = x1 - pad, y1 - pad, x2 + pad, y2 + pad
    corner = 135
    gold = (200, 166, 106, 220)
    for points in (
        ((x1, y1 + corner), (x1, y1), (x1 + corner, y1)),
        ((x2 - corner, y1), (x2, y1), (x2, y1 + corner)),
        ((x1, y2 - corner), (x1, y2), (x1 + corner, y2)),
        ((x2 - corner, y2), (x2, y2), (x2, y2 - corner)),
    ):
        draw.line(points, fill=gold, width=8, joint="curve")
    draw.line((x1 + 180, y1 - 16, x2 - 180, y1 - 16), fill=(200, 166, 106, 110), width=3)
    draw.ellipse((x2 - 26, y1 - 42, x2 + 26, y1 + 10), fill=(241, 236, 229, 240), outline=gold, width=5)


def render_shot05() -> None:
    material_dir = OUTPUT / "05_APF与AI省电" / "material"
    effect_dir = OUTPUT / "05_APF与AI省电" / "effect"
    product_paths = [PRODUCT / "2.png", PRODUCT / "3.png", PRODUCT / "1.png"]
    widths = [1450, 1460, 1530]
    positions = [(400, 2210), (440, 2260), (315, 2240)]
    for variant in range(1, 4):
        background = cover_resize(Image.open(GENERATED_BACKGROUNDS / f"shot05_bg_{variant:02d}.png"), TARGET).convert("RGBA")
        box = composite_rgba_with_shadow(background, product_paths[variant - 1], widths[variant - 1], positions[variant - 1])
        draw_lock_on(background, box)
        material_path = material_dir / f"shot05_material_{variant:02d}.png"
        effect_path = effect_dir / f"shot05_effect_{variant:02d}.png"
        background.convert("RGB").save(material_path, "PNG", optimize=True)

        effect = background.copy()
        draw_title_panel(effect, ["空调节能关键看"], (110, 170, 1540, 560), font_size=92)
        draw_factor_label(effect, (170, 750, 930, 920), "APF值")
        draw_factor_label(effect, (1150, 750, 1990, 920), "AI省电能力")
        effect.convert("RGB").save(effect_path, "PNG", optimize=True)


def make_product_stage(variant: int) -> Image.Image:
    width, height = TARGET
    image = Image.new("RGBA", TARGET, (0, 0, 0, 255))
    px = image.load()
    palettes = [
        ((42, 29, 30), (151, 142, 132)),
        ((31, 29, 30), (129, 123, 117)),
        ((55, 34, 35), (166, 156, 143)),
    ]
    top, bottom = palettes[variant - 1]
    for y in range(height):
        t = y / max(1, height - 1)
        t = min(1.0, max(0.0, t * 0.94))
        for x in range(width):
            vignette = abs(x - width / 2) / (width / 2)
            shade = int(18 * vignette * vignette)
            color = tuple(max(0, round(top[i] * (1 - t) + bottom[i] * t) - shade) for i in range(3))
            px[x, y] = (*color, 255)

    draw = ImageDraw.Draw(image)
    gold = (200, 166, 106, 140)
    faint = (200, 166, 106, 65)
    offsets = [0, 90, -70]
    shift = offsets[variant - 1]
    points = [(120, 1520 + shift), (520, 1320 + shift), (980, 1420 + shift), (1430, 1090 + shift), (2030, 1180 + shift)]
    draw.line(points, fill=gold, width=5)
    for x, y in points:
        draw.ellipse((x - 13, y - 13, x + 13, y + 13), fill=(241, 236, 229, 210), outline=gold, width=3)
    for delta in (150, 300, 450):
        draw.arc((80 + delta, 820 + shift, 2080 - delta // 2, 2780 + shift), 198, 337, fill=faint, width=3)

    # Empty architectural pedestal, later carrying the exact official product PNG.
    draw.rounded_rectangle((170, 3030, 1990, 3510), radius=30, fill=(100, 94, 88, 235), outline=(200, 166, 106, 150), width=5)
    draw.polygon([(170, 3030), (390, 2910), (1920, 2910), (1990, 3030)], fill=(171, 162, 150, 230))
    glow = Image.new("RGBA", TARGET, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((320, 1840, 1840, 3420), fill=(230, 207, 168, 70))
    glow = glow.filter(ImageFilter.GaussianBlur(170))
    image.alpha_composite(glow)
    return image


def draw_metric_proof(canvas: Image.Image) -> None:
    draw_title_panel(canvas, ["璀璨客餐厅中央空调C3D"], (100, 140, 2020, 530), font_size=76)
    draw = rounded_panel(canvas, (150, 650, 2010, 1190), radius=48, fill=(67, 53, 56, 218), outline=(200, 166, 106, 150), width=3)
    label_font = ImageFont.truetype(FONT_LIGHT, 55)
    number_font = ImageFont.truetype(FONT_MEDIUM, 170)
    big_font = ImageFont.truetype(FONT_MEDIUM, 156)
    warm = (241, 236, 229, 255)
    gold = (200, 166, 106, 255)
    draw.text((240, 740), "APF=", font=label_font, fill=warm)
    draw.text((430, 675), "4.4", font=number_font, fill=gold)
    draw.line((1020, 715, 1020, 1120), fill=(200, 166, 106, 120), width=3)
    draw.text((1120, 735), "一年劲省", font=label_font, fill=warm)
    draw.text((1110, 835), "594", font=big_font, fill=gold)
    draw.text((1725, 945), "元", font=label_font, fill=warm)


def render_shot06() -> None:
    material_dir = OUTPUT / "06_C3D产品证明" / "material"
    effect_dir = OUTPUT / "06_C3D产品证明" / "effect"
    product_paths = [PRODUCT / "2.png", PRODUCT / "3.png", PRODUCT / "1.png"]
    widths = [1540, 1500, 1620]
    positions = [(310, 2050), (350, 2070), (270, 2110)]
    for variant in range(1, 4):
        material = make_product_stage(variant)
        composite_rgba_with_shadow(material, product_paths[variant - 1], widths[variant - 1], positions[variant - 1], shadow_blur=54, shadow_offset=(0, 60))
        material_path = material_dir / f"shot06_material_{variant:02d}.png"
        effect_path = effect_dir / f"shot06_effect_{variant:02d}.png"
        material.convert("RGB").save(material_path, "PNG", optimize=True)
        effect = material.copy()
        draw_metric_proof(effect)
        effect.convert("RGB").save(effect_path, "PNG", optimize=True)


def draw_concept_energy_curve(canvas: Image.Image, variant: int) -> None:
    boxes = [(105, 2660, 1030, 3230), (1090, 2650, 2045, 3220), (125, 900, 920, 1450)]
    box = boxes[variant - 1]
    draw = rounded_panel(canvas, box, radius=44, fill=(67, 53, 56, 208), outline=(200, 166, 106, 150), width=3)
    x1, y1, x2, y2 = box
    points = [(x1 + 70, y2 - 120), (x1 + 210, y2 - 180), (x1 + 350, y2 - 155), (x1 + 520, y2 - 260), (x2 - 80, y1 + 105)]
    draw.line(points, fill=(200, 166, 106, 255), width=10, joint="curve")
    for x, y in points:
        draw.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(241, 236, 229, 255))
    small = ImageFont.truetype(FONT_LIGHT, 34)
    draw.text((x1 + 68, y1 + 58), "AI ENERGY", font=small, fill=(241, 236, 229, 235))


def render_shot07() -> None:
    material_dir = OUTPUT / "07_AI智省电" / "material"
    effect_dir = OUTPUT / "07_AI智省电" / "effect"
    controller_positions = [(1130, 2380), (100, 2280), (1120, 2080)]
    controller_widths = [900, 860, 920]
    for variant in range(1, 4):
        base_path = OUTPUT / "04_科学使用加高效空调" / "material" / f"shot04_material_{variant:02d}.png"
        material = cover_resize(Image.open(base_path), TARGET).convert("RGBA")
        # A subtle warm grade ties the reused, approved short-sleeve family scenes to the AI-energy UI.
        warm = Image.new("RGBA", TARGET, (76, 52, 40, 18))
        material.alpha_composite(warm)
        draw_concept_energy_curve(material, variant)
        composite_rgba_with_shadow(material, PRODUCT / "线控器白色.png", controller_widths[variant - 1], controller_positions[variant - 1], shadow_blur=34, shadow_offset=(18, 38))
        material_path = material_dir / f"shot07_material_{variant:02d}.png"
        effect_path = effect_dir / f"shot07_effect_{variant:02d}.png"
        material.convert("RGB").save(material_path, "PNG", optimize=True)
        effect = material.copy()
        draw_title_panel(effect, ["AI智省电｜精细化管理能耗"], (90, 150, 2050, 560), font_size=78)
        effect.convert("RGB").save(effect_path, "PNG", optimize=True)


def render_shot08() -> None:
    material_dir = OUTPUT / "08_栏目收尾" / "material"
    effect_dir = OUTPUT / "08_栏目收尾" / "effect"
    source_dir = ROOT / "deliverables" / "04c-轻薄吊顶客餐厅"
    source_paths = [
        source_dir / "04c-1-远景空镜-V2横长百叶.png",
        source_dir / "04c-2-仰视吊顶细节-V2横长百叶.png",
        source_dir / "04c-3-中景换机位-V2横长百叶.png",
    ]
    for variant, source_path in enumerate(source_paths, 1):
        material = cover_resize(Image.open(source_path), TARGET).convert("RGBA")
        # Late-afternoon calm finish; original brand space and exact long linear vent stay intact.
        grade = Image.new("RGBA", TARGET, (91, 58, 38, 24 + variant * 4))
        material.alpha_composite(grade)
        material_path = material_dir / f"shot08_material_{variant:02d}.png"
        effect_path = effect_dir / f"shot08_effect_{variant:02d}.png"
        material.convert("RGB").save(material_path, "PNG", optimize=True)
        effect = material.copy()
        draw_title_panel(effect, ["璀璨家的空气答案", "懂空气，更懂家的尺度"], (120, 250, 2010, 860), font_size=82)
        effect.convert("RGB").save(effect_path, "PNG", optimize=True)


def render_shot01() -> None:
    material_dir = OUTPUT / "01_电老虎" / "material"
    effect_dir = OUTPUT / "01_电老虎" / "effect"
    for variant in range(1, 4):
        material_path = material_dir / f"shot01_material_{variant:02d}.png"
        effect_path = effect_dir / f"shot01_effect_{variant:02d}.png"

        source = Image.open(material_path)
        material = cover_resize(source, TARGET).convert("RGBA")
        draw_clean_energy_panel(material, variant)
        material.convert("RGB").save(material_path, "PNG", optimize=True)

        effect = material.copy()
        draw_shot01_title(effect)
        effect.convert("RGB").save(effect_path, "PNG", optimize=True)


if __name__ == "__main__":
    render_shot01()
    render_shot02()
    render_shot03()
    render_shot04()
    render_shot05()
    render_shot06()
    render_shot07()
    render_shot08()
