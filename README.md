# brush

`$brush-creator-studio` 远程笔刷 / 插画师流程知识库。

## 目录

- `KB-MANIFEST.json`：Skill 远程解析入口，运行时优先读取。
- `knowledge/ARTIST-PROFILE.json`：插画师技术工作流档案（不存储或推断不必要的个人身份信息）。
- `knowledge/PROCESS-REGISTRY.json`：卡通 / 复古绘画过程素材索引。
- `knowledge/BRUSH-REGISTRY.json`：`.brush` / `.brushset` 笔刷资产索引。
- `knowledge/RUNTIME-CONTRACT.md`：`$brush-creator-studio` GitHub Resolver 运行合同。
- `插画师/`：卡通、复古录播与过程证据。
- `笔刷/`：卡通单笔刷、复古单笔刷、套装笔刷。

## 正常调用方式

用户通常只需要提供当前插画原稿，并调用 `$brush-creator-studio`。Skill 应先读取 `KB-MANIFEST.json`，再按索引选择对应的插画师流程和笔刷候选；仓库已经存在的笔刷和流程资料不应要求用户重复上传。

## 重要边界

- `.brushset` 使用 Git LFS 管理；Git API 返回约 133B 的对象时通常是 LFS pointer，不代表原文件损坏。
- 文件名只能作为笔刷用途的候选提示，不能据此虚构 Procreate / Photoshop 参数。
- 未经过实际软件导入、绘制或原生验证的参数与行为必须标记为 `PROPOSED / INFERRED / UNVERIFIED`。
- 原生 `.brush/.brushset/.abr` 只有完成目标软件验证后才可标记为 `FULL PASS`。
