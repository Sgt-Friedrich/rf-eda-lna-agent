# Template Script Library

The bundled templates are sanitized starter scripts for common RF/EDA agent
tasks. They are not tied to any private project, PDK, frequency band, or metric.
Each template has a `--dry-run` mode that validates config structure and writes
an evidence bundle before project-specific EDA hooks are filled in.

## Templates

| Template | Purpose | Main config |
|---|---|---|
| `schematic_generation_template.py` | Generate or update a schematic cell with explicit connectivity and acceptance evidence | `schematic_design_spec.example.json`, `eda_config.example.json` |
| `layout_growth_template.py` | Add one physical layout block or connection family with screenshot and geometry-audit expectations | `layout_block_plan.example.json` |
| `em_extraction_template.py` | Define an EM extraction block, ports, reference planes, frequency coverage, and DC handling | `em_plan.example.json` |
| `cosim_embedding_template.py` | Embed audited EM artifacts into a circuit harness with replace/audit/hybrid mode checks | `embedding_plan.example.json` |
| `optimizer_invocation_template.py` | Invoke a native or scripted optimizer with physical variables and hard targets | `optimizer_plan.example.json` |

## Materializing A Template

Use:

```bash
python skills/rf-eda-lna-agent/scripts/materialize_template.py \
  --template optimizer \
  --name c001_optimizer \
  --out-dir project/scripts
```

Then edit only the project-specific hook and config paths. Keep metrics, EDA
runtime paths, library names, and PDK names in project config, not in the public
template.

## Required Customization

For every materialized template:

1. replace the `run_*` hook with the project-specific EDA call;
2. keep the dry-run validation path intact;
3. write raw logs and manifests before summaries;
4. update the exploration tree after a real run;
5. keep hard targets user-configured;
6. preserve public/private boundaries.

## Promotion Boundary

Template dry-run output is never design evidence. It only proves that the
harness structure is ready to be connected to the user's EDA environment.
