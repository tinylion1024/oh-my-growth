# Growth Master 改进状态

## 更新时间
2026-06-06

## 本轮完成的修复

| 类别 | 修复内容 | 结果 |
|------|----------|------|
| CLI 可用性 | `assess` 输入契约与清晰度评估打通 | 示例命令可返回可行动结果 |
| 检索质量 | 玩法/理论检索改为索引 + 中文短语匹配 + 同义词扩展 | `裂变`、`SaaS冷启动` 可召回相关玩法与理论 |
| 能力对齐 | 新增 `match` 命令，`validate` 改为读取真实文件内容 | CLI 能力与 README/manifest 对齐 |
| 外脑能力 | 新增 `diagnose` 与场景快捷入口，输出“判断/优先级/实验计划” | 更接近增长负责人工作流 |
| 索引维护 | 补充 `scripts/update-indexes.py`，同步计数与玩法描述 | 索引元数据可自动更新 |
| 验证脚本 | `validate-agents.py` 移除对 PyYAML 的硬依赖 | 默认标准库环境可运行 |
| 报告校验 | 修复首章节解析 bug | `validate` 可正确识别首个 `##` 章节 |
| 测试体系 | 用真实 Python 测试替代模拟 shell 统计，并覆盖外脑输出/结构化上下文 | 当前 `22/22` 自动化检查通过 |
| 文档一致性 | README、manifest、测试文档、Agent 描述同步到真实数据 | 关键数字和命令不再失真 |
| 输入与输出 | 新增结构化上下文注入与 `executive/report/json` 视图 | 更贴近负责人周会、决策稿和系统集成场景 |

## 当前可验证状态

- 案例索引：81
- 玩法索引：111
- 理论索引：12
- 自动化检查：22/22 通过
- 核心 CLI：`assess`、`design`、`search`、`match`、`validate`
- 外脑入口：`diagnose`、`cold-start`、`retention`、`monetization`、`referral`
- 分层输出：`operator`、`executive`、`report`、`json`
- 结构化输入：`--context-json`、`--context-file`

## 仍可继续优化的方向

- 将 `Decision BRD` / `Learning Path` / `Audit` 从概念工作流落成 CLI 能力
- 用更强的排序信号替换当前的轻量字符串匹配
- 为知识索引增加增量重建和 schema 约束
