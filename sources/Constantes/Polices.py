"""
Contient les noms de polices utilisées et la fonction pixels_vers_taille_police().
projet : L'ascension de Esquimot
auteur : Dooheli, Lecodeurenretard, hibou509
"""

def pixels_vers_taille_police(taille_police : int) -> int:
    """Convertit une longueur en pixel vers une taille de police passée à la construction des objets Font."""
    return round(taille_police * 2/3)   # valeur trouvée expérimentalement


TITRE       : str|None = None # C moche # f"{ETC}Analog Whispers.ttf"
TEXTE       : str|None = None #         # f"{ETC}Analog Whispers.ttf"
FOURRE_TOUT : str|None = None #         # f"{ETC}Analog Whispers.ttf"