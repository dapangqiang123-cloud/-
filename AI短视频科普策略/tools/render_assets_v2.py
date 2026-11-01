from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "第二期_电费篇_批量生图_V2_老钱中古风"
PRODUCT = ROOT / "产品素材"
TARGET = (2160, 3840)
FONT_MEDIUM = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_LIGHT = "/System/Library/Fonts/STHeiti Light.ttc"

SHOTS = [
    "01_电老虎",
    "02_电费差异",
    "03_科学使用",
    "04_科学使用加高效空调",
    "05_APF与AI省电",
    "06_C3D产品证明",
    "07_AI智省电",
    "08_栏目收尾",
]


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


def clean_generated_source(image: Image.Image) -> Image.Image:
    # Reference sites sometimes leak a tiny lower-corner watermark into generations.
    # Trimming the lowest 3.5% removes it before the final 9:16 crop.
    trim = max(1, round(image.height * 0.035))
    image = image.crop((0, 0, image.width, image.height - trim))
    return cover_resize(image, TARGET).convert("RGBA")


def composite_with_shadow(
    canvas: Image.Image,
    source_path: Path,
    target_width: int,
    xy: tuple[int, int],
    shadow_blur: int = 42,
    shadow_offset: tuple[int, int] = (0, 42),
) -> tuple[int, int, int, int]:
    source = Image.open(source_path).convert("RGBA")
    target_height = round(source.height * target_width / source.width)
    source = source.resize((target_width, target_height), Image.Resampling.LANCZOS)
    x, y = xy
    alpha = source.getchannel("A")
    shadow = Image.new("RGBA", source.size, (24, 18, 14, 0))
    shadow.putalpha(alpha.filter(ImageFilter.GaussianBlur(shadow_blur)).point(lambda p: int(p * 0.43)))
    canvas.alpha_composite(shadow, (x + shadow_offset[0], y + shadow_offset[1]))
    canvas.alpha_composite(source, (x, y))
    return (x, y, x + target_width, y + target_height)


def blank_screen_controller() -> Image.Image:
    controller = Image.open(PRODUCT / "线控器白色.png").convert("RGBA")
    draw = ImageDraw.Draw(controller)
    # Preserve the official shell, proportions and buttons; only switch the LCD off.
    draw.rounded_rectangle((118, 173, 874, 594), radius=18, fill=(104, 111, 105, 255), outline=(72, 76, 72, 255), width=4)
    return controller


def composite_controller(
    canvas: Image.Image,
    target_width: int,
    xy: tuple[int, int],
) -> None:
    controller = blank_screen_controller()
    target_height = round(controller.height * target_width / controller.width)
    controller = controller.resize((target_width, target_height), Image.Resampling.LANCZOS)
    x, y = xy
    alpha = controller.getchannel("A")
    shadow = Image.new("RGBA", controller.size, (25, 18, 14, 0))
    shadow.putalpha(alpha.filter(ImageFilter.GaussianBlur(30)).point(lambda p: int(p * 0.36)))
    canvas.alpha_composite(shadow, (x + 18, y + 34))
    canvas.alpha_composite(controller, (x, y))


def render_materials() -> None:
    product_paths = [PRODUCT / "2.png", PRODUCT / "3.png", PRODUCT / "1.png"]
    product_layouts = {
        5: ([(355, 2320), (430, 2200), (470, 2340)], [1480, 1340, 1280]),
        6: ([(330, 2220), (350, 2260), (390, 2280)], [1500, 1480, 1420]),
    }
    controller_layouts = ([(1130, 1180), (1260, 2480), (1230, 2300)], [760, 760, 720])

    for shot_index, shot in enumerate(SHOTS, 1):
        material_dir = OUTPUT / shot / "material"
        for variant in range(1, 4):
            path = material_dir / f"shot{shot_index:02d}_material_{variant:02d}.png"
            material = clean_generated_source(Image.open(path))
            if shot_index in product_layouts:
                positions, widths = product_layouts[shot_index]
                composite_with_shadow(material, product_paths[variant - 1], widths[variant - 1], positions[variant - 1])
            elif shot_index == 7:
                positions, widths = controller_layouts
                composite_controller(material, widths[variant - 1], positions[variant - 1])
            material.convert("RGB").save(path, "PNG", optimize=True)


def panel(
    layer: Image.Image,
    box: tuple[int, int, int, int],
    radius: int = 42,
    fill: tuple[int, int, int, int] = (52, 40, 39, 218),
    outline: tuple[int, int, int, int] = (199, 165, 105, 190),
    width: int = 3,
) -> ImageDraw.ImageDraw:
    draw = ImageDraw.Draw(layer)
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)
    return draw


def centered_text(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, font, fill=(244, 238, 229, 255)) -> None:
    x1, y1, x2, y2 = box
    bounds = draw.textbbox((0, 0), text, font=font)
    tw = bounds[2] - bounds[0]
    th = bounds[3] - bounds[1]
    draw.text(((x1 + x2 - tw) / 2, (y1 + y2 - th) / 2 - bounds[1]), text, font=font, fill=fill)


def title_panel(layer: Image.Image, text: str, variant: int, size: int = 88) -> None:
    y = [150, 220, 110][variant - 1]
    box = (100, y, 2060, y + 360)
    draw = panel(layer, box, radius=46)
    draw.rounded_rectangle((160, y + 70, 176, y + 290), radius=8, fill=(200, 166, 106, 255))
    font = ImageFont.truetype(FONT_MEDIUM, size)
    draw.text((230, y + 92), text, font=font, fill=(244, 238, 229, 255))


def chip(layer: Image.Image, box: tuple[int, int, int, int], text: str, size: int = 46) -> None:
    draw = panel(layer, box, radius=34, fill=(52, 40, 39, 205))
    centered_text(draw, box, text, ImageFont.truetype(FONT_LIGHT, size))


def draw_energy_gauge(layer: Image.Image, variant: int) -> None:
    positions = [(1150, 2960, 2030, 3520), (105, 2860, 985, 3420), (1180, 2780, 2040, 3370)]
    box = positions[variant - 1]
    draw = panel(layer, box, radius=46, fill=(52, 40, 39, 200))
    x1, y1, x2, y2 = box
    draw.arc((x1 + 120, y1 + 105, x2 - 120, y2 + 210), 195, 345, fill=(200, 166, 106, 255), width=16)
    draw.line((x1 + 440, y1 + 330, x2 - 170, y1 + 170), fill=(244, 238, 229, 255), width=12)
    draw.ellipse((x1 + 418, y1 + 308, x1 + 462, y1 + 352), fill=(200, 166, 106, 255))
    centered_text(draw, (x1 + 100, y2 - 130, x2 - 100, y2 - 45), "用电负担", ImageFont.truetype(FONT_LIGHT, 42))


def draw_compare_ui(layer: Image.Image, variant: int) -> None:
    y = [3060, 2980, 2860][variant - 1]
    left = (100, y, 990, y + 410)
    right = (1170, y, 2060, y + 410)
    for box, label, amount in ((left, "使用习惯", 0.82), (right, "空调自身省电能力", 0.58)):
        draw = panel(layer, box, radius=42, fill=(52, 40, 39, 205))
        x1, y1, x2, y2 = box
        draw.text((x1 + 60, y1 + 58), label, font=ImageFont.truetype(FONT_LIGHT, 45), fill=(244, 238, 229, 255))
        draw.rounded_rectangle((x1 + 60, y1 + 210, x2 - 60, y1 + 270), radius=30, fill=(124, 108, 94, 180))
        draw.rounded_rectangle((x1 + 60, y1 + 210, x1 + 60 + int((x2 - x1 - 120) * amount), y1 + 270), radius=30, fill=(200, 166, 106, 255))


def draw_science_ui(layer: Image.Image, variant: int) -> None:
    y = [3210, 3110, 3040][variant - 1]
    labels = ["少频繁启停", "合理设温", "稳定运行"]
    for index, label in enumerate(labels):
        x1 = 100 + index * 690
        chip(layer, (x1, y, x1 + 610, y + 180), label, size=42)


def draw_metric_cards(layer: Image.Image, shot: int, variant: int) -> None:
    if shot == 5:
        y = [710, 760, 690][variant - 1]
        chip(layer, (120, y, 1010, y + 210), "全年能源消耗效率值", size=40)
        chip(layer, (1150, y, 2040, y + 210), "智能省电能力", size=44)
    else:
        y = [650, 720, 620][variant - 1]
        left = (120, y, 1040, y + 520)
        right = (1120, y, 2040, y + 520)
        draw = panel(layer, left, radius=44)
        draw.text((190, y + 70), "全年能源消耗效率值", font=ImageFont.truetype(FONT_LIGHT, 40), fill=(244, 238, 229, 255))
        draw.text((300, y + 190), "4.4", font=ImageFont.truetype(FONT_MEDIUM, 150), fill=(200, 166, 106, 255))
        draw = panel(layer, right, radius=44)
        draw.text((1190, y + 70), "一年劲省", font=ImageFont.truetype(FONT_LIGHT, 48), fill=(244, 238, 229, 255))
        draw.text((1230, y + 175), "594", font=ImageFont.truetype(FONT_MEDIUM, 145), fill=(200, 166, 106, 255))
        draw.text((1780, y + 265), "元", font=ImageFont.truetype(FONT_LIGHT, 56), fill=(244, 238, 229, 255))


def draw_smart_ui(layer: Image.Image, variant: int) -> None:
    boxes = [(110, 2860, 1040, 3470), (1120, 2860, 2050, 3470), (110, 790, 1040, 1400)]
    box = boxes[variant - 1]
    draw = panel(layer, box, radius=46, fill=(52, 40, 39, 198))
    x1, y1, x2, y2 = box
    points = [(x1 + 70, y2 - 120), (x1 + 220, y2 - 190), (x1 + 370, y2 - 170), (x1 + 560, y2 - 310), (x2 - 70, y1 + 110)]
    draw.line(points, fill=(200, 166, 106, 255), width=11, joint="curve")
    for x, y in points:
        draw.ellipse((x - 10, y - 10, x + 10, y + 10), fill=(244, 238, 229, 255))
    draw.text((x1 + 65, y1 + 55), "实时分析", font=ImageFont.truetype(FONT_LIGHT, 40), fill=(244, 238, 229, 255))
    draw.text((x1 + 65, y1 + 120), "精细管理", font=ImageFont.truetype(FONT_LIGHT, 40), fill=(200, 166, 106, 255))


def make_ui(shot: int, variant: int) -> Image.Image:
    layer = Image.new("RGBA", TARGET, (0, 0, 0, 0))
    if shot == 1:
        title_panel(layer, "中央空调＝“电老虎”？", variant, size=82)
        draw_energy_gauge(layer, variant)
    elif shot == 2:
        title_panel(layer, "后期使用省电关键", variant, size=88)
        draw_compare_ui(layer, variant)
    elif shot == 3:
        title_panel(layer, "科学使用更省电", variant, size=90)
        draw_science_ui(layer, variant)
    elif shot == 4:
        title_panel(layer, "省电＝科学使用＋高效空调", variant, size=78)
    elif shot == 5:
        title_panel(layer, "空调节能关键看", variant, size=90)
        draw_metric_cards(layer, shot, variant)
    elif shot == 6:
        title_panel(layer, "璀璨客餐厅中央空调 C3D", variant, size=69)
        draw_metric_cards(layer, shot, variant)
    elif shot == 7:
        title_panel(layer, "智能省电｜精细化管理能耗", variant, size=76)
        draw_smart_ui(layer, variant)
    elif shot == 8:
        y = [250, 300, 210][variant - 1]
        draw = panel(layer, (100, y, 2060, y + 600), radius=46)
        draw.text((220, y + 105), "璀璨家的空气答案", font=ImageFont.truetype(FONT_MEDIUM, 94), fill=(244, 238, 229, 255))
        draw.text((220, y + 275), "懂空气，更懂家的尺度", font=ImageFont.truetype(FONT_LIGHT, 72), fill=(200, 166, 106, 255))
    return layer


def render_effects_and_ui() -> None:
    for shot_index, shot in enumerate(SHOTS, 1):
        material_dir = OUTPUT / shot / "material"
        effect_dir = OUTPUT / shot / "effect"
        ui_dir = OUTPUT / shot / "ui_png"
        for variant in range(1, 4):
            material_path = material_dir / f"shot{shot_index:02d}_material_{variant:02d}.png"
            effect_path = effect_dir / f"shot{shot_index:02d}_effect_{variant:02d}.png"
            ui_path = ui_dir / f"shot{shot_index:02d}_ui_{variant:02d}.png"
            material = Image.open(material_path).convert("RGBA")
            ui = make_ui(shot_index, variant)
            ui.save(ui_path, "PNG", optimize=True)
            material.alpha_composite(ui)
            material.convert("RGB").save(effect_path, "PNG", optimize=True)


if __name__ == "__main__":
    render_materials()
    render_effects_and_ui()
