# Task: quality assurance enhacements

## Golder rule
* **Understand**: Ensure getting right the instructions. Warn any ambigueti and abort any output until it's clear what to do

## Pre-flight Checklist (Mandatory)
1. **Refresh Context:** Read the current contents of `GEMINI.md`, `docs/master-spec.md` and `docs/specs/overview.md`.
2. **Check Status:** Ensure no conflicting manual changes have been made since the last turn.

## Requirements
- I need to add to the `telemetry_summary.json` file a new key called slice_id, this way I can analyse later based on phase and slice.

## Output
- **Implementation:** Make neccesary changes in `docs/master-spec.md` or `docs/specs/overview.md` files to sync the spec with this new key in the json file. Also verify the telemetry files and fill the new slice data. For foundational prompts just add "Foundational" as the slice that belongs.
- **Telemetry Entry:** Modify the `telemetry.json` file with this new token utilization entry
- **Update telemetry** After all changes and telemetry updates run the /update-telemetry command to perform a full telemetry update. This time making the new slice aggrefation.
- **Token Receipt:** A breakdown of this interaction (Input, Reasoning, Output).
