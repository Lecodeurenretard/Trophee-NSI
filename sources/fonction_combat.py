from Monstre import *
from Joueur import *

def joueur_attaque(clef_attaque : str, cible : Monstre|Joueur) -> None:
    if len(Monstre.monstres_en_vie) == 0:
        return
    
    joueur.attaquer(cible.id, clef_attaque)

def monstres_attaquent() -> None:
    for monstre in Monstre.monstres_en_vie:
        monstre.attaquer(joueur.id, monstre.choisir_attaque())