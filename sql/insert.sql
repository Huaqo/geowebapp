-- Copy data into regions_population table
COPY public.Staging_Bevoelkerung (region_code, region_name, total_population, male_population, female_population)
FROM '/Users/huaqo/Developer/geowebapp/data/preprocessed/cleaned_bevoelkerung.csv'
DELIMITER ','
CSV HEADER;

-- Insert into Bundesland table
INSERT INTO Bundesland (id, name_b, total, total_w, total_m)
SELECT region_code, region_name, total_population, female_population, male_population
FROM Staging_Bevoelkerung
WHERE region_code < 17;

-- Insert into Regierungsbezirk table
INSERT INTO Regierungsbezirk (id, name_r, total, total_w, total_m, bundesland_id)
SELECT region_code, region_name, total_population, female_population, male_population, 
       (SELECT id FROM Bundesland WHERE name_b = SUBSTRING(region_name FROM 1 FOR POSITION(',' IN region_name) - 1))
FROM Staging_Bevoelkerung
WHERE region_name LIKE '%Regierungsbezirk%' OR region_name LIKE '%StatistischeRegion%';

-- Insert into Landkreis table
INSERT INTO Landkreis (id, name_l, total, total_w, total_m, regierungsbezirk_id)
SELECT region_code, region_name, total_population, female_population, male_population, 
       (SELECT id FROM Regierungsbezirk WHERE name_r = CASE 
            WHEN POSITION(',' IN region_name) > 0 
            THEN SUBSTRING(region_name FROM 1 FOR POSITION(',' IN region_name) - 1)
            ELSE region_name
        END)
FROM Staging_Bevoelkerung
WHERE region_name ILIKE '%Landkreis%' OR region_name ILIKE '%Kreis%';

-- Insert into Stadt table
INSERT INTO Stadt (id, name_s, total, total_w, total_m, landkreis_id)
SELECT region_code, region_name, total_population, female_population, male_population, 
       (SELECT id FROM Landkreis WHERE name_r = SUBSTRING(region_name FROM 1 FOR POSITION(',' IN region_name) - 1))
FROM Staging_Bevoelkerung
WHERE region_name LIKE '%kreisfreieStadt%' OR region_name LIKE '%Hansestadt%' 
    OR region_name LIKE '%Landeshauptstadt%' OR region_name LIKE '%Wissenschaftsstadt%' 
    OR region_name LIKE '%Regionalverbund%' OR region_name LIKE '%Stadtkreis%';

-- Copy data into Hochschulen table
COPY public.Hochschulen (Hochschulkurzname, Hochschulname, Hochschultyp, Traegerschaft, Bundesland, Anzahl_Studierende, Gruendungsjahr, Promotionsrecht, Habilitationsrecht, Strasse, Postleitzahl_Hausanschrift, Ort_Hausanschrift, Home_Page)
FROM '/Users/huaqo/Developer/geowebapp/data/preprocessed/cleaned_hochschulen.csv'
DELIMITER ','
CSV HEADER;