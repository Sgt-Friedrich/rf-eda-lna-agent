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
    harness-contracts.md
    optimizer-policy.md
    em-cosim-policy.md
    layout-growth-policy.md
    signoff-readiness-policy.md
    failure-catalog.md
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
    harness-contracts.md
    optimizer-policy.md
    em-cosim-policy.md
    layout-growth-policy.md
    signoff-readiness-policy.md
    failure-catalog.md
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
