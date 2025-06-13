from import_var import *

def attaque_soin(perso_stat, puissance_soin):
    soin = perso_stat["magie"] * puissance_soin * random.uniform(0.85, 1.0)
    soin = int(soin)
    return soin

def degat_infliger_physique(perso_stat, monstre_stat, puissance_attaque):
    attaque = perso_stat["force"]
    defense = monstre_stat["defense"]
    degats = ((attaque * puissance_attaque) / (defense + 10)) * random.uniform(0.85, 1.0)
    degats = max(1, int(degats))
    return degats

def degat_infliger_magique(perso_stat, monstre_stat, puissance_attaque):
    attaque = perso_stat["magie"]
    defense = monstre_stat["defense_magique"]
    degats = ((attaque * puissance_attaque) / (defense + 10)) * random.uniform(0.85, 1.0)
    degats = max(1, int(degats))
    return degats

def degat_recu_magique(monstre_stat, perso_stat, puissance_attaque):
    attaque = monstre_stat["magie"]
    defense = perso_stat["defense_magique"]
    degats = ((attaque * puissance_attaque) / (defense + 10)) * random.uniform(0.85, 1.0)
    degats = max(1, int(degats))
    return degats

def degat_recu_physique(monstre_stat, perso_stat, puissance_attaque):
    attaque = monstre_stat["force"]
    defense = perso_stat["defense"]
    degats = ((attaque * puissance_attaque) / (defense + 10)) * random.uniform(0.85, 1.0)
    degats = max(1, int(degats))
    return degats

def pourcentage_vie(vie_restante, vie_initiale):
    pourcentage = (vie_restante / vie_initiale) * 200
    return max(0, pourcentage)