# Task: Slice only for product

## Golder rule
* **Understand**: Ensure getting right the instructions. Warn any ambigueti and abort any output until it's clear what to do

## Pre-flight Checklist (Mandatory)
1. **Refresh Context:** Read the current contents of `GEMINI.md`, `docs/master-spec.md`
2. **Check Status:** Ensure no conflicting manual changes have been made since the last turn.

## Requirements
- I need to review and leave the slices only for product related specs. The slices json will be created on spec and posterior phases.
- From the schema_file.json contract delete the foundation phase type in phase object
- Remove from the slices metadata the usage, this is being managed in the telemetry files.

## Output
- **Implementation:** Make neccesary changes in `docs/master-spec.md` or `docs/specs/overview.md` files to define this new way to make slice jsons. Also Change in all the docs files the slices target. They are made to give the frontend dashboard information of product related slices, not those ones related to internal or bootstraping tasks.
- **Review slices json files** Review the `.factory/slices` folder and delete all the files but the ones related to spec, planning, implementation or validation slice phases
- **Telemetry Entry:** Modify the `telemetry.json` and add the telemetry information for this prompt. 
- **Token Receipt:** A breakdown of this interaction (Input, Reasoning, Output).
