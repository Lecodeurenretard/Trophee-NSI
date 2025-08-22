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
    
    CRIT_IMG : Surface = pygame.transform.scale(    # rétrécit l'image pour être en 20x20
        pygame.image.load(f"{CHEMIN_DOSSIER_IMG}/crit.png"),
        (40, 40)
    )
    
    toujours_crits : bool = False   # ne pas activer ici, utiliser les touches du mode debug plutôt
    attaques_du_tour : PriorityQueue['AttaquePriorisee'] = PriorityQueue(MAXIMUM_ENTITES_SIMULTANEES)
    
    
    def __init__(
            self,
            nom : str,
            desc : str,
            puissance : float,
            vitesse : int,
            type_attaque : TypeAttaque,
            crit_proba : float = .1,
            flags : AttaqueFlags = AttaqueFlags.ATTAQUE_ENNEMIS,
            dernier_changements : Callable[[float, bool], int] = (lambda degats, crit: round(degats)),
        ):
        self._nom    : str = nom
        self._desc   : str = desc
        self._puissance : float = puissance
        self._vitesse : int = vitesse
        
        self._type_attaque : TypeAttaque = type_attaque
        self._lanceur_id : int = -1
        self._cible_id : int = -1
        
        assert(0 <= crit_proba <= 1), "Les probabilités se calculent sur [0; 1] (test du constructeur d'Attaque)."
        self._prob_crit : float = crit_proba
        self._crit      : bool = False
        
        self._effet : EffetAttaque = None   # type: ignore
        self._drapeaux = flags
        
        self._nom_surf : Surface = POLICE_TITRE.render(nom, True, BLANC)  # Le nom de l'attaque rendered
        
        self._ajustement_degats = dernier_changements
    
    def __eq__(self, attaque: 'Attaque') -> bool:
        return self._nom == attaque._nom
    # l'opérateur != (méthode .__ne__()), est par défaut défini comme l'inverse de ==
    
    @property
    def _couleur(self) -> color:
        return self._type_attaque.couleur
    
    @property
    def dbg_str(self) -> str:
        return (
            "Attaque{"
            + f"nom: {self._nom}; "
            + f"desc: {self._desc}; "
            + f"puissance: {self._puissance}; "
            + f"type: {self._type_attaque}"
            + f"lanceur: {self._lanceur_id}"
            + f"cible: {self._cible_id}"
            + f"somme des flags: {self._drapeaux.value}"
            + "}"
        )
    
    @property
    def _lanceur(self): # -> Joueur|Monstre
        assert(globales.entites_vivantes[self._lanceur_id] is not None), f"L'ID du lanceur est incorrecte dans la propriété ._lanceur de l'attaque {self.dbg_str}."
        
        return globales.entites_vivantes[self._lanceur_id]
    
    @property
    def _cible(self): # -> Joueur|Monstre
        assert(globales.entites_vivantes[self._cible_id] is not None), f"L'ID de la cible est incorrecte dans la propriété ._lanceur de l'attaque {self.dbg_str}."
        
        return globales.entites_vivantes[self._cible_id]
    
    @property
    def puissance(self) -> float:
        return self._puissance
    
    @property
    def vitesse(self) -> int:
        return self._vitesse
    
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
    
    @staticmethod
    def lancer_toutes_les_attaques(reset_ecran : Callable[[], None]) -> None:
        if MODE_DEBUG:
            logging.debug("Début du lancement des attaques.")
        while not Attaque.attaques_du_tour.empty():
            attaque : Attaque = Attaque.attaques_du_tour.get_nowait().attaque
            if attaque._lanceur.est_mort():
                return
            
            if MODE_DEBUG:
                logging.debug(f"{attaque._lanceur.dbg_nom} (id: {attaque._lanceur.id}) utilise {attaque._nom} sur {attaque._cible.dbg_nom}")
            
            attaque.appliquer()
            
            reset_ecran()
            time.sleep(.2)
            
            attaque.dessiner(fenetre)
            pygame.display.flip()
            time.sleep(1)
        if MODE_DEBUG:
            logging.debug("Fin du lancement des attaques.")
    
    def _calcul_attaque_defense(self, puissance_attaquant : int, defense_cible : int, def_min : float) -> tuple[float, float]:
        if AttaqueFlags.IGNORE_STATS in self._drapeaux:
            return (self._puissance, 1)
        
        attaque : float = self._puissance * puissance_attaquant
        defense : float = max(def_min, defense_cible)
        return (attaque, defense)
    
    def calculer_degats(self, defense_min = 10) -> int:
        """
        Calcule les dégats qu'aurait causé l'attaque pour les paramètres donnés.  
        Renvoie une tuple contenant les dégats infligés et si un crit s'est passé.
        """
        stats_attaquant : Stat = self._lanceur.stats
        stats_victime : Stat = self._cible.stats
        
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
        
        self._crit = Attaque.toujours_crits or random.random() < self._prob_crit
        if self._crit:
            crit_facteur : float = stats_attaquant.crit_puissance / stats_victime.crit_resitance
            degats *= Attaque._PUISSANCE_CRIT * crit_facteur
        return self._ajustement_degats(degats, self._crit)
    
    def appliquer(self) -> None:
        self._effet     # faire quelque chose avec
        
        if AttaqueFlags.ATTAQUE_LANCEUR not in self._drapeaux and self._lanceur_id == self._cible_id:
            return
        elif AttaqueFlags.ATTAQUE_ALLIES in self._drapeaux and type(self._lanceur) != type(self._cible) and self._lanceur_id != self._cible_id:
            return
        elif AttaqueFlags.ATTAQUE_ENNEMIS in self._drapeaux and type(self._lanceur) == type(self._cible):
            return
        self._cible.recoit_degats(self.calculer_degats())
    
    def dessiner(self, surface : Surface) -> None:
        RECT_LARGEUR = 200
        RECT_HAUTEUR = 50
        
        pos_x : int = self._lanceur.pos_attaque_x
        pos_y : int = self._lanceur.pos_attaque_y
        
        pygame.draw.rect(fenetre, self._couleur, (pos_x, pos_y , RECT_LARGEUR, RECT_HAUTEUR), 5)
        surface.blit(self._nom_surf, (pos_x + 10, pos_y + 10))
        
        if self._crit:
            # Dessine l'image de crit
            surface.blit(
                Attaque.CRIT_IMG,
                (
                    pos_x + RECT_LARGEUR / 2 - Attaque.CRIT_IMG.get_width() / 2, # on centre l'étoile
                    pos_y + RECT_HAUTEUR / 2 - Attaque.CRIT_IMG.get_height() / 2,
                )
            )
    
    def enregister_lancement(self, id_lanceur : int, id_cible : int, flags_a_ajouter : AttaqueFlags = AttaqueFlags.AUCUN) -> None:
        copie : Attaque = copy(self)
        copie._cible_id = id_cible
        copie._lanceur_id = id_lanceur
        copie._drapeaux |= flags_a_ajouter
        
        Attaque.attaques_du_tour.put_nowait(AttaquePriorisee(copie, self._lanceur.stats.vitesse))

class AttaquePriorisee:
    """Classe permettant de classer les attaques pour pouvoir déterminer leur ordre d'application."""
    def __init__(self, attaque : Attaque, vitesse_lanceur : float):
        self.attaque = attaque
        self._score = AttaquePriorisee._calcul_score(attaque.vitesse, vitesse_lanceur)
    
    @staticmethod
    def _calcul_score(vitesse_attaque : float, vitesse_lanceur : float) -> float:
        if vitesse_attaque < 0 or vitesse_lanceur < 0:
            return VITESSE_MAXIMUM
        
        # Visualisez et essayez les modification de la formule ici: https://www.desmos.com/3D/332drqdeup
        # Les seules restrictions sont que la fonction doit être strictement décroissante pour vitesse_attaque et vitesse_joueur.
        return -max(0, min(VITESSE_MAXIMUM, 1.2 * vitesse_attaque + 1.0 * vitesse_lanceur))
    
    # les opérateurs strictement inférieur et strictement supérieur à
    # Ils sont surchargés pour que l'objet soit classé dans PriorityQueue
    def __lt__(self, other : 'AttaquePriorisee') -> bool:
        return self._score < other._score
    def __gt__(self, other : 'AttaquePriorisee') -> bool:
        return self._score > other._score


ATTAQUES_DISPONIBLES : dict[str, Attaque] = {
    "heal": Attaque(
        "Soin", "Soignez-vous de quelques PV",
        1.5,
        1000,
        TypeAttaque.SOIN,
        crit_proba=.2, flags=AttaqueFlags.ATTAQUE_EQUIPE
    ),
    "magie": Attaque(
        "Att. magique", "Infligez des dégâts magique à l'adversaire",
        25,
        20,
        TypeAttaque.MAGIQUE
    ),
    "physique": Attaque(
        "Torgnole", "Infligez des dégâts physiques à l'adversaire",
        20,
        30,
        TypeAttaque.PHYSIQUE
    ),
    "skip": Attaque(
        "Passer", "Passez votre tour.",
        0,
        -1,
        TypeAttaque.DIVERS,
        crit_proba=.5, flags=AttaqueFlags.AUCUN   # ça sert à rien d'augmenter la chance de crit mais ¯\_(ツ)_/¯ funny
    ),
}