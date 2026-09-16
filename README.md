# brush — `$brush-creator-studio V2.0.0` Remote Runtime KB

本仓库当前以 **`$brush-creator-studio V2.0.0`** 为最高兼容目标，同时保留已经完成的 Native Runtime、LFS、Capability Registry 与交付一致性增强。

## Runtime 第一入口

运行时第一步读取 `KB-MANIFEST.json`。

V2.0 canonical route 由以下顶层字段提供：
- `entrypoints`
- `process_dna`
- `source_directories`
- `resolver_policy`
- `routing`

即使调用端完全忽略 Manifest 的 `extensions`，V2.0 主链路也必须能够完成仓库解析。

`extensions` 仅提供条件加载、Native Runtime、LFS 和 artifact QA 等增强能力。

## Source of Truth

- `SKILL.md`：V2.0 系统执行链路、决策顺序、边界和失败行为。
- `KB-MANIFEST.json`：唯一 Runtime Router。
- `knowledge/RUNTIME-CONTRACT.md`：唯一 Acceptance / Gate Source。
- README 不是 Runtime Source of Truth。

## 关键结构

- `knowledge/`：规则、流程/笔刷索引和可复用 native capability evidence。
- `process-dna/`：cartoon / vintage branch baseline；Current Artwork 永远优先。
- `runtime/native_runtime.py`：Procreate `.brush/.brushset` inspect / build / validate，以及最终四方集合一致性验证。
- `templates/Procreate/Procreate新笔刷绘画操作流程_V2.xlsx`：唯一 canonical Mode B 模板。
- `插画师/`：仅按需调用的流程证据。
- `笔刷/`：单笔刷与 Git LFS brushset 资产。

## Mode B

Procreate Mode B 可执行 native delivery。最终结构交付要求：
`Expected Native Set = Delivered .brush Set = Brushset Member Set = XLSX Referenced Brush Set`。

没有真实 Procreate 导入/绘制测试时，只能达到结构层 `PACKAGE_PASS`，不得声称 `FULL_PASS`。

## Mode A / AB

当前仓库没有与 Procreate 等价完整的 Photoshop `.abr` native runtime/template/asset branch。

因此：
- Mode A 可做分析；请求 `.abr` 原生交付时返回 `PHOTOSHOP_NATIVE_RUNTIME_UNAVAILABLE`。
- Mode AB 可完成 Procreate 原生交付；Photoshop 原生交付仍返回 `PHOTOSHOP_NATIVE_RUNTIME_UNAVAILABLE`。

禁止为了兼容模式选项而伪造 `.abr`。

## 正常调用

用户通常只需要上传当前原稿并调用 `$brush-creator-studio V2.0.0`。推荐启动文本见 `START-PROMPT.md`。
