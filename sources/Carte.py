"""
Contient les classes relatives aux cartes sauf les attaques en elles-mêmes.
Tout le côté graphique, animation, effets, etc... se fait ici. Les dégats, et tout le reste se fait dans Attaques.py.
"""
from Attaque import *

@dataclass(frozen=True)
class CarteAnimInfo:
    GARDER  : int = field(default=-1, init=False)
    CHANGER : int = field(default=-2, init=False)
    
    destination : Pos
    duree       : Duree
    easing      : EasingFunction
    de_dos      : bool|int

class CarteAnimEtat(Enum):
    IDLE      = auto()
    REVENIR   = auto()
    PARTIR    = auto()
    EN_SURVOL = auto()
    JOUER     = auto()

class Carte:
    _HAUTEUR_SPRITE  : int     = Jeu.pourcentage_hauteur(40)
    _DUREE_INTER_JEU : Duree   = Duree(s=.5)
    
    _ANIM_SURVOL_DECALAGE : Vecteur = Jeu.pourcentages_fenetre(0, 2)
    _ANIM_DICO : dict[CarteAnimEtat, CarteAnimInfo] = {
        CarteAnimEtat.IDLE     : CarteAnimInfo(Pos(CarteAnimInfo.GARDER , CarteAnimInfo.GARDER)       , Duree(s=0) , Easing.NO_EASING, CarteAnimInfo.GARDER),
        CarteAnimEtat.REVENIR  : CarteAnimInfo(Pos(CarteAnimInfo.CHANGER, CarteAnimInfo.CHANGER)      , Duree(s=.3), Easing.FADE     , CarteAnimInfo.GARDER),
        CarteAnimEtat.PARTIR   : CarteAnimInfo(Pos(CarteAnimInfo.CHANGER, Jeu.hauteur)                , Duree(s=.3), Easing.FADE     , CarteAnimInfo.GARDER),
        CarteAnimEtat.EN_SURVOL: CarteAnimInfo(Pos(CarteAnimInfo.GARDER , Jeu.pourcentage_hauteur(80)), Duree(s=.5), Easing.FADE     , CarteAnimInfo.GARDER),
        CarteAnimEtat.JOUER    : CarteAnimInfo(Pos(CarteAnimInfo.CHANGER, CarteAnimInfo.CHANGER)      , Duree(s=1) , Easing.FADE_IN  , True),
    }
    
    SON_COUP : Sound = Sound(f"{Chemins.SFX}/hit.mp3")
    SON_HEAL : Sound = Sound(f"{Chemins.SFX}/heal.mp3")
    SON_CRIT : Sound = Sound(f"{Chemins.SFX}/smash-crit.wav")
    
    CRIT_IMG : Surface = pygame.transform.scale(
        pygame.image.load(f"{Chemins.IMG}/crit.png"),
        (40, 40)
    ).convert_alpha()
    
    donnees_JSON : list[dict]
    derniere_enregistree : 'Optional[Carte]' = None
    cartes_affichees : Array['Carte'] = Array()
    
    
    @overload 
    def __init__(self, nom_ou_id_attaque : str, pos_defaut : pos_t, de_dos = True): ...
    @overload
    def __init__(self, nom_ou_id_attaque : int, pos_defaut : pos_t, de_dos = True): ...
    
    def __init__(self, nom_ou_id_attaque : int|str, pos_defaut : pos_t, de_dos = True):
        id : int = 0
        if type(nom_ou_id_attaque) is int: id = nom_ou_id_attaque
        if type(nom_ou_id_attaque) is str: id = Attaque.avec_nom(nom_ou_id_attaque).id
        
        
        position = pos_t_vers_Pos(pos_defaut)
        self._pos_defaut  : Pos = position
        
        self._pos          : Pos = position
        self._anim_etat    : CarteAnimEtat = CarteAnimEtat.IDLE
        self._id_affichage : int = -1
        
        donnees_JSON : dict = Carte.donnees_JSON[id]
        
        self._nom        : str     = donnees_JSON["nom"]
        self._desc       : str     = donnees_JSON["description"]
        self._nom_sprite : str     = donnees_JSON["sprite"]
        self._attaque    : Attaque = Attaque(id)
        
        self._anim_gen      : Optional[Generator[bool, None, None]] = None
        self._de_dos_defaut : bool = de_dos
        
        self._finir_anim : bool = False
        
        # C'est un attribut non statique car il dépend de ._sprite qui n'est pas statique
        # mais il faut le traiter comme si
        self._TAILLE_SPRITE : tuple[int, int] = self._sprite.get_rect().size
    
    def __repr__(self):
        return (
            "Carte("
            f"nom={self._nom}"
            f"; sprite={self._nom_sprite}"
            f"; pos={self._pos}"
            f"; attaque={self._attaque}"
            ")"
        )
    
    @staticmethod
    def actualiser_donnees() -> None:
        with open(f"{Chemins.DATA}/cartes.json", encoding="utf-8") as fichier:
            Carte.donnees_JSON = json.load(fichier)
        
        # Envoie l'objet "attaque" avec le nom rajouté pour les attaques
        liste_attaques : list[dict]= []
        for carte in Carte.donnees_JSON:
            attaque_dict = deepcopy(carte["attaque"])
            attaque_dict["nom"] = carte["nom"]
            
            liste_attaques.append(attaque_dict)
        Attaque.set_liste(liste_attaques)
    
    @property
    def _hitbox(self) -> Rect:
        return Rect(self._pos.tuple, self._TAILLE_SPRITE)
    
    @property
    def _anim_infos(self) -> CarteAnimInfo:
        return Carte._ANIM_DICO[self._anim_etat]
    
    @property
    def _sprite(self) -> Surface:
        if self.est_de_dos:
            return self._preparation_sprite(f"{Chemins.IMG}/cartes/dos.png")
        return self._preparation_sprite(f"{Chemins.IMG}/cartes/{self._nom_sprite}")
    
    @property
    def est_de_dos(self) -> bool:
        """Renvoie si la carte doit être déssinée de dos en prenant en compte l'animation."""
        est_de_dos = self._anim_infos.de_dos
        if est_de_dos == CarteAnimInfo.GARDER:
            return self._de_dos_defaut
        if est_de_dos == CarteAnimInfo.CHANGER:
            raise NotImplementedError("Aucun changement prévu pour si la carte est de dos.")
        
        # c'est une int ssi c'est une des deux valeurs en haut
        assert(type(est_de_dos) is bool), f"CarteAnimInfo.de_dos devrait être un bool mais est un {type(est_de_dos).__name__} à la place."
        return est_de_dos
    
    @property
    def peut_attaquer_lanceur(self) -> bool:
        return self._attaque.peut_attaquer_lanceur
    
    @property
    def nom(self) -> str:
        return self._nom
    
    @property
    def description(self) -> str:
        return self._desc
    
    @property
    def puissance(self) -> float:
        return self._attaque._puissance
    
    @property
    def pos_defaut(self) -> Pos:
        return self._pos_defaut
    
    @property
    def est_a_pos_defaut(self) -> bool:
        return self._pos == self._pos_defaut
    
    @property
    def anim_etat(self) -> CarteAnimEtat:
        return self._anim_etat
    
    @property
    def est_affiche(self) -> bool:
        if self._id_affichage >= 0:
            assert(self._anim_gen is not None), "Tout objet dans Carte.cartes_affichees[] doit avoir un générateur d'animation."
            return True
        return False
    
    @property
    def animation_generateur(self) -> Generator[bool, None, None]:
        """
        Renvoie le générateur pour l'animation.
        Suppose que la carte est montrée, pour la dévoiler utiliser .afficher().
        """
        assert(self.est_affiche), "La carte est cachée (elle n'est pas dans Carte.animations_affichees)."
        return self._anim_gen   # type: ignore  # on vérifie en haut que c'est non none
    
    @anim_etat.setter
    def anim_etat(self, val : CarteAnimEtat) -> None:
        self._anim_etat = val
    
    @pos_defaut.setter
    def pos_defaut(self, val : Pos) -> None:
        self._pos_defaut = val
    
    @lru_cache
    def _preparation_sprite(self, chemin : str) -> Surface:
        """
        Renvoie l'image se situant dans `chemin` formattée comme un sprite de carte.
        Assez lent mais les résultats sont mémoisés.
        """
        img = pygame.image.load(chemin)
        img = etirer_garder_ratio(img, hauteur=Carte._HAUTEUR_SPRITE)
        
        res = Surface(img.get_bounding_rect().size, pygame.SRCALPHA)
        res.blit(img, (0, 0), img.get_bounding_rect())
        return res
    
    def _calcul_deplacement(self) -> Deplacement:
        """Détermine la destination de l'animation."""
        dest : Pos = copy(self._anim_infos.destination)
        
        if dest.x == CarteAnimInfo.GARDER: dest.x = self._pos.x
        if dest.y == CarteAnimInfo.GARDER: dest.y = self._pos.y
        
        match(self._anim_etat):
            case CarteAnimEtat.JOUER:
                dest = self._attaque.cible.pos_attaque
            case CarteAnimEtat.REVENIR:
                dest = self._pos_defaut
            case CarteAnimEtat.PARTIR:
                dest = Pos(self._pos_defaut.x, dest.y)
        
        assert(
                dest.x != CarteAnimInfo.CHANGER
            and dest.y != CarteAnimInfo.CHANGER
        ), f"La destination de l'animation \"{self._anim_etat.name}\" ({dest}) doit être changée."
        
        return Deplacement(self._pos, dest)
    
    def _animation(self, surface : Surface) -> Generator[bool, None, None]:
        """Renvoie un générateur avançant l'animation."""
        while True:
            if self._anim_etat not in Carte._ANIM_DICO.keys():
                logging.warning(
                    f"On ne reconnait pas l'animation \"{self._anim_etat.name}\", "
                    "On joue \"idle\" à la place."
                )
                self._anim_etat = CarteAnimEtat.IDLE
            
            debut_anim         : Duree         = copy(Jeu.duree_execution)
            animation_en_cours : CarteAnimEtat = self._anim_etat
            deplacement        : Deplacement   = self._calcul_deplacement()
            self._finir_anim = False
            
            # Si la durée est de 0, l'anim est déjà finie
            # (on évite aussi les divisions par 0 en dessous)
            if self._anim_infos.duree == Duree(s=0):
                self._pos = deplacement.calculer_valeur(1)
                self.dessiner(surface)
                
                yield True
                continue
            
            # On joue l'animation
            while Jeu.duree_execution <= debut_anim + self._anim_infos.duree:
                if animation_en_cours != self._anim_etat or self._finir_anim:
                    break   # changement d'animation
                
                t = (Jeu.duree_execution - debut_anim) / self._anim_infos.duree
                t = clamp(t, 0, 1)
                self._pos = deplacement.calculer_valeur(t, easing_fun=self._anim_infos.easing)
                
                self.dessiner(surface)
                yield False
            
            self._pos = deplacement.calculer_valeur(1)  # sécurité au cas où on revient trop tard dans la boucle du dessus
            self.dessiner(surface)  # évite que la carte ne soit pas dessinée pendant l'intervalle d'un yield
            
            if animation_en_cours == CarteAnimEtat.JOUER:
                self.jouer_sfx()
                self._attaque.appliquer()
                self.cacher()
                return      # La carte ne doit plus être dessinée après
            
            self._anim_etat = CarteAnimEtat.IDLE # Quand on finit l'animation, on arrête la carte
            yield True  # Changement d'animation
    
    def skip_animation(self) -> None:
        self._finir_anim = True
    
    def afficher(self) -> None:
        if self.est_affiche:
            return
        
        self._anim_gen = self._animation(Jeu.fenetre)
        self._id_affichage = Carte.cartes_affichees.search(None)
        if self._id_affichage >= 0:
            Carte.cartes_affichees[self._id_affichage] = self
        else:
            self._id_affichage = len(Carte.cartes_affichees)
            Carte.cartes_affichees.append(self)
    
    def cacher(self) -> None:
        Carte.cartes_affichees.pop(self._id_affichage)
        self._id_affichage = -1
    
    def dessiner(self, surface : Surface) -> None:
        if not self.est_affiche:
            return
        
        sprite = self._sprite
        Jeu.fenetre.blit(sprite, self._pos.tuple)
        
        if self._attaque._crit:
            blit_centre(
                surface,
                Carte.CRIT_IMG,
                (self._pos + Vecteur(sprite.get_rect().size) // 2).tuple, # on centre l'étoile
            )
    
    def enregister_lancement(self, id_lanceur : int, id_cible : int, flags_a_ajouter : AttaqueFlag = AttaqueFlag.AUCUN) -> None:
        """
        Indique le lanceur la cible, et si l'attaque est un crit, ajoute les drapeaux indiqués
        puis enregistre la carte dans Carte.derniere_enregistree et son attaque dans Attaque.attaques_jouees.
        """
        self._attaque._lanceur_id = id_lanceur
        self._attaque._cible_id   = id_cible
        self._attaque._drapeaux  |= flags_a_ajouter
        self._attaque.decider_crit()
        
        Attaque.attaques_jouees.append(self._attaque)
        Carte.derniere_enregistree = self
    
    def jouer_sfx(self) -> None:
        if self._attaque._crit:
            Carte.SON_CRIT.play()
        elif self._attaque._type == TypeAttaque.SOIN:
            Carte.SON_HEAL.play()
        else:
            Carte.SON_COUP.play()
    
    def dans_hitbox(self, pos : Pos) -> bool:
        return self._hitbox.collidepoint(pos.tuple)

Carte.actualiser_donnees()
