# Practice and Datasets

To sharpen your skills for a 500GB galaxy dataset, start with "bite-sized" versions of that data.

## 1. Where to Find Trial Datasets

### Elite Dangerous Data (The "Mini" Galaxy)
- **EDSM Nightly Dumps:** Download the *Systems with Coordinates (7 Days)*. It’s usually around 10MB and contains exactly the `{id64, coords:{x, y, z}}` structure you'll be using.
- **EDAstro Spreadsheets:** The *Neutron Stars (raw list)* (~300MB) is perfect for practicing the "Neutron Highway" routing logic.

### Real-World Star Catalogs (For Diversity)
- **The HYG Database:** A subset of 118,000 real stars (Hipparcos, Yale, Gliese catalogs). It’s a clean CSV with X,Y,Z coordinates in parsecs.
- **BSC5P-JSON-XYZ:** A GitHub repository with 9,000 naked-eye stars pre-processed into 3D JSON.

## 2. Learning Path

| Level | Task | Learning Goal |
| :--- | :--- | :--- |
| **Lvl 1** | Load the 7-day EDSM JSON dump via Python. | Stream processing and JSON parsing. |
| **Lvl 2** | Convert X,Y,Z into a PostGIS `PointZ`. | Data type transformation. |
| **Lvl 3** | Run a query to find the "densest" 1000ly³ cube of stars. | Using aggregate spatial functions. |
| **Lvl 4** | Build a Python function that creates a "Cylinder" between two points. | Preparing data for your routing algorithm. |
