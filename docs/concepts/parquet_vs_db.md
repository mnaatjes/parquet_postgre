# Parquet vs. Database: The "Where" and "How"

To clear up the confusion: Parquet is a file format; a Database is a management system.

## Parquet is Binary
It is not human-readable like JSON or CSV. If you open a `.parquet` file in a text editor like Nano or VS Code, you'll see gibberish. You need a library (like Python's `pandas` or `pyarrow`) to read it. This is why it's so much smaller and faster—it's optimized for computers, not eyeballs.

## The Workflow
Usually, you don't "load" a database into Parquet. Instead, your ETL process produces Parquet files as your Long-term Storage. Then, you load the specific data you need from those Parquet files into a database (like PostgreSQL) for your application to use.

### Does the Database store data as Parquet?
Generally, no. Databases like PostgreSQL or SQLite have their own proprietary internal storage formats optimized for "Row-based" lookups (finding one specific ID).

## Data Layers and Formats

| Layer | Format | Purpose |
| :--- | :--- | :--- |
| **Bronze** | `json.gz` | The original source files from Spansh/EDSM. |
| **Silver** | Parquet | Your "Clean" data. Only IDs and Coords. Compressed and ready for math. |
| **Gold** | SQLite/Postgres | The "Active" data. Indexed by coordinates for your routing API. |
