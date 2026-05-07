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
You MUST CREATE a new Markdown file named `.factory/slices/[ID]-PLAN.md` with the following structure. Do not just provide a markdown block; physically write the file to the repository.

#### 🎯 Architectural Alignment
* **Target Spec**: Reference the source Markdown in `docs/specs/`.
* **Scope**: List exactly which files will be created or modified.

#### 🛡️ Execution Steps (Atomic & Deterministic)
1.  **Step [N] [Task Name]**: 
    * **Description**: Detailed instruction of what to build.
    * **Definition of Done (DoD)**: The verifiable outcome.
    * **Validation**: The command or check to run (e.g., `python -m pytest`).

#### 💰 FinOps Forecast (Rating)
* **Complexity**: [Low | Medium | High]
* **Forecasted Input**: (Estimated tokens for full context read)
* **Forecasted Reasoning**: (Estimated tokens for logic/validation)
* **Cache Strategy**: Describe how to maximize cache hits (e.g., "Keep Master Contract in context").

### 3. Metadata Sync
* **Status Update**: Update the Slice status to `Planned` in the metadata JSON.
* **Forecast Injection**: Update the `forecast` object in `.factory/slices/[ID].json` with the new metrics.

**TERMINAL INSTRUCTION**: "Plan file and metadata updated for [ID]. Ready to proceed with implementation upon request."