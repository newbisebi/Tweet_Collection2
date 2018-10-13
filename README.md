# Collecteur de Tweets ! 

Ce programme permet de collecter des tweets correspondant à un ou des mots clés donnés. 
Il recherche également les informations du compte d'utilisateur de l'auteur du tweet. 


## Instructions

1. Lancer keywords.py pour initialiser la base de données et entrer les mots clés à rechercher
2. Lancer le programme scrap.py pour commencer la recherche. 
    Pour rechercher des tweets plus anciens que ceux déjà enregistrés dans la BDD : utiliser le paramètre --older
    ex : python scrap.py --older

## Traitement du texte
Pour retraiter le texte (réduction, lemmatisation), lancer processing.py (nécessite TreeTaggerWrapper)

## Nombre de retweets et de favoris
Pour obtenir le nombre de RT et de FAV de chaque tweet dans la base de données, lancer influence.py
REMARQUE : Laisser passer un délai entre la collecte des tweets et la collecte des informations d'influence : le nombre de RT et FAV peut changer régulièrement dans les jours suivants la diffusion d'un tweet. 