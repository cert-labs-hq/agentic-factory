# Skill: Plan Architect
**Description**: Transforms a technical Spec into a deterministic Implementation Plan Markdown file with FinOps forecasting.
**Triggers**: `/plan`, "generate plan", "planification phase", "how would you code this"

## Instructions
When triggered, you MUST NOT generate implementation code. Your goal is to produce the "Blueprint" for the next agent to follow.

### 1. Verification Phase
* **Identity Check**: Confirm the target **Slice ID** (e.g., BKP-004).
* **Contract Check**: Identify which files in `.factory/contracts/` must be enforced.
* **Halt-on-Ambiguity**: If requirements are missing, trigger the DRV-FAILURE protocol instead of planning.

### 2. Implementation Plan Artifact
You MUST CREATE two files for every planning phase:
1. A new Markdown file named `.factory/slices/[ID]-PLAN.md`.
2. A Python interface file in a new slice-specific directory: `src/[ID]/interfaces.py`.

#### 2.1 Planning Markdown (`[ID]-PLAN.md`)
The file must have the following structure:
...
#### 🛡️ Execution Steps (Atomic & Deterministic)
...
#### 💰 FinOps Forecast (Rating)
...

#### 🐍 Mandatory Architectural Stubs (in `src/[ID]/`)
You MUST generate Python class definitions that serve as the interface for the implementation.
- **Location**: These files MUST reside in `src/[ID]/interfaces.py`. This ensures a clean, isolated blueprint for the implementor.
- **Requirements**:
    - Use **Type Hints** for all parameters and return values.
    - Include **Docstrings** explaining the purpose of each class and method.
    - Use `pass` for method implementations.
    - **Contract Alignment**: Ensure classes and methods directly reflect the structures defined in `.factory/contracts/` schemas.
    - **Implementor Workflow**: Note in the plan that the implementor will be responsible for moving these interfaces to their final locations within `src/` during the Implementation phase.

### 3. Metadata Sync
* **Status Update**: Update the Slice status to `Planned` in the metadata JSON.
* **Forecast Injection**: Update the `forecast` object in `.factory/slices/[ID].json` with the new metrics.

**TERMINAL INSTRUCTION**: "Plan file and metadata updated for [ID]. Ready to proceed with implementation upon request."