from import_var import *

def joueur_calculer_attaque_soin(perso_stat, puissance_soin):
    soin = perso_stat["magie"] * puissance_soin * random.uniform(0.85, 1.0)
    soin = int(soin)
    return soin

def joueur_caluler_degat_physique_inflige(perso_stat, monstre_stat, puissance_attaque, defense_min=10):
    attaque = perso_stat["force"]
    defense = monstre_stat["defense"]
    degats = ((attaque * puissance_attaque) / (defense + defense_min)) * random.uniform(0.85, 1.0)
    degats = max(1, int(degats))
    return degats

def joueur_calculer_degat_magique_inflige(perso_stat, monstre_stat, puissance_attaque, defense_min=10):
    attaque = perso_stat["magie"]
    defense = monstre_stat["defense_magique"]
    degats = ((attaque * puissance_attaque) / (defense + defense_min)) * random.uniform(0.85, 1.0)
    degats = max(1, int(degats))
    return degats

def joueur_calculer_degat_magique_recu(monstre_stat, perso_stat, puissance_attaque, defense_min=10):
    attaque = monstre_stat["magie"]
    defense = perso_stat["defense_magique"]
    degats = ((attaque * puissance_attaque) / (defense + defense_min)) * random.uniform(0.85, 1.0)
    degats = max(1, int(degats))
    return degats

def joueur_caluler_degat_physique_recu(monstre_stat, perso_stat, puissance_attaque, defense_min=10):
    attaque = monstre_stat["force"]
    defense = perso_stat["defense"]
    degats = ((attaque * puissance_attaque) / (defense + defense_min)) * random.uniform(0.85, 1.0)
    degats = max(1, int(degats))
    return degats




def ratio_vie(vie_restante, vie_max):
    pourcentage = (vie_restante / vie_max)
    return max(pourcentage, 0)

def longueur_barre_de_vie(vie_restante, vie_max):
    return ratio_vie(vie_restante, vie_max) * UI_LONGUEUR_BARRE_DE_VIE

def update_barre_de_vie_joueur():
    variables_globales.barre_vie_remplie_joueur = longueur_barre_de_vie(variables_globales.joueur_vie, variables_globales.joueur_stat["vie"])

def update_barre_de_vie_monstre():
    variables_globales.barre_vie_remplie_monstre = longueur_barre_de_vie(variables_globales.monstre_vie, variables_globales.monstre_stat["vie"])

def reset_vie_joueur():
    variables_globales.joueur_vie = variables_globales.joueur_stat["vie"]
    update_barre_de_vie_joueur()

def reset_vie_monstre():
    variables_globales.monstre_vie = variables_globales.monstre_stat["vie"]
    update_barre_de_vie_monstre()