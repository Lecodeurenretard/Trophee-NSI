from Stat import *
from import_var import *

class TypeAttaque(Enum):
    """Tous les types d'attaques disponibles."""
    PHYSIQUE = auto(),
    MAGIQUE  = auto(),
    SOIN     = auto(),
    DIVERS   = auto(),

class EffetAttaque:
    pass        # TODO: définir les effets des attaques (poison, confus, ...) (un jour)

class Attaque:
    _PUISSANCE_CRIT : float = 1.5   # de combien doit le crit influencer l'attaque
    
    toujours_crits : bool = False   # ne pas activer ici, utiliser les touches du mode debug plutôt
    CRIT_IMG : Surface = pygame.transform.scale(    # rétrécit l'image pour être en 20x20
        pygame.image.load(f"{CHEMIN_DOSSIER_IMG}/crit.png"),
        (40, 40)
    )
    def __init__(
            self,
            nom : str,
            desc : str,
            puissance : float,
            type_attaque : TypeAttaque,
            crit_proba : float = .1,
            peut_toucher_amis    : bool = False,
            peut_toucher_ennemis : bool = True,
        ):
        self._nom    : str = nom
        self._desc   : str = desc
        self._puissance : float = puissance
        self._type_attaque : TypeAttaque = type_attaque

        assert(0 <= crit_proba <= 1), "Les probabilités se calculent sur [0; 1]."
        self._prob_crit  : float = crit_proba
        
        # Sera un bitmask (flags) si plusieurs effets peuvent être appliqués en même temps
        # sinon une enum normale
        self._effet : EffetAttaque
        
        self._friendly_fire = peut_toucher_amis
        self._ennemy_fire = peut_toucher_ennemis
        
        self._nom_surf : Surface = POLICE_TITRE.render(nom, True, BLANC)  # Le nom de l'attaque rendered
        
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
            + f"nom: {self._nom}; "
            + f"desc: {self._desc}; "
            + f"puissance: {self._puissance}; "
            + f"type: {self._type_attaque}"
            + "}"
        )
    
    def __eq__(self, attaque: 'Attaque') -> bool:
        return self._nom == attaque._nom
    # l'opérateur != (méthode .__ne__()), est par défaut défini comme l'inverse de ==

    @property
    def puissance(self) -> float:
        return self._puissance
    
    @property
    def desc(self) -> str:
        return self._desc
    
    @property
    def nom_surface(self) -> Surface:
        return self._nom_surf
    
    @property
    def friendly_fire(self) -> bool:
        return self._friendly_fire
    
    @property
    def ennemy_fire(self) -> bool:
        return self._ennemy_fire
    
    def calculer_degats(self, stats_attaquant : 'Stat', stats_victime : 'Stat', defense_min = 10) -> tuple[int, bool]:
        """
        Calcule les dégats qu'aurait causé l'attaque pour les paramètres donnés.  
        Renvoie une tuple contenant les dégats infligés et si un crit s'est passé.
        """
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
                degats = 0
            
            case _:
                raise ValueError("type_degat n'est pas un membre de TypeAttaque dans Attaque.calculer_degats.")
        
        crit : bool = Attaque.toujours_crits or (random.random() < self._prob_crit)
        if crit:
            crit_facteur : float = stats_attaquant.crit_puissance / stats_victime.crit_resitance
            degats *= Attaque._PUISSANCE_CRIT * crit_facteur
        return (round(degats), crit)

    def dessiner(self, surface : Surface, pos_x: int, pos_y: int, crit : bool = False) -> None:
        RECT_LARGEUR = 200
        RECT_HAUTEUR = 50
        
        pygame.draw.rect(fenetre, self._couleur, (pos_x, pos_y , RECT_LARGEUR, RECT_HAUTEUR), 5)
        surface.blit(self._nom_surf, (pos_x + 10, pos_y + 10))
        
        if crit:
            # Dessine l'image de crit
            surface.blit(Attaque.CRIT_IMG,
                (
                    pos_x + RECT_LARGEUR/2 - Attaque.CRIT_IMG.get_width()/2, # on centre l'étoile
                    pos_y + RECT_HAUTEUR/2 - Attaque.CRIT_IMG.get_height()/2,
                )
            )

ATTAQUES_DISPONIBLES : dict[str, Attaque] = {
    "heal":     Attaque("Soin", "Soignez-vous de quelques PV", 1.5, TypeAttaque.SOIN, crit_proba=.2, peut_toucher_amis=True),
    "magie":    Attaque("Att. magique", "Infligez des dégâts magique à l'adversaire", 45-10, TypeAttaque.MAGIQUE),
    "physique": Attaque("Torgnole", "Infligez des dégâts physiques à l'adversaire", 20, TypeAttaque.PHYSIQUE),
    "skip":     Attaque("Passer", "Passez votre tour.", 0, TypeAttaque.DIVERS, crit_proba=.3,peut_toucher_amis=False, peut_toucher_ennemis=False)   # ça sert à rien d'augmenter la chance de crit mais ¯\_(ツ)_/¯ funny
}