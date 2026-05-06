# Product Slices Overview

This document outlines the planned and proposed slices for the Agentic Code Supply Chain project, categorized by functional domain and implementation side.

## 1. Core Infrastructure (Foundations)
- **BKP-001-BOOTSTRAP**: Initial repository structure and schema definition. [Status: Warehoused]
- **BKP-002-TELEMETRY-SYSTEM**: Implementation of the universal telemetry logging protocol. [Status: Warehoused]
- **BKP-003-SCHEMA-VALIDATOR**: Automated validation of slice JSONs against the master schema. [Status: Planned]

## 2. Backend Services (BACK)
- **BKP-004-API-CORE**: REST API to serve slice metadata from `.factory/slices/`. [Status: Planned]
- **BKP-005-SYNC-GITHUB**: GitHub Action to synchronize local slice data with the dashboard backend/storage. [Status: Planned]
- **BKP-006-TELEMETRY-AGGREGATOR**: Service to process `telemetry.json` and generate project-wide token metrics. [Status: Proposed]
- **BKP-007-GIT-BRIDGE**: Integration logic to automatically transition slice states based on Pull Request and Git Tag events. [Status: Proposed]

## 3. Frontend Dashboard (FRONT)
- **FRT-001-DASHBOARD-SHELL**: Basic React/Tailwind application structure with navigation. [Status: Planned]
- **FRT-002-SLICE-EXPLORER**: Searchable and filterable interface to visualize the current state of all slices. [Status: Planned]
- **FRT-003-SLICE-DETAILS**: Detailed view for individual slices, showing telemetry history and specifications. [Status: Proposed]
- **FRT-004-FINOPS-METRICS**: Visual dashboard for monitoring "Token Economics" (input vs. reasoning vs. output tokens). [Status: Proposed]
- **FRT-005-PIPELINE-VIEW**: Graphical representation of the State Machine flow for active slices. [Status: Proposed]

## 4. Implementation Roadmap
| Slice ID | Title | Phase | Side | Priority |
| :--- | :--- | :--- | :--- | :--- |
| BACK-API-CORE | API to expose JSONs | Specs | BACK | P0 |
| BACK-SYNC-GITHUB | Sync functionality (GH Action) | Specs | BACK | P0 |
| FRONT-DASHBOARD-SHELL | Basic Dashboard Web App | Specs | FRONT | P0 |
| BACK-SCHEMA-VALIDATOR | Schema Enforcement | Specs | BACK | P1 |
| FRONT-SLICE-EXPLORER | Slice Visualization | Planning | FRONT | P1 |
| BACK-TELEMETRY-AGGREGATOR| Token Usage Aggregation | Planning | BACK | P2 |
| FRONT-FINOPS-METRICS | FinOps Dashboard | Implementation| FRONT | P2 |
