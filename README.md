# brush — $brush-creator-studio V2.0.0 远程知识库

本仓库是 `$brush-creator-studio` 的 canonical remote knowledge base。V2 的核心目标从“尽量减少笔刷数量”升级为 **Minimal Complete Production Set（最小完整生产笔刷集合）**：完整覆盖实际生产工序、对象/材质与专业笔刷行为，同时删除真正冗余。

## V2 关键入口
- `SKILL.md`：与安装包高度一致的 canonical V2 规则。
- `KB-MANIFEST.json`：运行时入口与精确路径。
- `START-PROMPT.md`：推荐启动 Prompt。
- `knowledge/PROCESS-STAGE-TAXONOMY.json`：完整生产工序审计。
- `knowledge/MATERIAL-TAXONOMY.json`：对象/材质覆盖。
- `knowledge/COMPLEXITY-RULES.json`：复杂度与欠覆盖复核。
- `knowledge/MERGE-GATE.md`：禁止“能画=应该合并”的多维 Merge Gate。
- `knowledge/BRUSH-CAPABILITY-REGISTRY.json`：仅保存真实 native metadata / 软件验证能力证据。
- `process-dna/`：卡通/复古基础 Process DNA。
- `templates/Procreate/Procreate新笔刷绘画操作流程_V2.xlsx`：V2 有效工作流模板。

## Mode B 原生交付硬约束
Procreate ZIP 必须实际包含：
1. 全部最终交付 `.brush`；
2. 1 个包含完整最终家族的 `.brushset`；
3. 项目专属 XLSX。

缺任一项不得标记 `PACKAGE PASS`。参数映射、说明文档或改扩展名文件不能替代原生笔刷。

## 数量规则
数量仍然动态产生，但不允许过度合并。正常完整插画若最终 Brush Role 少于 8 个，默认触发 `UNDERCOVERAGE_REVIEW_REQUIRED`，除非能证明项目确属极简且工序/材质 100% 覆盖。复杂多角色、多材质、毛发、服饰或场景应执行更严格检查。

## 真实性边界
- 文件名 / purpose_hint 仅用于发现候选；
- Git LFS pointer 不是 `.brushset` 原生内容；
- 未经过真实导入/绘制验证不得声称 FULL PASS；
- 严格区分 `VERIFIED / VERIFIED_METADATA / INFERRED / PROPOSED / UNVERIFIED`。
