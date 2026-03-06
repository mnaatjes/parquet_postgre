# ETL Pipeline: The Enforcer (The Data Plane)

The ETL pipeline is the "Muscle" of the architecture. It is designed for one thing: moving massive amounts of data at maximum speed, safely.

## 1. The Execution Lifecycle

The ETL process follows a strict, non-negotiable lifecycle based on **Data Contracts**:

1.  **Contract Scan:** The ETL runner looks for contracts in `data/contracts/approved/`. If a contract is not "Approved," it is ignored.
2.  **Validation:** The ETL reads a sample from the *full* file and compares its current schema against the "Approved Master Schema." 
    *   **Fail Fast:** If anything is different (missing column, type change), the process stops instantly and flags a "Schema Drift" error.
3.  **Transformation (Explosion):** Based on the contract's normalization rules, the ETL uses DuckDB to:
    *   Stream-read the raw `json.gz`.
    *   "Explode" nested arrays into child Parquet files (e.g., `systems -> stations`).
    *   Drop unwanted columns and cast types to the exact specifications.
4.  **Loading:** The clean, normalized Parquet files are bulk-loaded into PostgreSQL using high-speed commands like `COPY`.

## 2. Key Characteristics
*   **Dumb & Fast:** The ETL doesn't "guess" types. It follows the contract exactly.
*   **Idempotent:** Running the same contract twice should result in the same output.
*   **Isolated:** The ETL code is generic and doesn't change when a new source is added—only the contracts change.
