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

def monstre_choisis_attaque() -> Attaque:
    if variables_globales.nom_adversaire == "Blob":
        return ATTAQUES_DISPONIBLES["physique"]
    if variables_globales.nom_adversaire == "Sorcier":
        return ATTAQUES_DISPONIBLES["magie"]
    return ATTAQUES_DISPONIBLES["skip"]  # Si le monstre n'est pas reconnu, on ne fait rien

def monstre_attaque() -> None:
    assert(variables_globales.monstre_stat.est_initialise), "Appel de `monstre_attaque()` avant l'initialisation de `monstre_stat`"
    
    attaque_choisie : Attaque = monstre_choisis_attaque()
    
    if attaque_choisie == ATTAQUES_DISPONIBLES["skip"]:
        print("Warning: Le monstre n'a pas choisi d'attaque.")
        return
    
    if attaque_choisie != ATTAQUES_DISPONIBLES["physique"] and attaque_choisie != ATTAQUES_DISPONIBLES["magie"]:
        raise NotImplementedError("Le monstre à choisi un type d'attaque inconnue.")
    
    monstre_dessine_attaque(attaque_choisie)
    joueur.essuyer_attaque(variables_globales.monstre_stat, attaque_choisie)

def monstre_dessine_attaque(attaque : Attaque) -> None:
    attaque.dessiner(fenetre, 400, 300)
    pygame.display.flip()
    
    time.sleep(1)
    pygame.event.clear()