from combat import *

def nouveau_monstre():
    variables_globales.monstre_stat = random.choice([variables_globales.blob_stat, variables_globales.sorcier_stat])
    reset_vie_monstre()

    if variables_globales.monstre_stat == variables_globales.blob_stat:
        variables_globales.couleur = ROUGE
        variables_globales.nom_adversaire = "Blob"
    else:
        variables_globales.couleur = BLEU
        variables_globales.nom_adversaire = "Sorcier"

def monstre_attaque():
    degats : int
    col_rect : tuple[int, int, int]

    if variables_globales.nom_adversaire == "Blob":  # 50% de chance d'attaquer physiquement
        col_rect = ROUGE
        degats = degat_recu_physique(variables_globales.monstre_stat, variables_globales.perso_stat, variables_globales.charge_puissance)
    else:  # Attaque magique
        col_rect = ROUGE   #TODO: changer couleur
        degats = degat_recu_magique(variables_globales.monstre_stat, variables_globales.perso_stat, variables_globales.att_magique_puissance)

    pygame.draw.rect(fenetre, col_rect, (400, 300 , 200, 50), 5)
    pygame.display.flip()
    
    if not INVICIBLE_PLAYER:
        variables_globales.joueur_vie = max(0, variables_globales.joueur_vie - degats)
        update_barre_de_vie_joueur()
    time.sleep(1)
    pygame.event.clear()