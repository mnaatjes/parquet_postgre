# Exploratory Data Analysis (EDA) in Data Engineering

In Data Engineering, EDA is not about finding "business insights" (like a Data Scientist); it is about **profiling the structure, health, and weirdness** of the raw source files before you write a single line of ETL code.

## 1. The Engineering EDA Lifecycle

1.  **Sampling:** Extracting 1% of the data to see the "shape" of the JSON.
2.  **Inference:** Using tools (like DuckDB) to guess the data types.
3.  **Profiling:** Checking for NULLs, empty arrays, or massive outliers in coordinates.
4.  **Refinement:** Adjusting the "Contract" to handle these edge cases.

## 2. DuckDB: The King of Engineering EDA

DuckDB allows you to "interrogate" a JSON file without loading it into a database.

```sql
-- How many records have missing coordinates?
SELECT count(*) 
FROM read_json_auto('systems.sample.json') 
WHERE coords IS NULL;

-- What is the deepest level of nesting in the 'stations' array?
SELECT max(len(stations)) 
FROM read_json_auto('systems.sample.json');
```

## 3. Python Profile Example

This script demonstrates a basic "Profiler" that helps you decide on your data types.

```python
import duckdb

# Connect to an in-memory database
con = duckdb.connect(database=':memory:')

def profile_json(file_path):
    # Let DuckDB scan the first 20k lines
    con.execute(f"CREATE TABLE profile AS SELECT * FROM read_json_auto('{file_path}')")
    
    # Get high-level stats
    stats = con.execute("DESCRIBE profile").fetchall()
    
    print("| Column | Inferred Type | Nullable? |")
    print("| :--- | :--- | :--- |")
    for col in stats:
        print(f"| {col[0]} | {col[1]} | {col[2]} |")

# Running this on your sample tells you if 'id64' is really an INT or a FLOAT
profile_json('data/samples/systemsPopulated.sample.json')
```

## 4. Key Questions to Answer during EDA

- **Is the file truly JSON?** Is it an array of objects or one object per line (NDJSON)?
- **Are there nested arrays?** Do we need to "explode" (normalize) them into their own tables?
- **What is the Primary Key?** Is `id64` unique, or do we need a composite key?
- **What is the data range?** Are coordinates `x, y, z` within the expected 0-40,000 range?
