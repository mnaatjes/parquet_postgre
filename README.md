# Parquet Data Pipeline & Prototyping

This project is a high-performance framework designed for downloading, processing, and analyzing massive datasets (200GB+). It provides a structured workflow to determine database schemas and ingestion pipelines using "Contract-First Engineering" principles.

## Core Components

### 1. Data Management (`data/`, `scripts/`)
The project implements a multi-stage data lifecycle:
*   **Raw Storage:** Handles multi-hundred GB files in `data/raw/` (ignored by Git).
*   **Sampling:** `scripts/create_samples.py` generates smaller subsets in `data/samples/` for rapid prototyping.
*   **Schema Discovery:** `scripts/infer_schemas.py` extracts SQL or JSON schema definitions, which are stored in the `schemas/` directory.
*   **Processing:** `scripts/normalize_to_parquet.py` transforms and cleans data using DuckDB, Polars, and PyArrow.
*   **Validation:** `scripts/validate_data.py` ensures data integrity before final ingestion.

### 2. Knowledge Base (`docs/`)
Extensive documentation covering:
*   **Architecture:** ETL pipelines, data contracts, and "Control vs. Data Plane" design.
*   **Concepts:** Spatial indexing, normalization, and Parquet vs. traditional databases.
*   **Lab/Practice:** Guides for PostgreSQL setup and spatial data analysis.

### 3. Tech Stack
*   **Querying:** **DuckDB** for out-of-core processing of massive files.
*   **Manipulation:** **Polars**, **PyArrow**, and **Dask** for high-speed, parallelized data handling.
*   **JSON Parsing:** **ijson** for memory-efficient iterative parsing of large JSON structures.

## Directory Structure

| Directory | Purpose |
| :--- | :--- |
| `data/raw/` | **Storage for original datasets.** Contains the multi-hundred GB files as downloaded from sources. |
| `data/samples/` | **Prototyping subsets.** Contains small slices of data (e.g., first 10k rows) used for development. |
| `data/processed/` | **Transformed output.** Optimized Parquet formats ready for database ingestion. |
| `docs/` | **Knowledge Base.** Documentation, lab setups, and pipeline strategy guides. |
| `scripts/` | **Automation.** Python scripts for data extraction, schema discovery, and bulk processing. |
| `schemas/` | **Definitions.** SQL `CREATE TABLE` statements or JSON schema definitions. |
| `notebooks/` | **Exploration.** Jupyter Notebooks for interactive EDA. |

## Getting Started

### 1. Environment Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Recommended Workflow
1. Download a large file into `data/raw/`.
2. Use a script in `scripts/` to generate a small sample in `data/samples/`.
3. Use `duckdb` or `polars` to inspect the schema of the sample.
4. Export the resulting schema to the `schemas/` directory.
