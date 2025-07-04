from dessin import *
from fonctions_vrac import *
from Attaque import *

class Joueur:
    _STATS_DE_BASE : Stat = Stat(50-5, 35, 40-5, 20, 30, 50, 1.2, 1)
    est_invincible : bool = False
    dimensions_sprite : tuple[int, int] = (160, 160)
    
    def __init__(self, moveset : dict[str, Attaque], chemin_vers_sprite : str|None = None) -> None:
        # on assumera que _stats et _base_stats sont initialisés
        self._stats : Stat = Joueur._STATS_DE_BASE
        self._pseudo : str = ""
        self._moveset = moveset
        
        self._id = premier_indice_libre_de_entitees_vivantes()
        if self._id >= 0:
            entitees_vivantes[self._id] = self
            return
        
        if chemin_vers_sprite is not None:
            self._sprite  : Surface|None = pygame.transform.scale(pygame.image.load(chemin_vers_sprite), Joueur.dimensions_sprite)
        else:
            self._sprite : Surface|None = None
        
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
    
    def get_attaque_surface(self, clef_attaque : str) -> Surface:
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
        """
        Prend en charge l'attaque prise et retourne une tuple contenant s'il y a eu un crit..
        """
        assert(stats_attaquant.est_initialise), "stats_monstre pas initialisé dans Joueur.essuyer_attaque()."
        
        degats, crit = attaque.calculer_degats(stats_attaquant, self._stats)
        self.recoit_degats(degats)
        return crit
    
    def attaquer(self, id_cible : int, clef_attaque : str) -> bool:
        assert(entitees_vivantes[id_cible] is not None), "La cible est None dans Joueur.attaquer()."
        assert(clef_attaque in self.get_moveset_clefs())
        
        attaque : Attaque = self._moveset[clef_attaque]
        
        if attaque.get_friendly_fire():                                         # si friendly fire, se tape lui même
            return self.subir_attaque(attaque, self._stats)                     # il faudra ajouter un curseur si jamais 
        if attaque.get_ennemy_fire():                                           # l'attaque peut friendly fire et ennemy fire
            return entitees_vivantes[id_cible].subir_attaque(attaque, self._stats) # TODO:
        return False
    
    def dessiner(self, surface : Surface) -> None:
        if MODE_DEBUG:
            boite_de_contours = (LARGEUR // 4, 3 * HAUTEUR // 4 - 100, 100, 100)
            pygame.draw.rect(surface, BLEU, boite_de_contours, 0)
            return
        
        if self._sprite is not None:
            surface.blit(self._sprite, (LARGEUR // 4, 3 * HAUTEUR // 4 - 150))


    def dessine_barre_de_vie(self, surface : Surface, pos_x : int, pos_y : int) -> None:
        dessine_barre_de_vie(surface, pos_x, pos_y, self._stats.vie / self._stats.vie_max, self.longueur_barre_de_vie())
    
    def dessiner_attaque(self, surface : Surface, clef_attaque : str, crit : bool) -> None:
        assert(clef_attaque in self.get_moveset_clefs())
        
        self._moveset[clef_attaque].dessiner(surface, 400, 300, crit)
        pygame.display.flip()
        attendre(1)
    
    def est_mort(self) -> bool:
        return self._stats.est_mort()


joueur : Joueur = Joueur({
    "heal":     ATTAQUES_DISPONIBLES["heal"],
    "physique": ATTAQUES_DISPONIBLES["physique"],
    "magie":    ATTAQUES_DISPONIBLES["magie"],
    "skip":     ATTAQUES_DISPONIBLES["skip"],
}, chemin_vers_sprite=f"{CHEMIN_DOSSIER_IMG}/joueur_placeholder.png")