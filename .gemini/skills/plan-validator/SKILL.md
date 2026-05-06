# Skill: Plan Validator
**Description**: Intercepts implementation requests to provide a structured reasoning check before coding.
**Triggers**: "/plan", "implementation plan", "how would you code this"

## Instructions
When this skill is triggered, you MUST NOT generate code. Instead, provide a **Reasoning Check** following this template:

### 🎯 Architectural Alignment
*   Which section of the `master_spec.md` does this change address?
*   Are there any breaking changes to existing slice schemas?

### 🛡️ Security & Quality (The Guard)
*   Which SAST/SCA gates will this implementation trigger?
*   Are there any new dependencies being introduced?

### 💰 FinOps Projection
*   Estimated Input Tokens (Spec + Context):
*   Estimated Reasoning/Output Tokens:
*   Projected "Shadow Cost" for this slice implementation.

### 🏗️ Proposed Slices
*   List the specific files to be modified or created.

**TERMINAL INSTRUCTION**: "Waiting for your confirmation to proceed with implementation."