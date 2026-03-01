# Power Play Sample (powerPlay.sample.json)

This sample represents systems involved in Power Play factions.

## JSON Example

```json
{
  "power": "Edmund Mahon",
  "powerState": "Exploited",
  "id": 16363,
  "id64": 670417888705,
  "name": "LP 442-37",
  "coords": {
    "x": -29.65625,
    "y": 88.8125,
    "z": 57.65625
  },
  "allegiance": "Alliance",
  "government": "Corporate",
  "state": "None",
  "date": "2026-01-28 01:07:11"
}
```

## Property Summary

| Property | Description | Type | Correspondence |
| :--- | :--- | :--- | :--- |
| `power` | Name of the Power Play leader | VARCHAR | Faction Leader |
| `powerState` | Status of the power's influence in the system | VARCHAR | Influence State |
| `id` | Internal EDSM system ID | BIGINT | Primary Key |
| `id64` | 64-bit Elite Dangerous system ID | BIGINT | Unique Identifier |
| `name` | Name of the star system | VARCHAR | System Name |
| `coords` | 3D coordinates (X, Y, Z) | STRUCT | Spatial Position |
| `allegiance` | Superpower allegiance (e.g., Alliance, Federation) | VARCHAR | Alignment |
| `government` | Type of local government | VARCHAR | Political System |
| `state` | Current state of the system (e.g., None, Boom, War) | VARCHAR | Economic/Social State |
| `date` | Timestamp of the data record | TIMESTAMP | Metadata |

## SQL Schema

```sql
CREATE TABLE powerPlay (
    power VARCHAR,
    powerState VARCHAR,
    id BIGINT PRIMARY KEY,
    id64 BIGINT,
    name VARCHAR,
    coords STRUCT(x DOUBLE, y DOUBLE, z DOUBLE),
    allegiance VARCHAR,
    government VARCHAR,
    state VARCHAR,
    date TIMESTAMP
);
```
