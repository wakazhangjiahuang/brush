# $brush-creator-studio 启动 Prompt

## 推荐极简版

使用 `$brush-creator-studio`。根据我本次上传的插画原稿执行笔刷分析与创建；先通过 GitHub 读取 `wakazhangjiahuang/brush` 的 `KB-MANIFEST.json`，自动加载插画师工作流、绘画过程与笔刷索引，不要让我重复上传仓库里已有资料。默认根据原稿判断卡通 / 复古分支；若我指定 A / B / AB，则按指定模式执行。严格区分 VERIFIED / INFERRED / PROPOSED / UNVERIFIED，禁止虚构 Procreate / Photoshop 参数或软件测试结果。

## Procreate 模式 B 极简版

使用 `$brush-creator-studio`，模式 B（Procreate）。原稿见附件。先读取 GitHub `wakazhangjiahuang/brush/KB-MANIFEST.json` 并自动调用仓库中的插画师流程与笔刷资料；执行原稿分析 → Process DNA → Brush DNA → 现有笔刷 KEEP/ADJUST/DERIVE/NEW 匹配 → Procreate 参数映射 → 验证状态 → Brush Pack / Mapping / 上色流程。禁止要求我重复上传仓库已有资料，禁止虚构参数。

## 预期用户输入

正常情况下只需要：

1. 本次插画原稿；
2. 上述启动 Prompt；
3. 可选：指定 A / B / AB 或指定卡通 / 复古分支。
