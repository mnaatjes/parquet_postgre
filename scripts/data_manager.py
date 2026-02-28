import os
import json
import hashlib
import requests
import subprocess
from datetime import datetime
from urllib.parse import urlparse

# Configuration
RAW_DIR = "/srv/parquet/data/raw"
MANIFEST_PATH = "/srv/parquet/data/manifest.json"
CRON_SCHEDULE_PATH = "/srv/parquet/docs/pipeline/crontab_template"

def calculate_sha256(file_path):
    """Calculates the SHA-256 hash of a file for versioning."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read in chunks to handle large files
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def download_file(url, target_dir):
    """Downloads a file and stores it in a timestamped folder."""
    filename = os.path.basename(urlparse(url).path)
    today = datetime.now().strftime("%Y-%m-%d")
    versioned_dir = os.path.join(target_dir, today)
    os.makedirs(versioned_dir, exist_ok=True)
    
    target_path = os.path.join(versioned_dir, filename)
    
    print(f"Downloading {url} to {target_path}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(target_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            
    return target_path, today

def update_manifest(url, file_path, date_str):
    """Updates the manifest with the new versioned file."""
    with open(MANIFEST_PATH, "r") as f:
        manifest = json.load(f)
        
    filename = os.path.basename(file_path)
    file_hash = calculate_sha256(file_path)
    
    version_entry = {
        "filename": filename,
        "date": date_str,
        "path": os.path.relpath(file_path, "/srv/parquet"),
        "sha256": file_hash,
        "downloaded_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_url": url
    }
    
    # Track as a versioned raw file
    if "raw_versions" not in manifest["data"]:
        manifest["data"]["raw_versions"] = []
        
    manifest["data"]["raw_versions"].append(version_entry)
    manifest["last_updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)

def generate_cron_template():
    """Generates a crontab template for the user to implement."""
    template = f"""
# Elite Dangerous Data Lifecycle Management
# Edit with: crontab -e

# Daily at 01:00 AM - Small Updates
0 1 * * * python3 /srv/parquet/scripts/data_manager.py download https://downloads.spansh.co.uk/systems_1day.json.gz

# Weekly on Sunday at 02:00 AM - Medium Updates
0 2 * * 0 python3 /srv/parquet/scripts/data_manager.py download https://www.edsm.net/dump/bodies7days.json.gz

# Monthly on the 1st at 03:00 AM - Full Re-population
0 3 1 * * python3 /srv/parquet/scripts/data_manager.py download https://www.edsm.net/dump/systemsPopulated.json.gz
"""
    with open(CRON_SCHEDULE_PATH, "w") as f:
        f.write(template)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 data_manager.py [download <url> | setup_cron]")
        sys.exit(1)
        
    command = sys.argv[1]
    
    if command == "download":
        url = sys.argv[2]
        path, date = download_file(url, RAW_DIR)
        update_manifest(url, path, date)
        print(f"Successfully versioned and tracked {url}")
        
    elif command == "setup_cron":
        generate_cron_template()
        print(f"Cron template generated at {CRON_SCHEDULE_PATH}")
