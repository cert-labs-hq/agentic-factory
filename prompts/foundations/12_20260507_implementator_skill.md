# Task: Implementator skill

## Golder rule
* **Understand**: Ensure getting right the instructions. Warn any ambigueti and abort any output until it's clear what to do

## Pre-flight Checklist (Mandatory)
1. **Refresh Context:** Read the current contents of `/docs/master-spec.md`, `GEMINI.md`, `001-slice-metadata-definition.md` and `docs/specs/overview.md`.
2. **Check Status:** Ensure no conflicting manual changes have been made since the last turn.

## Requirements
- Based on the plan-validator skill and all the documentation I need to create an implementator skill. 
- The skill must take the all the information of the slice name given and then implement the code
- Must follow conventions and results of the plan-validator skill 
- Must do TDD, create a test folder and put the result code
- The definition of done is meet the requirements and pass all test for edge cases and happy paths

## Output
- **The implemenmtator Skill** The new skill ready to use.
- **Documentation improvements** Ensure to align all the documentation with new improve if needed.
- **Telemetry Entry:** Modify the `telemetry.json` and add the telemetry information for this prompt. 
- **Token Receipt:** A breakdown of this interaction (Input, Reasoning, Output).
