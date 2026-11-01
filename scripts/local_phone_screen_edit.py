from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter


FONT_REGULAR = "/System/Library/Fonts/STHeiti Light.ttc"
FONT_MEDIUM = "/System/Library/Fonts/STHeiti Medium.ttc"


def font(size: int, medium: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_MEDIUM if medium else FONT_REGULAR, size=size)


def right_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, text_font: ImageFont.FreeTypeFont, fill: str) -> None:
    x, y = xy
    box = draw.textbbox((0, 0), text, font=text_font)
    draw.text((x - (box[2] - box[0]), y), text, font=text_font, fill=fill)


def make_bill_ui(width: int = 720, height: int = 1500) -> Image.Image:
    scale = width / 720.0

    def s(value: float) -> int:
        return int(round(value * scale))

    teal = "#008C91"
    teal_dark = "#00777C"
    page = "#EEF3F4"
    white = "#FFFFFF"
    card = "#F9FBFC"
    line = "#DDE5E7"
    ink = "#182326"
    secondary = "#66777B"

    ui = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(ui)

    radius = s(62)
    draw.rounded_rectangle((0, 0, width - 1, height - 1), radius=radius, fill=teal)
    draw.rectangle((0, s(270), width, height), fill=page)
    draw.rounded_rectangle((0, s(235), width, s(355)), radius=s(50), fill=page)

    # Status bar and camera island.
    draw.text((s(48), s(28)), "9:41", font=font(s(27), True), fill=white)
    draw.rounded_rectangle((s(280), s(18), s(440), s(77)), radius=s(30), fill="#071416")
    draw.ellipse((s(408), s(37), s(424), s(53)), fill="#122B2F")
    draw.rectangle((s(592), s(38), s(602), s(58)), fill=white)
    draw.rectangle((s(608), s(32), s(618), s(58)), fill=white)
    draw.rectangle((s(624), s(25), s(634), s(58)), fill=white)
    draw.arc((s(646), s(27), s(684), s(61)), 205, 335, fill=white, width=s(5))
    draw.rounded_rectangle((s(681), s(27), s(710), s(57)), radius=s(6), outline=white, width=s(4))
    draw.rectangle((s(710), s(36), s(716), s(49)), fill=white)
    draw.rectangle((s(686), s(32), s(704), s(52)), fill=white)

    # Header navigation and a restrained State Grid mark.
    draw.line((s(48), s(154), s(66), s(136)), fill=white, width=s(5))
    draw.line((s(48), s(154), s(66), s(172)), fill=white, width=s(5))
    cx, cy = s(233), s(155)
    draw.ellipse((cx - s(33), cy - s(33), cx + s(33), cy + s(33)), outline=white, width=s(4))
    draw.arc((cx - s(23), cy - s(23), cx + s(23), cy + s(23)), 15, 165, fill=white, width=s(4))
    draw.arc((cx - s(23), cy - s(23), cx + s(23), cy + s(23)), 195, 345, fill=white, width=s(4))
    draw.line((cx, cy - s(24), cx, cy + s(24)), fill=white, width=s(4))
    draw.text((s(282), s(107)), "国家电网", font=font(s(46), True), fill=white)
    draw.text((s(284), s(166)), "STATE GRID", font=font(s(24), True), fill=white)

    # Page title.
    draw.text((s(48), s(285)), "电费账单", font=font(s(43), True), fill=ink)

    # Month selector card.
    draw.rounded_rectangle((s(32), s(375), s(688), s(515)), radius=s(28), fill=card)
    draw.ellipse((s(55), s(428), s(67), s(440)), fill=teal)
    draw.text((s(83), s(410)), "2026年08月", font=font(s(32), True), fill=teal_dark)
    draw.line((s(645), s(428), s(659), s(442)), fill="#95A6AA", width=s(4))
    draw.line((s(659), s(442), s(645), s(456)), fill="#95A6AA", width=s(4))

    # Amount card.
    draw.rounded_rectangle((s(32), s(532), s(688), s(812)), radius=s(30), fill=card)
    draw.text((s(48), s(578)), "电费金额（元）", font=font(s(27)), fill=secondary)
    amount_font = font(s(82), True)
    amount = "803.45"
    amount_box = draw.textbbox((0, 0), amount, font=amount_font)
    amount_width = amount_box[2] - amount_box[0]
    amount_x = (width - amount_width) // 2 - s(18)
    draw.text((amount_x, s(642)), amount, font=amount_font, fill=teal_dark)
    draw.text((amount_x + amount_width + s(12), s(687)), "元", font=font(s(34), True), fill=teal_dark)

    # Details.
    draw.text((s(42), s(848)), "账单详情", font=font(s(38), True), fill=ink)
    draw.rounded_rectangle((s(32), s(920), s(688), s(1382)), radius=s(30), fill=card)
    rows = [
        ("电费", "803.45元", False),
        ("基本电费", "0.00元", False),
        ("政府性基金及附加", "0.00元", False),
        ("合计", "803.45元", True),
    ]
    row_top = s(960)
    row_height = s(102)
    for index, (label, value, bold) in enumerate(rows):
        y = row_top + index * row_height
        row_font = font(s(29), medium=bold)
        draw.text((s(54), y), label, font=row_font, fill=ink)
        right_text(draw, (s(655), y), value, row_font, ink)
        if index < len(rows) - 1:
            line_y = y + s(68)
            draw.line((s(54), line_y, s(655), line_y), fill=line, width=s(2))

    # Very subtle screen sheen without reducing text clarity.
    sheen = Image.new("RGBA", ui.size, (0, 0, 0, 0))
    sheen_draw = ImageDraw.Draw(sheen)
    sheen_draw.polygon(
        [(0, 0), (s(190), 0), (s(470), height), (s(300), height)],
        fill=(255, 255, 255, 11),
    )
    return Image.alpha_composite(ui, sheen)


def perspective_coefficients(destination: list[tuple[float, float]], source: list[tuple[float, float]]) -> list[float]:
    matrix: list[list[float]] = []
    values: list[float] = []
    for (x, y), (u, v) in zip(destination, source):
        matrix.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        values.append(u)
        matrix.append([0, 0, 0, x, y, 1, -v * x, -v * y])
        values.append(v)
    return np.linalg.solve(np.asarray(matrix, dtype=np.float64), np.asarray(values, dtype=np.float64)).tolist()


def composite_ui(base: Image.Image, quad: list[tuple[float, float]], ui_width: int) -> tuple[Image.Image, Image.Image]:
    ui_height = int(round(ui_width * 1500 / 720))
    ui = make_bill_ui(ui_width, ui_height)
    source = [(0, 0), (ui.width - 1, 0), (ui.width - 1, ui.height - 1), (0, ui.height - 1)]
    coefficients = perspective_coefficients(quad, source)
    warped = ui.transform(
        base.size,
        Image.Transform.PERSPECTIVE,
        coefficients,
        resample=Image.Resampling.BICUBIC,
        fillcolor=(0, 0, 0, 0),
    )
    alpha = warped.getchannel("A")
    # A subpixel feather integrates the replacement with the existing glass edge.
    alpha = alpha.filter(ImageFilter.GaussianBlur(radius=0.45))
    warped.putalpha(alpha)
    result = Image.alpha_composite(base.convert("RGBA"), warped)
    return result, alpha


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    original = Image.open(args.source).convert("RGBA")

    # Screen-inner corners in the original 941×1672 image: top-left, top-right,
    # bottom-right, bottom-left. The phone bezel itself stays untouched.
    quad = [(560.0, 704.0), (716.0, 711.0), (670.0, 1070.0), (528.0, 1048.0)]
    edited, alpha = composite_ui(original, quad, ui_width=1080)
    original_output = args.output_dir / "手机屏幕局部修改_2026年08月_原尺寸.png"
    edited.convert("RGB").save(original_output, quality=100)

    # Verify that every pixel outside the screen alpha mask is identical.
    original_array = np.asarray(original.convert("RGB"))
    edited_array = np.asarray(edited.convert("RGB"))
    alpha_array = np.asarray(alpha)
    outside = alpha_array == 0
    outside_diff = np.abs(original_array.astype(np.int16) - edited_array.astype(np.int16))[outside]
    max_outside_diff = int(outside_diff.max()) if outside_diff.size else 0

    # A separate 4K delivery: upscale the untouched source first, then render the UI
    # again at the larger coordinates so the small Chinese text stays crisp.
    output_4k_size = (2160, 3840)
    upscale = original.resize(output_4k_size, Image.Resampling.LANCZOS)
    sx = output_4k_size[0] / original.width
    sy = output_4k_size[1] / original.height
    quad_4k = [(x * sx, y * sy) for x, y in quad]
    edited_4k, _ = composite_ui(upscale, quad_4k, ui_width=1800)
    output_4k = args.output_dir / "手机屏幕局部修改_2026年08月_4K.png"
    edited_4k.convert("RGB").save(output_4k, quality=100)

    # Save the clean UI plate as a reusable source for later month/amount changes.
    ui_plate = make_bill_ui(1080, 2250)
    ui_output = args.output_dir / "国家电网电费账单UI_2026年08月.png"
    ui_plate.save(ui_output)

    print(f"source={args.source}")
    print(f"original_size_output={original_output}")
    print(f"four_k_output={output_4k}")
    print(f"ui_plate={ui_output}")
    print(f"max_outside_screen_pixel_diff={max_outside_diff}")


if __name__ == "__main__":
    main()
