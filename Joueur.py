from Stats import *
from dessin import *
from combat import *

class Joueur:
    base_stats : Stat = Stat(50, 35, 40, 20, 30, 50)
    def __init__(self) -> None:
        # on assumera que _stats et base_stats sont initialisés
        self._stats : Stat = Joueur.base_stats
        self._pseudo : str = ""
    
    def set_pseudo(self, value : str) -> None:
        self._pseudo = value
    def get_pseudo(self) -> str:
        return self._pseudo
    
    def longueur_barre_de_vie(self) -> int:
        ratio = max(0, self._stats.vie / self._stats.vie_max)
        return round(ratio * UI_LONGUEUR_BARRE_DE_VIE)
    
    def reset_vie(self) -> None:
        self._stats.vie = self._stats.vie_max
    
    def recoit_degats(self, degats_recu : int) -> None:
        if INVICIBLE_JOUEUR and degats_recu >= 0:   # INVICIBLE_JOUEUR n'empèche pas les soins
            return
        
        self._stats.baisser_vie(degats_recu)
    
    def essuyer_attaque(self, stats_monstre : Stat, attaque : Attaque) -> None:
        assert(stats_monstre.est_initialise), "stats_monstre pas initialisé dans Joueur.essuyer_attaque()."
        self.recoit_degats(
            attaque.calculer_degats(stats_monstre, self._stats)
        )
    
    def attaquer(self, stats_cible : Stat, attaque : Attaque) -> None:
        assert(stats_cible.est_initialise), "stats_monstre pas initialisé dans Joueur.attaquer()."
    
        if attaque != ATTAQUES_DISPONIBLES["heal"]:  # si heal, on ne cible pas le monstre
            monstre_recoit_degats(
                attaque.calculer_degats(self._stats, stats_cible)
            )
        else:
            self.essuyer_attaque(self._stats, attaque)
    
    def attaque_heal(self) -> None:
        self.attaquer(self._stats, ATTAQUES_DISPONIBLES["heal"])

    def dessiner_barre_de_vie(self, pos_x, pos_y):
        dessiner_barre_de_vie(pos_x, pos_y, self._stats.vie / self._stats.vie_max, self.longueur_barre_de_vie())
    
    def est_mort(self) -> bool:
        return self._stats.est_mort()

joueur : Joueur = Joueur()