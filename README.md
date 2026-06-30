# RF EDA LNA Agent

English | [中文](#中文)

A configurable Codex skill/plugin for evidence-driven RF/LNA EDA workflows. It helps an agent collect user-defined design targets, maintain an exploration tree, run bounded harnesses, apply RF sanity checks, audit EM/layout evidence, and report signoff readiness.

This repository is workflow infrastructure. It does **not** include a PDK, foundry rule deck, private circuit database, private layout, private simulation data, textbook PDFs, or a guaranteed tapeout flow.

## What This Agent Does

- Collects the design contract from the user instead of assuming RF targets.
- Creates `goal.md`, configuration files, exploration-tree records, and artifact manifests.
- Maintains candidate history with hypothesis, parent, variables, evidence level, metrics, decision, and do-not-repeat rules.
- Provides reusable harness templates for schematic generation, optimization, Touchstone audit, EM/cosim, layout growth, GUI review, large-signal checks, and signoff readiness.
- Applies distilled RF/microwave textbook knowledge as sanity gates: cascade noise budget, matching/reference-plane consistency, stability, physical passive feasibility, layout connectivity, and nonlinear verification.
- Keeps heavy EDA artifacts out of Git by default.

## Core Principles

- **User-supplied targets**: no built-in frequency band, gain, noise, matching, stability, linearity, process, tool path, or PDK.
- **Exploration tree as architecture**: the tree is the agent's working memory, not a final report appendix.
- **Evidence before promotion**: a candidate must meet the configured evidence level before promotion.
- **No silent relaxation**: hard targets cannot be changed without user approval.
- **Smallest valid harness first**: use the cheapest reliable experiment that answers the current question.
- **Physics-aware checks**: textbook-derived RF checks are applied before trusting optimizer or EM output.
- **Layout grows incrementally**: screenshots and database connectivity checks are first-class gates.
- **Signoff is explicit**: DRC/LVS-clean claims require official decks and reports.
- **Public package stays clean**: no proprietary PDK data, private layouts, local paths, tokens, solver dumps, or copyrighted textbook bodies.

## Repository Layout

```text
skills/rf-eda-lna-agent/
  SKILL.md
  references/
    agent-architecture.md
    historical-workflow-distilled-lessons.md
    exploration-tree-management.md
    deep-harness-playbook.md
    optimizer-policy.md
    em-cosim-policy.md
    layout-growth-policy.md
    failure-catalog.md
    rf-textbook-distilled-knowledge.md
    rf-theory-source-map.md
    rf-formula-and-sanity-gates.md
    rf-passive-and-layout-checklists.md
    rf-large-signal-and-nonlinear-checklists.md
    rf-ads-cad-workflow-map.md
  scripts/
    init_project.py
    inventory_project.py
    metrics_gate.py
    touchstone_audit.py
    evidence_gate.py
    artifact_guard.py
    signoff_readiness.py
    script_family_inventory.py
    history_remote_audit.py
    public_safety_scan.py
    book_knowledge_inventory.py
    book_chapter_cards.py
    book_lesson_append.py
  templates/
    harnesses/
      schematic_generation_template.py
      optimizer_invocation_template.py
      em_extraction_template.py
      cosim_embedding_template.py
      layout_growth_template.py
    examples/
examples/synthetic_project/
tests/
```

## First-Run Workflow

1. Ask the user for the design contract: circuit/application, metrics, hard/stretch/report-only targets, EDA environment, PDK/signoff expectations, artifact budget, and GitHub policy.
2. Generate `config/project.yaml`, `config/metrics.yaml`, `config/artifact_policy.yaml`, `goal.md`, and `docs/exploration_tree.md`.
3. Create a baseline candidate and choose the smallest valid harness.
4. Run the harness, extract metric JSON, apply evidence gates, and update the exploration tree.
5. Preserve heavy outputs as manifests unless the project policy explicitly allows storing them.

## Bundled Script Families

| Family | Main scripts/templates | Purpose |
|---|---|---|
| Project bootstrap | `init_project.py` | Create generic RF/EDA project files from user input. |
| Exploration tree | `exploration_tree_append.py`, `status_append.py`, `evidence_gate.py` | Record candidate state and prevent premature promotion. |
| Inventory/history | `inventory_project.py`, `script_family_inventory.py`, `history_remote_audit.py` | Mine local and remote histories without copying private data. |
| Optimizer | `optimizer_invocation_template.py`, `metrics_gate.py` | Run bounded optimizers with hard gates and independent verification. |
| EM/cosim | `touchstone_audit.py`, `em_extraction_template.py`, `cosim_embedding_template.py` | Check SnP files, EM partitions, and embedding evidence. |
| Layout growth | `layout_growth_template.py` | Grow RF layout block by block with screenshots and connectivity checks. |
| Signoff readiness | `signoff_readiness.py` | Distinguish ready vs clean and report missing official collateral. |
| Artifact/process guard | `artifact_guard.py`, `process_guard.py`, `public_safety_scan.py` | Control disk usage, avoid killing unrelated EDA jobs, and check public-release boundaries. |
| Textbook knowledge | `book_knowledge_inventory.py`, `book_chapter_cards.py`, `book_lesson_append.py` | Convert local RF textbook reading into sanitized agent knowledge. |

## RF Knowledge Layer

The skill includes original, sanitized summaries distilled from RF/microwave textbook reading. These references convert theory into agent checks:

- cascade noise and effective gain budgeting;
- matching, Smith-chart, S-parameter, ABCD, and reference-plane sanity;
- stability and wideband verification;
- physical passive feasibility: inductors, capacitors, resistors, vias, airbridges, transformers, bias and decoupling networks;
- nonlinear and large-signal checks: compression, intermodulation, harmonic balance;
- EDA/CAD discipline: native optimizer setup, EM/circuit partitioning, GUI evidence, signoff readiness.

The repository does not include textbook PDFs or copied textbook text.

## Example Commands

Create a project scaffold:

```bash
python skills/rf-eda-lna-agent/scripts/init_project.py \
  --root /path/to/project \
  --project-name my-rf-project \
  --allow-tbd
```

Evaluate metrics:

```bash
python skills/rf-eda-lna-agent/scripts/metrics_gate.py \
  --metrics-json measured.json \
  --targets-json targets.json
```

Audit a Touchstone file:

```bash
python skills/rf-eda-lna-agent/scripts/touchstone_audit.py example.sNp --expect-ports N
```

Classify a legacy project into harness families:

```bash
python skills/rf-eda-lna-agent/scripts/script_family_inventory.py \
  --root /path/to/project \
  --out /tmp/rf-eda-script-families
```

Inventory local textbook sources without copying content:

```bash
python skills/rf-eda-lna-agent/scripts/book_knowledge_inventory.py \
  --books-dir /path/to/books \
  --out /tmp/rf-eda-book-inventory
```

Scan a public package before publishing:

```bash
python skills/rf-eda-lna-agent/scripts/public_safety_scan.py --root .
```

## Validation

```bash
python -m compileall skills/rf-eda-lna-agent/scripts
python -m unittest discover -s tests -v
python skills/rf-eda-lna-agent/scripts/public_safety_scan.py --root .
```

## What This Project Does Not Do

- It does not provide foundry collateral.
- It does not perform official DRC/LVS by itself.
- It does not certify a circuit for fabrication.
- It does not include private circuit/layout data.
- It does not choose RF targets for the user.
- It does not upload textbook PDFs or copied textbook bodies.
- It does not make a poor optimizer result valid by rewriting the goal.

## License

MIT

---

# 中文

[English](#rf-eda-lna-agent) | 中文

RF EDA LNA Agent 是一个面向 RF/LNA EDA 流程的 Codex skill/plugin。它的目标不是替代电路设计者做黑箱优化，而是把用户给定的设计指标、EDA 环境、PDK 约束、探索树、仿真 harness、EM/版图证据和签核 readiness 组织成可复现的工程流程。

本仓库是流程基础设施，不包含 PDK、foundry 规则 deck、私有电路数据库、私有版图、私有仿真数据、教材 PDF，也不承诺自动完成可流片签核。

## 能解决什么问题

- 先向用户采集设计契约，而不是内置固定频段或固定指标。
- 自动建立 `goal.md`、配置文件、探索树记录和 artifact manifest。
- 让每个候选都记录假设、父节点、变量、证据等级、指标、判定和 do-not-repeat。
- 提供原理图生成、优化器、Touchstone 审查、EM/cosim、版图逐块生长、GUI 截图、大信号验证、签核 readiness 等模板。
- 将 RF/微波教材知识沉淀为可执行检查：级联噪声预算、匹配与参考面、稳定性、物理无源可实现性、版图连通性、大信号验证。
- 默认不把重型 EDA 产物放入 Git。

## 核心原则

- **指标由用户给出**：不内置频段、增益、噪声、匹配、稳定性、线性度、工艺、工具路径或 PDK。
- **探索树是 agent 架构的一部分**：它是工作记忆和治理层，不是事后日志。
- **证据先于提升**：候选必须达到配置要求的证据等级才能 promotion。
- **不静默放宽硬门**：hard target 只能由用户明确修改。
- **先用最小可信 harness**：用最低成本回答当前问题。
- **理论检查前置**：优化器或 EM 输出必须经过 RF sanity gates。
- **版图逐块生长**：截图和数据库连通性检查是硬门。
- **签核必须真实**：DRC/LVS clean 必须有官方 deck 和真实报告。
- **开源包保持干净**：不包含专有 PDK、私有版图、本地路径、token、solver dump 或教材正文。

## 知识来源如何沉淀

本项目把两类经验转化为通用能力：

1. 长期 RF/EDA 自动化项目中的流程经验：探索树、harness、optimizer、EM/cosim、版图 GUI、artifact 控制和 blocker 报告。
2. RF/微波教材中的理论知识：传输线、S 参数、ABCD、匹配、噪声、稳定性、无源器件、via/airbridge、非线性和大信号。

这些内容只以原创摘要、检查清单、接口约定和失败模式进入仓库，不发布私有数据或教材正文。

## 使用与验证

创建项目、评估指标、审查 Touchstone、分类历史脚本、整理教材知识和发布前安全扫描的命令与英文部分相同。发布前至少运行：

```bash
python -m compileall skills/rf-eda-lna-agent/scripts
python -m unittest discover -s tests -v
python skills/rf-eda-lna-agent/scripts/public_safety_scan.py --root .
```

## 边界

- 不提供 foundry collateral。
- 不自行完成官方 DRC/LVS。
- 不认证电路可流片。
- 不包含私有电路或版图数据。
- 不替用户选择 RF 指标。
- 不上传教材 PDF 或复制教材正文。
- 不通过改写目标来美化失败结果。
