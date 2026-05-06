# Task: quality assurance enhacements
## Context
Referencing: `/docs/master-spec.md` and root `GEMINI.md`

## Golder rule
* **Understand**: Ensure getting right the instructions. Warn any ambigueti and abort any output until it's clear what to do

## Pre-flight Checklist (Mandatory)
1. **Refresh Context:** Read the current contents of `GEMINI.md` and `docs/master-spec.md`.
2. **Check Status:** Ensure no conflicting manual changes have been made since the last turn.

## Requirements
- I need to in the `telemetry.json` file a reference to the prompt. If the prompt comes from a file make a new entry, if not try to get the manual prompt that was enter.

## Output
- **Implementation:** Update the `telemetry.json` file and `schema_fie.json` to meet this new key for promt source reference
- **Telemetry Entry:** A JSON-formatted snippet representing this task as a new foundations task.
- **Token Receipt:** A breakdown of this interaction (Input, Reasoning, Output).
