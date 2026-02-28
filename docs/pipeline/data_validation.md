# Data Validation Strategy

This document defines the strategy for validating incoming raw data from Spansh and EDSM to ensure it matches our expected schema before it enters the "Silver" or "Gold" layers.

## 1. The Validation Trigger
Every new download (triggered by `data_manager.py`) must be validated before it is processed. This prevents "Schema Drift"—where an external API changes its JSON structure, causing our downstream pipelines to fail.

## 2. Validation Pattern: "Check-Before-Process"
We will use a **Schema-Match** validation pattern:
1. **Source:** Read a 1,000-line sample from the newly downloaded `.json.gz` file.
2. **Inference:** Use DuckDB to infer the schema of the new sample.
3. **Comparison:** Compare the new inferred schema against the "Master Schema" (the `.sql` files we already generated).
4. **Action:** If the core types (e.g., `id64` as BIGINT) match, proceed. If they mismatch, quarantine the file and alert the user.

## 3. Validation Rules
The `validate_data.py` script will check for:
- **Presence of Required Columns:** Does the file still have `id64` and `name`?
- **Type Compatibility:** Did a field change from `BIGINT` to `VARCHAR`?
- **Data Range (Optional):** Are the coordinates (`x`, `y`, `z`) within expected galactic ranges?
- **Null Checks:** Are essential fields (like `id64`) missing data in the new download?

## 4. Remediation Workflow
If validation fails:
1. **Quarantine:** Move the file to `data/quarantine/`.
2. **Log:** Write an error entry into `data/manifest.json`.
3. **Notify:** Flag the error in the console or log file for user review.
