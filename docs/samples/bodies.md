# Bodies Sample (bodies7days.sample.json)

This sample represents astronomical bodies (planets, stars, etc.) updated in the last 7 days.

## JSON Example

```json
{
  "id": 604201726,
  "id64": 828662425287803602,
  "bodyId": 23,
  "name": "Rhoolaa SM-L c24-0 E 3",
  "type": "Planet",
  "subType": "High metal content world",
  "parents": [
    {
      "Null": 21
    },
    {
      "Star": 8
    },
    {
      "Null": 0
    }
  ],
  "distanceToArrival": 38748,
  "isLandable": false,
  "gravity": 0.8211827044127425,
  "earthMasses": 0.47844,
  "radius": 4868.3115,
  "surfaceTemperature": 590,
  "surfacePressure": 1.2665763786133728,
  "volcanismType": "No volcanism",
  "atmosphereType": "Hot Sulphur dioxide",
  "atmosphereComposition": {
    "Sulphur dioxide": 65.5,
    "Carbon dioxide": 34.5
  },
  "solidComposition": {
    "Rock": 67.29,
    "Metal": 32.71,
    "Ice": 0
  },
  "terraformingState": "Not terraformable",
  "orbitalPeriod": 1.4307761771759258,
  "semiMajorAxis": 0.00023708570991008097,
  "orbitalEccentricity": 0.168326,
  "orbitalInclination": 1.453047,
  "argOfPeriapsis": 189.391901,
  "rotationalPeriod": 101.18602585490741,
  "rotationalPeriodTidallyLocked": true,
  "axialTilt": 0.493233,
  "updateTime": "2026-02-18 11:54:32",
  "systemId": 39506239,
  "systemId64": 93851632338,
  "systemName": "Rhoolaa SM-L c24-0"
}
```

## Property Summary

| Property | Description | Type | Correspondence |
| :--- | :--- | :--- | :--- |
| `id` | Internal EDSM ID | BIGINT | Primary Key |
| `id64` | 64-bit ID used by Elite Dangerous | BIGINT | Unique Identifier |
| `bodyId` | ID of the body within its system | BIGINT | System Local ID |
| `name` | Name of the astronomical body | VARCHAR | Name |
| `type` | General classification (e.g., Planet, Star) | VARCHAR | Category |
| `subType` | Specific classification (e.g., High metal content world) | VARCHAR | Sub-category |
| `parents` | Hierarchy of parent bodies | ARRAY(STRUCT) | Orbital Parentage |
| `distanceToArrival` | Distance from the arrival point in light seconds | BIGINT | Distance |
| `isLandable` | Whether the body can be landed upon | BOOLEAN | Capability |
| `gravity` | Surface gravity in G | DOUBLE | Physical Prop |
| `earthMasses` | Mass relative to Earth | DOUBLE | Physical Prop |
| `radius` | Radius in kilometers | DOUBLE | Physical Prop |
| `surfaceTemperature` | Surface temperature in Kelvin | BIGINT | Physical Prop |
| `surfacePressure` | Surface pressure in atmospheres | DOUBLE | Physical Prop |
| `volcanismType` | Type of volcanic activity | VARCHAR | Geological Prop |
| `atmosphereType` | Type of atmosphere | VARCHAR | Atmospheric Prop |
| `atmosphereComposition` | Detailed atmospheric components | STRUCT | Atmospheric Prop |
| `solidComposition` | Breakdown of rock, metal, and ice | STRUCT | Geological Prop |
| `terraformingState` | Status of terraforming potential | VARCHAR | Economic Prop |
| `orbitalPeriod` | Time to complete one orbit in days | DOUBLE | Orbital Prop |
| `semiMajorAxis` | Average orbital distance in AU | DOUBLE | Orbital Prop |
| `orbitalEccentricity` | Degree of orbital deviation from circular | DOUBLE | Orbital Prop |
| `orbitalInclination` | Tilt of orbit relative to system plane | DOUBLE | Orbital Prop |
| `argOfPeriapsis` | Orientation of orbital ellipse | DOUBLE | Orbital Prop |
| `rotationalPeriod` | Time for one rotation in days | DOUBLE | Orbital Prop |
| `rotationalPeriodTidallyLocked` | Whether rotation matches orbit | BOOLEAN | Orbital Prop |
| `axialTilt` | Tilt of rotation axis | DOUBLE | Orbital Prop |
| `updateTime` | Last update timestamp | TIMESTAMP | Metadata |
| `systemId` | ID of the parent star system | BIGINT | Foreign Key |
| `systemId64` | 64-bit ID of the parent star system | BIGINT | Foreign Key |
| `systemName` | Name of the parent star system | VARCHAR | Reference |

## SQL Schema

```sql
CREATE TABLE bodies7days (
    id BIGINT PRIMARY KEY,
    id64 BIGINT,
    bodyId BIGINT,
    name VARCHAR,
    type VARCHAR,
    subType VARCHAR,
    parents STRUCT("Null" BIGINT, Star BIGINT)[],
    distanceToArrival BIGINT,
    isLandable BOOLEAN,
    gravity DOUBLE,
    earthMasses DOUBLE,
    radius DOUBLE,
    surfaceTemperature BIGINT,
    surfacePressure DOUBLE,
    volcanismType VARCHAR,
    atmosphereType VARCHAR,
    atmosphereComposition STRUCT("Sulphur dioxide" DOUBLE, "Carbon dioxide" DOUBLE),
    solidComposition STRUCT(Rock DOUBLE, Metal DOUBLE, Ice BIGINT),
    terraformingState VARCHAR,
    orbitalPeriod DOUBLE,
    semiMajorAxis DOUBLE,
    orbitalEccentricity DOUBLE,
    orbitalInclination DOUBLE,
    argOfPeriapsis DOUBLE,
    rotationalPeriod DOUBLE,
    rotationalPeriodTidallyLocked BOOLEAN,
    axialTilt DOUBLE,
    updateTime TIMESTAMP,
    systemId BIGINT,
    systemId64 BIGINT,
    systemName VARCHAR
);
```
