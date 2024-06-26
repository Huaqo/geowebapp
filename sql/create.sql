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
