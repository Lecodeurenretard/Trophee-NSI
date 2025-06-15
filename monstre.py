from combat import *

def nouveau_monstre():
    variables_globales.monstre_stat = random.choice([variables_globales.blob_stat, variables_globales.sorcier_stat])
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

def monstre_choisis_attaque():
    if variables_globales.nom_adversaire == "Blob":
        return "physique"
    if variables_globales.nom_adversaire == "Sorcier":
        return "magique"
    return ''

def monstre_attaque():
    attaque_choisie = monstre_choisis_attaque()
    
    if attaque_choisie == "":
        print("Warning: Le monstre n'a pas choisi d'attaque.")
        return
    
    degats : int
    if attaque_choisie == "physique":
        monstre_dessine_attaque(ROUGE)
        degats = joueur_caluler_degat_physique_recu(variables_globales.monstre_stat, variables_globales.joueur_stat, variables_globales.charge_puissance)
    elif attaque_choisie == "magique":
        monstre_dessine_attaque(BLEU)
        degats = joueur_calculer_degat_magique_recu(variables_globales.monstre_stat, variables_globales.joueur_stat, variables_globales.att_magique_puissance)
    else:
        raise NotImplementedError("Le monstre à choisi un type d'attaque inconnue.")
    
    joueur_recoit_degats(degats)

def monstre_dessine_attaque(couleur):
    pygame.draw.rect(fenetre, couleur, (400, 300 , 200, 50), 5)
    pygame.display.flip()
    
    time.sleep(1)
    pygame.event.clear()



def monstre_recoit_degats(degats_recu):
    if INVICIBLE_ENNEMI and degats_recu >= 0:
        return
    
    variables_globales.monstre_vie -= degats_recu
    variables_globales.monstre_vie = max(variables_globales.monstre_vie, 0) # Empêche la vie de passer sous 0
    update_barre_de_vie_monstre()

def joueur_recoit_degats(degats_recu):
    if INVICIBLE_JOUEUR and degats_recu >= 0:   # INVICIBLE_JOUEUR n'empèche pas les soins
        return
    
    variables_globales.joueur_vie -= degats_recu
    variables_globales.joueur_vie = max( # Empêche la vie de passer sous 0 et d'aller au-dessus du max
        min(
            variables_globales.joueur_vie,
            variables_globales.joueur_stat["vie"]
        ),
        0
    )
    update_barre_de_vie_joueur()