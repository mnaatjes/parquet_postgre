import duckdb
import os
import json
from datetime import datetime

# Paths
SAMPLES_DIR = "/srv/parquet/data/samples"
PROCESSED_DIR = "/srv/parquet/data/processed"
MANIFEST_PATH = "/srv/parquet/data/manifest.json"

def normalize_systems_populated(sample_filename):
    """
    Demonstrates normalizing systemsPopulated.json into two separate 
    Parquet files: systems and stations.
    """
    sample_path = os.path.join(SAMPLES_DIR, sample_filename)
    
    # Define output paths
    systems_output = os.path.join(PROCESSED_DIR, "systems_core.parquet")
    stations_output = os.path.join(PROCESSED_DIR, "stations.parquet")
    
    # Initialize DuckDB
    con = duckdb.connect(database=':memory:')
    
    print(f"--- Normalizing {sample_filename} ---")
    
    # 1. Extract and Flatten Systems (Parent Table)
    # We flatten the 'coords' struct into individual x, y, z columns
    print("Generating systems_core.parquet...")
    con.execute(f"""
        COPY (
            SELECT 
                id as system_id,
                id64 as system_id64,
                name,
                coords.x as x,
                coords.y as y,
                coords.z as z,
                allegiance,
                government,
                state,
                security,
                population,
                date as update_time
            FROM read_json_auto('{sample_path}', format='array')
        ) TO '{systems_output}' (FORMAT PARQUET);
    """)
    
    # 2. Explode and Extract Stations (Child Table)
    # We use UNNEST to turn the stations array into individual rows
    print("Generating stations.parquet...")
    con.execute(f"""
        COPY (
            SELECT 
                id64 as system_id64,
                UNNEST(stations).id as station_id,
                UNNEST(stations).marketId as market_id,
                UNNEST(stations).name as station_name,
                UNNEST(stations).type as station_type,
                UNNEST(stations).distanceToArrival as distance_to_arrival,
                UNNEST(stations).haveMarket as has_market,
                UNNEST(stations).haveShipyard as has_shipyard,
                UNNEST(stations).haveOutfitting as has_outfitting
            FROM read_json_auto('{sample_path}', format='array')
            WHERE stations IS NOT NULL AND len(stations) > 0
        ) TO '{stations_output}' (FORMAT PARQUET);
    """)
    
    return [
        {"name": "systems_core.parquet", "path": systems_output, "source": sample_filename},
        {"name": "stations.parquet", "path": stations_output, "source": sample_filename}
    ]

def update_manifest(processed_files):
    with open(MANIFEST_PATH, 'r') as f:
        manifest = json.load(f)
    
    for file_info in processed_files:
        entry = {
            "filename": file_info['name'],
            "path": os.path.relpath(file_info['path'], "/srv/parquet"),
            "processed_at": datetime.now().strftime("%Y-%m-%d"),
            "source_file": file_info['source'],
            "type": "normalized_parquet"
        }
        # Add to manifest if not already there
        if not any(p['filename'] == file_info['name'] for p in manifest['data'].get('processed_files', [])):
            manifest['data']['processed_files'].append(entry)
            
    manifest['last_updated'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    with open(MANIFEST_PATH, 'w') as f:
        json.dump(manifest, f, indent=2)

if __name__ == "__main__":
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    # Target the populated systems sample for this test
    target_sample = "systemsPopulated.sample.json"
    
    if os.path.exists(os.path.join(SAMPLES_DIR, target_sample)):
        new_files = normalize_systems_populated(target_sample)
        update_manifest(new_files)
        print(f"
Normalization complete. Created {len(new_files)} Parquet files in {PROCESSED_DIR}.")
    else:
        print(f"Error: {target_sample} not found in {SAMPLES_DIR}. Run create_samples.py first.")
