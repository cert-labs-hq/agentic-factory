# Task: Improve planner skill

## Golder rule
* **Understand**: Ensure getting right the instructions. Warn any ambigueti and abort any output until it's clear what to do

## Pre-flight Checklist (Mandatory)
1. **Refresh Context:** Read the current contents of `/docs/master-spec.md`, `GEMINI.md` and `BKP-004-registry-generator.json`
2. **Check Status:** Ensure no conflicting manual changes have been made since the last turn.

## Requirements
- The plan-validator skill needs to generate Python class definitions with Type Hints and Docstrings, but with pass in the methods. Ensure the stubs align with the .factory/contracts/ schemas. This is mandatory, always a plan with logic code will make classes.
- The classe will be used to be imlemented with TDD.

## Output
- **Classes mandatory with plan** Generate along with the plan markdown the class or classes designed to be implememented later
- **Skill documentation upgrade** Add the requirements into the plan-validator skill definition for future planifications.
- **Documentation improvements** Ensure to align all the documentation with new improve if needed.
- **Telemetry Entry:** Modify the `telemetry.json` and add the telemetry information for this prompt. 
- **Token Receipt:** A breakdown of this interaction (Input, Reasoning, Output).
