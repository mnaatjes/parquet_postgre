import gzip
import json
import os
import glob
from datetime import datetime

RAW_DIR = "/srv/parquet/data/raw"
SAMPLES_DIR = "/srv/parquet/data/samples"
MANIFEST_PATH = "/srv/parquet/data/manifest.json"

def create_sample(file_path):
    filename = os.path.basename(file_path)
    sample_filename = filename.replace(".json.gz", ".sample.json")
    sample_path = os.path.join(SAMPLES_DIR, sample_filename)
    
    print(f"Sampling {filename}...")
    
    with gzip.open(file_path, 'rt') as f_in:
        # These files start with '['
        first_char = f_in.read(1)
        if first_char != '[':
            # Handle non-array files or different structures if needed
            f_in.seek(0)
            data_to_write = f_in.read(1024)
        else:
            # It's an array, let's grab objects until we hit ~1KB
            objects = []
            current_size = 0
            
            # Read line by line (objects are typically one per line after the opening '[')
            for line in f_in:
                clean_line = line.strip().rstrip(',')
                if not clean_line or clean_line == ']':
                    continue
                
                try:
                    obj = json.loads(clean_line)
                    objects.append(obj)
                    current_size += len(line)
                    if current_size >= 1024:
                        break
                except json.JSONDecodeError:
                    continue
            
            data_to_write = json.dumps(objects, indent=2)
            
    with open(sample_path, 'w') as f_out:
        f_out.write(data_to_write)
    
    return sample_filename, sample_path

def update_manifest(samples_info):
    with open(MANIFEST_PATH, 'r') as f:
        manifest = json.load(f)
    
    # Prepare a lookup for raw files to add derivations
    raw_files = manifest['data']['raw_files']
    
    for s_name, s_path, raw_filename in samples_info:
        # Create sample entry
        sample_entry = {
            "filename": s_name,
            "path": os.path.relpath(s_path, "/srv/parquet"),
            "created_at": datetime.now().strftime("%Y-%m-%d"),
            "raw_source": raw_filename,
            "size_kb": round(os.path.getsize(s_path) / 1024, 2)
        }
        
        # Add to manifest samples if not already there
        if not any(s['filename'] == s_name for s in manifest['data']['samples']):
            manifest['data']['samples'].append(sample_entry)
        
        # Update raw file derivations
        for raw in raw_files:
            if raw['filename'] == raw_filename:
                if s_name not in raw['derivations']:
                    raw['derivations'].append(s_name)
                    
    manifest['last_updated'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    with open(MANIFEST_PATH, 'w') as f:
        json.dump(manifest, f, indent=2)

if __name__ == "__main__":
    os.makedirs(SAMPLES_DIR, exist_ok=True)
    gz_files = glob.glob(os.path.join(RAW_DIR, "*.json.gz"))
    
    samples_created = []
    for gz_file in gz_files:
        s_name, s_path = create_sample(gz_file)
        samples_created.append((s_name, s_path, os.path.basename(gz_file)))
        
    update_manifest(samples_created)
    print(f"Successfully created {len(samples_created)} samples and updated manifest.")
