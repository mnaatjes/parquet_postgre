# Data Normalization Strategy

This document outlines the strategy for transforming nested Elite Dangerous JSON datasets (from Spansh and EDSM) into a normalized relational schema. Normalization is essential for efficient querying in PostgreSQL and maintaining data integrity across millions of records.

## 1. Core Objectives
- **Eliminate Redundancy:** Avoid storing system metadata (like coordinates) multiple times within station or body records.
- **Query Flexibility:** Enable direct searches on stations, factions, or materials without "unpacking" system-level objects.
- **Scalability:** Ensure the database can handle 200GB+ of data by optimizing table sizes and indexing.

## 2. Entity Relationship Model (ERM)

We will decompose the massive `systemsPopulated.json` and `bodies7days.json` files into the following primary entities:

### A. The "Systems" Layer (Parent)
- **Table: `systems`**
  - `id64` (Primary Key - BIGINT)
  - `name` (VARCHAR)
  - `x`, `y`, `z` (DOUBLE - Flattened from `coords` struct)
  - `allegiance`, `government`, `state`, `security` (VARCHAR)
  - `population` (BIGINT)
  - `update_time` (TIMESTAMP)

### B. The "Station" Layer (Child of Systems)
- **Table: `stations`**
  - `id` (Primary Key - BIGINT)
  - `system_id64` (Foreign Key - BIGINT)
  - `name`, `type` (VARCHAR)
  - `market_id`, `distance_to_arrival` (BIGINT)
  - `has_market`, `has_shipyard`, `has_outfitting` (BOOLEAN)
- **Table: `station_services`** (Bridge Table for Many-to-Many)
  - `station_id` (Foreign Key)
  - `service_name` (VARCHAR)

### C. The "Body" Layer (Child of Systems)
- **Table: `bodies`**
  - `id64` (Primary Key - BIGINT)
  - `system_id64` (Foreign Key - BIGINT)
  - `name`, `type`, `sub_type` (VARCHAR)
  - `distance_to_arrival`, `gravity`, `earth_masses`, `radius` (DOUBLE)
  - `is_landable`, `is_main_star` (BOOLEAN)
- **Table: `body_materials`** (Child of Bodies)
  - `body_id64` (Foreign Key)
  - `material_name` (VARCHAR)
  - `percentage` (DOUBLE)

### D. The "Faction" Layer (Child of Systems)
- **Table: `factions`**
  - `id` (Primary Key - BIGINT)
  - `name`, `allegiance`, `government` (VARCHAR)
- **Table: `system_factions`** (Many-to-Many Bridge)
  - `system_id64` (Foreign Key)
  - `faction_id` (Foreign Key)
  - `influence` (DOUBLE)
  - `state` (VARCHAR)

## 3. Implementation Workflow

### Phase 1: Flattening with DuckDB
We will use DuckDB's `UNNEST` function to "explode" the nested arrays in the JSON samples.
```sql
-- Example: Extracting stations from systems
CREATE TABLE stations AS 
SELECT 
    id64 as system_id64,
    UNNEST(stations).id as station_id,
    UNNEST(stations).name as station_name
FROM read_json_auto('systemsPopulated.sample.json');
```

### Phase 2: Parquet Intermediate Storage
To handle 200GB+ without crashing memory:
1. Stream the raw JSON through a Python script.
2. Use DuckDB to transform chunks of data into normalized Parquet files (e.g., `systems.parquet`, `stations.parquet`).
3. Parquet files will preserve the inferred types while being 10x smaller than JSON.

### Phase 3: PostgreSQL Bulk Load
Once normalized Parquet files are created, we will use the PostgreSQL `COPY` command or the `pg_duckdb` extension to perform high-speed ingestion.

## 4. Key Challenges & Solutions
- **ID Collisions:** Use `id64` as the primary identifier wherever possible, as it is a unique 64-bit integer provided by the Elite Dangerous API.
- **Memory Management:** Processing 200GB files will be done using **Dask** or **DuckDB's disk-spilling** capabilities to ensure we don't exceed the available 30GB of disk/RAM.
- **Data Integrity:** We must implement Foreign Key constraints *after* the initial bulk load to ensure the ingestion speed isn't bottlenecked by constraint checking.
