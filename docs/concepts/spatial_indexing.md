# Spatial Indexing (3D)

A standard index (B-Tree) sorts data in a straight line. This is perfect for "Find User #500." But for Elite Dangerous coordinates (X, Y, Z), a standard index is useless.

## 1. What is a Spatial Index?
A Spatial Index organizes data into **Bounding Boxes**. It groups nearby stars into a "cube," then groups those cubes into larger "super-cubes."

- **The fix:** Use the **PostGIS extension for PostgreSQL**. It allows you to create a **GiST Index** (Generalized Search Tree). In PostgreSQL, GiST is the "engine" that allows for spatial indexing. It is considered significantly more powerful and flexible for 3D coordinates.

## 2. Bounding Boxes (Conceptually)
A Bounding Box (specifically an Axis-Aligned Bounding Box or AABB) is the smallest possible "container" that can hold a set of points. Instead of the database remembering the exact location of 10 million individual stars, it remembers the "corners" of a box that contains a group of them.

### How the Index Uses Them
Imagine the galaxy as a giant cube. The database doesn't want to search the whole cube, so it breaks it down:
- **Level 1:** One giant box containing the entire galaxy.
- **Level 2:** Eight smaller boxes (Octants) inside that giant box.
- **Level 3:** Each of those boxes contains even smaller boxes that wrap around specific clusters of stars.

## 3. The "Pruning" Logic (The Power of the Box)
Pruning is what makes the routing API fast. When your router asks for stars near Sol, the database looks at the Level 2 boxes.

> *"Is Sol in Box A (the Galactic North)?" No. "Is Sol in Box B (the Galactic South)?" Yes.*

The database immediately throws away every star in Box A. By checking a few "corners" of a Bounding Box, it can eliminate 50% of your 500GB dataset in a single step.

## 4. Comparison Table: Index Structures

| Structure | Dimension | Logical Shape | Best For |
| :--- | :---: | :--- | :--- |
| **B-Tree** | 1D | A sorted list / Branching path | IDs, Names, Dates |
| **Quad-tree** | 2D | Squares inside squares | Maps, 2D Top-down games |
| **R-Tree/GiST** | 3D | Boxes inside boxes | Elite Dangerous Galaxy Coords |

## 5. Summary: Architecture for your Project
- **The Records:** Live in the table (**Heap**), likely ordered by when you imported them.
- **The Bounding Boxes:** Live in the **GiST Index**. They store the Min(X,Y,Z) and Max(X,Y,Z) of clusters of stars.
- **The Search:** Your "Corridor Search" is basically asking the DB: "Which Bounding Boxes intersect with my flight path?"
