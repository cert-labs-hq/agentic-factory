# Skill: Implementor
**Description**: Converts a Planned Slice into functional, verified code following TDD and architectural blueprints.
**Triggers**: `/implement [ID]`, "implement slice", "start implementation for [ID]", "code this slice"

## Instructions
When triggered, you MUST follow the Spec-Driven Development (SDD) protocol to move a slice from `Planned` to `In Review`.

### 1. Ingestion & Setup
* **State Verification**: Verify that the slice metadata (`.factory/slices/[ID].json`) is currently in **Phase: `planning`** and **Status: `Planned`** (per `docs/specs/foundations/005-skill-transition-matrix.md`). If not, STOP and inform the user.
* **Immediate Transition**: Update metadata to **Status: `In Progress`** and **Phase: `implementation`** BEFORE starting any code work.
* **Branching (Mandatory)**: Create and switch to a dedicated feature branch: `factory/slice-[ID]`. DO NOT work in `main`. This is a non-negotiable requirement.
* **Context Load**: Read the following files for the target [ID]:
    - Metadata: `.factory/slices/[ID].json`
    - Specification: `docs/specs/[ID].md`
    - Plan: `.factory/slices/[ID]-PLAN.md`
    - Blueprint: `src/[ID]/interfaces.py`

### 2. Progress Tracking (Mandatory)
* **Metadata Heartbeat**: Every 3 minutes (or at every major implementation step), update the `updated_at` field in the slice metadata and commit the change to the feature branch. This ensures the dashboard reflects live progress.

### 3. TDD Execution (Mandatory)
For every functional unit defined in the blueprint and plan:
1. **Define Test**: Create or update a test file in `tests/[ID]/test_[module].py`.
2. **Execute Test (Fail)**: Run the test to confirm it fails (Red phase).
3. **Implement Code**: Move the relevant interface from `src/[ID]/interfaces.py` to its permanent home in `src/` (or create a new file) and provide the implementation.
4. **Execute Test (Pass)**: Run the test again to confirm it passes (Green phase).
5. **Do no refactor**: With all the test passing do not refactor the code, just move to the next test. Refactoring will be done in a later stage by a different skill. 

### 4. Verification & Compliance
* **Edge Cases**: Ensure tests cover boundary conditions, null inputs, and error states.
* **Contract Validation**: Ensure the final implementation respects all schemas in `.factory/contracts/`.
* **Lint & Type Check**: Run project-standard tools (e.g., `mypy`, `ruff`) to ensure quality.

### 5. Finalization & Reporting
* **Completion Transition**: 
    - Change status to **`In Review`** and Phase to **`validation`** in `.factory/slices/[ID].json`.
    - Update `updated_at` timestamp.
* **PR Readiness**: Create a Pull Request (PR) from your feature branch to `main`. Prepare a summary of changes for the human reviewer.
* **Telemetry**: Conclude the session with the mandatory reporting block.

**TERMINAL INSTRUCTION**: "Implementation complete for [ID]. Tests passed, branch pushed, and metadata updated to 'In Review / validation'. Ready for PR validation."
