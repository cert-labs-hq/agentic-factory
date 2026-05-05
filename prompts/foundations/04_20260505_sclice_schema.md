# Task: Slice Schema update
## Context
Referencing: `/docs/master-spec.md` and root `GEMINI.md`

## Golder rule
* **Understand**: Ensure getting right the instructions. Warn any ambigueti and abort any output until it's clear what to do


## Pre-flight Checklist (Mandatory)
1. **Refresh Context:** Read the current contents of `GEMINI.md` and `docs/master-spec.md`.
2. **Check Status:** Ensure no conflicting manual changes have been made since the last turn.

## Requirements
- I want to create an `schema_file.json` and update `GEMINI.md` and/or `docs/master-spec.md` to enforce every slice implementation must respect that. Look into `.factory/slices` folder for examples to make the schema, must be aligned with those.

## Output
- **Implementation:** A new file in `.factory/slices` called `schema_file.json`
- **Telemetry Entry:** A JSON-formatted snippet representing this task as a new foundations task.
- **Token Receipt:** A breakdown of this interaction (Input, Reasoning, Output).
