# SIP: Structured Intake Protocol (The Control Plane)

The SIP protocol is the human-centric "Brain" of the data architecture. It handles discovery and sign-off for new or changed data sources.

## 1. The Structured Intake Workflow

When a new source file arrives (previously unknown or with a format change):

1.  **Isolation (Extraction):** SIP extracts a representative sample (e.g., first 10,000 lines) of the raw `json.gz` file.
2.  **Inference (Discovery):** DuckDB interrogates the sample to infer column names, types, and structure.
3.  **Refinement (Proposed Schema):** SIP generates a "Proposed" schema and normalization strategy.
4.  **Human Review (Sign-off):** An engineer reviews the proposed schema and manually edits it to:
    *   Delete unnecessary columns.
    *   Correct data types (e.g., `FLOAT` to `BIGINT`).
    *   Design the "Explosion" (Normalization) into child tables.
5.  **Promotion (Approval):** Once satisfied, the engineer runs a "Promote" command. SIP validates the manual edits, updates the **Data Contract**, and moves the schema to the "Master" directory.

## 2. Key Artifacts
*   **Inferred Schema:** Raw machine output from DuckDB.
*   **Proposed Contract:** A draft JSON contract awaiting approval.
*   **Approved Contract:** A final JSON contract that the ETL recognizes as "Production-Ready."

## 3. Organizational Role
SIP lives in its own standalone package (`src/sip/`). It is designed for interactive CLI use. Its primary goal is to produce high-quality, verified metadata for the ETL pipeline.
