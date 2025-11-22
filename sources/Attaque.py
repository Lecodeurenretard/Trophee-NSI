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
    
    SON_COUP : Sound = Sound(f"{Constantes.Chemins.SFX}/hit.mp3")
    SON_HEAL : Sound = Sound(f"{Constantes.Chemins.SFX}/heal.mp3")
    SON_CRIT : Sound = Sound(f"{Constantes.Chemins.SFX}/smash-crit.wav")
    
    LISTE : list['Attaque']
    CRIT_IMG : Surface = pygame.transform.scale(
        pygame.image.load(f"{Constantes.Chemins.IMG}/crit.png"),
        (40, 40)
    )
    
    toujours_crits : bool = False   # ne pas activer ici, utiliser les touches du mode debug plutôt
    attaques_jouees : list['Attaque'] = []
    
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
        
        self._effet : EffetAttaque = NotImplemented
        self._drapeaux = flags
        
        self._ajustement_degats = ajustement_degats
        self._autoriser_animation = glisser
    
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
            + f"Jouer animation: {self._autoriser_animation}"
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
        """Ouvre le JSON et actualise LISTE_ATTAQUE[]."""
        with open(f"{Constantes.Chemins.DATA}/attaques.json") as fichier:
            attaques : list[dict] = json.load(fichier)[1:]      # On prend tout le fichier sauf l'exemple
            Attaque.LISTE = [Attaque._depuis_json_dict(dico) for dico in attaques]
    
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
        if self._autoriser_animation:
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
    
    def _jouer_animation(self, surface : Surface) -> Generator[None, None, None]:
        """Joue l'animation et les SFX."""
        debut_attaque : Duree = copy(Jeu.duree_execution)
        fin_attaque   : Duree = debut_attaque + Attaque._DUREE_ANIMATION
        
        # animation
        while Jeu.duree_execution < fin_attaque:
            try                 : yield
            except GeneratorExit: break
            
            if Jeu.duree_execution - debut_attaque == 0:
                self._dessiner(surface, self.pos_anim_attaque(0))
                continue
            
            pos : Pos = self.pos_anim_attaque(
                (Jeu.duree_execution - debut_attaque) / Attaque._DUREE_ANIMATION
            )
            self._dessiner(surface, pos)
        
        self.jouer_sfx()
    
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
        stats_attaquant : Stat = self._lanceur.stats_totales
        stats_victime : Stat = self._cible.stats_totales
        
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
    
    def lancer(self, surface_dessin : Surface) -> Generator[None, None, None]:
        """
        Lance l'attaque et appelle ._animation().
        Ne modifie PAS l'objet originel.
        """
        if self._lanceur.est_mort:
            return
        
        if params.mode_debug.case_cochee:
            logging.debug(f"{self._lanceur.dbg_nom} (ID {self._lanceur_id}) utilise {self._nom} sur {self._cible.dbg_nom} (ID {self._cible_id}).")
        
        # https://stackoverflow.com/questions/9708902/in-practice-what-are-the-main-uses-for-the-yield-from-syntax-in-python-3-3
        # https://peps.python.org/pep-0380/#formal-semantics
        skip : bool = False
        try:
            yield from self._jouer_animation(surface_dessin)
        except GeneratorExit:
            skip = True
        
        self.appliquer()
        if skip:
            print("skip!")
            return
        
        # attente de la prochaine frame
        peut_sortir = pause(Attaque._DUREE_ENTRE_ATTAQUES)
        while not next(peut_sortir) and not (yield):
            continue
    
    def enregister_lancement(self, id_lanceur : int, id_cible : int, flags_a_ajouter : AttaqueFlag = AttaqueFlag.AUCUN) -> None:
        copie : Attaque = copy(self)
        
        copie._lanceur_id = id_lanceur
        copie._cible_id   = id_cible
        copie._drapeaux  |= flags_a_ajouter
        
        copie._crit = Attaque.toujours_crits or random.random() < self._prob_crit
        Attaque.attaques_jouees.append(copie)
    
    def jouer_sfx(self) -> None:
        if self._crit:
            Attaque.SON_CRIT.play()
        elif self._type == TypeAttaque.SOIN:
            Attaque.SON_HEAL.play()
        else:
            Attaque.SON_COUP.play()
    
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


Attaque.actualiser_liste()