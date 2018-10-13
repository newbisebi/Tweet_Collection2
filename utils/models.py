# -*- coding: utf-8 -*-
"""
Format des tables utilisées dans la base de données
"""
import time
from datetime import datetime, date
import sqlalchemy #Interface sqlite
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Float, Boolean
from sqlalchemy.orm import mapper, sessionmaker, relationship, backref
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Float, Boolean
from sqlalchemy.orm import mapper, sessionmaker
import time
from config.config import FICHIER_BDD

#Détermination de la date actuelle
auj = time.strftime('%y_%m_%d', time.localtime())


Base = declarative_base()

class KEYWORD(Base):
    __tablename__ = 'keywords'
    valeur = Column(String, primary_key=True)
    nb_rech = Column(Integer)
    active = Column(Boolean)
    plus_ancien_tweet = Column(Integer)
    plus_recent_tweet = Column(Integer)

    def __init__(self, valeur):
        self.valeur=valeur
        self.nb_rech=0
        self.active=True

    def __repr__(self):
        return self.valeur

class COMPTE(Base):
    __tablename__ = "compte"
    user_name = Column(String)
    user_id = Column(Integer, primary_key=True)
    description = Column(String)
    nb_abonnes = Column(Integer)
    nb_abonnements = Column(Integer)
    nb_tweets = Column(Integer)

    def __init__(self, user_response):
        self.user_name = user_response["screen_name"]
        self.user_id = user_response["id"]
        self.description = user_response["description"]
        self.nb_abonnements = user_response['friends_count']
        self.nb_abonnes = user_response["followers_count"]
        self.nb_tweets = user_response["statuses_count"]


    def __repr__(self):
        return self.user_name


class TWEET(Base):
    """
    Format de la table dans laquelle vont être stockés les tweets
    """
    __tablename__ = 'tweet'
    tweet_id = Column(Integer, primary_key=True)
    user_name = Column(String)
    date = Column(DateTime)
    mois = Column(String)
    annee = Column(String)
    texte = Column(String)
    texte_retraite = Column(String)
    retweet = Column(Boolean)
    hashtags = Column(String)
    nb_rt = Column(Integer)
    nb_favori = Column(Integer)
    date_influence = Column(String)
    mentions = Column(String)
    dest = Column(String)
    json = Column(String)

    compte_id = Column(Integer, ForeignKey('compte.user_id'))
    compte = relationship(
        COMPTE,
        backref=backref('tweets',
                         uselist=True,
                         cascade='delete,all'))

    def __init__(self, status):
        self.json = str(status)
        self.user_name = status["user"]["name"]
        self.tweet_id = status["id"]
        date = status["created_at"]
        date = datetime.strptime(date, '%a %b %d %H:%M:%S +0000 %Y')
        self.mois = date.strftime('%m')
        self.annee = date.strftime('%Y')
        self.hashtags = ','.join([ht["text"] for ht in status["entities"]["hashtags"]])
        mentions = status["entities"]["user_mentions"]
        if mentions:
            self.mentions = ','.join([f"{el['screen_name']} ({el['id']})" for el in mentions])
        else:
            self.mentions = ""
        id_dest = status["in_reply_to_user_id"]
        nom_dest = status["in_reply_to_screen_name"]
        if id_dest:
            self.dest = f"{nom_dest} ({id_dest})"
        else:
            self.dest = ""
        if 'retweeted_status' in status:
            self.retweet = True
            self.texte = status['retweeted_status']["full_text"]
        else:
            self.retweet = False
            self.texte = status["full_text"]


    def __repr__(self):
        return f"{self.user_name} >>> {self.texte}"


#CONNECTION ET CREATION DES TABLES
engine = sqlalchemy.create_engine(FICHIER_BDD, echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)