# Setup Postgresql

## Install

```bash
brew install postgresql@14
```

## Start
```bash
brew services start postgresql@14
```

```bash
psql -h localhost -p 5432 -U <username> -d postgres
```

# Run sql

1. create_database.sql

```sql
\i /path/to/geowebapp/sql/create_database.sql
```

2. Check

```sql
\l
```

3. Switch to geowebapp

```sql
\c geowebapp
```

4. create_hochschulen_and_bevoelkerung.sql

```sql
\i /path/to/geowebapp/sql/create_hochschulen_and_bevoelkerung.sql
```

5. create_hochschulen_join_bevoelkerung.sql

```sql
\i /path/to/geowebapp/sql/create_hochschulen_join_bevoelkerung.sql
```

6. Check 

```sql
\dt
```

# Install requirements

```bash
pip install -r requirements.txt
```

# Change server path
For example

```python
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://huaqo:0000@localhost:5432/geowebapp')
```

# Run app

```bash
python app.py
```

---

# Psql cheatsheet

## Show all databases

```sql
\l
```

## Create your database

```sql
CREATE DATABASE geowebapp;
```

## Switch database

```sql
\c geowebapp
```

## Delete database
```sql
DROP DATABASE database_name;
```

## Show all tables

```sql
\dt
```

## Show first 5 rows of table

```sql
SELECT * FROM your_table_name LIMIT 5;
```

## Delete tables

```sql
DROP TABLE table_name;
```

## Exit psql

```sql
\q
```

## Create user

```sql
CREATE USER newuser WITH PASSWORD 'newpassword';
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO newuser;
\q
```

## Change password

```sql
ALTER USER username WITH PASSWORD 'newpassword';
\q
```

