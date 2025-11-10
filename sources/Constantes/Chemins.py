import logging
from os import getcwd

RACINE : str
DATA   : str
IMG    : str
SAVE   : str
ANIM   : str
ETC    : str

MUSIQUE : str
RADIO   : str

RACINE = ''
if getcwd().endswith("sources"):
    RACINE = "../"    # rudimentaire mais fonctionnel
elif getcwd().endswith("Constantes"):
    RACINE = '../../'
else:
    logging.warning("Le dossier n'est pas reconnu, on suppose que l'on est à la racine.")

DATA = f"{RACINE}data"
ANIM = f"{DATA}/anim"
ETC  = f"{DATA}/etc"
IMG  = f"{DATA}/img"
SAVE = f"{DATA}/save"
SFX  = f"{DATA}/sfx"

MUSIQUE = f"{DATA}/musique"
RADIO   = f"{MUSIQUE}/radio"