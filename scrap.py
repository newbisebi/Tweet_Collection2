# Import des modules
from twython import TwythonRateLimitError

from config.config import API
from utils.models import session, COMPTE, TWEET, KEYWORD
from utils.mylog import logger as lg
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--older",
        help="Optional. Use to get tweets " +
        "older than those already stored in db",
        action="store_true")
    return parser.parse_args()


def scrap_older_tweets(keyword, min_id):
    """Run API query with a max_id parameter"""
    res = API.search(q=keyword.valeur,
                     count=100,
                     result_type="recent",
                     max_id=min_id,
                     include_entities=True,
                     tweet_mode='extended')
    return res


def scrap_newer_tweets(keyword, max_id):
    """Run API query with a min_id parameter"""
    res = API.search(q=keyword.valeur,
                     count=100,
                     result_type="recent",
                     since_id=max_id,
                     include_entities=True,
                     tweet_mode='extended')
    return res


def run_keyword(keyword, older):
    """Iteratively search over a given keyword"""
    lg.info(f"Searching tweets for keywords {keyword.valeur}")
    keyword.nb_rech += 1
    min_id = keyword.plus_ancien_tweet
    max_id = keyword.plus_recent_tweet

    keep_looking = True
    i = 0

    while keep_looking:
        i += 1
        try:
            lg.info(
                f"Searching for keyword {keyword.valeur}  ; loop number {i}")
            if older is True:
                lg.debug("Older is true")
                res = scrap_older_tweets(keyword, min_id)
            else:
                lg.debug("Older is false")
                res = scrap_newer_tweets(keyword, max_id)
                # then we search tweet oldest than those just collected
                older = True
            min_id = manage_result(res, keyword)
            if not min_id:
                keep_looking = False

        except TwythonRateLimitError:
            lg.warning(
                "Twitter limit reached." +
                "Wait 15 minutes before moving to next keyword")
            # time.sleep(900)
            break


def manage_result(res, keyword):
    """Manage the twitter response according to wether or not its empty"""

    if res['statuses']:
        # case where there are some results to write in database
        lg.info(f"Number of tweets : {len(res['statuses'])}")
        min_id = min([tweet['id'] for tweet in res['statuses']])-1
        lg.debug(f"min_id : {min_id}")

        # Formatting and writing data
        write_data(res, keyword)
        return min_id
    else:
        lg.info(
            "No more results for keyword '%s' ; moving to next keyword",
            keyword.valeur)
        return None


def write_data(res, keyword):
    """
    Reorganize result data and write them to sqlite database
    """

    for tw in res['statuses']:
        tweet_id = tw['id']
        user_id = tw['user']['id']

        # Writing User data:
        compte = session.query(COMPTE).filter(COMPTE.user_id == user_id)
        if not compte.all():    # Si non existant on le créé
            compte = COMPTE(tw['user'])
            session.add(compte)
        else:
            compte = compte.one()

        # Writing Tweet_data:
        tweet = session.query(TWEET).filter(TWEET.tweet_id == tweet_id)
        if not tweet.all():
            tweet = TWEET(tw)
            tweet.compte = compte
            session.add(tweet)

        # Updating Keyword data :
        if keyword.plus_ancien_tweet:
            if tweet_id < keyword.plus_ancien_tweet:
                keyword.plus_ancien_tweet = tweet_id
        else:
            keyword.plus_ancien_tweet = tweet_id

        if keyword.plus_recent_tweet:
            if tweet_id > keyword.plus_recent_tweet:
                keyword.plus_recent_tweet = tweet_id
        else:
            keyword.plus_recent_tweet = tweet_id

        session.commit()


def main(older=True):
    keywords = (
        session.query(KEYWORD)
        .filter(KEYWORD.active is True)
        .order_by(KEYWORD.nb_rech)
        .all()
    )
    for keyword in keywords:
        run_keyword(keyword, older)
    lg.info("Program over")


if __name__ == '__main__':
    args = parse_arguments()
    if args.older:
        main(older=True)
    else:
        main(older=False)
