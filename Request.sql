SELECT Lieu.arrondissement, COUNT(*) AS nb_tournage 
FROM Se_situe NATURAL JOIN Lieu NATURAL JOIN Metrage 
GROUP BY Lieu.arrondissement ORDER BY nb_tournage DESC;

SELECT Realisateur.Prenom_realisateur, Realisateur.Nom_realisateur 
FROM Realisateur NATURAL JOIN Realise NATURAL JOIN Metrage NATURAL JOIN Demandeur 
WHERE Demandeur.Nom_demandeur='FIRSTEP';

SELECT Type_metrage,AVG(DATEDIFF(Se_situe.Date_fin,Se_situe.Date_debut)+1) AS duree_moyenne_tournage,
MAX(DATEDIFF(Se_situe.Date_fin,Se_situe.Date_debut)+1) AS duree_maximale_tournage 
FROM Se_situe JOIN Metrage ON Metrage.id_metrage=Se_situe.id_metrage 
GROUP BY Type_metrage;