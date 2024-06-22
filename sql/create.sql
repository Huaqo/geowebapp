-- Create a staging table for loading CSV data
CREATE TABLE Staging_Bevoelkerung (
    region_code INTEGER,
    region_name VARCHAR(100),
    total_population INTEGER,
    male_population INTEGER,
    female_population INTEGER
);

-- Create the regions_population table
CREATE TABLE Bundesland (
    id INTEGER NOT NULL PRIMARY KEY,
    name_b VARCHAR(100) NOT NULL,
    total INTEGER,
    total_w INTEGER,
    total_m INTEGER
);

CREATE TABLE Regierungsbezirk (
    id INTEGER NOT NULL PRIMARY KEY,
    name_r VARCHAR(100) NOT NULL,
    total INTEGER,
    total_w INTEGER,
    total_m INTEGER,
    bundesland_id INTEGER,
    FOREIGN KEY (bundesland_id) REFERENCES Bundesland(id)
);

CREATE TABLE Landkreis (
    id INTEGER NOT NULL PRIMARY KEY,
    name_l VARCHAR(100) NOT NULL,
    total INTEGER,
    total_w INTEGER,
    total_m INTEGER,
    regierungsbezirk_id INTEGER,
    FOREIGN KEY (regierungsbezirk_id) REFERENCES Regierungsbezirk(id)
);

CREATE TABLE Stadt (
    id INTEGER NOT NULL PRIMARY KEY,
    name_s VARCHAR(100) NOT NULL,
    total INTEGER,
    total_w INTEGER,
    total_m INTEGER,
    landkreis_id INTEGER,
    FOREIGN KEY (landkreis_id) REFERENCES Landkreis(id)
);

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



