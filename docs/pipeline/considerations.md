# Pipeline Considerations

Handling large datasets (500GB+) requires specific strategies for performance and stability.

## 1. The "Spatial Index" (PostGIS)
In standard SQL, you index a column like `id64`. But for a router, you need to find stars "near" a 3D point (x, y, z).
Without a spatial index, a query like "Find stars within 30ly" will take minutes; with it, it takes milliseconds.

- **The fix:** Use the **PostGIS extension for PostgreSQL**. It allows you to create a **GIST Index**.

## 2. Chunking the Parquet Files
Don't try to create one single 80GB Parquet file. If it gets corrupted, you lose everything.

- **The fix:** Partition your Parquet output. You could group them by "Region" or simply by every 1 million rows. This makes the "Load to Postgres" step much more stable because you can load one small file at a time.

## 3. Memory Management in Python
Even if you have 32GB of RAM, 500GB of JSON will crash your script if you try to load it all.

- **The fix:** You must use **Generators or Streaming Parsers** (like `ijson` or the built-in `gzip` module). This ensures your Python script only uses ~100MB of RAM regardless of how big the source file is.

## Architectural Note: Language Choice
- **The ETL:** Python is king here (`pandas` + `pyarrow`).
- **The API:** You can stay in Python (`FastAPI`/`Flask`) or switch to Node.js if you prefer its asynchronous nature for web traffic. Both handle PostgreSQL equally well.
