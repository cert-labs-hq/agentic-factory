# Implementation Plan: BKP-004-REGISTRY-GENERATOR

## 🎯 Architectural Alignment
* **Target Spec**: `docs/specs/product/004-registry-generator.md`
* **Scope**: 
    - `src/registry_generator.py` (New)
    - `.factory/index.json` (New/Output)
    - `.factory/contracts/aggregate_slice_info.json` (New/Contract)
    - `tests/test_registry_generator.py` (New)

## 🛡️ Execution Steps (Atomic & Deterministic)

1. **Step 1: Define Aggregated Contract**
    * **Description**: Create `.factory/contracts/aggregate_slice_info.json` based on the spec.
    * **Definition of Done (DoD)**: Contract file exists and is valid JSON.
    * **Validation**: `jsonschema` check against draft-07 (if available) or manual JSON structure verification.

2. **Step 2: Core Aggregation Logic**
    * **Description**: Implement `src/registry_generator.py` to scan `.factory/slices/` for `[A-Z]{3}-[0-9]{3}*.json` and aggregate them.
    * **Definition of Done (DoD)**: Script successfully identifies and parses all product slices.
    * **Validation**: Run script with debug logging to print discovered slices.

3. **Step 3: Token & Status Summarization**
    * **Description**: Add logic to read `.factory/telemetry.json` and calculate global status and token metrics.
    * **Definition of Done (DoD)**: Final `index.json` contains accurate summary data.
    * **Validation**: Compare `index.json` metadata with `telemetry.json` project totals.

4. **Step 4: Automated Testing**
    * **Description**: Create `tests/test_registry_generator.py` with mock slice data.
    * **Definition of Done (DoD)**: All tests pass.
    * **Validation**: `python3 -m pytest tests/test_registry_generator.py`

5. **Step 5: Integration & CI Setup**
    * **Description**: Run the generator on the actual repo and verify output against the contract.
    * **Definition of Done (DoD)**: Valid `.factory/index.json` generated.
    * **Validation**: `python3 src/registry_generator.py && check-jsonschema --schemafile .factory/contracts/aggregate_slice_info.json .factory/index.json`

## 💰 FinOps Forecast (Rating)
* **Complexity**: Medium
* **Forecasted Input**: 25,000 tokens
* **Forecasted Reasoning**: 5,000 tokens
* **Cache Strategy**: Re-use `.factory/contracts/schema_file.json` and `telemetry.json` context across implementation turns.
