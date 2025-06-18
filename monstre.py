from combat import *
from Joueur import *

def reset_vie_monstre() -> None:
    assert(variables_globales.monstre_stat.est_initialise), "Stats du monstre non initialisée."
    
    variables_globales.monstre_stat.vie = variables_globales.monstre_stat.vie_max
    update_barre_de_vie_monstre()

def nouveau_monstre() -> None:
    stat_choix = (variables_globales.blob_stat, variables_globales.sorcier_stat)
    variables_globales.monstre_stat = copy(random.choice(stat_choix))
    reset_vie_monstre()
    
    if variables_globales.monstre_stat == variables_globales.blob_stat:
        variables_globales.couleur_monstre = ROUGE
        variables_globales.nom_adversaire = "Blob"
        return
    
    if variables_globales.monstre_stat == variables_globales.sorcier_stat:
        variables_globales.couleur_monstre = BLEU
        variables_globales.nom_adversaire = "Sorcier"
        return
    
    raise NotImplementedError(f"Le monstre avec pour stats {variables_globales.monstre_stat}, n'est pas reconnu comme existant.")

def monstre_choisis_attaque() -> str:
    if variables_globales.nom_adversaire == "Blob":
        return "physique"
    if variables_globales.nom_adversaire == "Sorcier":
        return "magique"
    return ''

def monstre_attaque() -> None:
    assert(variables_globales.monstre_stat.est_initialise), "Appel de `monstre_attaque()` avant l'initialisation de `monstre_stat`"
    
    attaque_choisie : str = monstre_choisis_attaque()
    
    if attaque_choisie == "":
        print("Warning: Le monstre n'a pas choisi d'attaque.")
        return
    
    degats : int
    if attaque_choisie == "physique":
        monstre_dessine_attaque(ROUGE)
        joueur.essuyer_attaque(
            variables_globales.monstre_stat,
            variables_globales.att_charge_puissance,
            TypeAttaque.PHYSIQUE
        )
    elif attaque_choisie == "magique":
        monstre_dessine_attaque(BLEU)
        joueur.essuyer_attaque(
            variables_globales.monstre_stat,
            variables_globales.att_magique_puissance,
            TypeAttaque.MAGIQUE
        )
    else:
        raise NotImplementedError("Le monstre à choisi un type d'attaque inconnue.")
    
def monstre_dessine_attaque(couleur : color) -> None:
    pygame.draw.rect(fenetre, couleur, (400, 300 , 200, 50), 5)
    pygame.display.flip()
    
    time.sleep(1)
    pygame.event.clear()