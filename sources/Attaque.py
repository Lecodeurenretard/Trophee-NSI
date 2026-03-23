"""Contient la classe Attaque et les classes associées (TypeAttaque et AttaqueFlag)."""
from import_local import *

class TypeAttaque(Enum):
    """Tous les types d'attaques disponibles."""
    PHYSIQUE = auto(),
    MAGIQUE  = auto(),
    SOIN     = auto(),
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
    _AJUSTEMENT_DEFAUT : _ajustements_t = _AJUSTEMENTS["base"]
    
    _liste          : list[dict]      = []
    _dico_entites   : ListeStable['Entite'] = ListeStable() # sera mis à Entite.vivants() plus tard  # type: ignore
    toujours_crits  : bool            = False   # ne pas activer ici, utiliser les touches du mode debug plutôt
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
        
        # Définition des modifications de stats
        modif_stats_cible = valeur_par_defaut(
            donnees_attaque["Modif stat cible"],
            si_none={"duree": 0},
        )
        modif_stats_lanceur = valeur_par_defaut(
            donnees_attaque["Modif stat lanceur"],
            si_none={"duree": 0},
        )
        
        self._modif_stats_cible_duree : int  = modif_stats_cible["duree"]
        self._modif_stats_cible       : Stat = Stat.depuis_dictionnaire_json(modif_stats_cible, valeur_par_defaut=0)
        
        self._modif_stats_lanceur_duree : int  = modif_stats_lanceur["duree"]
        self._modif_stats_lanceur       : Stat = Stat.depuis_dictionnaire_json(modif_stats_lanceur, valeur_par_defaut=0)
        
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
            Attaque._AJUSTEMENT_DEFAUT,
        )
    
    def __eq__(self, obj : object) -> bool:
        assert(type(obj) is Attaque), "On en peut comparer une attaque qu'avec une autre attaque."
        return self._nom == obj._nom
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
    def set_arr_entites(dico : ListeStable['Entite']) -> None: # pyright: ignore[reportUndefinedVariable]
        """Met le tableau `Attaque._dico_entites` à une référence de `dico`."""
        Attaque._dico_entites = dico
    
    @staticmethod
    def avec_nom(nom : str) -> 'Attaque':
        """Cherche l'attaque avec le nom correspondant dans _liste."""
        try:
            return Attaque(
                [   # Recherche le nom
                    i
                    for i, att in enumerate(Attaque._liste)
                    if nom == att["nom"]
                ][0]
            )
        except IndexError:
            raise ValueError(f"L'attaque \"{nom}\" n'a pas été trouvée.")
    
    @property
    def lanceur(self) -> Any: # -> Entite   # ça devrait être annoté avec object mais le type checker n'aime pas trop
        # https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals
        assert(Attaque._dico_entites.index_exists(self._lanceur_id)), f"L'ID du lanceur est incorrecte dans la propriété ._lanceur de l'attaque {self!r}."
        
        return Attaque._dico_entites[self._lanceur_id]
    
    @property
    def cible(self) -> Any: # -> Entite
        assert(Attaque._dico_entites.index_exists(self._cible_id)), f"L'ID de la cible est incorrecte dans la propriété ._lanceur de l'attaque {self!r}."
        
        return Attaque._dico_entites[self._cible_id]
    
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
    def type(self) -> TypeAttaque:
        return self._type
    
    @property
    def stats_changees_cible(self) -> Stat:
        return copy(self._modif_stats_cible)
    
    @property
    def stats_changees_lanceur(self) -> Stat:
        return copy(self._modif_stats_lanceur)
    
    @property
    def peut_attaquer_lanceur(self) -> bool:
        return AttaqueFlag.ATTAQUE_LANCEUR in self._drapeaux
    
    @property
    def peut_attaquer_adversaires(self) -> bool:
        return AttaqueFlag.ATTAQUE_ENNEMIS in self._drapeaux
    
    
    def _calcul_attaque_defense(self, puissance_attaquant : int, defense_cible : int) -> tuple[float, float]:
        if AttaqueFlag.IGNORE_STATS in self._drapeaux:
            return (self._puissance, 1)
        
        attaque : float = self._puissance * puissance_attaquant
        defense : float = defense_cible
        if defense_cible < 0:
            defense = abs(1 / defense_cible)
        
        if AttaqueFlag.IGNORE_DEFENSE in self._drapeaux:
            return (attaque, 1)
        return (attaque, defense)
    
    def calculer_degats(self) -> int:
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
                )
                degats *= attaque / defense
            
            case TypeAttaque.MAGIQUE:
                attaque, defense = self._calcul_attaque_defense(
                    stats_attaquant.magie,
                    stats_victime.defense_magique,
                )
                degats *= attaque / defense
            
            case TypeAttaque.SOIN:
                attaque : float = self._puissance * stats_attaquant.magie
                degats *= -attaque
            
            case TypeAttaque.DIVERS:
                if self._puissance == 0:
                    degats = 0
            
            case _:
                raise ValueError("type_degat n'est pas un membre de TypeAttaque dans Attaque.calculer_degats.")
        
        if self._crit:
            crit_facteur : float = stats_attaquant.crit_puissance / max(stats_victime.crit_resitance, .01)  # on évite la division par 0
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
        self.cible.recoit_degats(self.calculer_degats(), self)
        self.appliquer_effet()
    
    def actualiser(self) -> None:
        """Actualise l'objet pour qu'il respecte les valeurs dans le dictionnaire."""
        a_copier = Attaque.avec_nom(self._nom)
        
        self._nom          = a_copier._nom
        self._desc         = a_copier._desc
        self._puissance    = a_copier._puissance
        
        self._type         = a_copier._type
        # Le lanceur et la cible sont inchangés
        
        self._prob_crit    = a_copier._prob_crit
        # crit reste aussi
        
        self._effet        = a_copier._effet
        self._drapeaux     = a_copier._drapeaux
        
        self._ajustement_degats   = a_copier._ajustement_degats
        self._autoriser_animation = a_copier._autoriser_animation

    def appliquer_effet(self):
        self.cible.ajouter_modif_stats(self._modif_stats_cible, self._modif_stats_cible_duree)
        self.lanceur.ajouter_modif_stats(self._modif_stats_lanceur, self._modif_stats_lanceur_duree)