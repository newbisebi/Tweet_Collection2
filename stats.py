from utils.models import session, COMPTE, TWEET, KEYWORD


def print_stats():
    nb_tweets = session.query(TWEET).count()
    nb_tw_originaux = session.query(TWEET).filter(TWEET.retweet == False).count()
    nb_comptes = session.query(COMPTE).count()
    nb_keywords = session.query(KEYWORD).count()

    print(f"Nombre de tweets : {nb_tweets}")
    print(f"Nombre de tweets (hors RT): {nb_tw_originaux}")
    print(f"Nombre de comptes d'utilisateurs : {nb_comptes}")
    print(f"Nombre de keywords : {nb_keywords}")


if __name__ == '__main__':
    print_stats()
