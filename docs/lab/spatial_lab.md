# Enabling the "Spatial Lab" (PostGIS)

To perform "Bounding Box" queries, your standard PostgreSQL container needs the **PostGIS extension**.

## 1. Update `docker-compose.yml`
Update your `docker-compose.yml` image line to use the postgis-enabled version:

```yaml
services:
  db:
    image: postgis/postgis:16-3.4-alpine # This version includes PostGIS
```

## 2. Setup SQL
After running `docker compose up`, open a SQL console (in pgAdmin or via terminal) and run:

```sql
-- Enable the spatial extension
CREATE EXTENSION postgis;

-- Create your star table with a 3D Geometry column
CREATE TABLE stars_spatial (
    id64 BIGINT PRIMARY KEY,
    name TEXT,
    geom GEOMETRY(PointZ, 0) -- 'PointZ' means 3D (X, Y, Z)
);

-- Create the Spatial Index (the 3D Bounding Box engine)
CREATE INDEX idx_stars_spatial_geom ON stars_spatial USING GIST (geom);
```

## 3. Practice Workflow: The Bounded-Box Query
Once you have loaded your test data (using the Python script), you can practice "Cylindrical" or "Box" searches.

### The "Star Corridor" Query
If you are at Sol (0,0,0) and heading toward Beagle Point, you can find all stars within a "Box" around your current sector:

```sql
SELECT name, ST_Distance(geom, ST_MakePoint(500, 120, 3000)) as dist
FROM stars_spatial
WHERE ST_3DDWithin(geom, ST_MakePoint(500, 120, 3000), 50.0)
ORDER BY dist ASC;
```
