from import_var import *

def joueur_calculer_attaque_soin(perso_stat : Stat, puissance_soin : float) -> int:
    assert(perso_stat.est_initialise), "Vie du joueur non initialisée"

    soin : float = perso_stat.magie * puissance_soin * random.uniform(0.85, 1.0)
    return round(soin)

def joueur_caluler_degat_physique_inflige(perso_stat : Stat, monstre_stat : Stat, puissance_attaque : int, defense_min : int = 10) -> int:
    assert(perso_stat.est_initialise), "Vie du joueur non initialisée"
    assert(monstre_stat.est_initialise), "Vie du monstre non initialisée"
    
    attaque : int = perso_stat.force
    defense : int = monstre_stat.defense
    
    degats : float = ((attaque * puissance_attaque) / (defense + defense_min)) * random.uniform(0.85, 1.0)
    return max(1, round(degats))

def joueur_calculer_degat_magique_inflige(perso_stat : Stat, monstre_stat : Stat, puissance_attaque : int, defense_min : int = 10) -> int:
    assert(perso_stat.est_initialise), "Vie du joueur non initialisée"
    assert(monstre_stat.est_initialise), "Vie du monstre non initialisée"
    
    attaque : int = perso_stat.magie
    defense : int = monstre_stat.defense_magique
    
    degats : float = ((attaque * puissance_attaque) / (defense + defense_min)) * random.uniform(0.85, 1.0)
    return max(1, round(degats))

def joueur_calculer_degat_magique_recu(monstre_stat : Stat, perso_stat : Stat, puissance_attaque : int, defense_min : int = 10) -> int:
    assert(perso_stat.est_initialise), "Vie du joueur non initialisée"
    assert(monstre_stat.est_initialise), "Vie du monstre non initialisée"
    
    attaque : int = monstre_stat.magie
    defense : int = perso_stat.defense_magique
    
    degats : float = ((attaque * puissance_attaque) / (defense + defense_min)) * random.uniform(0.85, 1.0)
    return max(1, round(degats))

def joueur_caluler_degat_physique_recu(monstre_stat : Stat, perso_stat : Stat, puissance_attaque : int, defense_min : int = 10) -> int:
    assert(monstre_stat.est_initialise)
    
    attaque : int = monstre_stat.force
    defense : int = perso_stat.defense
    
    degats : float = ((attaque * puissance_attaque) / (defense + defense_min)) * random.uniform(0.85, 1.0)
    return max(1, int(degats))




def ratio_vie(vie_restante : int, vie_max : int) -> float:
    pourcentage : float = (vie_restante / vie_max)
    return max(pourcentage, 0)

def longueur_barre_de_vie(vie_restante : int , vie_max : int) -> int:
    return round(ratio_vie(vie_restante, vie_max) * UI_LONGUEUR_BARRE_DE_VIE)

def update_barre_de_vie_joueur() -> None:
    assert(variables_globales.joueur_stat.est_initialise)
    variables_globales.barre_vie_remplie_joueur = longueur_barre_de_vie(variables_globales.joueur_stat.vie, variables_globales.joueur_stat.vie_max)

def update_barre_de_vie_monstre() -> None:
    assert(variables_globales.monstre_stat.est_initialise), "La fonction `update_barre_de_vie_monstre()` à été appelée alors que `monstre_stat` n'est pas initialisé."
    
    variables_globales.barre_vie_remplie_monstre = longueur_barre_de_vie(variables_globales.monstre_stat.vie, variables_globales.monstre_stat.vie_max)

def reset_vie_joueur() -> None:
    assert(variables_globales.joueur_stat.est_initialise), "Stats du joueur non initialisée."
    
    variables_globales.joueur_stat.vie = variables_globales.joueur_stat.vie_max
    update_barre_de_vie_joueur()

def reset_vie_monstre() -> None:
    assert(variables_globales.monstre_stat.est_initialise), "Stats du monstr non initialisée."
    
    variables_globales.monstre_stat.vie = variables_globales.monstre_stat.vie_max
    update_barre_de_vie_monstre()