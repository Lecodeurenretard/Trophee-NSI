from import_local import *
from Stats import Stat

class TypeAttaque(Enum):
    """Tous les types d'attaques disponibles."""
    PHYSIQUE = auto(),
    MAGIQUE  = auto(),
    SOIN     = auto(),
    CHARGE   = auto(),
    DIVERS   = auto(),
    
    @property
    def couleur(self) -> rgb:
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


# Sera un bitmask si plusieurs effets peuvent être appliqués en même temps
# sinon une enum normale
class EffetAttaque:
    pass        # TODO: définir les effets des attaques (poison, confus, ...) (un jour)

class AttaqueFlags(Flag):
    """Des particularités que pourraient avoir les attaques"""
    AUCUN               = 0
    IGNORE_STATS        = auto()
    
    ATTAQUE_LANCEUR     = auto()
    ATTAQUE_ALLIES      = auto()
    ATTAQUE_ENNEMIS     = auto()
    ATTAQUE_EQUIPE = ATTAQUE_LANCEUR | ATTAQUE_ALLIES

class Attaque:
    _PUISSANCE_CRIT       : float = 1.5
    _DUREE_ANIMATION      : Duree = Duree(s=1)
    _DUREE_ENTRE_ATTAQUES : Duree = Duree(s=.5)
    
    CRIT_IMG : Surface = pygame.transform.scale(
        pygame.image.load(f"{Constantes.Chemins.DOSSIER_IMG}/crit.png"),
        (40, 40)
    )
    
    toujours_crits : bool = False   # ne pas activer ici, utiliser les touches du mode debug plutôt
    attaques_du_tour : PriorityQueue['AttaquePriorisee'] = PriorityQueue(Constantes.MAX_ENTITES_SIMULTANEES)
    
    
    def __init__(
            self,
            nom : str,
            desc : str,
            puissance : float,
            vitesse : int,
            type_attaque : TypeAttaque,
            crit_proba : float = .1,
            flags : AttaqueFlags = AttaqueFlags.ATTAQUE_ENNEMIS,
            ajustement_degats : Callable[[float, bool], int] = (lambda degats, crit: round(degats)),
            glisser : bool = True,
        ):
        self._nom    : str = nom
        self._desc   : str = desc
        self._puissance : float = puissance
        self._vitesse : int = vitesse
        
        self._type : TypeAttaque = type_attaque
        self._lanceur_id : int = -1
        self._cible_id : int = -1
        
        assert(0 <= crit_proba <= 1), "Les probabilités se calculent sur [0; 1] (test du constructeur d'Attaque)."
        self._prob_crit : float = crit_proba
        self._crit      : bool = False
        
        self._effet : EffetAttaque = None   # type: ignore
        self._drapeaux = flags
        
        self._ajustement_degats = ajustement_degats
        self._animation = glisser
    
    def __eq__(self, attaque: 'Attaque') -> bool:
        return self._nom == attaque._nom
    # l'opérateur != (méthode .__ne__()), est par défaut défini comme l'inverse de ==
    
    def __repr__(self) -> str:
        return (
            "Attaque("
            + f"nom={self._nom}, "
            + f"desc='{self._desc}', "
            + f"puissance={self._puissance}, "
            + f"vitesse={self._vitesse}, "
            + f"type={self._type.name}, "
            + f"ID lanceur: {self._lanceur_id}, "
            + f"ID cible: {self._cible_id}, "
            + f"somme des flags: {self._drapeaux.value}, "
            + f"Jouer animation: {self._animation}"
            + ")"
        )
    
    @staticmethod
    def lancer_toutes_les_attaques_gen(surface: Surface) -> Generator[None, Optional[bool], None]:
        if param.mode_debug.case_cochee:
            logging.debug("Début du lancement des attaques.")
        
        while not Attaque.attaques_du_tour.empty():
            attaque : Attaque = Attaque.attaques_du_tour.get_nowait().attaque
            if attaque._lanceur.est_mort:
                break
            
            if param.mode_debug.case_cochee:
                logging.debug(f"{attaque._lanceur.dbg_nom} (id: {attaque._lanceur.id}) utilise {attaque._nom} sur {attaque._cible.dbg_nom}.")
            
            debut_attaque : Duree = copy(Jeu.duree_execution)
            fin_attaque   : Duree = debut_attaque + Attaque._DUREE_ANIMATION
            
            skip_attaque : bool = False
            while Jeu.duree_execution < fin_attaque and not skip_attaque:
                if Jeu.duree_execution - debut_attaque == 0:
                    attaque._dessiner(surface, attaque.pos_anim_attaque(0))
                    skip_attaque = bool((yield))
                    continue
                
                pos : Pos = attaque.pos_anim_attaque(
                    (Jeu.duree_execution - debut_attaque) / Attaque._DUREE_ANIMATION
                )
                attaque._dessiner(surface, pos)
                skip_attaque = bool((yield))
            
            attaque.appliquer()
            
            # Pas de attendre() ici, on ne veut pas interrompre la boucle de l'état
            peut_sortir = pause(Attaque._DUREE_ENTRE_ATTAQUES)
            while not next(peut_sortir) and not skip_attaque:
                if (yield):   # None est "falsy", ça veut dire que çaa donnera le même résultat si `sent` est none que s'il était False.
                    break
        
        
        if bool(param.mode_debug):
            logging.debug("Fin du lancement des attaques.")
            logging.debug("")
    
    @property
    def _couleur(self) -> rgb:
        return self._type.couleur
    
    @property
    def _lanceur(self): # -> Joueur|Monstre
        # https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals
        assert(globales.entites_vivantes[self._lanceur_id] is not None), f"L'ID du lanceur est incorrecte dans la propriété ._lanceur de l'attaque {self!r}."
        
        return globales.entites_vivantes[self._lanceur_id]
    
    @property
    def _cible(self): # -> Joueur|Monstre
        assert(globales.entites_vivantes[self._cible_id] is not None), f"L'ID de la cible est incorrecte dans la propriété ._lanceur de l'attaque {self!r}."
        
        return globales.entites_vivantes[self._cible_id]
    
    @property
    def _deplacement(self) -> Deplacement:
        if self._animation:
            return Deplacement(self._lanceur.pos_attaque, self._cible.pos_attaque)
        return Deplacement(
            Pos.milieu(self._lanceur.pos_attaque, self._cible.pos_attaque),
            Pos.milieu(self._lanceur.pos_attaque, self._cible.pos_attaque)
        )
    
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
        return Constantes.Polices.TITRE.render(self._nom, True, BLANC)
    
    @property
    def peut_attaquer_allies(self) -> bool:
        return AttaqueFlags.ATTAQUE_EQUIPE in self._drapeaux
    
    @property
    def peut_attaquer_adversaires(self) -> bool:
        return AttaqueFlags.ATTAQUE_ENNEMIS in self._drapeaux
    
    def _dessiner(self, surface : Surface, position : Pos) -> None:
        RECT_LARGEUR = 200
        RECT_HAUTEUR = 50
        
        pygame.draw.rect(Jeu.fenetre, self._couleur, (position.x, position.y , RECT_LARGEUR, RECT_HAUTEUR), 5)
        
        if self._crit:
            blit_centre(
                surface,
                Attaque.CRIT_IMG,
                (
                    position.x + RECT_LARGEUR // 2, # on centre l'étoile
                    position.y + RECT_HAUTEUR // 2,
                )
            )
    
    def _calcul_attaque_defense(self, puissance_attaquant : int, defense_cible : int, def_min : float) -> tuple[float, float]:
        if AttaqueFlags.IGNORE_STATS in self._drapeaux:
            return (self._puissance, 1)
        
        attaque : float = self._puissance * puissance_attaquant
        defense : float = max(def_min, defense_cible)
        return (attaque, defense)
    
    def pos_anim_attaque(self, t : float) -> Pos:
        """La position de l'attaque pour un temps t. (t = 0 => animation finie à 0%, t = 0.5 => animation finie à 50%, ...)"""
        return self._deplacement.calculer_valeur(t, EasingType.ease_in(EasingType.POLYNOMIAL, 3))
    
    def calculer_degats(self, defense_min = 10) -> int:
        """
        Calcule les dégats qu'aurait causé l'attaque pour les paramètres donnés.  
        Renvoie une tuple contenant les dégats infligés et si un crit s'est passé.
        """
        stats_attaquant : Stat = self._lanceur.stats
        stats_victime : Stat = self._cible.stats
        
        degats : float = random.uniform(0.85, 1.0)
        match self._type:
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
        self._effet     #TODO: faire quelque chose avec
        
        if AttaqueFlags.ATTAQUE_LANCEUR not in self._drapeaux and self._lanceur_id == self._cible_id:
            return
        elif AttaqueFlags.ATTAQUE_ALLIES in self._drapeaux and type(self._lanceur) != type(self._cible) and self._lanceur_id != self._cible_id:
            return
        elif AttaqueFlags.ATTAQUE_ENNEMIS in self._drapeaux and type(self._lanceur) == type(self._cible):
            return
        elif AttaqueFlags.ATTAQUE_LANCEUR not in self._drapeaux and AttaqueFlags.ATTAQUE_ALLIES not in self._drapeaux and AttaqueFlags.ATTAQUE_ENNEMIS not in self._drapeaux:
            return
        self._cible.recoit_degats(self.calculer_degats())
    
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
    
    # les opérateurs strictement inférieur et strictement supérieur à
    # Ils sont surchargés pour que l'objet soit classé dans PriorityQueue
    def __lt__(self, other : 'AttaquePriorisee') -> bool:
        return self._score < other._score
    def __gt__(self, other : 'AttaquePriorisee') -> bool:
        return self._score > other._score
    
    @staticmethod
    def _calcul_score(vitesse_attaque : float, vitesse_lanceur : float) -> float:
        if vitesse_attaque < 0 or vitesse_lanceur < 0:
            return Stat.VITESSE_MAX
        
        # Visualisez et essayez les modification de la formule ici: https://www.desmos.com/3D/332drqdeup
        # Les seules restrictions sont que la fonction doit être strictement décroissante pour vitesse_attaque et vitesse_joueur.
        return -max(0, min(Stat.VITESSE_MAX, 1.2 * vitesse_attaque + 1.0 * vitesse_lanceur))


#TODO: mettre ça dans un module ou un truc du genre
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
        0,
        TypeAttaque.DIVERS,
        crit_proba=.5, flags=AttaqueFlags.AUCUN,   # ça sert à rien d'augmenter la chance de crit mais ¯\_(ツ)_/¯ funny
        glisser=False,
    ),
}