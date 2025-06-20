from dessin import *
from fonctions_vrac import *

class Joueur:
    base_stats : Stat = Stat(50-5, 35, 40-8, 20, 30, 50)
    est_invincible : bool = False
    
    def __init__(self, moveset : dict[str, Attaque]) -> None:
        # on assumera que _stats et base_stats sont initialisés
        self._stats : Stat = Joueur.base_stats
        self._pseudo : str = ""
        self._moveset = moveset
        
        self._id = premier_indice_libre_de_entitees_vivantes()
        if self._id >= 0:
            entitees_vivantes[self._id] = self
            return
        
        self._id = len(entitees_vivantes)
        entitees_vivantes.append(self)
    
    def __del__(self):
        # Appelé quand l'objet est détruit (plus utilisé ou détruit avec del())
        if self._id > 0 and entitees_vivantes is not None:
            self.meurt()
    
    def meurt(self) -> None:
        entitees_vivantes[self._id] = None
        self._id = -1
    
    def set_pseudo(self, value : str) -> None:
        self._pseudo = value
    
    def get_pseudo(self) -> str:
        return self._pseudo
    
    def get_id(self) -> int:
        return self._id
    
    def get_moveset_clefs(self) -> tuple[str, ...]:
        return tuple(self._moveset.keys())
    
    def get_attaque_surface(self, clef_attaque : str) -> pygame.Surface:
        assert(clef_attaque in self.get_moveset_clefs())
        return self._moveset[clef_attaque].get_nom_surface()
    
    def attaque_peut_toucher_allies(self, attaque_clef : str) -> bool:
        assert(attaque_clef in self.get_moveset_clefs()), "Attaque pas inclue dans moveset dans attaque_peut_toucher_allies()."
        
        return self._moveset[attaque_clef].get_friendly_fire()
    
    def attaque_peut_toucher_ennemis(self, attaque_clef : str) -> bool:
        assert(attaque_clef in self.get_moveset_clefs()), "Attaque pas inclue dans moveset dans attaque_peut_toucher_ennemis()."
        
        return self._moveset[attaque_clef].get_ennemy_fire()
    
    def longueur_barre_de_vie(self) -> int:
        ratio = max(0, self._stats.vie / self._stats.vie_max)
        return round(ratio * UI_LONGUEUR_BARRE_DE_VIE)
    
    def reset_vie(self) -> None:
        self._stats.vie = self._stats.vie_max
    
    def recoit_degats(self, degats_recu : int) -> bool:
        """Prend en charge les dégats prits et retourne si le monstre est mort."""
        if Joueur.est_invincible and degats_recu >= 0:   # Joueur.invincible n'empèche pas les soins
            return False
        
        self._stats.baisser_vie(degats_recu)
        return self.est_mort()

    def subir_attaque(self, attaque : Attaque, stats_attaquant : Stat) -> bool:
        """Prend en charge l'attaque prise et retourne si le joueur est mort."""
        assert(stats_attaquant.est_initialise), "stats_monstre pas initialisé dans Joueur.essuyer_attaque()."
        return self.recoit_degats(
            attaque.calculer_degats(stats_attaquant, self._stats)
        )
    
    def attaquer(self, id_cible : int, clef_attaque : str) -> bool:
        assert(entitees_vivantes[id_cible] is not None), "La cible est None dans Joueur.attaquer()."
        assert(clef_attaque in self.get_moveset_clefs())
        
        attaque : Attaque = self._moveset[clef_attaque]
        
        if attaque.get_friendly_fire():                                         # si friendly fire, se tape lui même
            return self.subir_attaque(attaque, self._stats)                     # il faudrat ajouter un curseur si jamais 
        if attaque.get_ennemy_fire():                                           # l'attaque peut friendly fire et ennemy fire
            return entitees_vivantes[id_cible].subir_attaque(attaque, self._stats) # TODO:
        return False
    
    def dessiner(self, surface : pygame.Surface) -> None:
        boite_de_contours = (LARGEUR // 4 , 3 * HAUTEUR // 4 - 100, 100, 100)
        pygame.draw.rect(surface, BLEU, boite_de_contours, 0)


    def dessine_barre_de_vie(self, pos_x, pos_y) -> None:
        dessine_barre_de_vie(pos_x, pos_y, self._stats.vie / self._stats.vie_max, self.longueur_barre_de_vie())
    
    def dessiner_attaque(self, clef_attaque : str) -> None:
        assert(clef_attaque in self.get_moveset_clefs())
        
        self._moveset[clef_attaque].dessiner(fenetre, 400, 300)
        pygame.display.flip()
        time.sleep(1)
    
    def est_mort(self) -> bool:
        return self._stats.est_mort()


joueur : Joueur = Joueur({
    "heal":     ATTAQUES_DISPONIBLES["heal"],
    "physique": ATTAQUES_DISPONIBLES["physique"],
    "magie":    ATTAQUES_DISPONIBLES["magie"],
    "skip":     ATTAQUES_DISPONIBLES["skip"],
})