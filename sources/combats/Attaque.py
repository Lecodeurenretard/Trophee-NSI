from Stat import *
from import_var import *

class TypeAttaque(Enum):
    """Tous les types d'attaques disponibles."""
    PHYSIQUE = auto(),
    MAGIQUE  = auto(),
    SOIN     = auto(),
    CHARGE   = auto(),
    DIVERS   = auto(),

    @property
    def couleur(self) -> color:
        match self:
            case TypeAttaque.PHYSIQUE:
                return ROUGE
            
            case TypeAttaque.MAGIQUE:
                return BLEU
            
            case TypeAttaque.SOIN:
                return VERT
            
            case TypeAttaque.DIVERS:
                return NOIR
            
            case _:
                raise NotImplementedError("Type d'attaque non implémenté dans TypeAttaque.couleur().")


# Sera un bitmask (flags) si plusieurs effets peuvent être appliqués en même temps
# sinon une enum normale
class EffetAttaque:
    pass        # TODO: définir les effets des attaques (poison, confus, ...) (un jour)

class AttaqueFlags(IntFlag):
    """Des particularités que pourraient avoir les attaques"""
    AUCUN               = 0
    IGNORE_STATS        = auto()    # Ignore l'attaque et la défense
    
    ATTAQUE_LANCEUR     = auto()    # Peut attaquer le lanceur
    ATTAQUE_ALLIES      = auto()    # Peut attaquer les alliés du lanceur
    ATTAQUE_ENNEMIS     = auto()    # Peut attaquer les adversaires du lanceur
    ATTAQUE_EQUIPE = ATTAQUE_LANCEUR | ATTAQUE_ALLIES # Si le joueur peut attaquer son équipe ou lui même.

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
            flags : AttaqueFlags = AttaqueFlags.ATTAQUE_ENNEMIS
        ):
        self._nom    : str = nom
        self._desc   : str = desc
        self._puissance : float = puissance
        self._type_attaque : TypeAttaque = type_attaque

        assert(0 <= crit_proba <= 1), "Les probabilités se calculent sur [0; 1] (test du constructeur d'Attaque)."
        self._prob_crit  : float = crit_proba
        self._effet : EffetAttaque
        
        self._drapeaux = flags
        
        self._nom_surf : Surface = POLICE_TITRE.render(nom, True, BLANC)  # Le nom de l'attaque rendered
    
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
    def _couleur(self) -> color:
        return self._type_attaque.couleur
    
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
        return  AttaqueFlags.ATTAQUE_EQUIPE in self._drapeaux
    
    @property
    def ennemy_fire(self) -> bool:
        return AttaqueFlags.ATTAQUE_ENNEMIS in self._drapeaux
    
    def _calcul_attaque_defense(self, puissance_attaquant : int, defense_cible : int, def_min : float) -> tuple[float, float]:
        if AttaqueFlags.IGNORE_STATS in self._drapeaux:
            return (self._puissance, 1)
        
        attaque : float = self._puissance * puissance_attaquant
        defense : float = max(def_min, defense_cible)
        return (attaque, defense)

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
                attaque, defense = self._calcul_attaque_defense(
                    stats_attaquant.force,
                    stats_victime.defense,
                    defense_min
                )
                degats *= attaque / defense

            case TypeAttaque.MAGIQUE:
                attaque, defense = self._calcul_attaque_defense(
                    stats_attaquant.magie,
                    stats_victime.defense_magique,
                    defense_min
                )
                degats *= attaque / defense

            case TypeAttaque.SOIN:
                attaque : float = self._puissance * stats_attaquant.magie
                degats *= -attaque
            
            case TypeAttaque.DIVERS:
                ...
            
            case _:
                raise ValueError("type_degat n'est pas un membre de TypeAttaque dans Attaque.calculer_degats.")
        
        crit : bool = Attaque.toujours_crits or random.random() < self._prob_crit
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
            surface.blit(
                Attaque.CRIT_IMG,
                (
                    pos_x + RECT_LARGEUR / 2 - Attaque.CRIT_IMG.get_width() / 2, # on centre l'étoile
                    pos_y + RECT_HAUTEUR / 2 - Attaque.CRIT_IMG.get_height() / 2,
                )
            )

ATTAQUES_DISPONIBLES : dict[str, Attaque] = {
    "heal": Attaque(
        "Soin", "Soignez-vous de quelques PV",
        1.5,
        TypeAttaque.SOIN,
        crit_proba=.2, flags=AttaqueFlags.ATTAQUE_EQUIPE
    ),
    "magie": Attaque(
        "Att. magique", "Infligez des dégâts magique à l'adversaire",
        20,
        TypeAttaque.MAGIQUE
    ),
    "physique": Attaque(
        "Torgnole", "Infligez des dégâts physiques à l'adversaire",
        20,
        TypeAttaque.PHYSIQUE
    ),
    "skip": Attaque(
        "Passer", "Passez votre tour.",
        0,
        TypeAttaque.DIVERS,
        crit_proba=.5, flags=AttaqueFlags.AUCUN   # ça sert à rien d'augmenter la chance de crit mais ¯\_(ツ)_/¯ funny
    ),
}