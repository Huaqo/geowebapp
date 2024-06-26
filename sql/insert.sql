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