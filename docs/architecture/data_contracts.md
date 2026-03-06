# Data Contracts: The Handshake

The Data Contract is the single point of truth that decouples the Control Plane from the Data Plane. It is the formal agreement between the "Lab" and the "Factory."

## 1. Anatomy of a Contract

A contract (`.json` or `.yaml`) contains everything the ETL needs to know:

```json
{
  "source_id": "systems_populated_v1",
  "raw_uri": "data/raw/systemsPopulated.json.gz",
  "status": "APPROVED",
  "schema_definition": "data/schemas/master/systems.sql",
  "normalization_rules": {
    "explode": ["stations", "factions"],
    "drop": ["eddb_id", "needs_permit"],
    "rename": {"id64": "system_id"}
  },
  "metadata": {
    "approved_by": "human_user",
    "approved_at": "2026-03-06",
    "hash_v1": "sha256:..."
  }
}
```

## 2. Schema Lifecycle (State Machine)

Contracts and schemas move through a controlled state machine:

1.  **INFERRED:** Machine output in `data/schemas/inferred/`.
2.  **PROPOSED:** In `data/contracts/pending/`. Awaiting human review.
3.  **APPROVED:** In `data/contracts/approved/`. The ETL reads this.
4.  **MASTER:** The final SQL schema in `data/schemas/master/` referenced by the approved contract.

## 3. Benefits of Contracts
*   **Versioning:** You can have `v1` and `v2` of a contract running side-by-side during a transition.
*   **Human-in-the-Loop:** A human must explicitly promote a contract to the "APPROVED" folder for the system to act.
*   **Traceability:** You have a historical record of who signed off on which schema and when.
