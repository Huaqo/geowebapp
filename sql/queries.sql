-- Die 10 ältesten Unis
CREATE TABLE IF NOT EXISTS aelteste_unis AS
SELECT h.Hochschulname, h.Gruendungsjahr
FROM Hochschulen h
ORDER BY h.Gruendungsjahr ASC
LIMIT 10;

-- Die 10 jümgsten Unis
CREATE TABLE IF NOT EXISTS juengste_unis AS
SELECT h.Hochschulname, h.Gruendungsjahr
FROM Hochschulen h
ORDER BY h.Gruendungsjahr DESC
LIMIT 10;

-- Bundesländer mit den meisten Unis
CREATE TABLE IF NOT EXISTS anzahl_hochschulen AS
SELECT Bundesland, COUNT(*) AS Anzahl_Hochschulen
FROM Hochschulen
GROUP BY Bundesland
ORDER BY Anzahl_Hochschulen DESC
Limit 3;

-- Alle typen von Hochschulen
CREATE TABLE type_anzahl_hoch AS
SELECT Hochschultyp, COUNT(*) AS Anzahl_Hochschulen
FROM Hochschulen
GROUP BY Hochschultyp
ORDER BY Anzahl_Hochschulen DESC;

-- Alle typen nach Bundesland von Hochschulen
CREATE TABLE type_bund_anzahl_hoch AS
SELECT 
    Bundesland,
    Hochschultyp,
    COUNT(*) AS Anzahl_Hochschulen
FROM 
    Hochschulen
GROUP BY 
    Bundesland, Hochschultyp
ORDER BY 
    Bundesland, Anzahl_Hochschulen ASC;

-- Studentenanteil der Städte in Prozent
CREATE TABLE Studentenanteil AS
SELECT s.name_s, (h.Anzahl_Studierende * 100 / s.total) AS Studentenanteil
FROM Stadt s
JOIN Hochschulen h ON s.name_s = h.Ort_Hausanschrift;


-- test
CREATE TABLE test2 AS
SELECT 
    b.name_b,
    (h.Anzahl_Studierende * 100 / b.total) AS Studentenanteil
FROM 
    Bundesland b
JOIN 
    Hochschulen h 
ON 
    h.Bundesland LIKE '%' || b.name_b || '%';