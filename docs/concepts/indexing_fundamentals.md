# Indexing Fundamentals

It is a common "Developer Myth" that databases are just glorified spreadsheets. While a spreadsheet (and a database Table) is how we view data logically, it is almost never how the database organizes it physically on your hard drive.

## 1. The B-Tree: A "Balanced Tree"
Imagine a massive library. A spreadsheet is like a single pile of books on the floor. To find a book, you have to look at every cover. A B-Tree is the shelving system.

A B-Tree (Balanced Tree) is a tree-like structure that keeps data sorted and allows for searches, sequential access, insertions, and deletions in "logarithmic time."

- **The Root:** The very top of the tree. It contains "pointers" to the next level.
- **The Branches (Internal Nodes):** These act as signposts. For example, a branch might say "IDs 1–1000 go left, IDs 1001–2000 go right."
- **The Leaves:** The bottom of the tree where the actual data (or a pointer to the row) lives.

### Is it a "Straight Line"?
"Straight line" refers to the **logical order** (1, 2, 3, 4...). Physically, the data is jumping all over the tree. In a table of 1 million rows, a spreadsheet-style scan takes 1,000,000 steps. A B-Tree takes about 20 steps.

## 2. Logical vs. Physical Organization
There are two ways the data actually sits on your Linux server's disk:

### The "Heap" (The Spreadsheet)
The actual data rows (the "Heap") are often stored in the order they were written. If you delete a row, that space just sits there empty until a new row fills it. It is messy and disorganized.

### The "Index" (The Map)
The Index is a separate, highly organized file. It doesn't contain the entire row (no coordinates, no names)—it only contains the **Indexed Column** (like `id64`) and a **Pointer** (the physical address on the disk) to where the rest of that row lives in the "Heap."

## 3. Comparison: How the DB "Thinks"

| Feature | The Table (Heap) | The B-Tree Index |
| :--- | :--- | :--- |
| **Analogy** | The pages of a book. | The Index at the back of the book. |
| **Structure** | Unordered (mostly). | Perfectly sorted tree. |
| **Search Method** | Sequential Scan (Read everything). | Binary Search (Jump to the right spot). |
| **Cost** | Takes up most of your disk space. | Small, but takes memory to keep "hot." |
