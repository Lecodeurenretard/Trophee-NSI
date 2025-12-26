"""
Contient les classes relatives aux cartes sauf les attaques en elles-mêmes.
Tout le côté graphique, animation, effets, etc... se fait ici. Les dégats, et tout le reste se fait dans Attaques.py.
"""
from Attaque import *

class Carte:
    _HAUTEUR_SPRITE  : int     = 200
    _DUREE_INTER_JEU : Duree   = Duree(s=.5)
    _SURVOL_DECALAGE : Vecteur = Vecteur(0, 20)
    
    _ANIM_GARDER  : int = -1
    _ANIM_CHANGER : int = -2
    
    # A chaque nom, associe une tuple contenant:
    # La position d'arrivée de l'animation, la duree de l'animation, la fonction d'easing à utiliser et si la carte dois être de dos
    _ANIM_DICO : dict[str, tuple[Pos, Duree, EasingFunction, bool|int]] = {       # TODO: mettre dans le JSON
        "idle"  : (Pos(_ANIM_CHANGER, _ANIM_CHANGER)             , Duree(s=0) , Easing.NO_EASING, _ANIM_GARDER),
        "survol": (Pos(_ANIM_GARDER, Jeu.pourcentage_hauteur(80)), Duree(s=.5), Easing.FADE     , _ANIM_GARDER),
        "jouer" : (Pos(_ANIM_CHANGER, _ANIM_CHANGER)             , Duree(s=1) , Easing.FADE_IN  , True),
    }
    
    SON_COUP : Sound = Sound(f"{Chemins.SFX}/hit.mp3")
    SON_HEAL : Sound = Sound(f"{Chemins.SFX}/heal.mp3")
    SON_CRIT : Sound = Sound(f"{Chemins.SFX}/smash-crit.wav")
    
    CRIT_IMG : Surface = pygame.transform.scale(
        pygame.image.load(f"{Chemins.IMG}/crit.png"),
        (40, 40)
    )
    
    donnees_JSON : list[dict]
    derniere_enregistree : 'Optional[Carte]' = None
    cartes_affichees : dict[int, 'Carte'] = {}
    
    @overload 
    def __init__(self, nom_ou_id_attaque : str, pos_defaut : pos_t, de_dos = True): ...
    @overload
    def __init__(self, nom_ou_id_attaque : int, pos_defaut : pos_t, de_dos = True): ...
    
    def __init__(self, nom_ou_id_attaque : int|str, pos_defaut : pos_t, de_dos = True):
        id : int
        if type(nom_ou_id_attaque) is int: id = nom_ou_id_attaque
        if type(nom_ou_id_attaque) is str: id = Attaque.avec_nom(nom_ou_id_attaque).id
        
        
        position = pos_t_vers_Pos(pos_defaut)
        self._pos_defaut  : Pos = position
        
        self._pos       : Pos         = position
        self._anim_nom  : str         = "idle"
        self._anim_sens : SensLecture = SensLecture.AVANT
        self._id_affichage : int = -1
        
        donnees_JSON : dict = Carte.donnees_JSON[id]
        
        self._nom        : str     = donnees_JSON["nom"]
        self._desc       : str     = donnees_JSON["description"]
        self._nom_sprite : str     = donnees_JSON["sprite"]
        self._attaque    : Attaque = Attaque(id)
        
        self._anim_gen      : Optional[Generator[bool, None, None]] = None
        self._de_dos_defaut : bool = de_dos
        
        self._finir_anim : bool = False
        
        # On ne crée pas assez de carte par seconde pour que ça ralentisse tout
        self._TAILLE_SPRITE : tuple[int, int] = self._get_sprite().get_rect().size
    
    def __repr__(self):
        return f"Carte(nom={self._nom}; sprite={self._nom_sprite}; pos={self._pos}; attaque={self._attaque})"
    
    @staticmethod
    def actualiser_donnees() -> None:
        with open(f"{Chemins.DATA}/cartes.json") as fichier:
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
    def _anim_destination(self) -> Pos:
        return Carte._ANIM_DICO[self._anim_nom][0]
    @property
    def _anim_duree(self) -> Duree:
        return Carte._ANIM_DICO[self._anim_nom][1]
    @property
    def _anim_easing(self) -> EasingFunction:
        return Carte._ANIM_DICO[self._anim_nom][2]
    @property
    def _anim_de_dos(self) -> bool|int:
        return Carte._ANIM_DICO[self._anim_nom][3]
    
    @property
    def est_de_dos(self) -> bool:
        """Renvoie si la carte doit être déssinée de dos e prenant en compte l'animation."""
        if self._anim_de_dos == Carte._ANIM_GARDER:
            return self._de_dos_defaut
        if self._anim_de_dos == Carte._ANIM_CHANGER:
            raise NotImplementedError("Aucun changement prévu pour si la carte est de dos.")
        
        # c'est une int ssi c'est une des deux valeurs en haut
        return self._anim_de_dos    # type: ignore
    
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
    def souris_survole(self) -> bool:
        return self._hitbox.collidepoint(pygame.mouse.get_pos())
    
    @property
    def anim_nom(self) -> str:
        return self._anim_nom
    
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
        return self._anim_gen   # type: ignore
    
    @anim_nom.setter
    def anim_nom(self, val : str) -> None:
        self._anim_nom = val
    
    @pos_defaut.setter
    def pos_defaut(self, val : Pos) -> None:
        self._pos_defaut = val
    
    def _get_sprite(self) -> Surface:
        """Génère le sprite de la carte. Assez lent."""
        img : Surface
        if self.est_de_dos:
            img = pygame.image.load(f"{Chemins.IMG}/cartes/dos.png")
        else:
            img = pygame.image.load(f"{Chemins.IMG}/cartes/{self._nom_sprite}")
        img = etirer_garder_ratio(img, hauteur=Carte._HAUTEUR_SPRITE)
        
        
        res = Surface(img.get_bounding_rect().size, pygame.SRCALPHA)
        res.blit(img, (0, 0), img.get_bounding_rect())
        return res
    
    def _calcul_deplacement(self) -> Deplacement:
        """Détermine la destination de l'animation."""
        dest : Pos = copy(self._anim_destination)
        
        if dest.x == Carte._ANIM_GARDER: dest.x = self._pos.x
        if dest.y == Carte._ANIM_GARDER: dest.y = self._pos.y
        
        match(self._anim_nom):
            case "jouer":
                dest = self._attaque.cible.pos_attaque
            case "idle":
                dest = self._pos_defaut
        
        assert(
                dest.x != Carte._ANIM_CHANGER
            and dest.y != Carte._ANIM_CHANGER
        ), f"La destination de l'animation \"{self._anim_nom}\" ({dest}) doit être changée."
        
        return Deplacement(self._pos, dest, sens_lecture=self._anim_sens)
    
    def _animation(self, surface : Surface) -> Generator[bool, None, None]:
        """Renvoie un générateur avançant l'animation."""
        while True:
            debut_anim         : Duree       = copy(Jeu.duree_execution)
            animation_en_cours : str         = self._anim_nom
            deplacement        : Deplacement = self._calcul_deplacement()
            self._finir_anim = False
            
            # Si la durrée est de 0, l'anim est déjà finie
            # (on évite aussi les divisions par 0 en dessous)
            if self._anim_duree == Duree(s=0):
                self._pos = deplacement.calculer_valeur(1)
                self.dessiner(surface)
                
                yield True
                continue
            
            # On joue l'animation
            while Jeu.duree_execution <= debut_anim + self._anim_duree and not self._finir_anim:
                if animation_en_cours != self._anim_nom:
                    break   # changement d'animation
                
                t = (Jeu.duree_execution - debut_anim) / self._anim_duree
                t = clamp(t, 0, 1)
                self._pos = deplacement.calculer_valeur(t, easing_fun=self._anim_easing)
                
                self.dessiner(surface)
                yield False
            
            if self._anim_nom == "jouer":
                self.jouer_sfx()
                self._attaque.appliquer()
                return      # La carte ne doit plus être dessinée après => plus de générateur
            
            yield True  # Changement d'animation
    
    def skip_animation(self) -> None:
        self._finir_anim = True
    
    def afficher(self, surface : Surface) -> None:
        if self.est_affiche:
            return
        
        self._anim_gen = self._animation(Jeu.fenetre)
        self._id_affichage = premier_indice_libre(Carte.cartes_affichees)
        Carte.cartes_affichees[self._id_affichage] = self
    
    def cacher(self) -> None:
        # del ne va pas appeler le .__del__() de l'objet
        # a moins qu'il ne soit stocké nulle part d'autre
        del Carte.cartes_affichees[self._id_affichage]
        self._id_affichage = -1
    
    def dessiner(self, surface : Surface) -> None:
        if not self.est_affiche:
            return
        
        sprite = self._get_sprite()
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

Carte.actualiser_donnees()