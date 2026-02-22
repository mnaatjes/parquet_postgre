# Storage and Scale

Moving from a 100GB compressed file to a live PostgreSQL database involves significant "Data Inflation," often 10x to 20x.

## 1. Estimating the Records (The "Haystack")
Based on current 2026 data trends (EDSM/Spansh):
- **~185 Million Star Systems:** Unique locations (id64 and coords).
- **~1 Billion+ Celestial Bodies:** Stars, planets, and moons.
- **~100,000+ Stations/Outposts:** Most are in "The Bubble" or Colonia.

## 2. Why the Size Explodes: The "Inflation" Factors
- **Fixed Storage:** PostgreSQL stores data in 8KB "Pages." Small rows take up set space.
- **Indexes (The Big Culprit):** For a 500GB dataset, you might have 300GB of data and 200GB of indexes. GiST indexes for 3D coordinates are heavy.
- **MVCC (Version Control):** PostgreSQL keeps old versions of rows for data integrity (Table Bloat).

## 3. Estimated PostgreSQL Disk Footprint
Realistic projection for storage:

| Table Type | Data Size | Index Size | Total Space |
| :--- | :--- | :--- | :--- |
| **Systems (Lean)** | ~40 GB | ~25 GB | 65 GB |
| **Bodies (Planetary)** | ~400 GB | ~200 GB | 600 GB |
| **Market/Station Data** | ~50 GB | ~30 GB | 80 GB |
| **TOTAL ESTIMATE** | | | **~750 GB to 1.2 TB** |

## 4. Hardware Considerations
Use `df -h` on your Linux environment to check space:
- **If you have < 1TB:** Only import the systems table and neutron stars. Skip billions of planets (bodies).
- **If you have > 2TB:** You can host the entire galaxy and run complex queries across every moon and station.
