# Populated Systems Sample (systemsPopulated.sample.json)

This sample contains comprehensive data for systems inhabited by human populations, including factions and stations.

## JSON Example

```json
{
  "id": 8713,
  "id64": 663329196387,
  "name": "4 Sextantis",
  "coords": {
    "x": 87.25,
    "y": 96.84375,
    "z": -65
  },
  "allegiance": "Federation",
  "government": "Corporate",
  "state": null,
  "economy": null,
  "security": "Low",
  "population": 14455,
  "controllingFaction": {
    "id": 13949,
    "name": "4 Sextantis Inc",
    "allegiance": "Federation",
    "government": "Corporate",
    "isPlayer": false
  },
  "stations": [
    {
      "id": 53599,
      "marketId": 3229189888,
      "type": "Outpost",
      "name": "Rukavishnikov Hangar",
      "distanceToArrival": 18187,
      "allegiance": "Federation",
      "government": "Corporate",
      "economy": "Refinery",
      "secondEconomy": null,
      "haveMarket": false,
      "haveShipyard": false,
      "haveOutfitting": false,
      "otherServices": [],
      "updateTime": {
        "information": "2017-11-07 10:08:35",
        "market": null,
        "shipyard": null,
        "outfitting": null
      }
    }
  ],
  "bodies": [],
  "date": "2015-05-12 15:29:33"
}
```

## Property Summary (Root Level)

| Property | Description | Type | Correspondence |
| :--- | :--- | :--- | :--- |
| `id` | Internal EDSM system ID | BIGINT | Primary Key |
| `id64` | 64-bit Elite Dangerous system ID | BIGINT | Unique Identifier |
| `name` | Name of the star system | VARCHAR | System Name |
| `coords` | 3D coordinates (X, Y, Z) | STRUCT | Spatial Position |
| `allegiance` | System-wide superpower allegiance | VARCHAR | Alignment |
| `government` | Type of system-wide government | VARCHAR | Political System |
| `state` | Current system state | VARCHAR | Economic/Social State |
| `economy` | Primary economy of the system | VARCHAR | Industry |
| `security` | Security level (e.g., High, Low, Anarchy) | VARCHAR | Law Enforcement |
| `population` | Total human population | BIGINT | Demographics |
| `controllingFaction`| Faction in control of the system | STRUCT | Governance |
| `stations` | List of space stations in the system | ARRAY(STRUCT) | Facilities (Child Table) |
| `bodies` | List of astronomical bodies in the system | ARRAY(STRUCT) | Astronomy (Child Table) |
| `factions` | Detailed list of factions in the system | ARRAY(STRUCT) | Minor Factions |
| `date` | Timestamp of the data record | TIMESTAMP | Metadata |

## SQL Schema (Raw Table)

```sql
CREATE TABLE systemsPopulated (
    id BIGINT PRIMARY KEY,
    id64 BIGINT,
    name VARCHAR,
    coords STRUCT(x DOUBLE, y DOUBLE, z DOUBLE),
    allegiance VARCHAR,
    government VARCHAR,
    state VARCHAR,
    economy VARCHAR,
    security VARCHAR,
    population BIGINT,
    controllingFaction STRUCT(id BIGINT, "name" VARCHAR, allegiance VARCHAR, government VARCHAR, isPlayer BOOLEAN),
    stations STRUCT(id BIGINT, marketId BIGINT, "type" VARCHAR, "name" VARCHAR, distanceToArrival DOUBLE, allegiance VARCHAR, government VARCHAR, economy VARCHAR, secondEconomy VARCHAR, haveMarket BOOLEAN, haveShipyard BOOLEAN, haveOutfitting BOOLEAN, otherServices VARCHAR[], updateTime STRUCT(information TIMESTAMP, market JSON, shipyard TIMESTAMP, outfitting JSON), controllingFaction STRUCT(id BIGINT, "name" VARCHAR))[],
    bodies STRUCT(id BIGINT, id64 BIGINT, bodyId BIGINT, "name" VARCHAR, "type" VARCHAR, subType VARCHAR, parents STRUCT("Null" BIGINT, Star BIGINT, Planet BIGINT)[], distanceToArrival BIGINT, isMainStar BOOLEAN, isScoopable BOOLEAN, age BIGINT, spectralClass VARCHAR, luminosity VARCHAR, absoluteMagnitude DOUBLE, solarMasses DOUBLE, solarRadius DOUBLE, surfaceTemperature BIGINT, orbitalPeriod DOUBLE, semiMajorAxis DOUBLE, orbitalEccentricity DOUBLE, orbitalInclination DOUBLE, argOfPeriapsis DOUBLE, rotationalPeriod DOUBLE, rotationalPeriodTidallyLocked BOOLEAN, axialTilt DOUBLE, updateTime TIMESTAMP, isLandable BOOLEAN, gravity DOUBLE, earthMasses DOUBLE, radius DOUBLE, surfacePressure DOUBLE, volcanismType VARCHAR, atmosphereType VARCHAR, atmosphereComposition STRUCT("Carbon dioxide" DOUBLE, Nitrogen DOUBLE, "Sulphur dioxide" DOUBLE, Water BIGINT, Oxygen DOUBLE, Argon DOUBLE, Hydrogen DOUBLE, Helium DOUBLE, Methane DOUBLE, Ammonia DOUBLE, Neon DOUBLE), solidComposition STRUCT(Rock DOUBLE, Metal DOUBLE, Ice DOUBLE), terraformingState VARCHAR, materials STRUCT(Iron DOUBLE, Nickel DOUBLE, Sulphur DOUBLE, Carbon DOUBLE, Manganese DOUBLE, Phosphorus DOUBLE, Zinc DOUBLE, Zirconium DOUBLE, Niobium DOUBLE, Tungsten DOUBLE, Antimony DOUBLE, Vanadium DOUBLE, Selenium DOUBLE, Cadmium DOUBLE, Tellurium DOUBLE, Molybdenum DOUBLE, Chromium DOUBLE, Germanium DOUBLE, Arsenic DOUBLE, Ruthenium DOUBLE, Mercury DOUBLE, Tin DOUBLE, Yttrium DOUBLE, Technetium DOUBLE, Polonium DOUBLE), belts STRUCT("name" VARCHAR, "type" VARCHAR, mass BIGINT, innerRadius BIGINT, outerRadius BIGINT)[], rings STRUCT("name" VARCHAR, "type" VARCHAR, mass BIGINT, innerRadius BIGINT, outerRadius BIGINT)[], reserveLevel VARCHAR)[],
    date TIMESTAMP,
    factions STRUCT(id BIGINT, "name" VARCHAR, allegiance VARCHAR, government VARCHAR, influence DOUBLE, state VARCHAR, activeStates STRUCT(state VARCHAR)[], recoveringStates JSON[], pendingStates JSON[], happiness VARCHAR, isPlayer BOOLEAN, lastUpdate BIGINT)[]
);
```

## Normalization Note

This dataset is normalized into `systems_core` and `stations` tables to handle the one-to-many relationship between systems and their space stations efficiently in Parquet format.
