from dessin import *
from fonctions_vrac import *
from Attaque import *

class Joueur:
    _STATS_DE_BASE : Stat = Stat(45, 35, 40-5, 20, 30, 50, 1.2, 1).reset_vie()
    DIMENSIONS_SPRITE : tuple[int, int] = (160, 160)
    
    def __init__(self, moveset : dict[str, Attaque], chemin_vers_sprite : str|None = None) -> None:
        # on assumera par la suite que _stats et _base_stats sont initialisés
        self._stats : Stat = Joueur._STATS_DE_BASE
        self._pseudo : str = ""
        self._moveset = moveset
        
        self._id = premier_indice_libre_de_entites_vivantes()
        if self._id >= 0:
            globales.entites_vivantes[self._id] = self
            return
        
        if chemin_vers_sprite is not None:
            self._sprite  : Surface|None = pygame.transform.scale(pygame.image.load(chemin_vers_sprite), Joueur.DIMENSIONS_SPRITE)
        else:
            self._sprite : Surface|None = None
        
        self._id = len(globales.entites_vivantes)
        globales.entites_vivantes.append(self)
    
    def __del__(self):
        # Appelé quand l'objet est détruit (plus utilisé ou détruit avec del())
        if self._id > 0 and globales.entites_vivantes is not None:
            self.meurt()
    
    @property
    def pseudo(self) -> str:
        return self._pseudo
    @property
    def dbg_nom(self) -> str:
        return self.pseudo
    
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def stats(self) -> Stat:
        return copy(self._stats)
    
    @property
    def moveset_clefs(self) -> tuple[str, ...]:
        return tuple(self._moveset.keys())
    
    @property
    def longueur_barre_de_vie(self) -> int:
        ratio = max(0, self._stats.vie / self._stats.vie_max)
        return round(ratio * UI_LONGUEUR_BARRE_DE_VIE)
    
    # propriété car la position pourrait changer suivant la position du ou des joueurs
    @property
    def pos_attaque_x(self) -> int:
        return 400
    @property
    def pos_attaque_y(self) -> int:
        return 300
    
    @property
    def pos_curseur_x(self) -> int:
        return 0
    @property
    def pos_curseur_y(self) -> int:
        return 0
    
    @pseudo.setter
    def pseudo(self, value : str) -> None:
        self._pseudo = value
    
    def recoit_degats(self, degats_recu : int) -> bool:
        """Prend en charge les dégats prits et retourne si un crit est retourné."""
        if bool(param.joueur_invincible) and degats_recu >= 0:   # joueur_invincible n'empèche pas les soins
            return False
        
        self._stats.baisser_vie(degats_recu)
        return self.est_mort()
    
    def meurt(self) -> None:
        globales.entites_vivantes[self._id] = None
        self._id = -1
    
    def get_attaque_surface(self, clef_attaque : str) -> Surface:
        assert(clef_attaque in self.moveset_clefs)
        return self._moveset[clef_attaque].nom_surface
    
    def attaque_peut_toucher_allies(self, clef_attaque : str) -> bool:
        assert(clef_attaque in self.moveset_clefs), "Attaque pas inclue dans moveset dans attaque_peut_toucher_allies()."
        
        return self._moveset[clef_attaque].friendly_fire
    
    def attaque_peut_toucher_ennemis(self, clef_attaque : str) -> bool:
        assert(clef_attaque in self.moveset_clefs), "Attaque pas inclue dans moveset dans attaque_peut_toucher_ennemis()."
        
        return self._moveset[clef_attaque].ennemy_fire
    
    def reset_vie(self) -> None:
        self._stats.vie = self._stats.vie_max
    
    def attaquer(self, id_cible : int, clef_attaque : str) -> None:
        assert(clef_attaque in self.moveset_clefs)
        
        if self._moveset[clef_attaque].friendly_fire:
            id_cible = self.id
        self._moveset[clef_attaque].enregister_lancement(self._id, id_cible)
    
    def dessiner(self, surface : Surface) -> None:
        if param.mode_debug.case_cochee:
            boite_de_contours = (LARGEUR // 4, pourcentage_hauteur(75) - 100, 100, 100)
            pygame.draw.rect(surface, BLEU, boite_de_contours, 0)
            return
        
        if self._sprite is not None:
            blit_centre(surface, self._sprite, (LARGEUR // 4, pourcentage_hauteur(60)))
    
    
    def dessine_barre_de_vie(self, surface : Surface, pos_x : int, pos_y : int) -> None:
        dessiner_barre_de_vie(surface, pos_x, pos_y, self._stats.vie / self._stats.vie_max, self.longueur_barre_de_vie)
    
    def est_mort(self) -> bool:
        return self._stats.est_mort()


joueur : Joueur = Joueur({
    "heal":     ATTAQUES_DISPONIBLES["heal"],
    "physique": ATTAQUES_DISPONIBLES["physique"],
    "magie":    ATTAQUES_DISPONIBLES["magie"],
    "skip":     ATTAQUES_DISPONIBLES["skip"],
}, chemin_vers_sprite=f"{CHEMIN_DOSSIER_IMG}/joueur_placeholder.png")