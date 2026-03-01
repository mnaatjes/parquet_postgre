# Systems Delta Samples (systems_1day, systems_1week, systems_2weeks)

These samples represent incremental updates to the star systems database over different time periods.

## JSON Example (systems_1day.sample.json)

```json
{
  "id64": 2392231,
  "name": "Bleae Thaa AA-A h0",
  "mainStar": "Wolf-Rayet NC Star",
  "coords": {
    "x": -2966.875,
    "y": 434.71875,
    "z": 2389.1875
  },
  "updateTime": "2026-02-26 18:32:37+00"
}
```

## Property Summary

| Property | Description | Type | Correspondence |
| :--- | :--- | :--- | :--- |
| `id64` | 64-bit Elite Dangerous system ID | BIGINT | Primary Key |
| `name` | Name of the star system | VARCHAR | System Name |
| `mainStar` | Type of the primary star in the system | VARCHAR | Stellar Class |
| `coords` | 3D coordinates (X, Y, Z) | STRUCT | Spatial Position |
| `updateTime` | Last update timestamp from the source | VARCHAR | Metadata |

## SQL Schema

```sql
CREATE TABLE systems_delta (
    id64 BIGINT PRIMARY KEY,
    name VARCHAR,
    mainStar VARCHAR,
    coords STRUCT(x DOUBLE, y DOUBLE, z DOUBLE),
    updateTime VARCHAR
);
```

*Note: The schema is identical for 1day, 1week, and 2weeks updates.*
