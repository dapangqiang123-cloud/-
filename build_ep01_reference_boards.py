from pathlib import Path
from PIL import Image, ImageOps, ImageDraw


OUT = Path("/Users/weipeilong/Desktop/Aaaaaaa/AI工作台/06_codex项目/璀璨codex任务/output/EP01_grille_v2/references")
OUT.mkdir(parents=True, exist_ok=True)

VENT = [
    Path("/var/folders/nz/ln59_g0j4jz7dpl9yp1xqz5c0000gn/T/codex-clipboard-f61b6a68-db8f-4f02-a724-89f2ad9176a5.png"),
    Path("/var/folders/nz/ln59_g0j4jz7dpl9yp1xqz5c0000gn/T/codex-clipboard-6c842a16-b117-4525-83dd-8f81a6df0847.png"),
    Path("/var/folders/nz/ln59_g0j4jz7dpl9yp1xqz5c0000gn/T/codex-clipboard-1063cec9-2fd1-4820-98d4-e4f46031427c.png"),
    Path("/var/folders/nz/ln59_g0j4jz7dpl9yp1xqz5c0000gn/T/codex-clipboard-a319f3b4-f153-4e4c-acab-e4783e3d4b9a.png"),
]

DECOR = [
    Path("/var/folders/nz/ln59_g0j4jz7dpl9yp1xqz5c0000gn/T/codex-clipboard-482732c2-5695-40f2-b96e-d989f4874c0e.png"),
    Path("/Users/weipeilong/Pictures/常用视觉库.library/images/MO5WMZ9P6V9UA.info/趁着不老，放松点，享受生活 PART-1_4_脆皮老岳又破防了_来自小红书网页版.jpg"),
    Path("/Users/weipeilong/Pictures/常用视觉库.library/images/MO5WMZ9PQBHZF.info/亲子宅的松弛感天花板_2_脆皮老岳又破防了_来自小红书网页版.jpg"),
    Path("/Users/weipeilong/Pictures/常用视觉库.library/images/MO5WMZ9PFDJEK.info/谁懂啊中古风的美，真的只有0次和无数次_5_杭州装修Nini_来自小红书网页版.jpg"),
    Path("/Users/weipeilong/Pictures/常用视觉库.library/images/MO5WMZ9PUCKLW.info/IMG_7089.jpg"),
    Path("/Users/weipeilong/Pictures/常用视觉库.library/images/MO5WMZ9PGYSQ0.info/IMG_7087.jpg"),
]


def board(paths, cols, rows, output):
    canvas_w, canvas_h = 1800, 1200
    gutter = 18
    cell_w = (canvas_w - gutter * (cols + 1)) // cols
    cell_h = (canvas_h - gutter * (rows + 1)) // rows
    canvas = Image.new("RGB", (canvas_w, canvas_h), "#F0EDE8")
    draw = ImageDraw.Draw(canvas)
    for idx, path in enumerate(paths):
        row, col = divmod(idx, cols)
        x = gutter + col * (cell_w + gutter)
        y = gutter + row * (cell_h + gutter)
        image = Image.open(path).convert("RGB")
        tile = ImageOps.fit(image, (cell_w, cell_h), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
        canvas.paste(tile, (x, y))
        draw.rectangle((x, y, x + cell_w - 1, y + cell_h - 1), outline="#3B2F2C", width=3)
    canvas.save(output, "PNG", optimize=True)


board(VENT, 2, 2, OUT / "vent_reference_board.png")
board(DECOR, 3, 2, OUT / "decor_reference_board.png")
