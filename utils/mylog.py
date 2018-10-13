"""
Crédits : http://sametmax.com/ecrire-des-logs-en-python/
"""

import logging
from logging.handlers import RotatingFileHandler

formatter = logging.Formatter("%(asctime)s -- %(levelname)s -- %(message)s")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG) # Premier niveau de filtre

## Logging dans le fichier log
file_handler = RotatingFileHandler(
    'logs/activity',
    mode="a",
    maxBytes=5000000,
    backupCount=10,
    encoding="utf-8")
file_handler.setLevel(logging.DEBUG) #deuxième niveau de filtre au moment de l'écriture dans le fichier
file_handler.setFormatter(formatter)

##Logging dans la console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)


logger.addHandler(file_handler)
logger.addHandler(stream_handler)