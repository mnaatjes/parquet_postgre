# Decoupled Directory Structure

This document illustrates how the Control Plane (SIP) and Data Plane (ETL) are physically separated to avoid "Big Ball of Mud" code bloat.

## 1. Project Root (`/srv/parquet`)

```text
├── src/
│   ├── common/                # Shared Domain Models (Contract, Manifest)
│   ├── sip/                   # CONTROL PLANE (The Lab)
│   │   ├── discovery/         # DuckDB Inference
│   │   ├── analyzer.py        # Inferred vs. Master Comparison
│   │   └── promoter.py        # HITL Sign-off logic
│   └── etl/                   # DATA PLANE (The Factory)
│       ├── validator.py       # Strict Schema Enforcement
│       ├── transformer.py     # High-speed 'Explosion'
│       └── loader.py          # PostgreSQL Bulk Load
│
├── data/
│   ├── contracts/             # THE COUPLING POINT (Data Contracts)
│   │   ├── pending/           # Draft contracts from SIP
│   │   └── approved/          # Final contracts for ETL
│   ├── schemas/               # Artifacts referenced by contracts
│   │   ├── inferred/          # Auto-generated SQL
│   │   └── master/            # Human-signed-off SQL
│   ├── samples/               # Small files for SIP
│   └── raw/                   # Massive json.gz files for ETL
```

## 2. Key Separation Rules
1.  **Code:** `src/etl` never imports from `src/sip`. They only share `src/common`.
2.  **Data:** `data/contracts/approved/` is the only source of truth for the ETL.
3.  **Ownership:** The human "owns" `data/schemas/master/`. The machine "owns" `data/schemas/inferred/`.
