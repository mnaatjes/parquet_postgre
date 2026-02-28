# Data Pipeline Architecture

This document defines the end-to-end workflow for processing 200GB+ of Elite Dangerous data within our infrastructure constraints.

## 1. The Optimized Pipeline Flow

Your proposed flow is conceptually correct but can be optimized to save disk space and processing time. We will use a "Stream-Normalize" approach:

| Phase | Action | Tool | Description |
| :--- | :--- | :--- | :--- |
| **1. Ingestion** | `Download` | `curl` / `wget` | Retrieve `.json.gz` files into `data/raw/`. |
| **2. Transformation** | `Stream-Normalize` | **DuckDB** | **Critical Step:** Instead of converting 1:1 to Parquet, we use DuckDB to read the JSON and "explode" it directly into multiple **Normalized Parquet** files (Systems, Stations, Bodies). |
| **3. Staging** | `Schema Prep` | `SQL` | Create the PostgreSQL database and tables using the SQL definitions in `data/schemas/`. |
| **4. Ingestion** | `Bulk Load` | `psql COPY` | Load the normalized Parquet files into PostgreSQL. |

---

## 2. Detailed Step-by-Step

### Step 1: Raw Data (`.json.gz`)
We keep the data compressed to save space. A 200GB JSON file might only be 20GB when compressed. We never uncompress these fully on disk.

### Step 2: The DuckDB "Explosion" (Normalization)
DuckDB can read `.json.gz` files directly. We write a Python script that tells DuckDB:
1. "Read `systemsPopulated.json.gz`."
2. "Select the core system fields and save as `systems.parquet`."
3. "Unnest (explode) the `stations` array and save as `stations.parquet`."
4. "Unnest the `factions` array and save as `factions.parquet`."

**Why Parquet?** Parquet is columnar. If you only want to query "Station Names," the database only reads the "Name" column from disk. It's much faster than JSON for the next steps.

### Step 3: PostgreSQL Schema Setup
Using our `data/schemas/*.sql` files, we initialize the database. We apply Primary Keys at this stage, but we **wait** to apply Foreign Key constraints until *after* the data is loaded to speed up the process.

### Step 4: High-Speed Loading
PostgreSQL cannot read Parquet natively without an extension (like `pg_duckdb` or `foreign data wrappers`). 
- **Option A:** Convert Parquet to a temporary CSV (very fast in DuckDB) and use `COPY`.
- **Option B:** Use the `pg_duckdb` extension to let Postgres "see" the Parquet files directly.

---

## 3. Handling Disk Constraints (30GB Limit)
Since we have 200GB+ of potential data and only 30GB of free space:
1. **Incremental Processing:** We process one file at a time (e.g., process `systems_1day`, load it, then delete the intermediate Parquet before starting `bodies`).
2. **External Storage:** If the final PostgreSQL database exceeds 30GB, we will need to consider using **DuckDB** as the primary database instead of Postgres, as DuckDB stores data much more efficiently on disk.

## 4. Manifest Tracking
Every step (Download -> Parquet -> DB Load) is recorded in `data/manifest.json` to ensure we can resume if the pipeline fails.
