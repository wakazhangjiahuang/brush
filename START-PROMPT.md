# $brush-creator-studio V2.0.0｜推荐启动 Prompt

使用 `$brush-creator-studio V2.0.0`，模式：{{A/B/AB}}，当前原稿见附件。  
先读取 `wakazhangjiahuang/brush/KB-MANIFEST.json`，按 V2.0 `entrypoints / process_dna / routing / resolver_policy` 解析本次所需资料，禁止全仓扫描。  
当前原稿优先；先完成 Stage / Object / Material / Brush Role，再检索 Registry 候选，每个 Role 只验证最佳 shortlist。  
先 Specialization 再 Merge；复杂项目禁止为了减少数量过度合并，必要时触发 `UNDERCOVERAGE_REVIEW_REQUIRED`。  
Mode B 在 Native Validation / Build 前必须先通过 **Binary Materialization Gate**：把 shortlist `.brush`、必要 `.brushset` 和 canonical V2 XLSX 取得为真实可用的本地二进制文件。  
如果直接 GitHub binary 物化不可用，必须先尝试 Manifest `extensions.binary_materialization_bridge` 指定的 GitHub Actions artifact（`procreate-runtime-cartoon` / `procreate-runtime-vintage`）；不得因为 Connector 只能读文本/base64 就立即结束任务。  
若使用 preferred `.brushset` 内成员，优先使用 bridge artifact 中已预提取的 standalone `.brush`，或调用 `runtime/binary_materialization.py` 提取后再进入 `derive_or_build_brush`。  
Mode B 必须实际生成全部最终 `.brush` + 1 个完整 `.brushset` + 项目 Procreate XLSX；`Expected Native / Delivered Brush / Brushset Members / XLSX References` 四方名称集合必须闭环一致。  
Git LFS pointer 不能当 native file；所有 bridge binary 应核对 SHA256/native structure。  
仅当本地路径、GitHub Actions artifact bridge、必要的本地 Git LFS 路由均失败后，才返回 `NATIVE_OUTPUT_BLOCKED / BINARY_MATERIALIZATION_UNAVAILABLE`。  
无真实 Procreate 导入/绘制验证时不得标记 `FULL_PASS`。  
Mode A / AB 若请求 Photoshop 原生 `.abr` 而没有可用外部 native runtime，则返回 `PHOTOSHOP_NATIVE_RUNTIME_UNAVAILABLE`。
