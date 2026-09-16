# brush — `$brush-creator-studio V2.0.0` Remote Runtime KB

本仓库是 `$brush-creator-studio V2.0.0` 的远程知识、流程证据、Procreate 原生笔刷资产、二进制物化桥与交付模板仓库。

## Runtime 入口

运行时第一步读取 `KB-MANIFEST.json`。

V2.0 canonical route 由以下字段提供：
- `entrypoints`
- `process_dna`
- `source_directories`
- `resolver_policy`
- `routing`

`extensions` 只提供增强能力，不改变 V2.0 主兼容目标。

`SKILL.md` 定义执行顺序与失败行为。  
`knowledge/RUNTIME-CONTRACT.md` 是唯一 Acceptance / Gate Source。  
README 不是 Runtime Source of Truth。

## 关键结构

- `knowledge/`：规则、索引和可复用 native evidence。
- `process-dna/`：cartoon / vintage 分支基线。
- `runtime/native_runtime.py`：Procreate 原生结构 inspect / build / validate。
- `runtime/binary_materialization.py`：二进制物化、brushset 成员提取、branch bundle 与 SHA256 manifest。
- `.github/workflows/procreate-native-bundle.yml`：GitHub Actions Binary Materialization Bridge。
- `templates/Procreate/Procreate新笔刷绘画操作流程_V2.xlsx`：唯一 canonical Mode B 模板。
- `插画师/`：按需调用的流程证据。
- `笔刷/`：单笔刷与 Git LFS brushset 资产。

## 为什么增加 Binary Materialization Bridge

普通 GitHub Connector 可以稳定读取仓库文本、Registry、元数据以及部分二进制的编码内容，但这不等于调用环境已经拿到一个可直接交给 native runtime 的本地 `.brush / .brushset / .xlsx` 文件路径。

因此 Mode B 在 Native Validation / Build 前增加 Binary Materialization Gate：

`Registry Shortlist`
→ `Binary Materialization`
→ `Native Validation`
→ `KEEP / ADJUST / DERIVE / NEW`
→ `.brush`
→ complete `.brushset`
→ XLSX
→ four-way set QA
→ ZIP

当直接本地二进制不可用时，优先使用 GitHub Actions artifact bridge，而不是立即返回 `BINARY_MATERIALIZATION_UNAVAILABLE`。

## Branch-scoped GitHub Actions artifacts

Workflow：`.github/workflows/procreate-native-bundle.yml`

Artifacts：
- `procreate-runtime-cartoon`
- `procreate-runtime-vintage`

每个 artifact 目标包含：
- 对应分支的 individual `.brush`；
- 对应 preferred `.brushset` 的真实 Git LFS bytes；
- preferred brushset 预提取出的 standalone `.brush` members；
- canonical Procreate V2 XLSX；
- `native-asset-manifest.json`（路径 / SHA256 / native status）；
- runtime scripts。

`mixed` 项目在确有需要时使用两个 branch artifacts，避免全仓大包。

## Load policy

禁止启动时全仓扫描。

Current Artwork 优先；先得到 Stage / Material / Brush Role，再按 Manifest 加载 Process DNA、Registry 和 shortlist。

只有 shortlist / native build 真正需要二进制时才进入 Binary Materialization Gate。

## Native Delivery contract

Mode B 最终必须真实交付：
- 全部 final `.brush`；
- 1 个完整 final `.brushset`；
- 1 个项目 Procreate XLSX；
- 1 个 final ZIP。

并要求：

`Expected Native Brush Set`
=
`Delivered .brush Set`
=
`Brushset Member Set`
=
`XLSX Referenced Brush Set`

没有真实 Procreate 导入/绘制测试时，可以达到结构层 `PACKAGE_PASS`，但不得声称 `FULL_PASS`。

## Capability boundary

Mode B（Procreate）具备仓库内 native runtime、binary materialization bridge、template 与 native assets。

当前仓库仍没有与之等价的 Photoshop `.abr` native runtime/template/asset branch；A / AB 的 Photoshop 原生交付边界以 Manifest 与 Runtime Contract 为准。

## 用户正常调用

通常只需上传当前原稿并调用 `$brush-creator-studio V2.0.0`。推荐启动文本见 `START-PROMPT.md`。
