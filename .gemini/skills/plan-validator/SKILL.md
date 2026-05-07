# Skill: Plan Architect
**Description**: Transforms a technical Spec into a deterministic Implementation Plan Markdown file with FinOps forecasting.
**Triggers**: `/plan`, "generate plan", "planification phase", "how would you code this"

## Instructions
When triggered, you MUST NOT generate implementation code. Your goal is to produce the "Blueprint" for the next agent to follow.

### 1. Verification Phase
* **Identity Check**: Confirm the target **Slice ID** (e.g., BKP-004).
* **Contract Check**: Identify which files in `.factory/contracts/` must be enforced.
* **Halt-on-Ambiguity**: If requirements are missing, trigger the DRV-FAILURE protocol instead of planning.

### 2. Implementation Plan Template
Generate a Markdown block for a new file named `.factory/slices/[ID]-PLAN.md` with the following structure:

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
* **Status Update**: Instruct the user to move the Slice status to `Planned` in the metadata JSON.
* **Forecast Injection**: Provide the `forecast` JSON block to be added to `.factory/slices/[ID].json`.

**TERMINAL INSTRUCTION**: "Plan generated for [ID]. Save this to `.factory/slices/[ID]-PLAN.md`? Once saved, I am ready to implement the first step."