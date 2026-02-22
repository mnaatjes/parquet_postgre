# PostgreSQL "Starter Lab" Setup

Starting your PostgreSQL journey in a Linux environment is the perfect way to get hands-on with the same tools you'll use for your galaxy-sized ETL project.

## 1. The Engine: Docker Compose
Instead of installing PostgreSQL directly on your host, we’ll use Docker. This keeps your system clean and allows you to "reset" the database by deleting a folder.

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  db:
    image: postgres:16-alpine
    container_name: ed_postgres_lab
    restart: always
    environment:
      POSTGRES_USER: commander
      POSTGRES_PASSWORD: password123
      POSTGRES_DB: galaxy_db
    ports:
      - "5432:5432"
    volumes:
      - ./pgdata:/var/lib/postgresql/data

  pgadmin:
    image: dpage/pgadmin4
    container_name: ed_pgadmin_lab
    restart: always
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "8080:80"
    depends_on:
      - db
```

**To start it:** Run `docker compose up -d`.

- **Database:** Port 5432.
- **pgAdmin GUI:** Port 8080 (Login: `admin@admin.com` / `admin`).

## 2. The Connector: Python venv
Set up your Python environment using `psycopg3` (the modern standard).

```bash
# 1. Create the virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate

# 3. Install the database adapter (binary version is easiest for labs)
pip install "psycopg[binary]"
```

## 3. The "Starter Lab" Script: `run_lab.py`

```python
import psycopg

# Connection string using the credentials from your docker-compose
DB_URL = "postgresql://commander:password123@localhost:5432/galaxy_db"

def run_lab():
    try:
        # 1. Connect to the database
        with psycopg.connect(DB_URL) as conn:
            # Open a cursor to perform database operations
            with conn.cursor() as cur:
                print("--- Connected to PostgreSQL! ---")

                # 2. Create a test table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS test_stars (
                        id64 BIGINT PRIMARY KEY,
                        name TEXT NOT NULL,
                        star_type TEXT
                    );
                """)

                # 3. Insert some test data
                test_stars = [
                    (123456, 'Sol', 'G'),
                    (987654, 'Jackson's Lighthouse', 'Neutron'),
                    (555444, 'Colonia', 'F')
                ]
                
                # Using executemany for efficiency
                cur.executemany(
                    "INSERT INTO test_stars (id64, name, star_type) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                    test_stars
                )
                print(f"Inserted {len(test_stars)} test stars.")

                # 4. Perform a query
                cur.execute("SELECT name, star_type FROM test_stars WHERE star_type = 'Neutron';")
                result = cur.fetchone()
                
                if result:
                    print(f"Query Result: Found a {result[1]} star named {result[0]}!")

                # Changes are committed automatically when the 'with' block ends
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_lab()
```
