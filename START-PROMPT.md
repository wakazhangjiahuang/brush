# $brush-creator-studio 启动 Prompt

## 推荐极简版

使用 `$brush-creator-studio`。根据我本次上传的插画原稿执行笔刷分析与创建；先通过 GitHub 读取 `wakazhangjiahuang/brush` 的 `KB-MANIFEST.json`，自动加载插画师工作流、绘画过程与笔刷索引，不要让我重复上传仓库里已有资料。默认根据原稿判断卡通 / 复古分支；若我指定 A / B / AB，则按指定模式执行。严格区分 VERIFIED / INFERRED / PROPOSED / UNVERIFIED，禁止虚构 Procreate / Photoshop 参数或软件测试结果。

**最重要：笔刷数量必须是 `Process DNA → Brush Function Clustering → Existing Brush Matching / Validation → KEEP / ADJUST / DERIVE / NEW → Merge / Redundancy Check` 全部完成后的结果，不是预设目标；若关键现有候选笔刷尚未解析或验证，只能标记 `PROVISIONAL_COUNT / PENDING_VALIDATION`，禁止提前输出 `FINAL_COUNT` 或因无法验证而直接判定 `NEW`。**

## Procreate 模式 B 极简版

使用 `$brush-creator-studio`，模式 B（Procreate）。原稿见附件。先读取 GitHub `wakazhangjiahuang/brush/KB-MANIFEST.json` 并自动调用仓库中的插画师流程、绘画过程、笔刷索引与已注册交付模板；执行：

`原稿分析 → Process DNA → Brush Function Clustering → Required Function Coverage Matrix → Existing Brush Matching → Existing Brush Validation → KEEP / ADJUST / DERIVE / NEW → Merge / Redundancy Check → Dynamic Quantity Decision → Procreate 原生笔刷生成 → 项目专属 XLSX → QA → ZIP`。

禁止要求我重复上传仓库已有资料，禁止虚构参数。存在候选笔刷但行为尚未验证时必须标记 `PENDING_VALIDATION`；关键候选资产仍可能影响最终数量时，只能输出 `PROVISIONAL_COUNT` 或 `QUANTITY_DECISION_BLOCKED`，不得宣称最终笔刷数量已确定。

## 预期用户输入

正常情况下只需要：

1. 本次插画原稿；
2. 上述启动 Prompt；
3. 可选：指定 A / B / AB 或指定卡通 / 复古分支。
