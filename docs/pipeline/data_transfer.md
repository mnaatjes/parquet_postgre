# Data Transfer and Payloads

Understanding how data moves from the database to your API is critical for performance tuning, especially when handling tens of thousands of records.

## 1. Data Format: What comes out of the wire?
When you query PostgreSQL from Python or Node.js, data moves through a Database Driver (e.g., `psycopg3` or `node-postgres`).

- **The Protocol:** PostgreSQL uses a binary "Frontend/Backend Protocol" sent as a stream of binary packets over a TCP socket.
- **Compression:** Usually disabled by default in the connection string. However, ID64s and floats are already compact.
- **The Transformation:** The driver "inflates" binary packets into language-native objects (e.g., Lists of Dictionaries in Python or Arrays of Objects in JS).

## 2. Estimating the Payload (The 50k Test)
How big is a 50,000-record "haystack"?
- **id64:** 8 bytes (BigInt)
- **x, y, z:** 4 bytes each (Float32) = 12 bytes
- **Total raw data per row:** ~20 bytes

**50,000 records × 20 bytes = 1,000,000 bytes (~1 MB).**

Even with object overhead in memory (which might triple the size), you are looking at 3–5 MB. On a modern Linux server, transferring 5MB is effectively instantaneous (milliseconds).

## 3. Network Optimization: Unix Domain Sockets
If your API and Database are on the same machine, connect via a **socket file** instead of a TCP port (`localhost:5432`). This removes the TCP/IP network overhead entirely.
