from import_var import *

def joueur_calculer_attaque_soin(perso_stat : dict[str, int], puissance_soin : float) -> int:
    soin : float = perso_stat["magie"] * puissance_soin * random.uniform(0.85, 1.0)
    return round(soin)

def joueur_caluler_degat_physique_inflige(perso_stat : dict[str, int], monstre_stat : dict[str, int|NaN], puissance_attaque : int, defense_min : int = 10) -> int:
    assert(not math.isnan(monstre_stat["defense"]))
    attaque : int = perso_stat["force"]
    defense : int = monstre_stat["defense"] # type: ignore
    
    degats : float = ((attaque * puissance_attaque) / (defense + defense_min)) * random.uniform(0.85, 1.0)
    return max(1, round(degats))

def joueur_calculer_degat_magique_inflige(perso_stat : dict[str, int], monstre_stat : dict[str, int|NaN], puissance_attaque : int, defense_min : int = 10) -> int:
    assert(not math.isnan(monstre_stat["defense_magique"]))
    attaque : int = perso_stat["magie"]
    defense : int = monstre_stat["defense_magique"] # type: ignore

    degats : float = ((attaque * puissance_attaque) / (defense + defense_min)) * random.uniform(0.85, 1.0)
    return max(1, round(degats))

def joueur_calculer_degat_magique_recu(monstre_stat : dict[str, int|NaN], perso_stat : dict[str, int], puissance_attaque : int, defense_min : int = 10) -> int:
    assert(not math.isnan(monstre_stat["magie"]))
    attaque : int = monstre_stat["magie"] # type: ignore
    defense : int = perso_stat["defense_magique"]

    degats : float = ((attaque * puissance_attaque) / (defense + defense_min)) * random.uniform(0.85, 1.0)
    return max(1, round(degats))

def joueur_caluler_degat_physique_recu(monstre_stat : dict[str, int|NaN], perso_stat : dict[str, int], puissance_attaque : int, defense_min : int = 10) -> int:
    assert(not math.isnan(monstre_stat["force"]))
    attaque : int = monstre_stat["force"] # type: ignore
    defense : int = perso_stat["defense"]

    degats : float = ((attaque * puissance_attaque) / (defense + defense_min)) * random.uniform(0.85, 1.0)
    return max(1, int(degats))




def ratio_vie(vie_restante : int, vie_max : int) -> float:
    pourcentage : float = (vie_restante / vie_max)
    return max(pourcentage, 0)

def longueur_barre_de_vie(vie_restante : int , vie_max : int) -> int:
    return round(ratio_vie(vie_restante, vie_max) * UI_LONGUEUR_BARRE_DE_VIE)

def update_barre_de_vie_joueur() -> None:
    variables_globales.barre_vie_remplie_joueur = longueur_barre_de_vie(variables_globales.joueur_vie, variables_globales.joueur_stat["vie"])

def update_barre_de_vie_monstre() -> None:
    assert(not math.isnan(variables_globales.monstre_stat["vie"])), "La fonction `update_barre_de_vie_monstre()` à été appelée alors que `monstre_stat` n'est pas initialisé."
    
    #ignore type warning
    variables_globales.barre_vie_remplie_monstre = longueur_barre_de_vie(variables_globales.monstre_vie, variables_globales.monstre_stat["vie"]) # type: ignore

def reset_vie_joueur() -> None:
    variables_globales.joueur_vie = variables_globales.joueur_stat["vie"]
    update_barre_de_vie_joueur()

def reset_vie_monstre() -> None:
    variables_globales.monstre_vie = variables_globales.monstre_stat["vie"]
    update_barre_de_vie_monstre()