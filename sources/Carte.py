"""
Contient les classes relatives aux cartes sauf les attaques en elles-mêmes.
Tout le côté graphique, animation, effets, etc... se fait ici. Les dégats, et tout le reste se fait dans Attaques.py.
"""
from Attaque import *

class Carte:
    _HAUTEUR_SPRITE  : int     = 200
    _DUREE_INTER_JEU : Duree   = Duree(s=.5)
    _SURVOL_DECALAGE : Vecteur = Vecteur(0, 20)
    
    _ANIM_GARDER_POS  : int = -1
    _ANIM_CHANGER_POS : int = -2
    
    # A chaque nom, associe une tuple contenant:
    # La position d'arrivée de l'animation, la duree de l'animation et la fonction d'easing à utiliser
    _ANIM_DICO : dict[str, tuple[Pos, Duree, EasingFunction]] = {
        "idle"  : (Pos(_ANIM_GARDER_POS, _ANIM_GARDER_POS)           , Duree(s=0) , Easing.NO_EASING),
        "survol": (Pos(_ANIM_GARDER_POS, Jeu.pourcentage_hauteur(80)), Duree(s=.5), Easing.FADE),
        "jouer" : (Pos(_ANIM_CHANGER_POS, _ANIM_CHANGER_POS)         , Duree(s=1) , Easing.FADE_IN),
    }
    _SPRITE_DOS                : Surface = etirer_garder_ratio(
        pygame.image.load(f"{Constantes.Chemins.IMG}/cartes/dos.png"),
        hauteur=_HAUTEUR_SPRITE
    )
    
    SON_COUP : Sound = Sound(f"{Constantes.Chemins.SFX}/hit.mp3")
    SON_HEAL : Sound = Sound(f"{Constantes.Chemins.SFX}/heal.mp3")
    SON_CRIT : Sound = Sound(f"{Constantes.Chemins.SFX}/smash-crit.wav")
    
    CRIT_IMG : Surface = pygame.transform.scale(
        pygame.image.load(f"{Constantes.Chemins.IMG}/crit.png"),
        (40, 40)
    )
    
    donnees_JSON : list[dict]
    derniere_enregistree : 'Optional[Carte]' = None
    
    @overload 
    def __init__(self, nom_ou_id_attaque : str, pos_defaut : pos_t): ...
    @overload
    def __init__(self, nom_ou_id_attaque : int, pos_defaut : pos_t): ...
    
    def __init__(self, nom_ou_id_attaque : int|str, pos_defaut : pos_t):
        id : int
        if type(nom_ou_id_attaque) is int: id = nom_ou_id_attaque
        if type(nom_ou_id_attaque) is str: id = Attaque.avec_nom(nom_ou_id_attaque).id
        
        
        position = pos_t_vers_Pos(pos_defaut)
        self._pos_defaut  : Pos = position
        
        self._pos       : Pos         = position
        self._anim_nom  : str         = "idle"
        self._anim_sens : SensLecture = SensLecture.AVANT
        
        donnees_JSON : dict = Carte.donnees_JSON[id]
        
        self._nom        : str     = donnees_JSON["nom"]
        self._desc       : str     = donnees_JSON["description"]
        self._nom_sprite : str     = donnees_JSON["sprite"]
        self._attaque    : Attaque = Attaque(id)
        
        # On ne crée pas assez de carte par seconde pour que ça ralentisse tout
        self._TAILLE_SPRITE : tuple[int, int] = self._get_sprite().get_rect().size
    
    def __repr__(self):
        return f"Carte(nom={self._nom}; sprite={self._nom_sprite}; pos={self._pos}; attaque={self._attaque})"
    
    @staticmethod
    def actualiser_donnees() -> None:
        with open(f"{Constantes.Chemins.DATA}/cartes.json") as fichier:
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
    
    @anim_nom.setter
    def anim_nom(self, val : str) -> None:
        self._anim_nom = val
    
    # méthode car C lent
    def _get_sprite(self) -> Surface:
        """Génère le sprite de la carte. Assez lent."""
        img = pygame.image.load(f"{Constantes.Chemins.IMG}/cartes/{self._nom_sprite}")
        res = Surface(img.get_bounding_rect().size, pygame.SRCALPHA)
        res.blit(img, (0, 0), img.get_bounding_rect())
        
        # On resize le sprite de façon à ce que les proprtions sont gardées
        ratio : float = res.get_bounding_rect().width / res.get_bounding_rect().height
        res = pygame.transform.scale(
            res,
            (Carte._HAUTEUR_SPRITE * ratio, Carte._HAUTEUR_SPRITE)
        )
        return res
    
    def _set_deplacement(self) -> None:
        """Détermine la destination de l'animation et actualise `._deplacement`."""
        if self._anim_nom == "idle":
            self._pos = self._pos_defaut
            return
        
        dest : Pos = copy(self._anim_destination)
        
        if dest.x == Carte._ANIM_GARDER_POS: dest.x = self._pos.x
        if dest.y == Carte._ANIM_GARDER_POS: dest.y = self._pos.y
        
        if self._anim_nom == "jouer":
            dest = self._attaque.cible.pos_attaque
        
        assert(
                dest.x != Carte._ANIM_CHANGER_POS
            and dest.y != Carte._ANIM_CHANGER_POS
        ), f"La destination de l'animation \"{self._anim_nom}\" ({dest}) doit être changée."
        self._deplacement = Deplacement(self._pos, dest, sens_lecture=self._anim_sens)
    
    def dessiner(self, surface : Surface, de_dos : bool = False) -> None:
        sprite = Carte._SPRITE_DOS if de_dos else self._get_sprite()
        Jeu.fenetre.blit(sprite, self._pos.tuple)
        
        if self._attaque._crit:
            blit_centre(
                surface,
                Carte.CRIT_IMG,
                (self._pos + Vecteur(sprite.get_rect().size) // 2).tuple, # on centre l'étoile
            )
    
    def jouer_animation(self, surface : Surface) -> Generator[None, None, None]:
        """Avance l'animation."""
        while True:
            debut_anim         : Duree = copy(Jeu.duree_execution)
            animation_en_cours : str   = self._anim_nom
            
            self._set_deplacement()
            while True:
                if debut_anim + self._anim_duree  == Jeu.duree_execution:
                    self._pos = self._deplacement.fin
                    break   # fin anim
                
                if animation_en_cours != self._anim_nom:
                    break   # changement d'animation
                
                t = (Jeu.duree_execution - debut_anim) / self._anim_duree
                self._pos = self._deplacement.calculer_valeur(t, easing_fun=self._anim_easing)
                yield
            
            if self._anim_nom == "jouer":
                self.jouer_sfx()
    
    def enregister_lancement(self, id_lanceur : int, id_cible : int, flags_a_ajouter : AttaqueFlag = AttaqueFlag.AUCUN) -> None:
        """
        Indique le lanceur la cible, et si l'attaque est un crit, ajoute les drapeaux indiqués
        puis enregistre la carte dans Carte.derniere_enregistree et son attaque dans Attaque.attaques_jouees.
        """
        # On veut garder la référence donc pas de copie
        
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
    
    def decaler_pos_defaut(self, v : Vecteur) -> None:
        self._pos_defaut += v

Carte.actualiser_donnees()