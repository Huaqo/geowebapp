-- Create the regions_population table
CREATE TABLE Bevoelkerung (
    region_code INTEGER NOT NULL PRIMARY KEY,
    region_name VARCHAR(100) NOT NULL,
    total_population INTEGER NOT NULL,
    male_population INTEGER NOT NULL,
    female_population INTEGER NOT NULL
);

-- Copy data into regions_population table
COPY public.Bevoelkerung (region_code, region_name, total_population, male_population, female_population)
FROM '/Users/huaqo/Developer/geowebapp/data/preprocessed/cleaned_bevoelkerung.csv'
DELIMITER ','
CSV HEADER;

-- Create the Hochschulen table
CREATE TABLE Hochschulen (
    Hochschulkurzname VARCHAR(50),
    Hochschulname VARCHAR(255) PRIMARY KEY,
    Hochschultyp VARCHAR(100),
    Traegerschaft VARCHAR(100),
    Bundesland VARCHAR(50),
    Anzahl_Studierende INT,
    Gruendungsjahr INT,
    Promotionsrecht VARCHAR(10),
    Habilitationsrecht VARCHAR(10),
    Strasse VARCHAR(255),
    Postleitzahl_Hausanschrift INT,
    Ort_Hausanschrift VARCHAR(100),
    Home_Page VARCHAR(255)
);

-- Copy data into Hochschulen table
COPY public.Hochschulen (Hochschulkurzname, Hochschulname, Hochschultyp, Traegerschaft, Bundesland, Anzahl_Studierende, Gruendungsjahr, Promotionsrecht, Habilitationsrecht, Strasse, Postleitzahl_Hausanschrift, Ort_Hausanschrift, Home_Page)
FROM '/Users/huaqo/Developer/geowebapp/data/preprocessed/cleaned_hochschulen.csv'
DELIMITER ','
CSV HEADER;

