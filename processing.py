# -*- coding: utf-8 -*-
"""
Date de création : 13/10/2018 par Sébastien Mariaux

Ce script a pour but de retraiter le texte des tweets
afin de pouvoir l'analyser
La ponctuation est supprimée, les mots sont lemmatisés,
et les mots outils supprimés

"""

# Import des modules
import time
from utils.models import session, TWEET
from utils.mylog import logger as lg
from utils.text_processing import processing

# Détermination de la date actuelle
auj = time.strftime('%y_%m_%d', time.localtime())


def main():
    tweets_to_process = (
        session.query(TWEET)
        .filter(TWEET.texte_retraite is None))
    lg.info(f"Tweet to process : {tweets_to_process.count()}")
    while tweets_to_process.count() > 0:
        for tweet in tweets_to_process.all()[0:1000]:
            tweet.texte_retraite = processing(tweet.texte)
        session.commit()
        session.close()
        tweets_to_process = (
            session.query(TWEET)
            .filter(TWEET.texte_retraite == ""))


if __name__ == '__main__':
    main()
