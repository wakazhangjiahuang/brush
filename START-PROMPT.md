# $brush-creator-studio｜推荐启动 Prompt

使用 `$brush-creator-studio`，模式：{{A/B/AB}}，当前原稿见附件。  
先读取 `wakazhangjiahuang/brush/KB-MANIFEST.json`，严格按 `runtime_load_policy` 动态加载本次任务需要的最少文件，禁止全仓扫描、全量加载笔刷或重复加载规则。  
当前原稿优先；先完成 Complexity、Stage、Object / Material、Brush Role，再读取对应 Process DNA。  
通过 Registry 为每个 Role 检索最佳候选，每个 Role 只 shortlist 2–3 个，并只验证 shortlist native files。  
优先使用 `BRUSH-CAPABILITY-REGISTRY` 中 SHA 仍匹配的 VERIFIED / VERIFIED_METADATA 证据；文件名和 purpose_hint 仅用于候选发现。  
未验证候选保持 `PENDING_VALIDATION`，禁止因无法读取就直接判 `NEW`。  
先 Specialization，再 Merge；每个 REQUIRED Role 必须映射独立 Native Brush 或明确 `MERGE_PASS`。  
必须输出 `ROLE_TO_NATIVE_MATRIX`；若 Role 被大量压缩而缺少逐项 Merge 证据，返回 `UNDERCOVERAGE_REVIEW_REQUIRED`。  
Git LFS pointer 不得视为 native file；只为 shortlist 且会影响决策的候选解析 LFS。  
Mode B 必须先实际构建全部最终 `.brush` + 1 个完整 `.brushset`，然后才加载 V2 XLSX 模板生成项目流程表。  
交付前重新打开 `.brush`、`.brushset`、XLSX 和 ZIP；Brush / Brushset / XLSX / Final Native Brush 数量与名称必须闭环一致。  
任一原生文件缺失、结构失败或数量不一致，不得标记 `PACKAGE_PASS`，应返回真实 BLOCKED / FAILED 状态。  
目标是 **Minimal Complete Production Set**，禁止为了减少数量过度 Merge。  
无真实 Procreate 导入/绘制测试时，不得宣称 `FULL_PASS`。  
Mode A / AB 若请求 Photoshop 原生 `.abr` 而 Manifest 未声明可用外部 runtime，则返回 `PHOTOSHOP_NATIVE_RUNTIME_UNAVAILABLE`。
