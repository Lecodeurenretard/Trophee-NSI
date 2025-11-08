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
    _DUREE_ANIMATION      : Duree = Duree(s=1)
    _DUREE_ENTRE_ATTAQUES : Duree = Duree(s=.5)
    
    _ajustements : TypeAlias = Callable[[float, bool], int]
    _AJUSTEMENTS : dict[str, _ajustements] = {
        "base": (lambda degats, crit: round(degats)),
    }
    
    LISTE : list['Attaque']
    CRIT_IMG : Surface = pygame.transform.scale(
        pygame.image.load(f"{Constantes.Chemins.IMG}/crit.png"),
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
            flags : AttaqueFlag = AttaqueFlag.ATTAQUE_ENNEMIS,
            ajustement_degats : _ajustements = _AJUSTEMENTS["base"],
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
    def _depuis_json_dict(json_dict : dict) -> 'Attaque':
        """Renvoie l'objet Attaque correpondant à `json_dict[]`."""
        ajustement : Attaque._ajustements = Attaque._AJUSTEMENTS[
            json_dict.get("nom_ajustement", "base")
        ]
        return Attaque(
            json_dict["nom"],
            json_dict["description"],
            json_dict["puissance"],
            json_dict["vitesse"],
            TypeAttaque.depuis_str(json_dict["type"]),
            
            crit_proba=json_dict.get("probabilité_crit", .1),
            flags=AttaqueFlag.depuis_liste(json_dict.get("flags", ["cible ennemis"])),
            ajustement_degats=ajustement,
            glisser=json_dict.get("animer", True),
        )
    
    @staticmethod
    def actualiser_liste() -> None:
        """Actualise LISTE_ATTAQUE[]."""
        with open(f"{Constantes.Chemins.DATA}/attaques.json") as fichier:
            attaques : list[dict] = json.load(fichier)[1:]      # On prend tout le fichier sauf l'exemple
            Attaque.LISTE = [Attaque._depuis_json_dict(dico) for dico in attaques]
    
    @staticmethod
    def lancer_toutes_les_attaques_gen(surface: Surface) -> Generator[None, Optional[bool], None]:
        """
        Renvoie un générateur qui affiche et applique toutes les attaques unes à unes.
        Si l'on envoie `True`, l'attaque qui est affichée sera passée.
        """
        if params.mode_debug.case_cochee:
            logging.debug("Début du lancement des attaques.")
        
        while not Attaque.attaques_du_tour.empty():
            # préparation
            attaque : Attaque = Attaque.attaques_du_tour.get_nowait().attaque
            if attaque._lanceur.est_mort:
                break
            
            if params.mode_debug.case_cochee:
                logging.debug(f"{attaque._lanceur.dbg_nom} (id: {attaque._lanceur.id}) utilise {attaque._nom} sur {attaque._cible.dbg_nom}.")
            
            # temps de début et de fin
            debut_attaque : Duree = copy(Jeu.duree_execution)
            fin_attaque   : Duree = debut_attaque + Attaque._DUREE_ANIMATION
            
            # animation
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
            
            # attente de la prochaine frame
            peut_sortir = pause(Attaque._DUREE_ENTRE_ATTAQUES)
            while not next(peut_sortir) and not skip_attaque:
                if (yield):   # None est "falsy", ça a le même effet que si l'utilisateur envoie `False`.
                    break
        
        
        if bool(params.mode_debug):
            logging.debug("Fin du lancement des attaques.")
            logging.debug("")
    
    @staticmethod
    def avec_nom(nom : str) -> 'Attaque':
        """Cherche l'attaque avec le nom correspondant dans LISTE."""
        return Attaque.LISTE[
            [att.nom for att in Attaque.LISTE].index(nom)   # Recherche le nom
        ]
    
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
    def nom(self) -> str:
        return self._nom
    
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
    def peut_attaquer_lanceur(self) -> bool:
        return AttaqueFlag.ATTAQUE_LANCEUR in self._drapeaux
    
    @property
    def peut_attaquer_adversaires(self) -> bool:
        return AttaqueFlag.ATTAQUE_ENNEMIS in self._drapeaux
    
    
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
        if AttaqueFlag.IGNORE_STATS in self._drapeaux:
            return (self._puissance, 1)
        
        attaque : float = self._puissance * puissance_attaquant
        defense : float = max(def_min, defense_cible)
        
        if AttaqueFlag.IGNORE_DEFENSE in self._drapeaux:
            return (attaque, 1)
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
        
        if self._crit:
            crit_facteur : float = stats_attaquant.crit_puissance / stats_victime.crit_resitance
            crit_facteur = max(1, crit_facteur) # un crit ne doit jamais baisser les dégats de l'attaque
            degats *= Attaque._PUISSANCE_CRIT * crit_facteur
        
        return self._ajustement_degats(degats, self._crit)
    
    def appliquer(self) -> None:
        if AttaqueFlag.ATTAQUE_LANCEUR not in self._drapeaux and self._lanceur_id == self._cible_id:
            return
        elif AttaqueFlag.ATTAQUE_ENNEMIS in self._drapeaux and type(self._lanceur) == type(self._cible):
            return
        elif AttaqueFlag.ATTAQUE_LANCEUR not in self._drapeaux and AttaqueFlag.ATTAQUE_ENNEMIS not in self._drapeaux:
            return
        self._cible.recoit_degats(self.calculer_degats())
    
    def enregister_lancement(self, id_lanceur : int, id_cible : int, flags_a_ajouter : AttaqueFlag = AttaqueFlag.AUCUN) -> None:
        """Pousse une copie de l'attaque sur `attaques_du_tour[]`. Ne modifie PAS l'objet originel."""
        copie : Attaque = copy(self)
        copie._cible_id = id_cible
        copie._lanceur_id = id_lanceur
        copie._drapeaux |= flags_a_ajouter
        
        copie._crit = Attaque.toujours_crits or random.random() < self._prob_crit
        
        Attaque.attaques_du_tour.put_nowait(AttaquePriorisee(copie, self._lanceur.stats.vitesse))

@total_ordering
class AttaquePriorisee:
    """Classe permettant de classer les attaques pour pouvoir déterminer leur ordre d'application."""
    def __init__(self, attaque : Attaque, vitesse_lanceur : float):
        self.attaque = attaque
        self._score = AttaquePriorisee._calcul_score(attaque.vitesse, vitesse_lanceur)
     
    def __lt__(self, other : 'AttaquePriorisee'):
        return self._score < other._score
    def __eq__(self, other : 'AttaquePriorisee'):
        return self._score == other._score
    
    @staticmethod
    def _calcul_score(vitesse_attaque : float, vitesse_lanceur : float) -> float:
        if vitesse_attaque < 0 or vitesse_lanceur < 0:
            return Stat.VITESSE_MAX
        
        # Visualisez et essayez les modification de la formule ici: https://www.desmos.com/3D/332drqdeup
        # Les seules restrictions sont que la fonction doit être strictement décroissante pour vitesse_attaque et vitesse_joueur.
        score_vitesse = 1.2 * vitesse_attaque + 1.0 * vitesse_lanceur
        return -clamp(score_vitesse, 0, Stat.VITESSE_MAX)


Attaque.actualiser_liste()