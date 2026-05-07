# Slice Metadata Definition

This document provides a detailed explanation of the JSON metadata schema used to track **Slices** within the Agentic Factory. Every slice MUST have a corresponding JSON file in `.factory/slices/` that adheres to this specification.

## 1. Schema Overview

The schema is defined in `.factory/contracts/schema_file.json`. It ensures consistency across all development phases and provides the necessary data for the FinOps Dashboard.

## 2. Field Definitions

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | `string` | A unique identifier for the slice (e.g., `BKP-001`, `FRT-002`). |
| `title` | `string` | A concise, human-readable title for the slice. |
| `status` | `enum` | The current state in the lifecycle (see **Section 3**). |
| `created_at` | `string` | ISO 8601 timestamp of when the slice was first created. |
| `updated_at` | `string` | ISO 8601 timestamp of the last modification. |
| `assigned_to` | `string` | Name or ID of the Agent or Human currently responsible for the slice. |
| `phase` | `enum` | The development phase: `specs`, `planning`, `implementation`, `validation`. |
| `spec_path` | `string` | Relative path to the Markdown specification file (e.g., `docs/specs/BKP-001.md`). |
| `prompt_source` | `string` | The origin of the instruction: a file path or `MANUAL`. |
| `dependencies` | `array` | A list of Slice IDs that must be completed before this slice can start. |
| `metadata_version`| `string` | The version of the schema used (e.g., `1.0.0`). |

---

## 3. Lifecycle States (`status`)

*   **`Planned`**: The requirement is defined, but work has not started.
*   **`In Progress`**: An agent or developer is actively working on the implementation.
*   **`In Review`**: Implementation is complete; a Pull Request is open for validation.
*   **`Approved`**: Human reviewer has verified the work; ready for integration.
*   **`Warehoused`**: The code is merged into the main branch and released.
*   **`Rejected`**: The slice failed validation or identified a contradiction; requires re-planning.

---

## 4. Token Metrics

Token consumption for all slices is tracked exclusively in the **Central Telemetry Ledger** (`.factory/telemetry.json`). Individual slice metadata no longer stores these metrics to ensure a single source of truth for FinOps reporting.

---

## 5. Aggregation Logic

Individual slice JSONs are processed by the **Registry Generator** (BKP-004) to create a unified `index.json`. This aggregated file is what the Frontend Dashboard consumes to visualize the factory state.
