import logging
from os import getcwd

RACINE : str
DOSSIER_IMG  : str
DOSSIER_SAVE : str
DOSSIER_ETC  : str

RACINE = ''
if getcwd().endswith("sources"):
    RACINE = "../"    # rudimentaire mais fonctionnel
elif getcwd().endswith("Constantes"):
    RACINE = '../../'
else:
    logging.warning("Le dossier n'est pas reconnu, on suppose que l'on est à la racine.")

DOSSIER_IMG  = f"{RACINE}data/img"
DOSSIER_SAVE = f"{RACINE}data/save"
DOSSIER_ETC  = f"{RACINE}data/etc"