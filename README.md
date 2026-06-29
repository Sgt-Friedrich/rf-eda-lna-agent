# RF EDA LNA Agent

English | [中文](#中文)

A configurable Codex skill/plugin for disciplined RF/LNA design workflows around EDA tools. It helps an agent collect user-defined design targets, create a goal file, maintain an exploration tree, run reusable harnesses, audit evidence, and report signoff readiness.

This project is workflow infrastructure. It does **not** include a PDK, foundry rule deck, private circuit database, private layout, private simulation data, or a guaranteed tapeout flow.

## What It Is

RF EDA LNA Agent turns a long RF design effort into a structured, evidence-driven process:

- collect the design contract from the user;
- create `goal.md` and configuration files;
- maintain a GitHub-friendly exploration tree;
- run bounded simulation, optimizer, EM/cosim, layout, and signoff-readiness harnesses;
- reject degenerate optimizer results;
- separate provisional evidence from signoff-grade evidence;
- keep heavy EDA artifacts out of Git by default.

It is intentionally target-agnostic. The agent does not assume a frequency band, gain target, noise target, matching target, stability target, linearity target, process technology, tool path, or PDK. Those values must come from the user or project configuration.

The project is built from long-form EDA workflow lessons: exploration-tree governance, bounded optimizer practice, EM/cosim embedding controls, GUI-reviewed layout growth, artifact budgeting, and truthful blocker reporting. The public package keeps those lessons generic and does not publish private circuit data.

## Core Principles

- **User-supplied targets**: no built-in RF specifications.
- **Evidence before promotion**: a candidate must meet the configured evidence level before it can be promoted.
- **No silent relaxation**: hard targets cannot be changed without user approval.
- **Smallest valid harness first**: use the cheapest test that can answer the current question.
- **Layout grows incrementally**: visual review and database connectivity checks are first-class gates.
- **Signoff is explicit**: DRC/LVS-clean claims require official decks and reports.
- **Public package stays clean**: no proprietary PDK data, private layouts, local paths, tokens, or solver dumps.

## First-Run Workflow

1. Ask the user for the design contract.
2. Write:
   - `config/project.yaml`
   - `config/metrics.yaml`
   - `config/artifact_policy.yaml`
   - `goal.md`
   - `docs/exploration_tree.md`
3. Initialize or connect a GitHub repository if requested.
4. Create the first baseline candidate.
5. Run the smallest valid harness and record evidence.

## Repository Layout

```text
skills/rf-eda-lna-agent/
  SKILL.md
  references/
    user-intake-and-bootstrap.md
    configuration-schema.md
    agent-architecture.md
    exploration-tree-management.md
    netlist-exploration-playbook.md
    schematic-generation-playbook.md
    harness-contracts.md
    optimizer-policy.md
    em-cosim-optimizer-playbook.md
    em-cosim-policy.md
    layout-exploration-playbook.md
    layout-growth-policy.md
    signoff-readiness-policy.md
    failure-catalog.md
    do-not-repeat-patterns.md
    history-mining-and-remote-audit.md
    deep-harness-playbook.md
    template-script-library.md
    eda-adapter-patterns.md
    rf-design-lessons.md
    blocker-and-failure-playbook.md
    export-policy.md
  scripts/
    init_project.py
    inventory_project.py
    metrics_gate.py
    touchstone_audit.py
    exploration_tree_append.py
    status_append.py
    artifact_guard.py
    signoff_readiness.py
    process_guard.py
    script_family_inventory.py
    history_remote_audit.py
    failure_catalog_append.py
    harness_scaffold.py
    evidence_gate.py
    materialize_template.py
  templates/
    harnesses/
      schematic_generation_template.py
      layout_growth_template.py
      em_extraction_template.py
      cosim_embedding_template.py
      optimizer_invocation_template.py
    examples/
      *.example.json
examples/synthetic_project/
  config/
  docs/
  manifests/
  results/
```

## Bundled Scripts

| Script | Purpose |
|---|---|
| `init_project.py` | Create a configurable RF/EDA project scaffold from user-supplied inputs. |
| `inventory_project.py` | Index candidates, docs, scripts, reports, and artifacts. |
| `metrics_gate.py` | Evaluate measured metric JSON against user-supplied target JSON. |
| `touchstone_audit.py` | Check Touchstone port count, frequency coverage, and DC handling. |
| `exploration_tree_append.py` | Append a candidate record to Markdown and JSONL registry files. |
| `status_append.py` | Append a compact candidate status entry. |
| `artifact_guard.py` | Report repository size and largest artifacts without deleting anything. |
| `signoff_readiness.py` | Check signoff collateral presence without claiming signoff-clean. |
| `process_guard.py` | List possible EDA-related processes without killing them by default. |
| `script_family_inventory.py` | Classify a large legacy script/doc tree into generic harness families. |
| `history_remote_audit.py` | Compare local and snapshot/ref histories by path and content hash. |
| `failure_catalog_append.py` | Append structured failure or blocker lessons to Markdown and JSONL. |
| `harness_scaffold.py` | Create a parameterized harness skeleton for simulation, optimizer, EM/cosim, layout growth, signoff, or diagnostics. |
| `evidence_gate.py` | Check whether a candidate has enough evidence and hard-gate status to be promoted. |
| `materialize_template.py` | Copy a bundled schematic/layout/EM/cosim/optimizer template into a project. |

## Encoded Workflow Lessons

The skill encodes these recurring RF/EDA project lessons:

- local worktrees are not always the full history; remote branches and archives must be audited before writing a project narrative;
- optimizer rows are evidence, not authority, until hard gates are independently verified;
- analytic or ideal schematic primitives can be optimistic relative to true physical EM;
- SnP black-box replacement is unsafe on paths that carry DC, noise reference, or high-impedance coupled behavior unless a control harness proves equivalence;
- pin-level net equivalence is not enough for layout; conductive geometry and screenshots are separate gates;
- passive full-chip EM is not the same as active/noise signoff;
- missing official DRC/LVS decks are external blockers, not something the agent can silently work around;
- heavy solver output belongs in manifests or external storage, not normal Git history.

## Example Commands

Create a project scaffold with placeholder fields:

```bash
python skills/rf-eda-lna-agent/scripts/init_project.py \
  --root /path/to/project \
  --project-name my-rf-project \
  --allow-tbd
```

Index the synthetic example:

```bash
python skills/rf-eda-lna-agent/scripts/inventory_project.py \
  --root examples/synthetic_project \
  --out /tmp/rf-eda-inventory \
  --candidate-regex '(?P<id>C\d{3})'
```

Evaluate a metrics file:

```bash
python skills/rf-eda-lna-agent/scripts/metrics_gate.py \
  --metrics-json measured.json \
  --targets-json targets.json
```

Audit a Touchstone file:

```bash
python skills/rf-eda-lna-agent/scripts/touchstone_audit.py example.sNp --expect-ports N
```

Check signoff readiness:

```bash
python skills/rf-eda-lna-agent/scripts/signoff_readiness.py \
  --require-drc \
  --require-lvs \
  --drc-deck /path/to/drc.rules \
  --lvs-deck /path/to/lvs.rules
```

Classify a legacy project into harness families:

```bash
python skills/rf-eda-lna-agent/scripts/script_family_inventory.py \
  --root /path/to/project \
  --out /tmp/rf-eda-script-families
```

Compare a local project with an archived branch snapshot:

```bash
python skills/rf-eda-lna-agent/scripts/history_remote_audit.py \
  --root /path/to/project \
  --snapshot old-main=/path/to/snapshot \
  --out /tmp/rf-eda-history-audit
```

Create a new harness skeleton:

```bash
python skills/rf-eda-lna-agent/scripts/harness_scaffold.py \
  --family optimizer \
  --name c001_optimizer \
  --out /tmp/rf-eda-harnesses
```

Copy a concrete template script into a project:

```bash
python skills/rf-eda-lna-agent/scripts/materialize_template.py \
  --template schematic \
  --name c001_schematic_builder \
  --out-dir /path/to/project/scripts
```

## Validation

Run:

```bash
python -m compileall skills/rf-eda-lna-agent/scripts
python -m unittest discover -s tests -v
```

The GitHub Actions workflow runs the same validation on push and pull request.

## What This Project Does Not Do

- It does not provide foundry collateral.
- It does not perform official DRC/LVS by itself.
- It does not certify a circuit for fabrication.
- It does not include private circuit/layout data.
- It does not choose RF targets for the user.
- It does not make a poor optimizer result valid by rewriting the goal.

## License

MIT

---

# 中文

[English](#rf-eda-lna-agent) | 中文

RF EDA LNA Agent 是一个可配置的 Codex skill/plugin，用于把 RF/LNA 电路设计流程组织成可审计、可维护、可复现的工程工作流。它帮助 agent 采集用户指标、生成目标文件、维护探索树、运行通用 harness、审查证据，并输出签核准备状态。

这个项目是流程基础设施，不包含 PDK、foundry rule deck、私有电路数据库、私有版图、私有仿真数据，也不承诺自动流片。

这个项目吸收的是长周期 EDA 自动化项目中的通用经验：探索树治理、受控 optimizer、EM/cosim 嵌回控制、GUI 审查的版图逐块生长、artifact 预算、以及真实 blocker 报告。公开包只保留通用方法，不发布私有电路数据。

## 它解决什么问题

长周期 RF/EDA 设计经常会遇到这些问题：

- optimizer 为了一个指标牺牲另一个硬指标；
- 粗频点优化结果在细扫时失效；
- schematic 模型和真实 EM 几何不一致；
- S 参数黑盒嵌回破坏 DC 或噪声参考；
- pin 名称看似正确，但真实金属没有连通；
- 被动全片 EM 被误当成有源/噪声签核；
- DRC/LVS deck 不存在却被误报为 clean；
- 大量临时仿真文件把仓库撑爆。

这个 agent 的目标不是替代 RF 工程判断，而是把这些风险变成明确的门禁、harness 和记录。

## 核心原则

- **指标由用户给出**：不内置任何频段、增益、噪声、匹配、稳定性或线性度目标。
- **证据先于 promotion**：候选必须达到配置要求的 evidence level 才能升级。
- **不静默放宽目标**：hard target 只能由用户明确修改。
- **先跑最小可信 harness**：用最小成本回答当前问题。
- **版图逐块生长**：截图审查和数据库连通性检查都是硬门。
- **签核必须真实**：DRC/LVS clean 必须有官方 deck 和真实报告。
- **开源包保持干净**：不放 PDK、私有版图、本机路径、token 或重型 solver 输出。

## 首次使用流程

1. 向用户采集设计合同。
2. 生成：
   - `config/project.yaml`
   - `config/metrics.yaml`
   - `config/artifact_policy.yaml`
   - `goal.md`
   - `docs/exploration_tree.md`
3. 按需创建或连接 GitHub 仓库。
4. 建立第一个 baseline candidate。
5. 运行最小可信 harness，并记录证据。

## 目录结构

```text
skills/rf-eda-lna-agent/
  SKILL.md
  references/
    user-intake-and-bootstrap.md
    configuration-schema.md
    agent-architecture.md
    exploration-tree-management.md
    netlist-exploration-playbook.md
    schematic-generation-playbook.md
    harness-contracts.md
    optimizer-policy.md
    em-cosim-optimizer-playbook.md
    em-cosim-policy.md
    layout-exploration-playbook.md
    layout-growth-policy.md
    signoff-readiness-policy.md
    failure-catalog.md
    do-not-repeat-patterns.md
    history-mining-and-remote-audit.md
    deep-harness-playbook.md
    template-script-library.md
    eda-adapter-patterns.md
    rf-design-lessons.md
    blocker-and-failure-playbook.md
    export-policy.md
  scripts/
    init_project.py
    inventory_project.py
    metrics_gate.py
    touchstone_audit.py
    exploration_tree_append.py
    status_append.py
    artifact_guard.py
    signoff_readiness.py
    process_guard.py
    script_family_inventory.py
    history_remote_audit.py
    failure_catalog_append.py
    harness_scaffold.py
    evidence_gate.py
    materialize_template.py
  templates/
    harnesses/
      schematic_generation_template.py
      layout_growth_template.py
      em_extraction_template.py
      cosim_embedding_template.py
      optimizer_invocation_template.py
    examples/
      *.example.json
examples/synthetic_project/
  config/
  docs/
  manifests/
  results/
```

## 脚本说明

| 脚本 | 作用 |
|---|---|
| `init_project.py` | 根据用户输入创建通用 RF/EDA 项目骨架。 |
| `inventory_project.py` | 索引 candidate、文档、脚本、报告和 artifact。 |
| `metrics_gate.py` | 用用户目标 JSON 判定仿真指标 JSON 是否过门。 |
| `touchstone_audit.py` | 检查 Touchstone 文件的端口数、频率覆盖和 DC 处理。 |
| `exploration_tree_append.py` | 向 Markdown 和 JSONL 探索树追加候选记录。 |
| `status_append.py` | 追加简洁状态记录。 |
| `artifact_guard.py` | 报告仓库大小和最大文件，不默认删除。 |
| `signoff_readiness.py` | 检查签核 collateral 是否存在，但不声称 clean。 |
| `process_guard.py` | 列出可能的 EDA 进程，默认不杀进程。 |
| `script_family_inventory.py` | 把大型历史脚本/文档树归类为通用 harness 家族。 |
| `history_remote_audit.py` | 对比本地项目与历史快照/远端快照的路径和内容哈希。 |
| `failure_catalog_append.py` | 结构化追加 failure/blocker 经验到 Markdown 和 JSONL。 |
| `harness_scaffold.py` | 生成 simulation、optimizer、EM/cosim、layout growth、signoff 或 diagnostic harness 骨架。 |
| `evidence_gate.py` | 检查候选证据等级、hard-gate 状态和红旗是否允许 promotion。 |
| `materialize_template.py` | 把内置的原理图、版图、EM、联仿或 optimizer 模板复制到项目中。 |

## 已固化的流程经验

- 本地 worktree 不一定包含完整历史，写总结前要审计远端分支和历史快照。
- optimizer 输出只是证据，必须经过独立 hard-gate 验证才能 promotion。
- 解析/理想 schematic primitive 往往比真实物理 EM 乐观。
- 带 DC、噪声参考、高阻耦合语义的路径不能盲目用 SnP 黑盒替换。
- pin 级 net 等价不等于真实金属连通，版图必须检查 conductive geometry 和截图。
- 被动全片 EM 不等于有源/噪声签核。
- 缺官方 DRC/LVS deck 是 external blocker，不能伪造 clean。
- 重型 solver 输出默认不进 Git，只保留 manifest 和轻量证据。

## 使用示例

创建带占位字段的项目骨架：

```bash
python skills/rf-eda-lna-agent/scripts/init_project.py \
  --root /path/to/project \
  --project-name my-rf-project \
  --allow-tbd
```

索引 synthetic 示例项目：

```bash
python skills/rf-eda-lna-agent/scripts/inventory_project.py \
  --root examples/synthetic_project \
  --out /tmp/rf-eda-inventory \
  --candidate-regex '(?P<id>C\d{3})'
```

评估指标：

```bash
python skills/rf-eda-lna-agent/scripts/metrics_gate.py \
  --metrics-json measured.json \
  --targets-json targets.json
```

审查 Touchstone 文件：

```bash
python skills/rf-eda-lna-agent/scripts/touchstone_audit.py example.sNp --expect-ports N
```

检查签核准备状态：

```bash
python skills/rf-eda-lna-agent/scripts/signoff_readiness.py \
  --require-drc \
  --require-lvs \
  --drc-deck /path/to/drc.rules \
  --lvs-deck /path/to/lvs.rules
```

## 验证

运行：

```bash
python -m compileall skills/rf-eda-lna-agent/scripts
python -m unittest discover -s tests -v
```

GitHub Actions 会在 push 和 pull request 时运行同样的验证。

## 这个项目不做什么

- 不提供 foundry collateral。
- 不自行完成官方 DRC/LVS。
- 不认证电路可流片。
- 不包含私有电路或版图数据。
- 不替用户选择 RF 指标。
- 不通过改写目标来美化失败结果。

## License

MIT
