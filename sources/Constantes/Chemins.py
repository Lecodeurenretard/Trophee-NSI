"""Contient les chemins de fichiers vers les différents dossiers."""

import logging
from os import getcwd

DATA  : str
ANIM  : str
ETC   : str
IMG   : str
JSON  : str
POOLS : str
SAVE  : str

MUSIQUE : str
SFX     : str
RADIO   : str

RACINE = ''
if getcwd().endswith("sources"):
    RACINE = "../"    # rudimentaire mais fonctionnel
else:
    logging.warning("Le dossier n'est pas reconnu, on suppose que l'on est à la racine.")

DATA  = f"{RACINE}data/"
ANIM  = f"{DATA}anim/"
ETC   = f"{DATA}etc/"
IMG   = f"{DATA}img/"
JSON  = f"{DATA}JSON/"
POOLS = f"{JSON}pools/"
SAVE  = f"{DATA}save/"

MUSIQUE = f"{DATA}musique/"
SFX     = f"{DATA}sfx/"
RADIO   = f"{MUSIQUE}radio/"