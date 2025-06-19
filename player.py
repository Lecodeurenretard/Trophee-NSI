from monstre import *
from UI import *

def joueur_dessine_attaque(attaque : Attaque) -> None:
    attaque.dessiner(fenetre, 400, 300)
    pygame.display.flip()
    time.sleep(1)
    
    rafraichir_ecran()
    time.sleep(1)
    
    pygame.event.clear()

def joueur_attaque_soin() -> None:
    joueur.attaque_heal()
    joueur_dessine_attaque(ATTAQUES_DISPONIBLES["heal"])

def joueur_attaque(clef_attaque : str) -> None:
    attaque : Attaque = ATTAQUES_DISPONIBLES[clef_attaque]
    
    joueur.attaquer(variables_globales.monstre_stat, attaque)
    joueur_dessine_attaque(attaque)


def joueur_selectionne_attaque():
    curseur_empl : tuple[int|NaN, int|NaN] = get_curseur_emplacement()

    if curseur_empl == (0, 0):
        joueur_attaque_soin()
        return
    
    if curseur_empl == (1, 0):
        joueur_attaque("magie")
        return
    
    if curseur_empl == (0, 1):
        joueur_attaque("physique")
        return
    
    if curseur_empl == (1, 1):
        joueur_attaque("skip")
        return
    
    print(f"Verbose: le curseur est à l'emplacement {curseur_empl} (position {(variables_globales.curseur_x, variables_globales.curseur_y)}).")
    print(f"Verbose: positions x attendues: {variables_globales.curseur_pos_attendue_x[0]} ou {variables_globales.curseur_pos_attendue_x[1]}.")
    print(f"Verbose: positions y attendues: {variables_globales.curseur_pos_attendue_y[0]} ou {variables_globales.curseur_pos_attendue_y[1]}.")
    raise ValueError("Le curseur n'est pas à la bonne position!")