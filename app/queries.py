HOCHSCHULEN = """
SELECT {attributes}
FROM Hochschulen h
WHERE h.{search_attr} ILIKE :search
ORDER BY {sort_by} {order}
LIMIT {limit};
"""

# Alle Typen von Hochschulen
HOCHSCHULEN_TYPES_COUNT_DESC = """
SELECT typ, COUNT(*) AS Anzahl_Hochschulen
FROM Hochschulen
GROUP BY typ
ORDER BY Anzahl_Hochschulen DESC;
"""

# Bundesländer mit den meisten Unis
BUNDESLAND_HOCHSCHULEN_COUNT = """
SELECT land, COUNT(*) AS Anzahl_Hochschulen
FROM Hochschulen
GROUP BY land
ORDER BY Anzahl_Hochschulen DESC
LIMIT 3;
"""

# Alle Typen nach Bundesland von Hochschulen
HOCHSCHULEN_TYPES_COUNT_DESC_GROUP_BY_BUNDESLAND = """
SELECT land, typ, COUNT(*) AS Anzahl_Hochschulen
FROM Hochschulen
GROUP BY land, typ
ORDER BY land, Anzahl_Hochschulen ASC;
"""

# Studentenanteil Bundesländer
STUDENTENANTEIL_BUNDESL = """
SELECT 
    b.name_b,
    SUM(h.studenten * 100.0 / b.total) AS Studentenanteil
FROM 
    Bundesland b
JOIN 
    Hochschulen h 
ON 
    LOWER(h.land) = LOWER(
        CASE 
            WHEN POSITION(',' IN b.name_b) > 0 
            THEN SUBSTRING(b.name_b FROM 1 FOR POSITION(',' IN b.name_b) - 1)
            ELSE b.name_b
        END
    )
GROUP BY 
    b.name_b
ORDER BY Studentenanteil DESC;
"""


# Studentenanteil Städte
STUDENTENANTEIL_STAEDTE = """
SELECT 
    s.name_s,
    SUM(h.studenten * 100.0 / s.total) AS Studentenanteil
FROM 
    Stadt s
JOIN 
    Hochschulen h 
ON 
    LOWER(h.ort) = LOWER(
        CASE 
            WHEN POSITION(',' IN s.name_s) > 0 
            THEN SUBSTRING(s.name_s FROM 1 FOR POSITION(',' IN s.name_s) - 1)
            ELSE s.name_s
        END
    )
GROUP BY 
    s.name_s
ORDER BY Studentenanteil DESC;
"""