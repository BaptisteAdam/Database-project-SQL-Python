import pandas as pd

dt = pd.read_csv('tournages_xy_propre.csv',sep=";")
Demandeur = pd.read_csv('Demandeur.csv',sep=";")
Metrage = pd.read_csv('Metrage.csv',sep=";")
Lieu = pd.read_csv('LIEU.csv',sep=";")
Realisateur = pd.read_csv('Realisateur.csv',sep=";")

#gerer les adresses qui font chier
for i in range(len(dt['adresse'])):
    if "°" in dt['adresse'][i]:
        dt['adresse'][i] = dt['adresse'][i].replace("°", "'")
    if "Ë" in dt['adresse'][i]:
        dt['adresse'][i] = dt['adresse'][i].replace("Ë", "E") 

#gerer les titres qui font chier
for i in range(len(dt['titre'])):
    if "°" in dt['titre'][i]:
        dt['titre'][i] = dt['titre'][i].replace("°", "'")
    if "Ï" in dt['titre'][i]:
        dt['titre'][i] = dt['titre'][i].replace("Ï", "I")

#gerer les noms qui font chier
for i in range(len(dt['prenom_realisateur'])):
    if "Ö" in dt['prenom_realisateur'][i]:
        dt['prenom_realisateur'][i] = dt['prenom_realisateur'][i].replace("Ö", "O")
    if "Ü" in dt['prenom_realisateur'][i]:
        dt['prenom_realisateur'][i] = dt['prenom_realisateur'][i].replace("Ü", "U")
    if "Ï" in dt['prenom_realisateur'][i]:
        dt['prenom_realisateur'][i] = dt['prenom_realisateur'][i].replace("Ï", "I")

#-------------------------------------------------------------------------------------
def create_tables():
    return """DROP TABLE IF EXISTS se_situe;
DROP TABLE IF EXISTS Realise;
DROP TABLE IF EXISTS Metrage;
DROP TABLE IF EXISTS Demandeur;
DROP TABLE IF EXISTS LIEU;
DROP TABLE IF EXISTS Realisateur;

CREATE TABLE Realisateur(
        id_realisateur     Int  Auto_increment  NOT NULL ,
        Nom_realisateur    Varchar (100) NOT NULL ,
        Prenom_realisateur Varchar (100) NOT NULL
    ,CONSTRAINT Realisateur_PK PRIMARY KEY (id_realisateur)
)ENGINE=InnoDB;

CREATE TABLE Lieu(
        Adresse        Varchar (100) NOT NULL ,
        x              Varchar (50) NOT NULL ,
        y              Varchar (50) NOT NULL ,
        Arrondissement Varchar (100) NOT NULL
        ,CONSTRAINT Lieu_PK PRIMARY KEY (Adresse)
)ENGINE=InnoDB;

CREATE TABLE Demandeur(
        id_demandeur  Int  Auto_increment  NOT NULL ,
        Nom_demandeur Varchar (100) NOT NULL
    ,CONSTRAINT Demandeur_PK PRIMARY KEY (id_demandeur)
)ENGINE=InnoDB;

CREATE TABLE Metrage(
        id_metrage   Int  Auto_increment  NOT NULL ,
        Titre        Varchar (100) NOT NULL ,
        Type_metrage Varchar (100) NOT NULL ,
        id_demandeur Int NOT NULL
        ,CONSTRAINT Metrage_PK PRIMARY KEY (id_metrage)

        ,CONSTRAINT Metrage_Demandeur_FK FOREIGN KEY (id_demandeur) REFERENCES Demandeur(id_demandeur)
)ENGINE=InnoDB;

CREATE TABLE Realise(
        id_realisateur Int NOT NULL ,
        id_metrage     Int NOT NULL
        ,CONSTRAINT Realise_PK PRIMARY KEY (id_realisateur,id_metrage)

        ,CONSTRAINT Realise_Realisateur_FK FOREIGN KEY (id_realisateur) REFERENCES Realisateur(id_realisateur)
        ,CONSTRAINT Realise_Metrage0_FK FOREIGN KEY (id_metrage) REFERENCES Metrage(id_metrage)
)ENGINE=InnoDB;

CREATE TABLE Se_situe(
        Adresse    Varchar (100) NOT NULL ,
        id_metrage Int NOT NULL ,
        Date_debut Date NOT NULL ,
        Date_fin   Date NOT NULL
        ,CONSTRAINT Se_situe_PK PRIMARY KEY (Adresse,id_metrage)

        ,CONSTRAINT Se_situe_Lieu_FK FOREIGN KEY (Adresse) REFERENCES Lieu(Adresse)
        ,CONSTRAINT Se_situe_Metrage0_FK FOREIGN KEY (id_metrage) REFERENCES Metrage(id_metrage)
)ENGINE=InnoDB;
"""

def demandeur(dt):
    string = "INSERT INTO Demandeur(nom_demandeur)\nVALUES"
    organisme_demandeur = dt['organisme_demandeur'].unique()
    for index in range(len(organisme_demandeur)-1):
        string += '("'+str(organisme_demandeur[index])+'"),\n'
    string += '("'+str(organisme_demandeur[len(organisme_demandeur)-1])+'");\n'
    return string

def lieu(dt):
    #gerer a la main le ';' de la fin
    string = "INSERT INTO Lieu(Adresse, x, y, Arrondissement)\nVALUES"
    xy = dt['xy']
    ardt = dt['ardt']
    adresse = dt['adresse']
    carac_parasite = adresse[0][3]
    list_adresse = []
    for index in range(len(xy)-1):
        if not adresse[index].upper() in list_adresse:
            list_adresse.append(adresse[index].upper())
            string += '("'+str(adresse[index].replace('"', "'").replace(carac_parasite, "").upper()) +'","'+ str(xy[index].split(',')[0]) +'","'+ str(xy[index].split(',')[1])+'","'+ str(ardt[index]) + '"),\n'
    if not adresse[index] in list_adresse:
        string +='("'+str(adresse[len(xy)-1].replace('"','').upper()) +'","'+ str(xy[len(xy)-1].split(',')[0]) +'","'+ str(xy[len(xy)-1].split(',')[1])+'","'+ str(ardt[len(xy)-1]) + '");\n'
    string = string[:len(string)-2]+';\n'
    return string

def realisateur(dt):
    nom_realisateur = dt['nom_realisateur']
    prenom_realisateur = dt['prenom_realisateur']
    list_tupl = []
    for index in range(len(nom_realisateur)):
        if (nom_realisateur[index], prenom_realisateur[index]) not in list_tupl:
            list_tupl.append((nom_realisateur[index], prenom_realisateur[index]))
    
    string = "INSERT INTO Realisateur(nom_realisateur, prenom_realisateur)\nVALUES"
    for index in range(len(list_tupl)):
        if type(list_tupl[index][0]) == type(str()):
            string +='("'+str(list_tupl[index][0])+'","'+ str(list_tupl[index][1]) + '"),\n'
    #gerer les 3 cas exlcu plus haut
    string += '("TOLENADO","ERIC"),\n("NAKACHE","OLIVIER"),\n("MOCTARI","MOHAMED MUSTAPHA `MAMANE`");\n'
    return string


def metrage(dt, demandeur):   
    id_demandeur = demandeur['id_demandeur']
    Nom_demandeur = demandeur['Nom_demandeur']
    dico_demandeur = {}
    for i in range(len(id_demandeur)):
        dico_demandeur[Nom_demandeur[i]] = id_demandeur[i]
        
    titre = dt['titre']
    type_metrage = dt['type_de_tournage']
    organisme_demandeur = dt['organisme_demandeur']
    list_film = []
    
    string = "INSERT INTO Metrage(Titre, Type_metrage, id_demandeur)\nVALUES"
    for index in range(len(titre)-1):
        if titre[index] in list_film:
            continue
        list_film.append(titre[index])
        string += '("'+str(titre[index])+'","'+ str(type_metrage[index]) + '",' + str(dico_demandeur[organisme_demandeur[index]]) + '),\n'
    string += '("'+str(titre[len(titre)-1])+'","'+ str(type_metrage[len(titre)-1]) + '",' + str(dico_demandeur[organisme_demandeur[index]]) + ');\n'
    return string

def change_date(date):
    jour, mois, annee = date.split('/')
    new_date = annee+'-'+mois+'-'+jour
    return new_date

def se_situe(dt, metrage):
    date_debut = dt['date_debut']
    date_fin = dt['date_fin']
    titre_tournage = dt['titre']
    adresse_tournage = dt['adresse']
    carac_parasite = adresse_tournage[0][3]
    
    id_metrage = metrage['id_metrage']
    titre_metrage = metrage['Titre']
    dico_metrage = {}
    for i, titre in enumerate(titre_metrage):
        dico_metrage[titre] = id_metrage[i]
    
    list_ad_id = []
 
    string = "INSERT INTO Se_situe(Adresse, id_metrage, Date_debut, Date_fin)\nVALUES"
    for i in range(len(titre_tournage)-1):
        titre = titre_tournage[i]
        adresse = adresse_tournage[i].replace('"', "'").replace(carac_parasite, '').upper()
        if (adresse, dico_metrage.get(titre)) not in list_ad_id:
            list_ad_id.append((adresse, dico_metrage.get(titre)))
            string += '("'+str(adresse)+'",'+str(dico_metrage.get(titre))+',"'+str(change_date(date_debut[i]))+'","'+str(change_date(date_fin[i]))+'"),\n'

    titre = titre_tournage[len(titre_tournage)-1]
    adresse = adresse_tournage[len(titre_tournage)-1].replace('"', "'").replace(carac_parasite, '').upper()
    string += '("'+str(adresse)+'",'+str(dico_metrage.get(titre))+',"'+str(change_date(date_debut[len(titre_tournage)-1]))+'","'+str(change_date(date_fin[i]))+'");\n'
    return string

def realise(dt, metrage, realisateur):
    titre = dt['titre']
    nom_r = dt['nom_realisateur']
    prenom_r = dt['prenom_realisateur']
    id_tournage = metrage['id_metrage']
    titre_tournage = metrage['Titre']
    id_realisateur = realisateur['id_realisateur']
    nom_realisateur = realisateur['Nom_realisateur']
    prenom_realisateur = realisateur['Prenom_realisateur']
    
    list_realisateur_tournage = []
    dict_realisateur = {}
    dict_tournage = {}
    for i in range(len(id_realisateur)):
        full_realisateur = str(prenom_realisateur[i]) + " " + str(nom_realisateur[i])
        dict_realisateur[full_realisateur] = id_realisateur[i]
    for j in range(len(id_tournage)):
        dict_tournage[titre_tournage[j]] = id_tournage[j]   

    string = "INSERT INTO Realise(id_realisateur, id_metrage)\nVALUES"
    for index in range(len(titre)):
        if prenom_r[index] == 'E.TOLENADO/O.NAKACHE' or prenom_r[index] == 'MAMANE':
            continue
        realisateur_dt = str(prenom_r[index]) + " " + str(nom_r[index])
        id_r = dict_realisateur[realisateur_dt]
        id_t = dict_tournage[titre[index]]
        combinaison = str(id_r) + ":" + str(id_t)
        if combinaison in list_realisateur_tournage:
            continue
        list_realisateur_tournage.append(combinaison)
        string += '('+str(id_r)+','+ str(id_t) + '),\n'
    #gerer les 3 cas exlcu plus haut
    string += '(198,181),\n(196,111),\n(197,111);\n'
    return string
#------------------------------------------------------------------------------------
def ecrire_ficher(dt, Demandeur, Metrage, Realisateur):
    liste = []
    liste.append(create_tables())
    liste.append(demandeur(dt))
    liste.append(lieu(dt))
    liste.append(realisateur(dt))
    liste.append(metrage(dt, Demandeur))
    liste.append(se_situe(dt, Metrage))
    liste.append(realise(dt, Metrage, Realisateur))

    with open('Code SQL.sql', 'w') as file:
        for string in liste:
            file.write(string+'\n')

ecrire_ficher(dt, Demandeur, Metrage, Realisateur)