# Pipeline Stages

The transformation from raw data to a serving API involves six distinct stages.

| Stage | Process | Data Format | Goal |
| :--- | :--- | :--- | :--- |
| **1. Ingestion** | Download + Checksum (MD5/SHA) | `.json.gz` | Ensure data integrity from the source (e.g., Spansh/EDSM). |
| **2. Transformation** | "Stream, Filter {id64, coords}, & Write" | Parquet | Reduce 500GB of "noise" into a lean, binary "Silver" layer. |
| **3. Validation** | Row-count & Checksum | Parquet | Ensure no systems were lost during the stream/transform. |
| **4. Loading** | `COPY` or Bulk Insert | PostgreSQL | Move the data into a system designed for high-speed lookups. |
| **5. Indexing** | `CREATE INDEX` (Spatial) | DB Internal | (Crucial Step) Enable the DB to find coordinates without scanning every row. |
| **6. Serving** | API Query -> Algorithm -> JSON | Result Set | Calculate the jump path and return it to the user/client. |
