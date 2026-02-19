from .Chemins import DATA

def pixels_vers_taille_police(taille_police : int) -> int:
    """Convertit une longueur en pixel vers une taille de police passée à la construction des objets Font."""
    return round(taille_police * 2/3)   # valeur trouvée expérimentalement


TITRE       : str|None = None # C moche # f"{DATA}/Analog Whispers.ttf"
TEXTE       : str|None = None #         # f"{DATA}/Analog Whispers.ttf"
FOURRE_TOUT : str|None = None #         # f"{DATA}/Analog Whispers.ttf"