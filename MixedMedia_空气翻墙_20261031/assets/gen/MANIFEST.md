# 阶段 1：生图素材清单

日期：2026-10-31。依据项目 `BRIEF.md` 及本轮用户的 10 项素材清单执行。

生成方式：全部使用内置 `image_gen / imagegen`，每张单独生成；生成完成后逐张从默认生成目录复制至本目录。未使用 CLI/API 生图替代。

本阶段仅交付素材与说明，未编写或修改成片引擎。

## 文件、尺寸与背景

尺寸为实际 PNG 像素宽 × 高，未经放大、锐化或连续编辑。

| 文件 | 尺寸（px） | 模式／背景 | 内容 |
|---|---:|---|---|
| [paper_texture.png](paper_texture.png) | 940 × 1672 | RGB／不透明米白暖色底 | 米白细纤维纸底，原生竖版输出；平均 RGB 约 (243,239,232)，接近目标色 #F5F2ED。 |
| [window_closed.png](window_closed.png) | 1024 × 1536 | RGBA／真实透明 Alpha | 现代中国家居关窗摄影切片，闭合窗扇、把手、纱帘；暖光、无室外景物。 |
| [wall_cutaway.png](wall_cutaway.png) | 1254 × 1254 | RGBA／真实透明 Alpha | 石膏纸面／纤维保温层／纸板背层的可撕开截面拼贴，示意用途。 |
| [duct_paper.png](duct_paper.png) | 1254 × 1254 | RGBA／真实透明 Alpha | 中空纸质圆风道，香槟金边缘，三分之四视角。 |
| [core_plates.png](core_plates.png) | 1254 × 1254 | RGBA／真实透明 Alpha | 5 张咖金交替、错位层叠薄板；抽象热交换示意，不代表真实内部结构。 |
| [airflow_strip_warm.png](airflow_strip_warm.png) | 2098 × 749 | RGBA／真实透明 Alpha | 连续暖金纸条、棕暖色背面、柔和曲线；完整两端，供气流动画合成。 |
| [airflow_strip_cool.png](airflow_strip_cool.png) | 2172 × 724 | RGBA／真实透明 Alpha | 连续橄榄／冷灰绿纸条、柔和曲线；完整两端，供气流动画合成。 |
| [filter_sheet.png](filter_sheet.png) | 1254 × 1254 | RGBA／真实透明 Alpha | 薄滤纸、细纤维纹理、轻卷角；独立物件，无机械外框。 |
| [dust_stickers.png](dust_stickers.png) | 1254 × 1254 | RGBA／真实透明 Alpha | 一张图包含多个互不相连的深咖颗粒贴纸，可整体使用或后续拆分。 |
| [table_surface.png](table_surface.png) | 941 × 1672 | RGB／不透明米白暖色底 | 浅暖木台面俯视局部，满幅无杂物，为后续官方产品及落地阴影提供底面。 |

## 画幅说明

`paper_texture.png` 按 9:16 竖版提示生成，内置工具原生输出 940×1672；与严格 9:16 的宽高比相差约 0.053%。保留原生输出，不通过放大或锐化伪造清晰度。后续合成到 1080×1920 画幅时可按 cover 使用。
`table_surface.png` 为 941×1672 竖版局部。其他透明物件按完整轮廓与可合成留白构图，无须统一画幅。

## 检查记录

- 10 个 PNG 均已成功解码，文件名与清单对应。
- 8 张物件均具有真实 Alpha 通道，含全透明背景像素；纸底与台面为不透明 RGB。
- 已查看每张生成结果，并将透明素材叠放到 #F5F2ED 底色上进行整体目检。
- 窗框、闭合把手、墙体撕口、管口、薄板边缘、纸纤维和气流条轮廓可辨认。
- 无空调外机、Mini 机身、Logo、山野户外、人物脸、大标题或其他生成文字。
- 交换芯可辨认 5 层，符合 5–7 层要求；仅为抽象纸板示意。
- 素材为静态 PNG；气流弯曲、撕墙、层叠装配等动态需后续阶段实现。

## 生成提示词

每张实际提交的完整提示词及透明背景参数见 [PROMPTS.json](PROMPTS.json)。未进行多轮退化编辑。

## 文件校验

| 文件 | 完全透明像素占比 | SHA-256 |
|---|---:|---|
| paper_texture.png | 0.00% | `667268258dee9715428658e432ac78f7e80692548b1a9ea795ad3ff8293dedc7` |
| window_closed.png | 27.83% | `c264bf5f5ec62df3bbd8d4bda4608bfb46e81324b6ca2beaf08270e720725caf` |
| wall_cutaway.png | 48.55% | `93cc934c0b97e126dd3a0d6e237bb855ff1d673cc9005f7ee671a766646d93b7` |
| duct_paper.png | 60.60% | `bfbb949c48c2f935d3a359c033a361c3241abc87a3cd77ad5c87b8c4f40f4000` |
| core_plates.png | 55.40% | `bd03313ad62a90d07b80d5d88b88e6e6fdf49cc96e41c985fc06236b132f7ee2` |
| airflow_strip_warm.png | 84.39% | `af0b1f72bcb24c536327eb4a4643d50e28bd55982189a2980984a4bb1d8083e7` |
| airflow_strip_cool.png | 82.89% | `bc734894e2fbfa410398d2bb0e6b416445232abc04c2dc25d7465c3c5bf74616` |
| filter_sheet.png | 57.25% | `572b6132aa3d63542343532a0c5aae96ebcc9b5903efba3ca46d3630220bd548` |
| dust_stickers.png | 88.88% | `1f5fd8dd116289b5234360a34d790e3cda2da5e0783b44c4331b5b61546a0f66` |
| table_surface.png | 0.00% | `baf5251efd5fccddae8f8a7b315b81053bd6477193516651dfc98e46104b2b68` |
