# Task: Factory contracts

## Golder rule
* **Understand**: Ensure getting right the instructions. Warn any ambigueti and abort any output until it's clear what to do

## Pre-flight Checklist (Mandatory)
1. **Refresh Context:** Read the current contents of `/docs/master-spec.md`, `GEMINI.md`, `001-slice-metadata-definition.md` and `docs/specs/overview.md`.
2. **Check Status:** Ensure no conflicting manual changes have been made since the last turn.

## Requirements
- I need to define a folder called .factory/contracts to put inside all the contracts made for the factory to run.

## Output
- **Move current contracts:** Move the current `schema_file.json`to this new folder. Also modify any reference to that file in documentation files
- **New contract for telemetry** Generate a new contract for the `telemetry.json` information from the current content. Add references to this schema in the documentation files.
- **Telemetry Entry:** Modify the `telemetry.json` and add the telemetry information for this prompt. 
- **Token Receipt:** A breakdown of this interaction (Input, Reasoning, Output).
