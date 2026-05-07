# BKP-004-REGISTRY-GENERATOR: Static Registry Aggregator

## 1. Objective
Provide a deterministic mechanism to aggregate distributed slice metadata into a single, unified `index.json` file. This registry serves as the primary data source for the Frontend Dashboard, enabling static hosting on GitHub Pages without a live backend.

## 2. Technical Requirements
- **Language:** Python 3.x
- **Inputs:** 
    - Master Schema: `.factory/contracts/schema_file.json`
    - Slice Directory: `.factory/slices/` (excluding the schema file itself)
- **Output:** `.factory/slices/index.json`
- **Execution:** Triggered via GitHub Actions on every push to the `main` branch or when a slice is updated.

## 3. Functional Specifications

### 3.1 Aggregation Logic
1.  **Discovery:** Scan the `.factory/slices/` directory for all `.json` files.
2.  **Exclusion:** Process only JSON files matching the pattern [A-Z]{3}-[0-9]{3}*.json. Explicitly ignore all other files in the directory.
3.  **Validation:** 
    - Each slice file MUST be validated against the master schema using standard python libraries.
    - If a file fails validation, the generator must log an error and skip the file (or fail the build depending on configuration).
4.  **Transformation:**
    - Extract all fields from individual slices.
    - Ensure dates are treated as ISO 8601 strings.
5.  **Summarization:** Calculate global metrics to be included in the registry root:
    - `total_slices`: Count of all discovered slices.
    - `status_counts`: Breakdown of slices by state (e.g., `Warehoused: 10`, `Planned: 5`).
    - `total_token_investment`: Aggregate sum of `token_usage.total` across all slices.
    - `last_registry_update`: ISO 8601 timestamp of the generation.

### 3.2 Defined contract
A contract taken from the example shown in section 3.2 must be generated in `.factory/contracts/aggregate_slice_info.json`. This will be the template to validatation.

## 4. Architectural Constraints
- **Idempotency:** Running the generator multiple times with the same inputs must produce identical outputs.
- **Performance:** Must handle up to 1,000 slices within a <10 second execution window.
- **Zero-Dependency (Preferred):** Minimize external Python dependencies to ensure fast execution in GitHub Actions environments.
- **Validation** After the `index.json` the file created must be validated against the contract defined in `.factory/contracts/aggregate_slice_info.json`.

## 5. Definition of Done
- Python script implemented in `src/registry_generator.py`.
- Unit tests validating the aggregation and summary logic.
- Integration test confirming `index.json` matches the expected schema defined in `.factory/contracts/aggregate_slice_info.json`
- The generated 
