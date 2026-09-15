# $brush-creator-studio V2.0.0｜推荐启动 Prompt

使用 `$brush-creator-studio` V2.0.0，模式：{{A＝Photoshop｜B＝Procreate｜AB＝双模式}}。
当前插画原稿见附件。

## GitHub 知识库
先读取：`https://github.com/wakazhangjiahuang/brush`
按 `KB-MANIFEST.json` 自动加载 Artist Profile、Process Registry、Process DNA、Brush Registry、Brush Capability Registry、Process Stage Taxonomy、Material Taxonomy、Complexity Rules、Merge Gate、Runtime Contract 与注册模板。
**禁止要求我重复上传仓库已有资料、笔刷、录播或模板。**

## 执行链路
`原稿审计 → Artwork Complexity Profile → Style / Color / Material DNA → Full Production Stage Decomposition → Process DNA → Object / Material Map → Brush Role Inventory → Required Role Coverage Matrix → Existing Brush Matching → Native Metadata / Capability Validation → KEEP / ADJUST / DERIVE / NEW → Brush Specialization Gate → Merge Eligibility Gate → Redundancy Check → Undercoverage Review → Complexity Sanity Check → Dynamic Quantity Decision → Native Brush Build → Native Delivery Gate → 项目专属 XLSX → QA → ZIP`

## 核心数量原则
最终目标是 **Minimal Complete Production Set（最小完整生产笔刷集合）**，不是“最少笔刷”。
- 禁止预设固定最终数量；
- 也禁止为了减少数量而过度合并；
- 正常完整插画若最终 Brush Role 少于 8 个，必须触发 `UNDERCOVERAGE_REVIEW_REQUIRED`，除非能证明项目确属极简并且所有 REQUIRED 工序与材质均完整覆盖；
- 多角色、多材质、毛发、服饰、纹理或复杂场景应执行更严格的欠覆盖检查。

## 完整工序审计
每个生产阶段必须标记 `REQUIRED / OPTIONAL / NOT_APPLICABLE`。
至少审计：草稿/结构、主线稿、细节线、底色、透明铺色、局部色、湿边/晕染、底纹/颗粒、阴影、干刷、毛发/头发、服饰/材质、图案/装饰、场景、精细刻画、高光、精修叠色、最终收口；根据当前原稿动态增加其他阶段。

## Object / Material Coverage
对角色、动物毛发、服饰、装扮、材质、场景分别建立覆盖关系。可见的专用材质行为不得因为通用笔刷“勉强能画”而被删除。

## Merge 硬约束
只有在 Shape / Grain / Edge / Opacity / Pressure / Wet-Dry Behavior / Size Range / Stroke Rhythm / 参数切换成本 / 工作效率 / 成品质量 / 材质专属性均兼容时才允许 `MERGE_PASS`。
“某支笔刷也能完成另一个动作”不得作为合并依据。

## 真实性
严格区分 `VERIFIED / VERIFIED_METADATA / INFERRED / PROPOSED / UNVERIFIED`。
禁止虚构笔压、倾斜习惯、Brush Studio 参数、导入结果或实测手感。
已有候选但未验证时标记 `PENDING_VALIDATION`，禁止因无法验证直接判 `NEW`。

## Mode B｜Procreate 原生交付硬约束
最终 ZIP **必须实际包含**：
1. **全部最终交付的原生 `.brush` 文件**；
2. **1 个原生 `.brushset`，且必须包含完整最终笔刷家族**；
3. `[项目名]｜Procreate 新笔刷绘画操作流程.xlsx`。

禁止出现：
- 只有 XLSX、没有 `.brush`；
- 有 `.brush`、没有 `.brushset`；
- XLSX 引用了未实际交付的笔刷；
- 用修改扩展名伪造 `.brush / .brushset`；
- 用参数说明文件替代原生笔刷。

只要 `.brush / .brushset / XLSX` 任一缺失，就不得标记 `PACKAGE PASS`；应返回 `NATIVE_OUTPUT_BLOCKED / NATIVE_BUILD_FAILED / DELIVERY_TEMPLATE_MISSING` 等真实状态。

## FINAL_COUNT Hard Gate
只有以下全部 PASS 后才能输出 `FINAL_COUNT`：
`Stage Coverage + Material Coverage + Object Coverage + Candidate Validation + Specialization + Merge + Redundancy + Undercoverage + Complexity Sanity`。

每支最终交付笔刷必须记录：
`对应生产阶段 + Brush Role + 对象/材质 + 为什么需要 + 已有候选 + KEEP/ADJUST/DERIVE/NEW + 是否可合并 + 不合并原因 + 证据状态`。

XLSX 中每个 REQUIRED 阶段都必须映射到真实交付笔刷，禁止占位笔刷。

---

## 极简版

使用 `$brush-creator-studio` V2.0.0，模式 B（Procreate），原稿见附件。先读取 `wakazhangjiahuang/brush/KB-MANIFEST.json`，按仓库规则完成完整生产阶段、对象/材质、Brush Role、现有笔刷验证、专用化、Merge、Redundancy、Undercoverage 与 Complexity Sanity，再动态确定 **Minimal Complete Production Set**。正常完整插画若最终 Role 少于 8 个必须触发欠覆盖复核，禁止为减少数量过度合并。最终 ZIP 必须实际包含全部 `.brush` + 1 个包含完整家族的 `.brushset` + 项目专属 XLSX；任何一项缺失都不得标记 PACKAGE PASS。严格区分 VERIFIED / VERIFIED_METADATA / INFERRED / PROPOSED / UNVERIFIED，禁止虚构参数和实测结果。
