-- Question 2 
SELECT AVG(qualite) FROM Mesure ;

-- Question 3 
SELECT Count(*) FROM Mesure
WHERE qualite > (SELECT AVG(qualite) FROM Mesure)

-- Question 4 
SELECT COUNT(*) FROM Point WHERE Longitude < 0 

-- Question 5 :
SELECT COUNT(*) FROM Point as p 
INNER JOIN Departement as d ON p.code_insee_dep = d.code_insee WHERE d.nom LIKE 'Ariège' 
or d.nom LIKE 'Aude'
or d.nom LIKE 'Haute-Garonne'
or d.nom LIKE 'Hautes-Pyrénées'
or d.nom LIKE 'Pyrénées-Orientales'
or d.nom LIKE 'Pyrénées-Atlantiques'

-- Question 6 
SELECT Nom FROM Departement as d
INNER JOIN Point AS P ON d.code_insee = p.code_insee_dep
WHERE p.longitude = (SELECT MIN(longitude) FROM Point)

-- Question 7 
SELECT DISTINCT d.Nom FROM Departement as d
INNER JOIN Point AS p ON d.code_insee = p.code_insee_dep
INNER JOIN Mesure as m ON p.id_point = m.id_point
INNER JOIN Operateur as o ON m.id_operateur = o.id_operateur 
WHERE o.nom = "Orange"

-- Question 8 
SELECT DISTINCT COUNT(*) FROM Point as P
LEFT JOIN Mesure as m ON p.id_point = m.id_point
WHERE m.id_point IS NULL

-- Question 9
SELECT DISTINCT Nom FROM Departement AS D
LEFT JOIN Point AS p ON d.code_insee = p.code_insee_dep
WHERE p.id_point IS NULL