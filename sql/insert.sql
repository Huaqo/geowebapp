-- Copy data into Bevoelkerung staging table
COPY public.Bevoelkerung (id, name_bev, total, total_w, total_m)
FROM '/Users/huaqo/Developer/geowebapp/data/preprocessed/cleaned_bevoelkerung.csv'
DELIMITER ','
CSV HEADER;

-- Insert into Bundesland table
INSERT INTO Bundesland (id, name_b, total, total_w, total_m)
SELECT id, name_bev, total, total_w, total_m
FROM Bevoelkerung
WHERE id < 17;

-- Insert into Regierungsbezirk table
INSERT INTO Regierungsbezirk (id, name_r, total, total_w, total_m, bundesland_id)
SELECT id, name_bev, total, total_w, total_m, 
       (SELECT id FROM Bundesland WHERE name_b = SUBSTRING(name_bev FROM 1 FOR POSITION(',' IN name_bev) - 1))
FROM Bevoelkerung
WHERE name_bev LIKE '%Regierungsbezirk%' OR name_bev LIKE '%StatistischeRegion%';

-- Insert into Landkreis table
INSERT INTO Landkreis (id, name_l, total, total_w, total_m, regierungsbezirk_id)
SELECT id, name_bev, total, total_w, total_m, 
       (SELECT id FROM Regierungsbezirk WHERE name_r = CASE 
            WHEN POSITION(',' IN name_bev) > 0 
            THEN SUBSTRING(name_bev FROM 1 FOR POSITION(',' IN name_bev) - 1)
            ELSE name_bev
        END)
FROM Bevoelkerung
WHERE name_bev ILIKE '%Landkreis%' OR name_bev ILIKE '%Kreis%';

-- Insert into Stadt table
INSERT INTO Stadt (id, name_s, total, total_w, total_m, landkreis_id)
SELECT id, name_bev, total, total_w, total_m, 
       (SELECT id FROM Landkreis WHERE name_l = SUBSTRING(name_bev FROM 1 FOR POSITION(',' IN name_bev) - 1))
FROM Bevoelkerung
WHERE name_bev LIKE '%kreisfreieStadt%' OR name_bev LIKE '%Hansestadt%' 
    OR name_bev LIKE '%Landeshauptstadt%' OR name_bev LIKE '%Wissenschaftsstadt%' 
    OR name_bev LIKE '%Regionalverbund%' OR name_bev LIKE '%Stadtkreis%';

-- Copy data into Hochschulen table
COPY public.Hochschulen (namekurz_h, name_h, typ, traeger, land, studenten, gjahr, precht, hrecht, str, plz, ort, web)
FROM '/Users/huaqo/Developer/geowebapp/data/preprocessed/cleaned_hochschulen.csv'
DELIMITER ','
CSV HEADER;