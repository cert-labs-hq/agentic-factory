# Implementation Plan: FRT-001 (FinOps Dashboard)

## 1. Objective
Implement a single-page, zero-dependency static dashboard that visualizes the AI Factory's output. The dashboard will consume the `.factory/index.json` registry to display project velocity, token investment, and financial savings.

## 2. Architectural Constraints
- **Stack**: HTML5, Tailwind CSS (via CDN), Vanilla JavaScript (ES6+).
- **No-Build Policy**: Single file `dashboard/index.html`. No `npm`, `node_modules`, or Python backend.
- **Data Source**: Native `fetch()` targeting `../.factory/index.json`.
- **Aesthetic**: "Technical Architect" (Dark mode, monospace fonts, emerald/slate color palette).

## 3. DOM Mapping Contract
The implementation agent MUST map the following JSON fields from `index.json` to these specific HTML elements:

| JSON Source Field | HTML Target ID | Visual Representation |
| :--- | :--- | :--- |
| `metadata.total_slices` | `count-slices` | Big Metric Card |
| `metadata.total_token_investment` | `count-tokens` | Big Metric Card |
| `metadata.estimated_usd_saved` | `count-savings` | Big Metric Card (Text-Emerald-400) |
| `slices[]` (Array) | `registry-table-body` | Dynamic Table Rows |
| `metadata.last_registry_update` | `last-updated` | Footer Timestamp |

## 4. Execution Steps (Visual-TDD Protocol)

### Step 1: Structural Skeleton
- Create `dashboard/index.html`.
- Define a grid-based layout: 
    - `nav`: Project title and status badge.
    - `header`: 3 KPI Cards for Slices, Tokens, and Savings.
    - `main`: A container for the `<table>` with headers (ID, Name, Status, Usage).
    - `footer`: Version and timestamp.

### Step 2: Styling & Aesthetic (Tailwind)
- Apply `bg-slate-950` and `text-slate-200`.
- Use `font-mono` for all numeric values and IDs.
- Define status badges classes:
    - `.status-approved`: `bg-emerald-500/10 text-emerald-400`
    - `.status-in-progress`: `bg-amber-500/10 text-amber-400`
    - `.status-planned`: `bg-slate-500/10 text-slate-400`

### Step 3: Data Ingestion (Fetch Logic)
- Implement `async function initDashboard()`.
- Fetch `../.factory/index.json`.
- Handle "File Not Found" errors by displaying a UI notification in the `registry-table-body`.

### Step 4: Reactive Rendering
- Create `renderMetrics(metadata)` to update the KPI cards.
- Create `renderTable(slices)` to map the array into `<tr>` templates.
- **Logic Rule**: Format `total_token_investment` with commas and `estimated_usd_saved` with two decimal places.

### Step 5: Verification & Audit
- Serve via `python3 -m http.server` and verify fetch success.
- Confirm mobile responsiveness (Table should scroll horizontally on small screens).

## 5. Definition of Done
- `dashboard/index.html` is fully functional and standalone.
- The UI accurately reflects the data in the current `.factory/index.json`.
- Zero console errors during the fetch and render lifecycle.
- Metadata for FRT-001 updated to `Status: In Review / Phase: validation`.

## 💰 FinOps Forecast
- **Complexity**: Low-Medium (Single-turn implementation).
- **Input Tokens**: ~8k (with spec context).
- **Output Tokens**: ~1.2k (Single HTML file).