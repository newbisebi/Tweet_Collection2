# -*- coding: utf-8 -*-
"""
Date de création : 14/06/2017 par Sébastien Mariaux
Miseà jour : 03/10/2018 par Sébastien MAriaux - passage Python 3

Pour chaque tweet dans la base de donnée, le script recherche
le nombre de favoris et le nombre de retweets
et met à jour la BDD en conséquence.
Cette collecte est faite séparemment de la collecte des tweets
car le nombre de favoris et de rt
évolue dans les jours suivant la diffusion du tweet
"""

# Import des modules
import time
from utils.models import session, TWEET
from config.config import API
from utils.mylog import logger as lg

# Détermination de la date actuelle
auj = time.strftime('%y_%m_%d', time.localtime())


def api_query(liste_id):
    """
    Query the twitter API to get number of rts and favorites
    """
    results = {}
    query_results = API.lookup_status(id=liste_id)
    for tweet in query_results:
        tweet_id = tweet["id"]
        nb_rt = tweet["retweet_count"]
        nb_favori = tweet["favorite_count"]
        results[tweet_id] = {"nb_rt": nb_rt, "nb_favori": nb_favori}
    return results


def main():
    tweets_to_process = session.query(TWEET).filter(TWEET.nb_rt is None)
    while tweets_to_process.count() > 0:
        lg.info(
            f"""Searching influence data. Tweets remaining :
            {tweets_to_process.count()}"""
            )
        tweet_list = tweets_to_process.all()[0:100]
        ids = [tweet.tweet_id for tweet in tweet_list]
        results = api_query(ids)

        for tweet in tweets_to_process.all()[0:100]:
            tweet.nb_favori = results[tweet.tweet_id]["nb_favori"]
            tweet.nb_rt = results[tweet.tweet_id]["nb_rt"]
            tweet.date_influence = auj

        session.commit()
        session.close()
        tweets_to_process = session.query(TWEET).filter(TWEET.nb_rt is None)


if __name__ == '__main__':

    for annee in range(2006, 2018):
        lg.info(f"Collecte des informations d'influence")
        main()
