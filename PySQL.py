#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module pour l'execution de requêtes SQL si dbBrowser ne fonctionne pas
======================================================================

@author : Alexandre CONDETTE
@mail : alexandre.condette@spacebel.fr
@version : 1.0.1
@date : 16/11/2022

Commentaires sur la version :
=============================
16/11/22 : | VERSION 1.0.1 | 
----------------------------
- Correction sur la méthode requete pour pouvoir executer plusieurs requetes d'affilé
- Optimisation pour future utilisation avec GUI dédié 

16/11/22 : | VERSION 1.0.0 | 
----------------------------
- Premiere version pour gérer les requetes SQL Basiques du TP n°1 IPSA
- A n'utiliser que si le logiciel dbBrowser ne fonctionne pas correctement (plusieurs cas constatés principalement sur MacOS)
- A améliorer au fil des séances notamment gestion d'erreur, mais aussi les requêtes plus complexes

Comment l'utiliser : 
====================
- Dans un dossier mettre ce fichier + créer un nouveau fichier .py (Exemple PlatformIoT.py)
- Dans le fichier PlatformIoT.py :  - from PySQL import *
									- instancier la classe SQL (MaBase = SQL(NomDeLaBase))
									- executer des requetes avec MaBase.requete(MaRequeteSQL)
									- a la fin du fichier fermer la base avec MaBase.close()
"""

import sqlite3

class SQL(object) :
    """
	L'init permet de créer la base de donnée si elle n'existe pas, ou de s'y connecter sinon
	"""
    
    def __init__(self, dbName, extension='.db'):
        self.connexion = sqlite3.connect(dbName + extension)
    
    def requete(self, query):
        """
		Fonction permettant d'exécuter directement des requetes et de les soumettre à la BDD
		"""
        try :
            queries = query.split(";")
            for currentQuery in queries :
                print(currentQuery)
                self.cursor = self.connexion.execute(currentQuery)
                self.connexion.commit()
                self.cursor.close()
            
            if "SELECT" in currentQuery.upper() :
                self._displayResult()
            print("Requête exécutée avec succès")
            
        # Gestion des cas d'erreurs --> A Completer au fur et à mesure
        except sqlite3.OperationalError as e:
            msg = e.args[0]

            if "table" and "already exist" in msg : # Table déja créée
                print("La table existe déja")
                return(-1)

            elif "no such table" in msg:	# Table non créée
                tableError = msg.split(": ")[-1]
                print("La table {table} n'existe pas".format(table=tableError))
                return(-2)

            elif "has more than one primary key" in msg:
                tableError = msg.split(" has")[0]
                print("La {table} a plus d'une clé primaire\n".format(table=tableError),
					" -- Pour ajouter plusieurs clés primaires, utilisez la syntaxe : PRIMARY KEY(cle1, cle2, ..., cleN)")
            else :
                print("OperationalError")
                print(str(msg))	# Autre erreur --> Si c'est la cas reporter l'erreur à alexandre.condette@spacebel.fr pour l'ajouter à la gestion d'erreur
                return(-3)
	
        except sqlite3.IntegrityError as e: 
            msg = e.args[0]

            if "UNIQUE constraint failed" in msg :	# Erreur d'unicité de la clé primaire
                keyError = msg.split(": ")[-1]
                print("Erreur sur la clé primaire {cle} : La valeur doit être unique".format(cle=keyError))
                return(-4)
			
            elif "NOT NULL constraint failed" in msg :
                keyError = msg.split(": ")[-1]
                print("La cle {cle} ne doit pas être NULL, entrez une valeur".format(cle=keyError))
                return(-5)

            else :		# Autre erreur --> Si c'est la cas reporter l'erreur à alexandre.condette@spacebel.fr pour l'ajouter à la gestion d'erreur
                print("IntegrityError")
                print(str(msg))
                return (-6)

        except :
            return(-7)
		
        finally :
            self.connexion.commit()	# Mise à jour de la BDD après la requête

    def _diplayResult(self):
        for row in self.cursor:
            print(row)
        
    
    def close(self):
        """
		Fermer la connexion avec la BDD
		"""
        self.connexion.close()
        
        

