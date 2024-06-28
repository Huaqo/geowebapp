# Data preprocessing 

```bash
cd path/to/geowebapp
```

(OPTIONAL)

Eigentlich sind die Daten schon verarbeitet in data/preprocessed

```bash
python3 data/preprocess_bevoelkerung.py
```
```bash
python3 data/preprocess_hochschulen.py # Nur wenn nötig, dauert sehr lange wegen Koordinaten und kann auch abrechen
```
```bash
python3 data/preprocess_mieten.py
```

# Setup Postgresql MacOS

Bei MacOS installiert man im Terminal mit Brew, weis nicht was das bei Windows ist. Geht bestimmt auch über den normalen Installer von deren Website.

## Install


```bash
brew install postgresql@14
```

## Start

```bash
brew services start postgresql@14
```


# Run sql 

```bash
psql -h localhost -p 5432 -U <username> -d postgres
```

1. create_database.sql

```sql
CREATE DATABASE geowebapp;
```

2. Check

```sql
\l
```

3. Switch to geowebapp

```sql
\c geowebapp
```

4. Create tables

```sql
-- Create a staging table for loading CSV data
CREATE TABLE Bevoelkerung (
    region_code VARCHAR(10) PRIMARY KEY,
    region_name VARCHAR(50),
    total_population INT,
    male_population INT,
    female_population INT,
    region_type VARCHAR(20),
    bundesland VARCHAR(50)
);

-- Create the Hochschulen table
CREATE TABLE Hochschulen (
    namekurz_h VARCHAR(50),
    name_h VARCHAR(255) PRIMARY KEY,
    typ VARCHAR(100),
    traeger VARCHAR(100),
    land VARCHAR(50),
    studenten INT,
    gjahr INT,
    precht VARCHAR(10),
    hrecht VARCHAR(10),
    str VARCHAR(255),
    plz INT,
    ort VARCHAR(100),
    web VARCHAR(255),
    lat DECIMAL(18, 10),
    lon DECIMAL(18, 10)
);

-- Mieten
CREATE TABLE Mieten (
    land VARCHAR(50) PRIMARY KEY,
    mieten_ab_2019 DECIMAL(4,1),
    mieten_insgesamt DECIMAL(4,1)
);
```

5. Insert data

```sql
-- Copy data into Bevoelkerung staging table
COPY public.Bevoelkerung (region_code, region_name, total_population, male_population, female_population, region_type, bundesland)
FROM '/Users/huaqo/Developer/geowebapp/data/preprocessed/cleaned_bevoelkerung.csv'
DELIMITER ','
CSV HEADER;

-- Copy data into Hochschulen table
COPY public.Hochschulen (namekurz_h, name_h, typ, traeger, land, studenten, gjahr, precht, hrecht, str, plz, ort, web, lat, lon)
FROM '/Users/huaqo/Developer/geowebapp/data/preprocessed/cleaned_hochschulen.csv'
DELIMITER ','
CSV HEADER;

-- Copy data into Mieten table
COPY public.Mieten (land, mieten_ab_2019, mieten_insgesamt)
FROM '/Users/huaqo/Developer/geowebapp/data/preprocessed/cleaned_mieten.csv'
DELIMITER ','
CSV HEADER;
```

6. Check 

```sql
\dt
```

```sql
SELECT * FROM your_table_name LIMIT 5;
```

# Install requirements

```bash
pip install -r requirements.txt
```

# Change server path in app.py
For example

```python
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://huaqo:0000@localhost:5432/geowebapp')
```

huaqo sollte mit deinem usernamen ersetzt werden und 0000 mit deinem password. Der rest sollte gleich sein. Vielleicht hast du einen anderen port, nicht 5432.

# Run app

```bash
python app.py
```

öffne `http://127.0.0.1:5000` in einem Browser um die App zu sehen, solange flask im Terminal läuft.