from pathlib import Path
import json


SOURCE = Path("/Users/weipeilong/Downloads/assets_manifest.json")
OUTPUT = Path("/Users/weipeilong/Desktop/Aaaaaaa/AI工作台/06_codex项目/璀璨codex任务/output/EP01_grille_v2/assets_manifest_grille_v2.json")

data = json.loads(SOURCE.read_text(encoding="utf-8"))
brand = data["brand_spec"]

old_exclusions = brand.get("global_exclusions", [])
drop_phrases = (
    "vertical grille bars on the vent",
    "any round, square, or multi-slot ceiling vent style other than the locked single linear slot",
)
brand["global_exclusions"] = [item for item in old_exclusions if item not in drop_phrases]
brand["global_exclusions"].extend([
    "single black-line shadow-gap slot vent without visible grille blades",
    "vertical grille bars / upright dividers inside the vent",
    "square cells, checkerboard mesh, perforated diffuser, or square louvers",
])

brand["vent_style_lock"] = {
    "cn": "吊顶内嵌横向长条格栅风口 / 细长矩形 / 内部均匀横向细格栅或百叶条 / 与吊顶一体化融合 / 不要单一黑线式缝隙 / 不要竖向格栅 / 不要方形百叶",
    "en": "recessed horizontal long-strip grille vent, slim elongated rectangular frame integrated flush with the ceiling, clearly visible closely packed evenly spaced fine horizontal louver blades running continuously along the long axis, NOT a single black shadow-gap slit, NO vertical grille bars or upright dividers, NO square cells, NO checkerboard mesh, NO square or rectangular diffuser louvers",
    "apply_to": "每一张出现吊顶或出风口的图（EP01_01、EP01_02、EP01_03、EP01_05、EP01_07）均强制执行；内部百叶必须沿风口长边延伸并呈密集均匀横线。",
}

brand["reference_images_note"] = (
    "风口参考使用用户本轮提供的前4张图片，仅参考长条矩形外框与内部横向细百叶结构；"
    "第5至10张仅参考暖白、木色、自然光与中古松弛感，不复制具体户型、家具组合或陈设。"
)

data["output_rules"]["scene_size_policy"] = (
    "All delivered scenes and diagrams are native portrait 9:16 assets; do not create or retain a 3:2 base, and do not upscale or outpaint."
)
data["revision"] = {
    "version": "grille_v2",
    "date": "2026-08-12",
    "reason": "User replaced the earlier single-slot vent requirement with an integrated horizontal fine-grille vent based on supplied references.",
    "source_manifest": str(SOURCE),
}

OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
