from Monstre import *
from Joueur import *

def joueur_attaque(clef_attaque : str, monstre_cible : Monstre) -> None:
    if len(Monstre.monstres_en_vie) == 0:
        return
    
    crit = joueur.attaquer(monstre_cible.get_id(), clef_attaque)   # attaque le premier monstre
    joueur.dessiner_attaque(fenetre, clef_attaque, crit)

def monstres_attaquent() -> None:
    for monstre in Monstre.monstres_en_vie:
        attaque_choisie : Attaque = monstre.choisir_attaque()
        
        crit = monstre.attaquer(joueur.get_id(), attaque_choisie)
        monstre.dessiner_attaque(fenetre, attaque_choisie, crit)