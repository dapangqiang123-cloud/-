# EP01 格栅风口修正版 · 编辑提示词

本轮使用内置图像编辑模式。每张图的第1张输入均为原 `clean` 底图，第2张输入为仅包含用户前4张风口参考的 `vent_reference_board.png`。装修参考板只用于视觉分析，没有作为待复制的设计输入。

## 通用编辑规则

`Replace ONLY the existing single black ceiling slit with one recessed horizontal long-strip air-conditioning grille: a slim elongated rectangular frame integrated flush into the ceiling or soffit; inside it, clearly visible, closely packed, evenly spaced very fine horizontal louver blades run continuously along the long axis. The assembly must read as one narrow rectangular HVAC grille, not as several independent slots.`

`NOT a single black shadow gap. NO vertical crossbars or upright grille bars. NO square cells, checkerboard mesh, perforations, diffuser fins, or square/rectangular louvers.`

`Preserve the exact room or diagram, camera angle, crop, 9:16 framing, geometry, furniture, lighting, shadows, colors, materials, negative-space areas, and all non-vent details. Change only the vent. No new objects, people, text, logo, or watermark.`

## 分镜差异

- **EP01_01**：保持原风口的纵深透视和左侧标尺留白；内部细百叶沿纵深长轴收敛。
- **EP01_02**：保持原斜向天花轴线和下三分之一字幕留白。首轮只有3条疏线，第二轮要求 `approximately 8–10 closely packed fine horizontal louver blades` 后通过。
- **EP01_03**：只修改局部边吊盒体正面的风口；保持内机、铜管、原顶和剖面比例不变。
- **EP01_05**：保持正视、近水平长条位置及完整天花构图；只将单黑缝替换为密集横向百叶格栅。
- **EP01_07**：保持暮色大宅和下中部片尾文字安全区。模型连续3次只生成3条疏线，最终使用确定性局部绘制：擦除既有风口窄带，在原位置绘制薄矩形外框和9条等距横向细百叶；风口以外像素不做程序处理。

## 装修参考的非抄袭规则

用户第5至10张图片只拆解为以下抽象风格特征：暖白墙顶、温润木色、自然侧光、适量绿植、低饱和软装、中古与现代混合的松弛感、适度生活痕迹。禁止复制任何一张参考图的具体户型结构、固定家具组合、墙面造型、陈设位置或标志性构图。本轮根据“其他空间、构图保持不变”的要求，没有主动重做现有房间。
