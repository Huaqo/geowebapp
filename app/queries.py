DATASET = """
SELECT {attributes}
FROM Hochschulen h
JOIN Mieten m ON m.land = h.land
LEFT JOIN Bevoelkerung b ON b.region_name = h.ort 
AND b.bundesland = h.land 
AND (
    b.region_type = 'kreis' 
    OR b.region_name = 'Berlin' 
    OR b.region_name = 'Hamburg' 
    OR b.region_name = 'Bremen' 
    OR b.region_name = 'Hannover' AND b.region_type = 'landeshauptstadt' 
    OR b.region_name = 'Saarbrücken' AND b.region_type = 'landeshauptstadt')
WHERE {search_attr} ILIKE :search
ORDER BY {sort_by} {order}
LIMIT {limit};
"""

DATASET_GROUPED = """
SELECT {group_by}, COUNT(*) AS Anzahl
FROM Hochschulen
GROUP BY {group_by}
ORDER BY Anzahl DESC;
"""


# Studentenanteil Städte
STUDENTENANTEIL_STAEDTE = """
SELECT 
    b.region_name,
    ROUND(SUM(h.studenten * 100.0 / b.total_population)) AS Studentenanteil_in_Prozent
FROM 
    Bevoelkerung b
JOIN 
    Hochschulen h 
ON 
    LOWER(h.ort) = LOWER(
        CASE 
            WHEN POSITION(',' IN b.region_name) > 0 
            THEN SUBSTRING(b.region_name FROM 1 FOR POSITION(',' IN b.region_name) - 1)
            ELSE b.region_name
        END
    )
GROUP BY 
    b.region_name
ORDER BY Studentenanteil_in_Prozent DESC;
"""