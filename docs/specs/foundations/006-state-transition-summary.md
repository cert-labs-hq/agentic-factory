# Slice Status and Phase Transition Definition

## 1. Overview
This document defines the mandatory state transitions for Slices in the Agentic Factory. Every skill MUST verify the entrance criteria before acting and update the state upon completion.

## 2. Skill-Specific Transitions

### 2.1 Plan Architect (Skill: plan-validator)
- **Entrance Criteria**: Status: `Planned`, Phase: `specs`.
- **Action Start**: Transition to Status: `In Progress`, Phase: `planning`.
- **Exit Criteria**: Transition to Status: `Planned`, Phase: `planning`.
- **Required Artifacts**: `.factory/slices/[ID]-PLAN.md` and `src/[ID]/interfaces.py`.

### 2.2 Implementor (Skill: implementor)
- **Entrance Criteria**: Status: `Planned`, Phase: `planning`.
- **Action Start**: Transition to Status: `In Progress`, Phase: `implementation`.
- **Git Protocol**: MUST create branch `factory/slice-[ID]`.
- **Exit Criteria**: Transition to Status: `In Review`, Phase: `validation`.
- **Final Action**: Open Pull Request to `main`.

## 3. Mandatory Protocols
- **State Verification**: Every interaction MUST begin with an empirical check of `.factory/slices/[ID].json`.
- **Branching**: NO implementation work is allowed on the `main` branch.
- **Progress Tracking**: Heartbeat commits every 3 minutes during Implementation phase to update `updated_at`.

## 4. Transition Matrix

| Skill | From (Status/Phase) | To (Status/Phase) |
| :--- | :--- | :--- |
| **Architect** | `Proposed/specs` | `Planned/specs` |
| **Plan Architect** | `Planned/specs` | `Planned/planning` |
| **Implementor** | `Planned/planning` | `In Review/validation` |
| **Reviewer** | `In Review/validation` | `Approved/validation` |
| **System** | `Approved/validation` | `Warehoused/-` |
