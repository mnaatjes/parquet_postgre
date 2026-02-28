import duckdb
import os
import json
import gzip
import tempfile
from datetime import datetime

# Paths
SCHEMAS_DIR = "/srv/parquet/data/schemas"
RAW_DIR = "/srv/parquet/data/raw"

def get_master_schema(table_name):
    """Reads the inferred SQL schema to get the 'Master' column list and types."""
    sql_path = os.path.join(SCHEMAS_DIR, f"{table_name}.sql")
    if not os.path.exists(sql_path):
        return None
        
    with open(sql_path, 'r') as f:
        sql = f.read()
        
    # Extract column names and types (simple parsing for this proof of concept)
    lines = sql.split('
')[1:-1]
    master_schema = {}
    for line in lines:
        parts = line.strip().rstrip(',').split(' ')
        if len(parts) >= 2:
            col_name = parts[0]
            col_type = parts[1]
            master_schema[col_name] = col_type
    return master_schema

def validate_file(file_path, table_name):
    """Validates a new .json.gz file against the master schema."""
    master = get_master_schema(table_name)
    if not master:
        return False, f"Master schema for {table_name} not found."
        
    print(f"Validating {file_path} against {table_name} schema...")
    
    # Extract a small sample to a temp file for DuckDB to read
    with tempfile.NamedTemporaryFile(suffix='.json', mode='w') as tmp:
        with gzip.open(file_path, 'rt') as f_in:
            # We only need the first few objects to check the schema
            tmp.write(f_in.read(5000)) # 5KB should be enough
            tmp.flush()
            
            # Use DuckDB to infer schema of the new sample
            con = duckdb.connect(database=':memory:')
            try:
                con.execute(f"CREATE TABLE tmp AS SELECT * FROM read_json_auto('{tmp.name}', format='array')")
                new_columns = con.execute("DESCRIBE tmp").fetchall()
                
                new_schema = {col[0]: col[1] for col in new_columns}
                
                # Check for missing columns
                missing = [col for col in master if col not in new_schema]
                if missing:
                    return False, f"Missing core columns: {missing}"
                
                # Check for type changes
                type_mismatches = []
                for col, m_type in master.items():
                    if col in new_schema:
                        n_type = new_schema[col]
                        # DuckDB types can be slightly different (e.g. DOUBLE vs FLOAT), 
                        # so we check if the new type is 'compatible' or identical.
                        if m_type != n_type:
                            type_mismatches.append(f"{col}: expected {m_type}, got {n_type}")
                
                if type_mismatches:
                    return False, f"Type mismatches detected: {type_mismatches}"
                    
                return True, "Schema validation successful."
                
            except Exception as e:
                return False, f"Validation Error: {str(e)}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python3 validate_data.py <file_path> <table_name>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    table_name = sys.argv[2]
    
    success, message = validate_file(file_path, table_name)
    print(message)
    if not success:
        sys.exit(1)
