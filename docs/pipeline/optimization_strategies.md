# Optimization Strategies

Strategies for making your routing API lightning-fast and managing memory effectively.

## 1. Table Width: Lean vs. Wide
Extra columns (names, planets, FKs) don't slow the Spatial Index, but they do affect other factors.

| Aspect | Lean (ID + Coords) | Wide (All Metadata) |
| :--- | :--- | :--- |
| **Index Speed** | Identical | Identical |
| **Disk Read Speed** | Fast (Sequential) | Slower (Scattered) |
| **Transfer Size** | ~1MB | ~20MB+ |
| **API RAM Usage** | Minimal | Significant |

- **Recommendation:** Use a "Lean" table for the router. You can have a main table for "fluff" and a `stars_minimal` table (or Materialized View) with only `id64` and `coords`.

## 2. Hybrid Speed Strategy
1. **Filter (DB):** Use the GiST index to find IDs within your 3D corridor.
2. **Stream (Network):** Use your API to fetch only `id64` and `x, y, z`.
3. **Graph (Memory):** Load these into a high-speed Graph structure.
4. **Lookup (Final Step):** Once your router finds the path (e.g., 300 IDs), run a second query for human-readable names and planet info.

## 3. Lean Import Strategy
Filter your data during the ETL pipeline to save disk space and boost performance.

1. **Extract:** Read the `json.gz` stream.
2. **Filter:** Keep only `id64`, `name`, `coords`, and `star_type`.
3. **Discard:** Toss body data, atmosphere types, and market prices unless needed.

If filtered, your 100GB `.json.gz` will shrink into a ~50GB PostgreSQL table.
