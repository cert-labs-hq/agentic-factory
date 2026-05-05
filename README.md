# 🏗️ Agentic Factory: Spec-Driven Supply Chain

This repository implements a **Digital Supply Chain** for software production. Instead of traditional "coding," this project treats software development as a logistics problem where **Synthetic Labor** (AI Agents) is orchestrated through a deterministic state machine.

## 🏭 Core Philosophy: The Logistics of Code
In a world where code production is no longer the bottleneck, the primary constraint is **Human Validation Latency**. This project demonstrates a high-efficiency implementation flow where:
1. **Human Brain** = Quality Control & Architecture.
2. **Gemini CLI** = Synthetic Factory Worker.
3. **GitHub** = The Single Source of Truth & Warehouse.

## 🔄 The State Machine
Every feature is broken into a **Slice**—a discrete unit of work with a JSON metadata schema. Slices move through the factory floor in the following stages:

| State | Description |
| :--- | :--- |
| **Planned** | The slice input is defined and ready for implementation. |
| **In Progress** | An Agent is currently generating the code for this slice. |
| **In Review** | Code is generated and exists in a PR for human validation. |
| **Approved** | Human reviewer has signed off. Triggers automated validation. |
| **Warehoused** | Implementation is merged, git-tagged, and released. |
| **Rejected** | Implementation failed logic or quality gates; sent back for re-plan. |

## 🛠️ System Constraints
* **Single Source of Truth:** All states and code live in this GitHub repository.
* **Spec-Driven:** No code is written without a corresponding `.md` spec and `.json` metadata.
* **FinOps Optimized:** Engineered to run on the **Gemini Free Tier**, proving that structured logic is more valuable than expensive token budgets.
* **Live Telemetry:** Progress is tracked via a web-based dashboard visualizing the current "inventory" of slices.

## 📂 Repository Structure
* `/docs/specs/`: Technical Work Orders for each slice.
* `./factory/telemetry.json`: 
* `/.factory/slices/`: JSON metadata tracking the state and token cost of every unit.
* `/.github/workflows/`: The "Factory Machinery" (Automation).