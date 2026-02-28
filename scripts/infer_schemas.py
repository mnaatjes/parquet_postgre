import duckdb
import os
import json
from datetime import datetime

SAMPLES_DIR = "/srv/parquet/data/samples"
SCHEMAS_DIR = "/srv/parquet/data/schemas"  # Moving to data/schemas to keep with manifest
MANIFEST_PATH = "/srv/parquet/data/manifest.json"

def infer_schema(sample_path):
    table_name = os.path.basename(sample_path).replace(".sample.json", "").replace(".", "_")
    print(f"Inferring schema for {table_name}...")
    
    con = duckdb.connect(database=':memory:')
    
    # DuckDB's read_json_auto is powerful for type inference
    # We use format='array' because your samples are JSON arrays
    try:
        con.execute(f"CREATE TABLE tmp AS SELECT * FROM read_json_auto('{sample_path}', format='array')")
        
        # Get column info
        columns = con.execute("DESCRIBE tmp").fetchall()
        
        sql_lines = [f"CREATE TABLE {table_name} ("]
        summary_rows = []
        
        pk_suggestions = ['id64', 'id', 'systemId64', 'systemId']
        suggested_pk = None
        
        for col in columns:
            name, dtype, null, pk, dflt, extra = col
            
            # Suggest PK
            pk_suffix = ""
            if not suggested_pk and name.lower() in pk_suggestions:
                suggested_pk = name
                pk_suffix = " PRIMARY KEY"
            
            sql_lines.append(f"    {name} {dtype}{pk_suffix},")
            summary_rows.append(f"| {name} | {dtype} | {'Yes' if pk_suffix else 'No'} |")
            
        # Remove trailing comma from last column
        sql_lines[-1] = sql_lines[-1].rstrip(',')
        sql_lines.append(");")
        
        sql_content = "\n".join(sql_lines)
        sql_path = os.path.join(SCHEMAS_DIR, f"{table_name}.sql")
        
        with open(sql_path, 'w') as f:
            f.write(sql_content)
            
        return table_name, sql_path, summary_rows
        
    except Exception as e:
        print(f"Error inferring {table_name}: {e}")
        return None, None, None

def update_manifest(schema_info):
    with open(MANIFEST_PATH, 'r') as f:
        manifest = json.load(f)
    
    for name, path, _ in schema_info:
        entry = {
            "table_name": name,
            "path": os.path.relpath(path, "/srv/parquet"),
            "inferred_at": datetime.now().strftime("%Y-%m-%d")
        }
        if not any(s['table_name'] == name for s in manifest['data'].get('inferred_schemas', [])):
            if 'inferred_schemas' not in manifest['data']:
                manifest['data']['inferred_schemas'] = []
            manifest['data']['inferred_schemas'].append(entry)
            
    with open(MANIFEST_PATH, 'w') as f:
        json.dump(manifest, f, indent=2)

if __name__ == "__main__":
    os.makedirs(SCHEMAS_DIR, exist_ok=True)
    sample_files = [os.path.join(SAMPLES_DIR, f) for f in os.listdir(SAMPLES_DIR) if f.endswith(".json")]
    
    all_summaries = {}
    schema_results = []
    
    for sample in sample_files:
        name, path, summary = infer_schema(sample)
        if name:
            schema_results.append((name, path, summary))
            all_summaries[name] = summary
            
    update_manifest(schema_results)
    
    # Create a Summary Markdown file
    with open(os.path.join(SCHEMAS_DIR, "SUMMARY.md"), "w") as f:
        f.write("# Inferred Schemas Summary\n\n")
        for table, rows in all_summaries.items():
            f.write(f"## {table}\n")
            f.write("| Column | Type | Suggested PK |\n")
            f.write("| :--- | :--- | :--- |\n")
            f.write("\n".join(rows) + "\n\n")
    

    print(f"Successfully inferred {len(schema_results)} schemas. Check {SCHEMAS_DIR} for details.")
