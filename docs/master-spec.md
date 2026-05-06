
# 🛠️ Master Specification: Agentic Code Supply Chain

## 1. System Objective
Generate an Agentic code implementation supply chain to deliver product implementations based on a static, spec-driven development model.

## 2. Infrastructure Constraints
*   **Single Source of Truth:** A GitHub repository.
*   **Static Architecture:** Data consumption is purely via static JSON files (Slices and Registry) hosted on GitHub/GitHub Pages. No live backend API is utilized.
*   **Inputs:** All code generation must be derived from provided specs and plans.
*   **Trigger:** Code generation is strictly executed via GitHub Actions.
*   **Telemetry:** A web-based dashboard will visualize live updates using the aggregated JSON metadata of all slices.

## 3. The Logic of Slices
The project is divided into discrete units of work called **Slices**.
*   **Atomic Storage:** Each slice maintains its own JSON metadata in `.factory/slices/[ID].json` for distributed development.
*   **Aggregated Consumption:** A single `slices.json` (or `index.json`) is generated from individual slices to serve as the unified data source for the frontend.
*   **Compliance:** All slice metadata MUST strictly adhere to the schema defined in `.factory/slices/schema_file.json`.
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
The day-to-day execution of the factory floor is governed by the **Factory Protocol** 

## 8 Security
* All code must adhere to OWASP Top 10 for LLM Applications
* No Critical or High vulnerabilities allowed in the main branch.
* The codebase must be free from secrets or api leaks
* The tools for SAST will be Semgrep. FOR sca will be owasp dependency check.
* All specs and prompts must be secure againt Input Integrity.

## 9. Spec-Driven Development Phases
The lifecycle of a product implementation is divided into five distinct phases, each represented by a dedicated directory in `prompts/`:

1.  **Foundations:** Initial setup, architectural alignment, and core protocol definitions.
2.  **Specs:** Detailed technical specifications for individual features or components.
3.  **Planning:** Strategic breakdown of specs into actionable slices. This phase MUST produce testable Python class designs (interfaces or stubs) to ensure architectural integrity before the Implementation phase.
4.  **Implementation:** Active code generation and development turns.
5.  **Validation:** Testing, QA, and verification of implemented slices against the original specs.

# 📑 Factory Protocol: Standard Operating Procedure (SOP)

**Version:** 1.0.0  
**Role:** Synthetic Implementation Agent  
**Objective:** Deterministic conversion of Slices from `Planned` to `In Review`.

---

## 1. Interaction Lifecycle
Every session with the Gemini CLI **MUST** follow this sequence to ensure process integrity.

### 1.1 Ingestion Phase
*   The Agent **MUST** use `ls -R` or `glob` to verify the current file structure at the start of every session.
*   The Agent **MUST** perform a fresh `read_file` of all critical files (`GEMINI.md`, `docs/master-spec.md`) at the start of EVERY new directive, even if they were read in a previous turn.
*   **Cache-Busting:** The Agent MUST NOT assume the context provided in the `session_context` is the absolute current state if manual edits are frequent; empirical verification via tool calls is mandatory.
*   The Agent **MUST** read the target Slice JSON in `/.factory/slices/[ID].json`.
*   The Agent **MUST** read the corresponding Markdown specification in `/docs/specs/[ID].md`.


### 1.2 Validation Phase
*   The Agent **SHOULD** verify that all architectural dependencies are present in the repository.
*   If a dependency is missing or a spec is ambiguous, the Agent **MUST NOT** proceed with implementation. Instead, follow the **Rejection Protocol** (See Section 3).

### 1.3 Implementation Phase
*   Code **MUST** be written to a dedicated feature branch: `factory/slice-[ID]`.
*   The Agent **MUST** adhere to the coding standards defined in the Master Spec.
*   The Agent **MUST** include inline documentation for complex logic to assist the Human Reviewer.

---

## 2. Telemetry & Reporting Requirements
To maintain the **Central Telemetry Ledger**, the Agent **MUST** wrap every final response with a metadata block.

### 2.1 The Reporting Block
Every successful implementation response **MUST** conclude with a JSON block in the following format:
```json
{
  "telemetry": {
    "slice_id": "SCH-XXX",
    "status_change": "Planned -> In Review",
    "tokens": {
      "input": "[actual_input]",
      "reasoning": "[actual_reasoning]",
      "output": "[actual_output]"
    }
  }
}
```

### 2.2 Universal Telemetry Logging

*   **Mandatory Capture:** EVERY interaction (markdown prompts, free-text chat, or ad-hoc tasks) MUST be recorded in `/.factory/telemetry.json`.
*   **Context Categorization:** 
    *   Tasks derived from `prompts/` must use their Slice ID.
    *   Ad-hoc chat or configuration changes must use the context `GENERAL` or `AD-HOC`.
*   **Total Cost Tracking:** The `project_total_cost` field must be updated incrementally with every new log entry.

---

## 3. Rejection & Exception Handling
This protocol prioritizes **Accuracy over Completion**.

*   **Rule:** If the Agent identifies a logical contradiction in the spec, it **MUST** move the slice state to `Rejected`.
*   **Action:** The Agent **MUST** append a `rejection_log` to the Slice JSON explaining the specific conflict.
*   **Goal:** This data is used to measure **Spec Clarity Ratios** for PhD research.

---

## 4. Definition of "In Review"
A slice is considered `In Review` only when:
1.  A Pull Request (PR) has been opened.
2.  The JSON metadata has been updated with the PR link.
3.  The `usage_metadata` for the entire implementation session has been recorded.