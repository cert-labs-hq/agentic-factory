# Product Slices Overview: Agentic Code Supply Chain

This document serves as the master blueprint for the **Agentic Factory** MVP, defining the transition from non-deterministic AI labor to a deterministic, warehoused implementation.

## 1. Core Infrastructure (Foundations)
*   **BKP-001-BOOTSTRAP**: Initial repository structure and schema definition. [Status: **Warehoused**]
*   **BKP-002-TELEMETRY-SYSTEM**: Implementation of the universal telemetry logging protocol for token usage. [Status: **Warehoused**]
*   **BKP-003-SCHEMA-VALIDATOR**: Automated validation of slice JSONs against the master contract to ensure architectural alignment. [Status: **Planned - P0**]

## 2. Warehouse & Logistics (Backend)
*   **BKP-004-REGISTRY-GENERATOR**: Logic to aggregate individual slice JSONs into a single `index.json` registry for static consumption. [Status: **Planned - P0**]
*   **BKP-005-SYNC-ENGINE**: GitHub Action to synchronize local slice data with the GitHub Pages "Warehouse" using deterministic git-auto-commits. [Status: **Planned - P0**]
*   **BKP-006-TELEMETRY-AGGREGATOR**: Service to process token metrics and calculate "Shadow Costs" for LLM FinOps reporting. [Status: **Proposed - P2**]
*   **BKP-007-GIT-BRIDGE**: Integration logic to transition slice states (e.g., `In Review` to `Approved`) based on Pull Request and Git Tag events. [Status: **Proposed - P1**]

## 3. Security & Quality (The Guard)
*   **SEC-001-GATEKEEPER**: Implementation of SAST (Static Analysis) and SCA (Dependency Scanning) via GitHub Actions to protect the factory output. [Status: **Planned - P1**]

## 4. Frontend Dashboard (The Showroom)
*   **FRT-001-DASHBOARD-SHELL**: Basic React/Tailwind/TypeScript application structure hosted via GitHub Pages. [Status: **Planned - P0**]
*   **FRT-002-SLICE-EXPLORER**: Searchable interface to visualize the current state of the "Warehouse" based on the `index.json` registry. [Status: **Planned - P1**]
*   **FRT-003-FINOPS-METRICS**: Visual dashboard for monitoring "Token Economics" (Input vs. Reasoning vs. Output tokens). [Status: **Proposed - P2**]

---

## 5. Implementation Roadmap

| Slice ID | Title | Component | Priority | Side |
| :--- | :--- | :--- | :--- | :--- |
| **BKP-003** | **Schema Enforcement** | Foundations | **P0** | BACK |
| **BKP-005** | **GitHub Sync Engine** | Warehouse | **P0** | BACK |
| **BKP-004** | **Registry Generator** | Warehouse | **P0** | BACK |
| **FRT-001** | **Dashboard Shell** | Showroom | **P0** | FRONT |
| **SEC-001** | **Security Gatekeeper** | Guard | **P1** | SEC |
| **BKP-007** | **Git Bridge Logic** | Logistics | **P1** | BACK |
| **FRT-002** | **Slice Visualization**| Showroom | **P1** | FRONT |
| **FRT-003** | **FinOps Dashboard** | Showroom | **P2** | FRONT |