# TASK: Refactor BKP-004 (Registry Generator) - FinOps Aggregation & Lifecycle
## 1. Context (Direct Injection)
- **Master Spec:** <<< /docs/master-spec.md
- **Aggregation contract:** <<< .factory/contracts/aggregate_slice_info.json
- **Implementation plan:** <<< .factory/slices/BKP-004-PLAN.md
- **Python class:** <<< src/registry_generator.py
- **Source Telemetry:** <<< telemetry.json

## 2. SDD Protocol & Lifecycle Management (MANDATORY)
Since BKP-004 is being refactored, you MUST follow these state-change steps:

1. **State Reversion**: Immediately update `.factory/slices/BKP-004.json` metadata:
   - Set **Status** to `In Progress`.
   - Set **Phase** to `implementation`.
2. **Branching**: Create a new feature branch for this refactor: `factory/slice-BKP-004-finops`. DO NOT work on `main`.
3. **Implementation**: Execute the technical requirements below.
4. **Transition to Review**: Upon completion, update `.factory/slices/BKP-004.json`:
   - Set **Status** to `In Review`.
   - Set **Phase** to `validation`.
5. **PR Readiness**: Provide a summary of changes and instructions for a PR from `factory/slice-BKP-004-finops` to `main`.

## 3. Technical Requirements: FinOps Aggregator
Refactor `src/registry_generator.py` and the contract to support automated dashboard updates.

### 3.1 Update Contract (`aggregate_slice_info.json`)
Modify the schema to include the `global_finops` object, specifically validating:
- `project_total_cost`: {prompt, reasoning, output, total}
- `phase_stats`: A dictionary of phase objects containing token breakdowns.

### 3.2 Implement Aggregation Logic
1. **Telemetry Feed**: Read `telemetry.json` and iterate through all `logs`.
2. **Phase Mapping**: Group and sum tokens by the `phase` field (foundations, specs, planning, implementation, validation).
3. **Global Investment**: Calculate the total lifecycle cost (Prompt/Reasoning/Output) for the entire project.
4. **Integration**: Ensure `index.json` output now includes this aggregated data in the `metadata` block.

## 4. Mandatory Outputs
1. **Updated `.factory/contracts/aggregate_slice_info.json`**
2. **Updated `src/registry_generator.py`** (with TDD verified logic).
3. **Telemetry Entry**: Add a log for this turn:
   - **Context**: "BKP-004-FINOPS-LIFECYCLE-REFACTOR"
   - **Phase**: "implementation"
   - **Slice_id**: "BKP-004"
   - **Tokens (Estimate)**: { prompt: 22000, reasoning: 5000, output: 1500, total: 28500 }

**FINAL INSTRUCTION**: Reopen the slice, create the branch, implement the logic, and move to 'In Review'. Provide all updated code and the PR summary.