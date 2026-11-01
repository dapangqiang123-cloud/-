from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter


SOURCE = Path("/Users/weipeilong/.codex/generated_images/019ff51e-66f2-7ab2-bd2a-74dd9b45c809/exec-912acf80-53b3-4d4b-965a-567d08f773e9.png")
BASE_OUT = Path("/Users/weipeilong/Desktop/Aaaaaaa/AI工作台/06_codex项目/璀璨codex任务/output/EP01_grille_v2/01_base/EP01_07_scene_grand_ending_clean.png")
FINAL_OUT = Path("/Users/weipeilong/Desktop/Aaaaaaa/AI工作台/06_codex项目/璀璨codex任务/output/EP01_grille_v2/02_final/EP01_07_scene_grand_ending_clean.png")

image = Image.open(SOURCE).convert("RGB")
w, h = image.size

# The accepted edit preserved the room but left only three sparse lines. Restrict
# this deterministic correction to the existing vent band in the upper ceiling.
x1, x2 = round(w * 0.10), round(w * 0.922)
y1, y2 = round(h * 0.188), round(h * 0.205)

# Borrow the immediately adjacent ceiling texture to erase the sparse-line band.
texture = image.crop((x1 - 5, y1 - 24, x2 + 5, y2 - 24)).resize((x2 - x1 + 10, y2 - y1), Image.Resampling.LANCZOS)
image.paste(texture, (x1 - 5, y1))

draw = ImageDraw.Draw(image)
frame = (66, 55, 47)
blade = (28, 25, 22)

# Thin integrated rectangular frame.
draw.rectangle((x1, y1, x2, y2), outline=frame, width=1)

# Nine fine, evenly spaced horizontal/lengthwise blades.
inner_top = y1 + 3
inner_bottom = y2 - 3
for idx in range(9):
    y = round(inner_top + idx * (inner_bottom - inner_top) / 8)
    draw.line((x1 + 4, y, x2 - 4, y), fill=blade, width=1)

BASE_OUT.parent.mkdir(parents=True, exist_ok=True)
FINAL_OUT.parent.mkdir(parents=True, exist_ok=True)
image.save(BASE_OUT, "PNG", optimize=True)
image.save(FINAL_OUT, "PNG", optimize=True)
