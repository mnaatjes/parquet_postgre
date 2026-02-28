# Parquet Data Pipeline & Prototyping

This project is designed for downloading, processing, and analyzing massive datasets (200GB+) to determine database schemas and ingestion workflows.

## Directory Structure

| Directory | Purpose |
| :--- | :--- |
| `data/raw/` | **Storage for original datasets.** Contains the multi-hundred GB files (Parquet, JSON, CSV) as downloaded from sources. Always ignored by Git. |
| `data/samples/` | **Prototyping subsets.** Contains small slices of data (e.g., first 10k rows) used for rapid development and schema testing. |
| `data/processed/` | **Transformed output.** Files that have been cleaned or converted into optimized Parquet formats before database ingestion. |
| `docs/` | **Knowledge Base.** Contains conceptual documentation, lab setups, and pipeline strategy guides. |
| `scripts/` | **Automation.** Python scripts for data extraction, schema discovery, and bulk processing. |
| `schemas/` | **Definitions.** Extracted SQL `CREATE TABLE` statements or JSON schema definitions used for database mapping. |
| `notebooks/` | **Exploration.** Jupyter Notebooks for interactive data visualization and ad-hoc analysis. |

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

## Tools Overview
- **DuckDB**: For querying 200GB+ files directly on disk without memory overflow.
- **Polars/PyArrow**: High-performance data manipulation.
- **ijson**: Iterative JSON parsing for massive JSON structures.
- **Dask**: Parallelized processing for multi-core scaling.
