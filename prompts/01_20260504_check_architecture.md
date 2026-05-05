# Task: Factory Alignment Check

**Important**

* The `/docs/master-spec.md`, `GEMINI.md`, and this promt markdown files are constantly changing, refresh the context to a new file version if you see a change. Display a message when you need to refresh the content because an update was made.

## Context
Referencing: `/docs/master-spec.md` and root `GEMINI.md`

Parse the markdown prompt and execute the tasks withi

## Requirements
- Review `GEMINI.md` and `/docs/master-spec.md` to align with the "Agentic Code Supply Chain" logic.
- **Implementation Proof:** Explain specifically how you will apply the TDD (Test-Driven Development) protocol and the "State Machine" transitions (Section 4) when working on a new slice.
- Identify any "red flags" in the current spec that might lead to token waste or architectural debt.

## Output
- **Operational Constraints:** A concise list of rules you will adhere to for every code generation task.
- **Telemetry Entry:** Update .factory/telemetry.json with the new slice metadat
- **Token Receipt:** A breakdown of this interaction (Input, Reasoning, Output).
- Notify me for final review, if you need to create any files or modify, do it and If I don't approve undo changes.