# Understanding Data Normalization

Normalization is the process of organizing data in a database to reduce redundancy and improve data integrity. In our project, we use these principles to transform "messy" nested JSON files into clean, efficient Parquet tables.

## The Goal
1.  **Eliminate Redundant Data**: Don't store the same name or address in 50 different rows.
2.  **Ensure Data Integrity**: If a customer changes their name, you should only have to update it in one place.
3.  **Optimize Storage**: Flat, consistent tables are much faster for analytical engines (like DuckDB or Spark) to scan.

---

## A Simple Example: The "Orders" Spreadsheet

Imagine we are tracking sales. A "denormalized" (flat) version might look like this:

| OrderID | CustomerName | CustomerEmail | Product | Price |
| :--- | :--- | :--- | :--- | :--- |
| 101 | Alice | alice@email.com | Laptop | 1200 |
| 102 | Bob | bob@email.com | Mouse | 25 |
| 103 | Alice | alice@email.com | Keyboard | 75 |

### The Problem
Notice that **Alice's email** is stored twice. 
- If Alice changes her email, we have to find every row and update it.
- if we miss one, our data is "corrupt" (inconsistent).

---

## The Normalized Solution

We split the data into two tables and link them with an **ID**.

### Table 1: Customers
| CustomerID (PK) | Name | Email |
| :--- | :--- | :--- |
| 1 | Alice | alice@email.com |
| 2 | Bob | bob@email.com |

### Table 2: Orders
| OrderID (PK) | CustomerID (FK) | Product | Price |
| :--- | :--- | :--- | :--- |
| 101 | 1 | Laptop | 1200 |
| 102 | 2 | Mouse | 25 |
| 103 | 1 | Keyboard | 75 |

**Now, Alice's email is stored exactly once.** The `Orders` table simply points to `CustomerID: 1`.

---

## The "Normal Forms" (Simplified)

### 1. First Normal Form (1NF): No Repeating Groups
Every cell should contain a single value. No lists or arrays inside a cell.
*   *JSON Problem:* A `stations` array inside a system object violates 1NF.
*   *Fix:* Unnest the array into its own rows.

### 2. Second Normal Form (2NF): Full Functional Dependency
All non-key columns must depend on the *entire* primary key. 
*   *Example:* In a table with `(OrderID, ProductID)`, the `CustomerName` doesn't belong because it only depends on the Order, not the Product.

### 3. Third Normal Form (3NF): No Transitive Dependency
Non-key columns shouldn't depend on other non-key columns.
*   *Example:* If you have `ZipCode` and `City`, the `City` depends on the `ZipCode`. You should move `ZipCode -> City` to a separate lookup table.

---

## Why this matters for Parquet
While traditional databases (PostgreSQL) love 3NF for writing data, analytical formats (Parquet) often prefer a balance. 

In this project:
- We **Normalize** nested arrays (like `stations` in `systemsPopulated.json`) because scanning a 50GB file is impossible if every row contains a giant hidden list.
- We **Denormalize** coordinates (`x`, `y`, `z`) from a JSON object into three separate columns to allow for fast spatial math.

By breaking down the JSON "blobs" into normalized tables, we make our data searchable, scalable, and professional.
