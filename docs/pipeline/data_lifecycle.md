# Data Lifecycle Management

This document defines the strategy for versioning, scheduling, and integrating recurring Elite Dangerous data dumps.

## 1. The Medallion Architecture Pattern
We will follow a simplified "Medallion" data architecture to manage data state:

| Layer | Directory | Format | Versioning Strategy |
| :--- | :--- | :--- | :--- |
| **Bronze (Raw)** | `data/raw/` | `.json.gz` | **Timestamped Folders:** Each download is stored in `data/raw/YYYY-MM-DD/`. |
| **Silver (Cleaned)** | `data/processed/` | `.parquet` | **Partitioned:** Stored by source and date. |
| **Gold (Database)** | `PostgreSQL` | `SQL Tables` | **Idempotent Loads:** Using `UPSERT` (Insert on Conflict) to update existing records. |

## 2. Data Versioning Strategy
Since we are dealing with 200GB+ files, we cannot use Git for data. Instead:
1. **Physical Isolation:** New downloads are never overwritten. They are saved in a date-stamped directory.
2. **Symlink "Latest":** We maintain a `data/raw/latest/` symlink that points to the most recent successful download.
3. **Manifest Tracking:** The `data/manifest.json` acts as the "Source of Truth," tracking the hash, source URL, and timestamp for every file.

## 3. Scheduling & Automation
For this environment, we will use **Cron** for scheduling.
- **Daily Task:** Download `systems_1day.json.gz`.
- **Weekly Task:** Download `systems_1week.json.gz` and `bodies7days.json.gz`.
- **Monthly Task:** Perform a full refresh of `systemsPopulated.json.gz`.

## 4. Database Integration Pattern (UPSERT)
To prevent duplicate records when loading new data, we use the `INSERT ... ON CONFLICT (id64) DO UPDATE` pattern.
- **Systems:** Unique by `id64`.
- **Stations:** Unique by `marketId`.
- **Bodies:** Unique by `id64`.

This ensures that if a system's population changes in a new download, the database is updated rather than creating a second record.
