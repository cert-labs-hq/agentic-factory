# Task: [Slice Title]
## Context
Referencing: `/docs/master-spec.md` and root `GEMINI.md`

## Golder rule
* **Understand**: Ensure getting right the instructions. Warn any ambigueti and abort any output until it's clear what to do


## Pre-flight Checklist (Mandatory)
1. **Refresh Context:** Read the current contents of `GEMINI.md` and `docs/master-spec.md`.
2. **Check Status:** Ensure no conflicting manual changes have been made since the last turn.

## Requirements
- I want to create a new skill called 'telemetry-analyst' to track my SDD token costs. I want to see total and ssd phase cost. Also be able to see input, reasoning and output usage.

## Output
- **Implementation:** A new skill.md for this project (not for all gemini) with its resouces like scripts and assets on it.
- **Json backend** A new file to store all the summary information.
- **Telemetry Entry:** A JSON-formatted snippet representing this task as a "Slice".
- **Token Receipt:** A breakdown of this interaction (Input, Reasoning, Output).
