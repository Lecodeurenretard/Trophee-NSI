from Monstre import *
from Joueur import *
from UI import *

def joueur_attaque(clef_attaque : str, monstre_cible : Monstre) -> None:
    if len(Monstre.monstres_en_vie) == 0:
        return
    
    crit = joueur.attaquer(monstre_cible.get_id(), clef_attaque)   # attaque le premier monstre
    joueur.dessiner_attaque(fenetre, clef_attaque, crit)
    
    rafraichir_ecran()
    attendre(1)

def joueur_selectionne_attaque():
    curseur_menu_empl : tuple[int, int] = curseur_menu_combat.get_position_dans_position()
    
    if curseur_menu_empl == (0, 0):
        joueur_attaque("heal",      Monstre.monstres_en_vie[0])
        return
    
    if curseur_menu_empl == (1, 0):
        joueur_attaque("magie",     Monstre.monstres_en_vie[0])
        return
    
    if curseur_menu_empl == (0, 1):
        joueur_attaque("physique",  Monstre.monstres_en_vie[0])
        return
    
    if curseur_menu_empl == (1, 1):
        joueur_attaque("skip",      Monstre.monstres_en_vie[0])
        return
    
    raise ValueError(f"Le curseur du menu est à une position imprévue ({curseur_menu_empl} dans ses positions possibles)!")

def monstres_attaquent() -> None:
    for monstre in Monstre.monstres_en_vie:
        attaque_choisie : Attaque = monstre.choisir_attaque()
        
        crit = monstre.attaquer(joueur.get_id(), attaque_choisie)
        monstre.dessiner_attaque(fenetre, attaque_choisie, crit)