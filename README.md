# brush — `$brush-creator-studio` Remote Runtime KB

本仓库是 `$brush-creator-studio` 的远程知识、流程证据、Procreate 原生笔刷资产与交付模板仓库。

## Runtime 入口
运行时第一步只读取 `KB-MANIFEST.json`。Manifest 是唯一 Runtime Router，负责：
- mode capability；
- branch routing；
- conditional load policy；
- Git LFS policy；
- native runtime；
- delivery template；
- artifact contract。

`SKILL.md` 只定义执行顺序与失败行为。  
`knowledge/RUNTIME-CONTRACT.md` 是唯一 Acceptance / Gate Source。

## 关键结构
- `knowledge/`：规则、索引和可复用 native evidence。
- `process-dna/`：cartoon / vintage 分支基线。
- `runtime/native_runtime.py`：Procreate 原生结构 inspect / build / validate。
- `templates/Procreate/Procreate新笔刷绘画操作流程_V2.xlsx`：唯一 canonical Mode B 模板。
- `插画师/`：按需调用的流程证据。
- `笔刷/`：单笔刷与 Git LFS brushset 资产。

## Load policy
禁止启动时全仓扫描。  
Current Artwork 优先；先得到 Stage / Material / Brush Role，再按 Manifest 条件加载 Process DNA、Registry、shortlist native files 和 delivery template。

## Capability boundary
Mode B（Procreate）具备仓库内 native runtime + template + native assets。  
当前仓库没有与之等价的 Photoshop `.abr` native runtime/template/asset branch；A / AB 的 Photoshop 原生交付边界以 Manifest 与 Runtime Contract 为准。

## 用户正常调用
通常只需上传当前原稿并调用 `$brush-creator-studio`。推荐启动文本见 `START-PROMPT.md`。
