# 璀璨家的空气答案 EP01 · 最终提示词集

## 统一拼接规则

下列 5 个 AI 生成资产均为无参考图的新图生成，按各资产专属主体描述，加上统一品牌风格、排除项和风口锁词后提交。所有提示词均要求：`native vertical 9:16 full-frame portrait image, no crop guides or borders`，且不生成任何文字。

统一风格：

`photorealistic editorial architectural interior photography, restrained COLMO / Architectural Digest / Guanxia mood, refined, calm, premium, cinematic, high detail, realistic matte materials, palette of deep coffee brown + champagne gold + fog white, warm restrained natural lighting, no orange cast, no HDR halo`

统一排除项：

`No people. No product branding. No text, caption, label, watermark, logo, brand name, or signage. Do not include any wall-mounted air conditioner, split AC unit, outdoor condenser, external AC unit, round or circular ceiling vent, wooden boardwalk, showroom display stand, product display platform, clutter, oversaturation, distortion, or extra vents. No internal blades, separators, fins, ribs, cells, squares, bars, or repeated modules.`

所有相关图末尾原样追加：

`concealed horizontal linear slot vent, ultra-long narrow slit, single straight continuous line shape, flush-mounted flat with the ceiling surface, NO vertical grille bars, NO square or rectangular louvers, NO diffuser fins`

## EP01_01 · 客厅＋层高标尺底图

`Ultra-high-end modern Chinese living-dining room at golden hour, with generous visible ceiling height. Floor-to-ceiling windows with restrained soft daylight; fog-white walls; deep coffee-brown wood; champagne-gold metal accents; matte stone floor; minimalist designer sofa and low table. Wide architectural view with stable verticals. Keep the LEFT third calm and low-detail as usable negative space for a later height-scale overlay. Ceiling and one air outlet clearly visible. Show exactly ONE concealed horizontal black shadow-gap slot in the ceiling, extremely long, razor-thin and perfectly continuous from end to end. It must read as a single unbroken architectural slit, not a grille, register, diffuser, or array.`

## EP01_02 · 客厅空镜（换机位）

`The same premium modern Chinese living-dining visual language, but from a distinctly different wider camera angle, calm, airy, and elegant. Open-plan living-dining room with fog-white walls, deep coffee-brown wood volumes, subtle champagne-gold accents, matte stone, floor-to-ceiling glass, understated designer furniture. Wider diagonal view than shot 01. Show the ceiling clearly. Leave the LOWER third visually calm and low-detail for later on-screen captions. Show exactly ONE concealed horizontal black shadow-gap slot running across the ceiling, extremely long, razor-thin and perfectly continuous.`

## EP01_03 · 局部边吊剖面示意（最终为第2次生成）

`Clean, architecturally plausible isometric 3D cutaway explaining a localized perimeter ceiling bulkhead along one wall while the large central ceiling remains at the original full height. Along ONE wall, a shallow localized soffit conceals one generic slim horizontal ducted indoor unit and simple pipes. The central ceiling plane is clearly higher and uninterrupted. Conceptual, unbranded, with no technical dimensions. Premium minimalist vector-like 3D architectural model, matte materials, simplified geometry, plain fog-white studio background, plain matte pale-stone floor, no wood-slat wall. Object occupies the middle 50–60%; generous blank space at upper-left, center, and right for later labels. The entire illustration contains EXACTLY ONE visible black slot, located only on the lower/front face of the localized soffit. It is an ultra-long razor-thin unbroken horizontal shadow gap. There are zero other black slits, zero short slots, zero secondary openings, zero grilles, zero panels with stripes, and zero repeated lines anywhere else. The concealed indoor unit is a plain closed rectangular dark-coffee box without visible intake or outlet openings.`

首轮剔除原因：剖面内出现额外短缝；最终版本通过加强 `EXACTLY ONE visible black slot / zero short slots / zero secondary openings` 后重跑获得。

## EP01_05 · 完工客餐厅空镜

`Finished high-end open-plan living-dining room that communicates airy ceiling height and an uninterrupted, carefully integrated ceiling. Premium modern Chinese residence; open living and dining zones; fog-white plaster; deep coffee-brown wood; matte pale stone; restrained champagne-gold accents; elegant low furniture; floor-to-ceiling glazing. Architectural wide view from the living area toward dining. Give the upper half to the clean uninterrupted ceiling and preserve a strong sense of height. Show exactly ONE concealed horizontal black shadow-gap slot integrated into the ceiling edge, extremely long, razor-thin, perfectly straight and continuous.`

## EP01_07 · 大宅片尾底图

`Grand yet restrained open living-dining room in a large modern Chinese residence at dusk, suitable for the final brand title card. Expansive residence with strong spatial scale, floor-to-ceiling glass, fog-white plaster, deep coffee-brown wood, matte stone, sparse elegant furniture, subtle champagne-gold metal accents. A symmetrical or near-symmetrical architectural view that feels conclusive. Show the ceiling and integrated slot clearly. Keep the LOWER-CENTER area intentionally dark, calm, and low-detail for later two-line end-title typography; no furniture highlight or plant crosses this text-safe area. Dusk outside, warm restrained champagne-gold ambient light inside. Show exactly ONE concealed horizontal black shadow-gap slot naturally integrated into the ceiling, extremely long, razor-thin, perfectly straight and continuous.`

## 纯图形卡和带字版

- EP01_00、EP01_06 为 1080×1920 程序渲染，无 AI 生图提示词。
- EP01_03、EP01_07 的 `withtext` 由对应 `clean` 原图本地叠字得到，没有独立生成背景。
- 中文标题字体文件 `assets/fonts/title_zh.otf` 未随任务提供，因此本次统一使用系统 `STHeiti Medium` 作为替代；拉丁字符使用 Arial。
