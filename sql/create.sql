-- Create a staging table for loading CSV data
CREATE TABLE Bevoelkerung (
    id INTEGER,
    name_bev VARCHAR(100),
    total INTEGER,
    total_w INTEGER,
    total_m INTEGER
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
    web VARCHAR(255)
);
