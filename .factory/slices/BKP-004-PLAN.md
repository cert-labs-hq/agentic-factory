## 🎯 Architectural Alignment
* **Target Spec**: `docs/specs/product/004-registry-generator.md`
* **Scope**: 
    - `src/registry_generator.py` (New)
    - `.factory/slices/index.json` (New/Output)
    - `.factory/contracts/aggregate_slice_info.json` (Verify Existing)
    - `tests/test_registry_generator.py` (New)

## 🛡️ Execution Steps (Atomic & Deterministic)

1. **Step 1: Environment & Contract Setup**
    * **Description**: Verify `.factory/contracts/aggregate_slice_info.json` exists. Initialize `src/registry_generator.py` with `argparse` for directory inputs.
    * **DoD**: Script runs with `--help` and contract is readable.
    * **Validation**: `python3 src/registry_generator.py --help`

2. **Step 2: Deterministic Scanner**
    * **Description**: Implement `glob` or `os.listdir` with the regex `^[A-Z]{3}-[0-9]{3}.*\.json$`. 
    * **DoD**: Script ignores non-conforming files and master schemas.
    * **Validation**: Log the count of discovered slices (e.g., "Found 12 valid slices").

3. **Step 3: FinOps & Status Aggregation**
    * **Description**: Iterate through slices to sum tokens. 
    * **Logic**: Implement the "Savings Formula": 
      $$Savings = (CacheReadTokens \times 0.10) \times Rate_{standard}$$ 
      *(Note: Use 0.10 as the multiplier for the cache discount).*
    * **DoD**: Summary includes `Quota-Blocked` count and `total_cache_read_tokens`.
    * **Validation**: Manually verify the sum of 2 slices against the generated `index.json`.

4. **Step 4: Self-Validation Layer**
    * **Description**: Add a `validate_output()` function using `jsonschema` (or a strict dictionary check) before writing to disk.
    * **DoD**: Script exits with code 1 if the generated registry violates the contract.
    * **Validation**: Temporary break a slice's JSON and ensure the generator fails.

5. **Step 5: Manual Runtime Verification**
    * **Description**: Execute the full script locally using actual project slices to ensure integration readiness.
    * **DoD**: `.factory/index.json` is generated correctly without errors.
    * **Validation**: `python3 src/registry_generator.py`

6. **Step 6: CI/CD Registry Hook**
    * **Description**: Add a "Final Check" step to the existing GitHub Action to run this generator and commit the `index.json`.
    * **DoD**: GitHub Pages dashboard shows updated metrics after a push.
    * **Validation**: Check the "Actions" tab for a successful registry sync.

## 💰 FinOps Forecast (Rating)
* **Complexity**: Medium
* **Forecasted Input**: 28,000 tokens
* **Forecasted Reasoning**: 4,000 tokens
* **Cache Strategy**: The Registry Generator will become the "Heavy Reader." By keeping the slice structure consistent, we maximize the **83.8% cache hit rate** seen in your `/stats`.