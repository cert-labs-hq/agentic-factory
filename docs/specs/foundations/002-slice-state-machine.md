# Slice State Machine & Phase Transitions

This document defines the deterministic lifecycle of a **Slice** within the Agentic Factory. Adherence to these states and phases is mandatory for all agents and human contributors.

## 1. Lifecycle Overview

The lifecycle is divided into four primary phases, each with associated statuses. A phase represents the *type* of work being done, while a status represents the *readiness* or *result* of that work.

| Phase | Status | Trigger / Action | Responsible |
| :--- | :--- | :--- | :--- |
| **specs** | `Proposed` | Initial idea or requirement. | Architect |
| **specs** | `Planned` | Technical specification is complete. | Architect |
| **planning** | `In Progress` | Planning Architect is breaking down the spec. | Plan Architect |
| **planning** | `Planned` | Implementation plan and interfaces are ready. | Plan Architect |
| **implementation** | `In Progress` | Implementor is actively writing code and tests. | Implementor |
| **implementation** | `In Review` | PR is open; implementation is complete. | Implementor |
| **validation** | `In Review` | QA/Reviewer is validating the slice. | Reviewer |
| **validation** | `Approved` | Slice passed validation. | Reviewer |
| **validation** | `Rejected` | Slice failed validation; returns to Planning. | Reviewer |
| **-** | `Warehoused` | Merged and released. | System |

## 2. Mandatory Verification Protocol

Before starting any task, the Agent MUST verify the current state of the slice.

*   **To Plan**: Slice must be in Phase: `specs` and Status: `Planned`.
*   **To Implement**: Slice must be in Phase: `planning` and Status: `Planned`.
*   **To Validate**: Slice must be in Phase: `implementation` and Status: `In Review`.

## 3. Implementor Transition Rules

When the **Implementor** skill is triggered:
1.  **Immediate Transition**: Update metadata to Status: `In Progress` and Phase: `implementation`.
2.  **Git Protocol**: Create a feature branch `factory/slice-[ID]`.
3.  **Active Logging**: Commit metadata updates every 3 minutes (or at logical sub-steps) to track progress.
4.  **Completion Transition**: Upon opening a PR, update metadata to Status: `In Review` and Phase: `validation`.

## 4. Plan Architect Transition Rules

When the **Plan Architect** skill is triggered:
1.  **Immediate Transition**: Update metadata to Status: `In Progress` and Phase: `planning`.
2.  **Completion Transition**: Upon generating the plan and stubs, update metadata to Status: `Planned` and Phase: `planning`.
