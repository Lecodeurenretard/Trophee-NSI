"""
Contient les classes relatives aux cartes sauf les attaques en elles-mêmes.
Tout le côté graphique, animation, effets, etc... se fait ici. Les dégats, et tout le reste se fait dans Attaques.py.
"""
from Attaque import *

class Carte:
    _HAUTEUR_SPRITE        : int   = 200
    _DUREE_INTER_ANIMATION : Duree = Duree(s=.5)
    _DUREE_ANIMATION       : Duree = Duree(s=1)
    
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
    def __init__(self, nom_ou_id : str): ...
    @overload
    def __init__(self, nom_ou_id : int): ...
    
    def __init__(self, nom_ou_id : int|str):
        id : int
        if type(nom_ou_id) is int: id = nom_ou_id
        if type(nom_ou_id) is str: id = Attaque.avec_nom(nom_ou_id).id
        
        donnees_JSON : dict = Carte.donnees_JSON[id]
        
        self._nom            : str     = donnees_JSON["nom"]
        self._desc           : str     = donnees_JSON["description"]
        self._nom_sprite  : str     = donnees_JSON["sprite"]
        self._attaque        : Attaque = Attaque(id)
        
        self._autoriser_animation : bool = valeur_par_defaut(
            donnees_JSON["animer"],
            True,
        )
    
    @staticmethod
    def actualiser_donnees() -> None:
        with open(f"{Constantes.Chemins.DATA}/cartes.json", encoding="utf-8") as fichier:
            Carte.donnees_JSON = json.load(fichier)
        
        # Envoie l'objet "attaque" avec le nom rajouté pour les attaques
        liste_attaques : list[dict]= []
        for carte in Carte.donnees_JSON:
            attaque_dict = deepcopy(carte["attaque"])
            attaque_dict["nom"] = carte["nom"]
            
            liste_attaques.append(attaque_dict)
        Attaque.set_liste(liste_attaques)
    
    @property
    def _deplacement(self) -> Deplacement:
        if self._autoriser_animation:
            return Deplacement(self._attaque.lanceur.pos_attaque, self._attaque.cible.pos_attaque)
        return Deplacement(
            Pos.milieu(self._attaque.lanceur.pos_attaque, self._attaque.cible.pos_attaque),
            Pos.milieu(self._attaque.lanceur.pos_attaque, self._attaque.cible.pos_attaque)
        )
    
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
    
    def _jouer_animation(self, surface : Surface) -> Generator[None, None, None]:
        """Joue l'animation et les SFX."""
        debut_attaque : Duree = copy(Jeu.duree_execution)
        fin_attaque   : Duree = debut_attaque + Carte._DUREE_ANIMATION
        
        # animation
        while Jeu.duree_execution < fin_attaque:
            try                 : yield
            except GeneratorExit: break
            
            if Jeu.duree_execution - debut_attaque == 0:
                self._dessiner(surface, self.pos_anim_attaque(0))
                continue
            
            pos : Pos = self.pos_anim_attaque(
                (Jeu.duree_execution - debut_attaque) / Carte._DUREE_ANIMATION
            )
            self._dessiner(surface, pos)
        
        self.jouer_sfx()
    
    def _dessiner(self, surface : Surface, position : Pos) -> None:
        RECT_LARGEUR = 200
        RECT_HAUTEUR = 50
        
        sprite = self._get_sprite()
        Jeu.fenetre.blit(sprite, position.tuple)
        
        if self._attaque._crit:
            blit_centre(
                surface,
                Carte.CRIT_IMG,
                (
                    position.x + RECT_LARGEUR // 2, # on centre l'étoile
                    position.y + RECT_HAUTEUR // 2,
                )
            )
    
    def pos_anim_attaque(self, t : float) -> Pos:
        """La position de l'attaque pour un temps t. (t = 0 => animation finie à 0%, t = 0.5 => animation finie à 50%, ...)"""
        return self._deplacement.calculer_valeur(t, EasingType.ease_in(EasingType.POLYNOMIAL, 3))
    
    def jouer(self, surface_dessin : Surface) -> Generator[None, None, None]:
        """
        Lance l'attaque et appelle ._animation().
        """
        if self._attaque.lanceur.est_mort:
            return
        
        if params.mode_debug.case_cochee:
            logging.debug(
                f"{self._attaque.lanceur.dbg_nom} (ID {self._attaque.lanceur.id}) "
                f"utilise {self._nom} "
                f"sur {self._attaque.cible.dbg_nom} (ID {self._attaque.cible.id})."
            )
        
        # https://stackoverflow.com/questions/9708902/in-practice-what-are-the-main-uses-for-the-yield-from-syntax-in-python-3-3
        # https://peps.python.org/pep-0380/#formal-semantics
        skip : bool = False
        try:
            yield from self._jouer_animation(surface_dessin)
        except GeneratorExit:
            skip = True
        
        self._attaque.appliquer()
        if skip:
            print("skip!")
            return
        
        # attente de la prochaine frame
        peut_sortir = pause(Carte._DUREE_INTER_ANIMATION)
        while not next(peut_sortir) and not (yield):
            continue
    
    def enregister_lancement(self, id_lanceur : int, id_cible : int, flags_a_ajouter : AttaqueFlag = AttaqueFlag.AUCUN) -> None:
        """
        Indique le lanceur la cible, et si l'attaque est un crit, ajoute les drapeaux indiqués
        puis enregistre la carte dans Carte.derniere_enregistree et son attaque dans Attaque.attaques_jouees.
        """
        # On veut garder la référence
        # copie : Attaque = copy(self._attaque)
        
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
