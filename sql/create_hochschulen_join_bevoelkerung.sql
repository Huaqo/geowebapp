-- Join to tables to a new one
CREATE TABLE Hochschulen_Bevoelkerung AS
SELECT h.*, b.total_population, b.male_population, b.female_population
FROM Bevoelkerung b
JOIN Hochschulen h
ON b.region_name = h.Bundesland;
