import logging
from os import getcwd

RACINE : str
DATA   : str
IMG    : str
SAVE   : str
ANIM : str
ETC    : str

RACINE = ''
if getcwd().endswith("sources"):
    RACINE = "../"    # rudimentaire mais fonctionnel
elif getcwd().endswith("Constantes"):
    RACINE = '../../'
else:
    logging.warning("Le dossier n'est pas reconnu, on suppose que l'on est à la racine.")

DATA = f"{RACINE}data"
IMG  = f"{RACINE}data/img"
SAVE = f"{RACINE}data/save"
ANIM = f"{RACINE}data/anim"
ETC  = f"{RACINE}data/etc"