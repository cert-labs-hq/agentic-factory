# Slice Status and Phase Definitions

This document outlines the lifecycle of a slice through different phases and statuses, managed by various agent skills.

## 1. Phases and Statuses

| Phase         | Status        | Description                                                                                                                              | Managed By       |
| :------------ | :------------ | :--------------------------------------------------------------------------------------------------------------------------------------- | :--------------- |
| **Foundations** | `Proposed`    | Initial proposal or idea for a new slice.                                                                                                | User/Spec Architect |
| **Specs**     | `Planned`     | Specifications for the slice are defined and approved.                                                                                   | Spec Architect    |
| **Planning**  | `Planned`     | A detailed implementation plan, including code interfaces and FinOps forecast, has been generated. Ready for implementation.                | Plan Architect    |
| **Implementation** | `In Progress` | The slice is actively being coded. Branching, regular commits, and metadata updates are ongoing.                                         | Implementor       |
| **Validation**| `In Review`   | The implementation is complete, a PR is created, and the slice is awaiting review.                                                     | Implementor/Gatekeeper |
| **Validation**| `Approved`    | The implementation has been reviewed and approved.                                                                                       | Gatekeeper        |
| **Validation**| `Rejected`    | The implementation has been reviewed and rejected, requiring further work or revision.                                                   | Gatekeeper        |

## 2. Skill Responsibilities and Transitions

### 2.1 Spec Architect
- **Trigger**: User provides a high-level idea or requirement.
- **Action**: Defines slice specifications.
- **Input State**: `Foundations` / `Proposed`
- **Output State**: `Specs` / `Planned`

### 2.2 Plan Architect (plan-validator)
- **Trigger**: Slice is in `Specs` / `Planned`.
- **Action**: Generates an implementation plan (`[ID]-PLAN.md`) and Python interfaces (`src/[ID]/interfaces.py`). Updates slice metadata with the plan.
- **Input State**: `Specs` / `Planned`
- **Output State**: `Planning` / `Planned` (Signals readiness for implementation)

### 2.3 Implementor
- **Trigger**: Slice is in `Planning` / `Planned`.
- **Action**:
    - Creates a feature branch (`factory/slice-[ID]`).
    - Implements the code according to the plan.
    - Commits metadata updates every 3 minutes.
    - Creates a Pull Request to `main`.
- **Input State**: `Planning` / `Planned`
- **Output State**: `Validation` / `In Review`

### 2.4 Gatekeeper
- **Trigger**: Slice is in `Validation` / `In Review`.
- **Action**: Reviews the PR and code.
- **Input State**: `Validation` / `In Review`
- **Output State**: `Validation` / `Approved` or `Validation` / `Rejected`

## 3. Key Workflow Rules

- **Branching**: All implementation work MUST be done on feature branches.
- **Commit Frequency**: Metadata updates (heartbeats) are required every 3 minutes during implementation.
- **PR Requirement**: A Pull Request is mandatory for moving from implementation to review.
