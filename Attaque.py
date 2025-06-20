from Stats import *
from import_var import *

class TypeAttaque(Enum):
    """Tous les types d'attaques disponibles."""
    PHYSIQUE = auto(),
    MAGIQUE  = auto(),
    SOIN     = auto(),
    DIVERS   = auto(),

class Effet:
    pass        # TODO: définir les effets des attaques (poison, confus, ...) (un jour)

class Attaque:
    def __init__(
            self,
            nom : str,
            desc : str,
            puissance : float,
            type_attaque : TypeAttaque,
            peut_toucher_amis    : bool = False,
            peut_toucher_ennemis : bool = True,
        ):
        self._nom    : str = nom
        self._desc   : str = desc
        self._puissance : float = puissance
        self._type_attaque : TypeAttaque = type_attaque
        
        # Sera un bitmask si plusieurs effets peuvent être appliqués en même temps
        # sinon une enum
        self._effet : Effet
        
        self._friendly_fire = peut_toucher_amis
        self._ennemy_fire = peut_toucher_ennemis
        
        self._nom_surf : pygame.Surface = POLICE_GRAND.render(nom, True, BLANC)  # Le nom de l'attaque rendered
        
        match self._type_attaque:
            case TypeAttaque.PHYSIQUE:
                self._couleur = ROUGE
            
            case TypeAttaque.MAGIQUE:
                self._couleur = BLEU
            
            case TypeAttaque.SOIN:
                self._couleur = VERT
            
            case TypeAttaque.DIVERS:
                self._couleur = NOIR
            
            case _:
                raise ValueError("type_attaque n'est pas un membre de TypeAttaque dans Attaque.__init__().")

    def __str__(self):
        return (
            "Attaque{"
            + f"nom: {self._nom};"
            + f"dégâts: {self._puissance};"
            + f"type: {self._type_attaque}"
            + "}"
        )
    
    def __eq__(self, attaque: 'Attaque') -> bool:
        return self._nom == attaque._nom
    def __ne__(self, attaque: 'Attaque') -> bool:
        return not self == attaque
    
    def get_puissance(self) -> float:
        return self._puissance
    def get_desc(self) -> str:
        return self._desc
    def get_nom_surface(self) -> pygame.Surface:
        return self._nom_surf
    def get_friendly_fire(self) -> bool:
        return self._friendly_fire
    def get_ennemy_fire(self) -> bool:
        return self._ennemy_fire
    
    def calculer_degats(self, stats_attaquant : 'Stat', stats_victime : 'Stat', defense_min = 10) -> int:
        assert(stats_attaquant.est_initialise), "stat_attaquant n'est pas initialisé dans Stat.calculer_degats()"
        assert(stats_victime.est_initialise), "stat_victime n'est pas initialisé dans Stat.calculer_degats()"
        
        degats : float = random.uniform(0.85, 1.0)
        match self._type_attaque:
            case TypeAttaque.PHYSIQUE:
                attaque = self._puissance * stats_attaquant.force
                defense = max(defense_min, stats_victime.defense)
                
                degats *= attaque / defense
            
            case TypeAttaque.MAGIQUE:
                attaque = self._puissance * stats_attaquant.magie
                defense = max(defense_min, stats_victime.defense_magique)
                
                degats *= attaque / defense
            
            case TypeAttaque.SOIN:
                attaque = self._puissance * stats_attaquant.magie
                degats *= -attaque
            
            case TypeAttaque.DIVERS:
                pass
            
            case _:
                raise ValueError("type_degat n'est pas un membre de TypeAttaque dans Attaque.calculer_degats.")
        return round(degats)

    def dessiner(self, surface : pygame.Surface, pos_x: int, pos_y: int) -> None:
        pygame.draw.rect(fenetre, self._couleur, (pos_x, pos_y , 200, 50), 5)
        surface.blit(self._nom_surf, (pos_x + 10, pos_y + 10))

ATTAQUES_DISPONIBLES : dict[str, Attaque] = {
    "heal":     Attaque("Soin", "Soignez-vous de quelques PV", 1.5, TypeAttaque.SOIN, peut_toucher_amis=True),
    "magie":    Attaque("Att. magique", "Infligez des dégâts magique à l'adversaire", 45-10, TypeAttaque.MAGIQUE),
    "physique": Attaque("Torgnole", "Infligez des dégâts physiques à l'adversaire", 20, TypeAttaque.PHYSIQUE),
    "skip":     Attaque("Passer", "Passez votre tour.", 0, TypeAttaque.DIVERS, peut_toucher_amis=False, peut_toucher_ennemis=False)
}