from combat import *

def nouveau_monstre():
    variables_globales.monstre_stat = random.choice([variables_globales.blob_stat, variables_globales.sorcier_stat])
    variables_globales.monstre_vie = variables_globales.monstre_stat["vie"]
    if variables_globales.monstre_stat == variables_globales.blob_stat:
        variables_globales.couleur = ROUGE
        variables_globales.nom_adversaire = "Blob"
    else:
        variables_globales.couleur = BLEU
        variables_globales.nom_adversaire = "Sorcier"

def monstre_attaque():
    if variables_globales.nom_adversaire == "Blob":  # 50% de chance d'attaquer physiquement
        pygame.draw.rect(fenetre, ROUGE, (400, 300 , 200, 50), 5)
        degats = degat_recu_physique(variables_globales.monstre_stat, variables_globales.perso_stat, variables_globales.charge)
        joueur_vie = max(0, variables_globales.joueur_vie - degats)
        variables_globales.barre_vie_joueur = pourcentage_vie(joueur_vie, variables_globales.perso_stat["vie"])
        pygame.display.flip()
        time.sleep(1)
        pygame.event.clear()
    else:  # Attaque magique
        pygame.draw.rect(fenetre, ROUGE, (400, 300 , 200, 50), 5)
        degats = degat_recu_magique(variables_globales.monstre_stat, variables_globales.perso_stat, variables_globales.att_magique)
        joueur_vie = max(0, variables_globales.joueur_vie - degats)
        variables_globales.barre_vie_joueur = pourcentage_vie(joueur_vie, variables_globales.perso_stat["vie"])
        pygame.display.flip()
        time.sleep(1)
        pygame.event.clear()