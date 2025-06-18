from import_var import *

def ratio_vie(vie_restante : int, vie_max : int) -> float:
    pourcentage : float = (vie_restante / vie_max)
    return max(pourcentage, 0)

def longueur_barre_de_vie(vie_restante : int , vie_max : int) -> int:
    return round(ratio_vie(vie_restante, vie_max) * UI_LONGUEUR_BARRE_DE_VIE)

def update_barre_de_vie_monstre() -> None:
    assert(variables_globales.monstre_stat.est_initialise), "La fonction `update_barre_de_vie_monstre()` à été appelée alors que `monstre_stat` n'est pas initialisé."
    
    variables_globales.barre_vie_remplie_monstre = longueur_barre_de_vie(variables_globales.monstre_stat.vie, variables_globales.monstre_stat.vie_max)

def monstre_recoit_degats(degats_recu : int) -> None:
    if INVICIBLE_ENNEMI and degats_recu >= 0:
        return
    
    variables_globales.monstre_stat.baisser_vie(degats_recu)
    update_barre_de_vie_monstre()