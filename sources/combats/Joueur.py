from dessin import *
from fonctions_vrac import *
from Attaque import *

class Joueur:
    _STATS_DE_BASE : Stat = Stat(
        45,
        35, 35,
        20, 30,
        50,
        1.2, 1,
    )
    est_invincible : bool = False
    dimensions_sprite : tuple[int, int] = (160, 160)
    
    def __init__(self, moveset : dict[str, Attaque], chemin_vers_sprite : str|None = None) -> None:
        # on assumera que _stats et _base_stats sont initialisés
        self._stats : Stat = Joueur._STATS_DE_BASE
        self._pseudo : str = ""
        self._moveset = deepcopy(moveset)
        
        self._id = premier_indice_libre_de_entites_vivantes()
        if self._id >= 0:
            entites_vivantes[self._id] = self
            return
        
        if chemin_vers_sprite is not None:
            self._sprite  : Surface|None = pygame.transform.scale(pygame.image.load(chemin_vers_sprite), Joueur.dimensions_sprite)
        else:
            self._sprite : Surface|None = None
        
        self._id = len(entites_vivantes)
        entites_vivantes.append(self)
    
    def __del__(self):
        # Appelé quand l'objet est détruit (plus utilisé ou détruit avec del())
        if self._id > 0 and entites_vivantes is not None:
            self.meurt()
    
    # meurt est ici car il n'est appelé que dans __del__()
    def meurt(self) -> None:
        entites_vivantes[self._id] = None
        self._id = -1
    
    @property
    def id(self) -> int:
        return self._id

    @property
    def pseudo(self) -> str:
        return self._pseudo
    
    @property
    def moveset_clefs(self) -> tuple[str, ...]:
        return tuple(self._moveset.keys())
    
    @property
    def stats(self) -> Stat:
        return self._stats
    
    @pseudo.setter
    def pseudo(self, value : str) -> None:
        self._pseudo = value
    
    def get_attaque_surface(self, clef_attaque : str) -> Surface:
        assert(clef_attaque in self.moveset_clefs)
        return self._moveset[clef_attaque].nom_surface
    
    def attaque_peut_toucher_allies(self, attaque_clef : str) -> bool:
        assert(attaque_clef in self.moveset_clefs), "Attaque pas inclue dans moveset dans attaque_peut_toucher_allies()."
        
        return self._moveset[attaque_clef].friendly_fire
    
    def attaque_peut_toucher_ennemis(self, attaque_clef : str) -> bool:
        assert(attaque_clef in self.moveset_clefs), "Attaque pas inclue dans moveset dans attaque_peut_toucher_ennemis()."
        
        return self._moveset[attaque_clef].enemy_fire
    
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

    def subir_attaque(self, attaque : Attaque, stats_attaquant : Stat) -> None:
        """
        Prend en charge l'attaque prise et retourne une tuple contenant s'il y a eu un crit..
        """
        assert(stats_attaquant.est_initialise), "stats_monstre pas initialisé dans Joueur.essuyer_attaque()."
        assert(attaque.cible_id == -1 or attaque.cible_id == self._id), f"L'attaque n'est pas dirigée vers l'entité id {self.id} mais vers celle id {attaque.cible_id}."
        attaque.cible_id = self.id

        degats = attaque.calculer_degats(stats_attaquant)
        self.recoit_degats(degats)
    
    def attaquer(self, id_cible : int, clef_attaque : str) -> None:
        assert(entites_vivantes[id_cible] is not None), "La cible est None dans Joueur.attaquer()."
        assert(clef_attaque in self.moveset_clefs)
        
        attaque : Attaque = self._moveset[clef_attaque]
        attaque.cible_id = id_cible
        
        if attaque.friendly_fire:                                 # si friendly fire, se tape lui même
            attaque.inserer_dans_liste_attaque(self._id)          # TODO: il faudra ajouter un curseur pour choisir la cible
            return
        if attaque.enemy_fire:
            attaque.inserer_dans_liste_attaque(id_cible)
            return
    
    def dessiner(self, surface : Surface) -> None:
        if MODE_DEBUG:
            boite_de_contours = (LARGEUR // 4, pourcentage_hauteur(75) - 100, 100, 100)
            pygame.draw.rect(surface, BLEU, boite_de_contours, 0)
            return
        
        if self._sprite is not None:
            surface.blit(self._sprite, (LARGEUR // 4, pourcentage_hauteur(75) - 150))


    def dessine_barre_de_vie(self, surface : Surface, pos_x : int, pos_y : int) -> None:
        dessine_barre_de_vie(surface, pos_x, pos_y, self._stats.vie / self._stats.vie_max, self.longueur_barre_de_vie())
    
    def dessiner_attaque(self, surface : Surface, attaque : str|Attaque) -> None:
        if type(attaque) is str:
            assert(attaque in self.moveset_clefs), f"L'argument `attaque` de Joueur.dessiner_attaque() n'est pas une clef du moveset de l'entitée d'ID {self._id}."
            attaque = self._moveset[attaque]
        elif type(attaque) is Attaque:
            assert(attaque in self._moveset.values()), f"L'argument `attaque` de Joueur.dessiner_attaque() n'est pas dans le moveset de l'entitée d'ID {self._id}."
        else:
            raise TypeError(f"L'argument `attaque` de doit être de type str ou Attaque mais est de type {type(attaque)}.")
        
        attaque.dessiner(surface, 400, 300)
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