
# 🛠️ Master Specification: Agentic Code Supply Chain

## 1. System Objective
Generate an Agentic code implementation supply chain to generate a product implementation based on a plan and spec-driven development.

## 2. Infrastructure Constraints
*   **Single Source of Truth:** A GitHub repository.
*   **Inputs:** All code generation must be derived from provided specs and plans.
*   **Trigger:** Code generation is strictly executed via GitHub Actions.
*   **Telemetry:** A web-based dashboard will visualize live updates using the JSON metadata of each slice.

## 3. The Logic of Slices
The project is divided into discrete units of work called **Slices**.
*   Each slice must have a corresponding JSON metadata schema.
*   The metadata schema tracks the state, token cost, and implementation history.

## 4. State Machine (The Factory Floor)
Agents and humans must strictly adhere to the following states:

1.  **Planned:** The slice input/specification is defined and ready for implementation.
2.  **In Progress:** An Agent is actively generating the code for the slice.
3.  **In Review:** Code generation is complete; a Pull Request is open for human validation.
4.  **Approved:** The reviewer has validated the implementation. This state triggers the automated "Outbound" action.
5.  **Warehoused:** The slice is integrated into the main branch with a proper artifact, git tag, and release.
6.  **Rejected:** The implementation failed validation and is returned for re-planning or correction.

## 5. Definition of Done (Warehousing)
A slice is only considered "Warehoused" when:
*   The PR is merged.
*   Automated tests and validations pass.
*   A Git Tag and Release are defined for the specific version.

## 6. Implementation Protocols
### 6.1 Mandatory TDD (Test-Driven Development)
*   No implementation code is accepted without a preceding test suite.
*   **Sequence:** Define Test -> Run Test (Fail) -> Generate Code -> Run Test (Pass).

### 6.2 Architectural Constraints
*   **Modularity:** Every slice must be self-contained and export its telemetry.
*   **Error Handling:** All Agent-generated code must include structured error logging that reports back to the State Machine.

## 7. Operational Governance
The day-to-day execution of the factory floor is governed by the **Factory Protocol** (`docs/factory/protocol.md`). This document defines the step-by-step requirements for ingestion, implementation, and reporting. Any deviation from the Protocol results in an automatic `Rejected` status.