from import_local import *

class TypeAttaque(Enum):
    """Tous les types d'attaques disponibles."""
    PHYSIQUE = auto(),
    MAGIQUE  = auto(),
    SOIN     = auto(),
    CHARGE   = auto(),
    DIVERS   = auto(),
    
    @staticmethod
    def depuis_str(s : str) -> 'TypeAttaque':
        match s.strip().lower():
            case "physique":
                return TypeAttaque.PHYSIQUE
            case "magique":
                return TypeAttaque.MAGIQUE
            case "soin":
                return TypeAttaque.SOIN
            case "charge":
                return TypeAttaque.CHARGE
            case "divers":
                return TypeAttaque.DIVERS
            case _:
                raise ValueError(f'La valeur "{s}" ne renvoie à aucun type d\'attaque.')


# Sera une enum (1 seul effet par attaque)
class EffetAttaque:
    pass        # TODO: définir les effets des attaques (poison, confus, ...) (un jour)

class AttaqueFlag(Flag):
    """Des particularités que pourraient avoir les attaques"""
    AUCUN               = 0
    IGNORE_DEFENSE      = auto()
    IGNORE_STATS        = auto()
    
    ATTAQUE_LANCEUR     = auto()
    ATTAQUE_ENNEMIS     = auto()
    
    @staticmethod
    def depuis_liste(lst : list[str]) -> 'AttaqueFlag':
        res : AttaqueFlag = AttaqueFlag.AUCUN
        for flag in lst:
            match flag.strip().lower():
                case "ignore defense":
                    res |= AttaqueFlag.IGNORE_DEFENSE
                case "ignore stats":
                    res |= AttaqueFlag.IGNORE_STATS
                case "cible lanceur":
                    res |= AttaqueFlag.ATTAQUE_LANCEUR
                case "cible ennemis" | "cible adversaire":
                    res |= AttaqueFlag.ATTAQUE_ENNEMIS
                case _:
                    raise ValueError(f'Drapeau inconnu "{flag}".')
        
        return res

class Attaque:
    _PUISSANCE_CRIT       : float = 1.3
    
    _ajustements_t : TypeAlias = Callable[[float, bool], int]
    _AJUSTEMENTS : dict[str, _ajustements_t] = {
        "base": (lambda degats, crit: round(degats)),
    }
    
    _DEFAUT_PROB_CRIT  : float        = .1
    _DEFAUT_FLAGS      : AttaqueFlag  = AttaqueFlag.ATTAQUE_ENNEMIS
    _DEFAUT_AJUSTEMENT : _ajustements_t = _AJUSTEMENTS["base"]
    
    _liste : list[dict] = []
    toujours_crits : bool = False   # ne pas activer ici, utiliser les touches du mode debug plutôt
    attaques_jouees : list['Attaque'] = []
    
    def __init__(self, id : int):
        # Définitions de l'id
        self._id = id
        
        donnees_attaque : dict = Attaque._liste[id]
        
        # Définitions des valeurs non null dans le JSON
        self._nom       : str   = donnees_attaque["nom"]
        self._puissance : float = donnees_attaque["puissance"]
        self._type      : TypeAttaque = TypeAttaque.depuis_str(
            donnees_attaque["type"]
        )
        
        # Définitions des id du lanceur/cible.
        self._lanceur_id : int = -1
        self._cible_id : int = -1
        
        # Définition de l'effet infligé par l'attaque.
        self._effet : EffetAttaque = NotImplemented
        
        # Définitions des valeurs potentiellement null (None) dans le JSON
        self._prob_crit : float = valeur_par_defaut(
            donnees_attaque["probabilité_crit"],
            Attaque._DEFAUT_PROB_CRIT,
        )
        
        assert(0 <= self._prob_crit <= 1), "Les probabilités se calculent sur [0; 1]."
        self._crit      : bool = False
        
        if donnees_attaque["flags"] is None:
            self._drapeaux : AttaqueFlag = Attaque._DEFAUT_FLAGS
        else:
            self._drapeaux : AttaqueFlag = AttaqueFlag.depuis_liste(
                donnees_attaque["flags"]
            )
        
        nom_ajustement : Optional[str] = donnees_attaque["nom_ajustement"]
        self._ajustement_degats = valeur_par_defaut(
            Attaque._AJUSTEMENTS.get(nom_ajustement),   # type: ignore
            Attaque._DEFAUT_AJUSTEMENT,
        )
    
    def __eq__(self, attaque: 'Attaque') -> bool:
        return self._nom == attaque._nom
    # l'opérateur != (méthode .__ne__()), est par défaut défini comme l'inverse de ==
    
    def __repr__(self) -> str:
        return (
            "Attaque("
            + f"nom={self._nom}, "
            + f"puissance={self._puissance}, "
            + f"type={self._type.name}, "
            + f"ID lanceur: {self._lanceur_id}, "
            + f"ID cible: {self._cible_id}, "
            + f"somme des flags: {self._drapeaux.value}, "
            + ")"
        )
    
    @staticmethod
    def set_liste(lst : list[dict]) -> None:
        Attaque._liste = lst    
    
    @staticmethod
    def avec_nom(nom : str) -> 'Attaque':
        """Cherche l'attaque avec le nom correspondant dans _liste."""
        return Attaque(
            [att["nom"] for att in Attaque._liste].index(nom)   # Recherche le nom
        )
    
    @property
    def lanceur(self): # -> Joueur|Monstre
        # https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals
        assert(globales.entites_vivantes[self._lanceur_id] is not None), f"L'ID du lanceur est incorrecte dans la propriété ._lanceur de l'attaque {self!r}."
        
        return globales.entites_vivantes[self._lanceur_id]
    
    @property
    def cible(self): # -> Joueur|Monstre
        assert(globales.entites_vivantes[self._cible_id] is not None), f"L'ID de la cible est incorrecte dans la propriété ._lanceur de l'attaque {self!r}."
        
        return globales.entites_vivantes[self._cible_id]
    
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def nom(self) -> str:
        return self._nom
    
    @property
    def puissance(self) -> float:
        return self._puissance
    
    @property
    def desc(self) -> str:
        return self._desc
    
    @property
    def nom_surface(self) -> Surface:
        return Polices.TITRE.render(self._nom, True, BLANC)
    
    @property
    def peut_attaquer_lanceur(self) -> bool:
        return AttaqueFlag.ATTAQUE_LANCEUR in self._drapeaux
    
    @property
    def peut_attaquer_adversaires(self) -> bool:
        return AttaqueFlag.ATTAQUE_ENNEMIS in self._drapeaux
    
    
    def _calcul_attaque_defense(self, puissance_attaquant : int, defense_cible : int, def_min : float) -> tuple[float, float]:
        if AttaqueFlag.IGNORE_STATS in self._drapeaux:
            return (self._puissance, 1)
        
        attaque : float = self._puissance * puissance_attaquant
        defense : float = max(def_min, defense_cible)
        
        if AttaqueFlag.IGNORE_DEFENSE in self._drapeaux:
            return (attaque, 1)
        return (attaque, defense)
    
    def calculer_degats(self, defense_min = 10) -> int:
        """
        Calcule les dégats qu'aurait causé l'attaque pour les paramètres donnés.  
        Renvoie une tuple contenant les dégats infligés et si un crit s'est passé.
        """
        stats_attaquant : Stat = self.lanceur.stats_totales
        stats_victime : Stat = self.cible.stats_totales
        
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
        
        if self._crit:
            crit_facteur : float = stats_attaquant.crit_puissance / stats_victime.crit_resitance
            crit_facteur = max(1, crit_facteur) # un crit ne doit jamais baisser les dégats de l'attaque
            degats *= Attaque._PUISSANCE_CRIT * crit_facteur
        
        return self._ajustement_degats(degats, self._crit)
    
    def decider_crit(self) -> None:
        self._crit = Attaque.toujours_crits or random.random() < self._prob_crit
    
    def appliquer(self) -> None:
        if AttaqueFlag.ATTAQUE_LANCEUR not in self._drapeaux and self._lanceur_id == self._cible_id:
            return
        elif AttaqueFlag.ATTAQUE_ENNEMIS in self._drapeaux and type(self.lanceur) == type(self.cible):
            return
        elif AttaqueFlag.ATTAQUE_LANCEUR not in self._drapeaux and AttaqueFlag.ATTAQUE_ENNEMIS not in self._drapeaux:
            return
        self.cible.recoit_degats(self.calculer_degats())
    
    def actualiser(self) -> None:
        """Actualise l'objet pour qu'il respecte les valeurs dans le dictionnaire."""
        a_copier = Attaque.avec_nom(self._nom)
        
        self._nom          = a_copier._nom
        self._desc         = a_copier._desc
        self._puissance    = a_copier._puissance
        self._vitesse      = a_copier._vitesse
        
        self._type         = a_copier._type
        # Le lanceur et la cible sont inchangés
        
        self._prob_crit    = a_copier._prob_crit
        # crit reste aussi
        
        self._effet        = a_copier._effet
        self._drapeaux     = a_copier._drapeaux
        
        self._ajustement_degats   = a_copier._ajustement_degats
        self._autoriser_animation = a_copier._autoriser_animation