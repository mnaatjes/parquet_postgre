# Data Contracts: The Interface

A Data Contract is a **formal agreement** between a data producer and a data consumer. In our architecture, it is the "handshake" between the **Control Plane (SIP)** and the **Data Plane (ETL)**.

## 1. The Anatomy of a Contract

A robust Data Contract should include four key sections:

| Section | Purpose | Example |
| :--- | :--- | :--- |
| **Identity** | Who is this? Where is it? | `source_id: "systems_v1"`, `raw_uri: "s3://..."` |
| **Schema** | What is the structure? | `columns: { "id64": "BIGINT", "name": "VARCHAR" }` |
| **Quality** | What are the rules? | `rules: { "id64": "NOT NULL", "x": "BETWEEN -40k AND 40k" }` |
| **Transformation** | How do we change it? | `normalization: { "explode": ["stations"] }` |

## 2. Directory Structure for Contracts

Version-controlling your contracts is essential for managing changes over time.

```text
/data/contracts
├── v1/
│   ├── systems.contract.json
│   └── bodies.contract.json
└── v2/                         # When Spansh changes their API
    └── systems.contract.json
```

## 3. JSON Example: A Complete Contract

```json
{
  "contract_version": "1.0",
  "source": {
    "id": "ed_systems_populated",
    "format": "json.gz",
    "path": "data/raw/systemsPopulated.json.gz"
  },
  "schema": {
    "target_table": "systems",
    "columns": [
      {"name": "id64", "type": "BIGINT", "primary_key": true},
      {"name": "name", "type": "VARCHAR", "nullable": false},
      {"name": "x", "type": "DOUBLE"},
      {"name": "y", "type": "DOUBLE"},
      {"name": "z", "type": "DOUBLE"}
    ]
  },
  "normalization": {
    "strategy": "explode_child_arrays",
    "children": [
      {"array_name": "stations", "target_table": "stations"},
      {"array_name": "factions", "target_table": "factions"}
    ]
  },
  "status": "APPROVED",
  "owner": "engineer_name"
}
```

## 4. The Benefit: "No Surprises"

- **Contract Enforcement:** If the incoming data doesn't match the contract, the ETL fails *before* it messes up your database.
- **Consumer Trust:** The developer building the API (The Consumer) can read the contract and know exactly what data will be in the PostgreSQL tables without looking at the ETL code.
- **Audit Trail:** You can see exactly when a human "Approved" a change to the schema.
