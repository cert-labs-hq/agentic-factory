# 📑 Factory Protocol: Standard Operating Procedure (SOP)

**Version:** 1.0.0  
**Role:** Synthetic Implementation Agent  
**Objective:** Deterministic conversion of Slices from `Planned` to `In Review`.

---

## 1. Interaction Lifecycle
Every session with the Gemini CLI **MUST** follow this sequence to ensure process integrity.

### 1.1 Ingestion Phase
*   The Agent **MUST** read the `docs/master_spec.md` to understand the global system constraints.
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