# Agent Skill Transition Matrix

This document defines the specific status and phase requirements for each Agent Skill to operate, and the transitions they are responsible for.

## 1. Skill Operating Requirements

| Skill | Required Phase | Required Status | Resulting Phase | Resulting Status |
| :--- | :--- | :--- | :--- | :--- |
| **Spec Architect** | `Foundations` | `Proposed` | `specs` | `Planned` |
| **Plan Architect** | `specs` | `Planned` | `planning` | `Planned` |
| **Implementor** | `planning` | `Planned` | `implementation` | `In Review` |
| **Gatekeeper** | `implementation`| `In Review` | `validation` | `Approved` |

## 2. Detailed Protocols

### 2.1 Plan Architect (plan-validator)
- **Start**: Moves slice to `Phase: planning`, `Status: In Progress`.
- **End**: Moves slice to `Phase: planning`, `Status: Planned`.
- **Artifacts**: Produces `[ID]-PLAN.md` and `src/[ID]/interfaces.py`.

### 2.2 Implementor
- **Start**: Moves slice to `Phase: implementation`, `Status: In Progress`.
- **Branching**: MUST create branch `factory/slice-[ID]`.
- **Heartbeat**: MUST commit metadata updates every 3 minutes.
- **End**: Moves slice to `Phase: validation`, `Status: In Review`.
- **PR**: MUST create a Pull Request to `main`.

### 2.3 Gatekeeper
- **Start**: Moves slice to `Phase: validation`, `Status: In Progress`.
- **End**: Moves slice to `Phase: validation`, `Status: Approved` (or `Rejected`).

## 3. Mandatory Verification
Agents MUST verify the `Required Phase` and `Required Status` before executing any core logic. If the slice is not in the correct state, the agent MUST stop and report the discrepancy.
