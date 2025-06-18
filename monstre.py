from combat import *

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
        degats = joueur_caluler_degat_physique_recu(variables_globales.monstre_stat, variables_globales.joueur_stat, variables_globales.att_charge_puissance)
    elif attaque_choisie == "magique":
        monstre_dessine_attaque(BLEU)
        degats = joueur_calculer_degat_magique_recu(variables_globales.monstre_stat, variables_globales.joueur_stat, variables_globales.att_magique_puissance)
    else:
        raise NotImplementedError("Le monstre à choisi un type d'attaque inconnue.")
    
    joueur_recoit_degats(degats)

def monstre_dessine_attaque(couleur : color) -> None:
    pygame.draw.rect(fenetre, couleur, (400, 300 , 200, 50), 5)
    pygame.display.flip()
    
    time.sleep(1)
    pygame.event.clear()



def monstre_recoit_degats(degats_recu : int) -> None:
    if INVICIBLE_ENNEMI and degats_recu >= 0:
        return
    
    variables_globales.monstre_stat.baisser_vie(degats_recu)
    update_barre_de_vie_monstre()

def joueur_recoit_degats(degats_recu : int) -> None:
    if INVICIBLE_JOUEUR and degats_recu >= 0:   # INVICIBLE_JOUEUR n'empèche pas les soins
        return
    
    variables_globales.joueur_stat.baisser_vie(degats_recu)
    update_barre_de_vie_joueur()