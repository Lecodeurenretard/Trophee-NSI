"""
Contient les classes relatives aux cartes sauf les attaques en elles-mêmes.
Tout le côté graphique, animation, effets, etc... se fait ici. Les dégats, et tout le reste se fait dans Attaques.py.
projet : L'ascension de Esquimot
auteur : Dooheli, Lecodeurenretard, hibou509
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
    _HAUTEUR_SPRITE  : int   = Fenetre.pourcentage_hauteur(40)
    
    _ANIM_SURVOL_DECALAGE : Vecteur = Fenetre.pourcentages_fenetre(0, -2)
    _ANIM_DICO : dict[CarteAnimEtat, CarteAnimInfo] = {
        CarteAnimEtat.IDLE     : CarteAnimInfo(Pos(CarteAnimInfo.GARDER , CarteAnimInfo.GARDER) , Duree(s=0) , Easing.NO_EASING, CarteAnimInfo.GARDER),
        CarteAnimEtat.REVENIR  : CarteAnimInfo(Pos(CarteAnimInfo.CHANGER, CarteAnimInfo.CHANGER), Duree(s=.3), Easing.FADE     , CarteAnimInfo.GARDER),
        CarteAnimEtat.PARTIR   : CarteAnimInfo(Pos(CarteAnimInfo.CHANGER, Fenetre.hauteur)      , Duree(s=.3), Easing.FADE     , CarteAnimInfo.GARDER),
        CarteAnimEtat.EN_SURVOL: CarteAnimInfo(Pos(CarteAnimInfo.CHANGER, CarteAnimInfo.CHANGER), Duree(s=.1), Easing.FADE     , CarteAnimInfo.GARDER),
        CarteAnimEtat.JOUER    : CarteAnimInfo(Pos(CarteAnimInfo.CHANGER, CarteAnimInfo.CHANGER), Duree(s=1) , Easing.FADE_IN  , False),
    }
    
    SON_COUP : Sound = Sound(f"{Chemins.SFX}/hit.mp3")
    SON_HEAL : Sound = Sound(f"{Chemins.SFX}/heal.mp3")
    SON_CRIT : Sound = Sound(f"{Chemins.SFX}/smash-crit.wav")
    
    CRIT_IMG : Surface = pygame.transform.scale(
        pygame.image.load(f"{Chemins.IMG}crit.png"),
        (40, 40)
    ).convert_alpha()
    
    donnees_JSON : list[dict]
    derniere_enregistree : 'Optional[Carte]' = None
    cartes_affichees : ListeStable['Carte'] = ListeStable()
    
    
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
        self._id_affichage : Optional[int] = None
        
        donnees_JSON : dict = Carte.donnees_JSON[id]
        
        self._nom        : str     = donnees_JSON["nom"]
        self._desc       : str     = donnees_JSON["description"]
        self._nom_sprite : str     = donnees_JSON["sprite"]
        self._attaque    : Attaque = Attaque(id)
        
        self._anim_gen      : Optional[Generator[bool, None, None]] = None
        self._de_dos_defaut : bool = de_dos
        
        self._finir_anim     : bool = False
        self._dessiner_infos : bool = False
        
        self._TAILLE_SPRITE : tuple[int, int] = self._sprite.get_rect().size
    
    def __repr__(self):
        return (
            "Carte("
            f"nom={self._nom}"
            f"; sprite={self._nom_sprite}"
            f"; pos={self._pos}"
            f"; pos_defaut={self._pos_defaut}"
            f"; anim_etat={self._anim_etat}"
            f"; attaque={self._attaque}"
            ")"
        )
    
    @staticmethod
    def actualiser_donnees() -> None:
        """Actualise les données JSON des cartes et des attaques."""
        with open(f"{Chemins.JSON}cartes.json", encoding="utf-8") as fichier:
            Carte.donnees_JSON = json.load(fichier)
        
        # Envoie l'objet "attaque" avec le nom rajouté pour les attaques
        liste_attaques : list[dict]= []
        for carte in Carte.donnees_JSON:
            attaque_dict = deepcopy(carte["attaque"])
            attaque_dict["nom"] = carte["nom"]
            
            liste_attaques.append(attaque_dict)
        Attaque.set_liste(liste_attaques)
    
    @staticmethod
    def vider_cartes_affichees() -> None:
        copie = copy(Carte.cartes_affichees)
        for _, c in copie.no_holes():
            c.cacher()
        Carte.cartes_affichees.clear()
    
    @staticmethod
    def ordre_dessin(cartes : Iterable[Carte], inverse : bool = False) -> list[Carte]:
        """
        Renvoie les cartes dans l'ordre où elles seront dessinées.
        Si inverse est True, les renvoie dans l'ordre inverse,
        dans ce cas les cartes visuellement au dessus sont donc en première.
        """
        return sorted(cartes, reverse=inverse, key=lambda c: c.pos_defaut.x)
    
    @property
    def _hitbox(self) -> Rect:
        return Rect(self._pos.tuple, self._TAILLE_SPRITE)
    
    @property
    def _anim_infos(self) -> CarteAnimInfo:
        return Carte._ANIM_DICO[self._anim_etat]
    
    @property
    def _sprite(self) -> Surface:
        if self.est_de_dos:
            return self._preparation_sprite(f"{Chemins.IMG}cartes/dos.png")
        return self._preparation_sprite(f"{Chemins.IMG}cartes/{self._nom_sprite}/1.png")
    
    @property
    def est_de_dos(self) -> bool:
        """Renvoie si la carte doit être dessinée de dos en prenant en compte l'animation."""
        est_de_dos = self._anim_infos.de_dos
        if est_de_dos == CarteAnimInfo.GARDER:
            return self._de_dos_defaut
        if est_de_dos == CarteAnimInfo.CHANGER:
            raise NotImplementedError("Aucun changement prévu pour si la carte est de dos.")
        
        # c'est une int si et seulement si c'est une des deux valeurs en haut
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
    def dessiner_infos(self) -> bool:
        return self._dessiner_infos
    
    @property
    def est_affiche(self) -> bool:
        if self._id_affichage is not None:
            assert(self._anim_gen is not None), "Tout objet dans Carte.cartes_affichees[] doit avoir un générateur d'animation."
            return True
        return False
    
    @property
    def animation_generateur(self) -> Generator[bool, None, None]:
        """
        Renvoie le générateur pour l'animation.
        Suppose que la carte est affichée, pour la dévoiler utiliser .afficher().
        """
        assert(self.est_affiche), "La carte est cachée (elle n'est pas dans Carte.animations_affichees)."
        return self._anim_gen   # type: ignore  # on vérifie en haut que c'est non none
    
    @anim_etat.setter
    def anim_etat(self, val : CarteAnimEtat) -> None:
        self._anim_etat = val
    
    @dessiner_infos.setter
    def dessiner_infos(self, val : bool) -> None:
        self._dessiner_infos = val
    
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
        return res.convert_alpha()
    
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
            case CarteAnimEtat.EN_SURVOL:
                dest = self._pos_defaut + Carte._ANIM_SURVOL_DECALAGE
        
        assert(
                dest.x != CarteAnimInfo.CHANGER
            and dest.y != CarteAnimInfo.CHANGER
        ), f"La destination de l'animation \"{self._anim_etat.name}\" ({dest}) doit être changée."
        
        return Deplacement(self._pos, dest)
    
    # TODO: déplacer les définitions de fonctions autre part pour raccourcir la fonction
    def _dessin_infos(self, num_couche : int) -> None:
        if self.est_de_dos:
            return
        
        # Dessine le fond derrière les infos au dessus de la carte
        Jeu.verifier_parametre("ratio hauteur menu carte")
        ratio = Jeu.parametres["ratio hauteur menu carte"]
        rect = Rect(
            *(self._pos - Vecteur(0, self._TAILLE_SPRITE[1] * ratio)).tuple,
            self._TAILLE_SPRITE[0], self._TAILLE_SPRITE[1] * ratio
        )
        dessiner_rect(
            num_couche,
            rect.topleft,
            rect.size,
            couleur_remplissage=GRIS_CLAIR,
            couleur_bords=GRIS,
            epaisseur_trait=3,
            border_radius=10
        )
        
        PADDING = 10
        INTER_INFO = 5
        def dessiner_dans_rect() -> Generator[None, str, None]:
            """Renvoie un générateur qui dessine le texte envoyé dans le rectangle rect."""
            POLICE_STATS = pygame.font.Font(Polices.TEXTE, 16)
            x = rect.x + PADDING
            y = rect.y + PADDING
            while True:
                texte = (yield)
                y = Fenetre.blit_couche(
                    num_couche,
                    POLICE_STATS.render(texte, True, NOIR),
                    (x, y + INTER_INFO),
                ).bottom
        
        dessinateur = dessiner_dans_rect()
        next(dessinateur)   # démarre le générateur
        
        def dessiner_stats_modifiees(stats : Stat, stats_de_qui : str, adversaire : bool) -> None:
            """Dessine le texte les stats modifées par l'attaque dans le rectangle."""
            aucun_changement = True
            dessinateur.send(f"Stats de {stats_de_qui} modifiées:")
            for nom, stat in stats.__dict__.items():
                if not bool(params.mode_debug):
                    nom = Stat.joli_nom(nom)
                
                if stat != 0 and nom != "vie":
                    aucun_changement = False
                    dessinateur.send(f"    {nom}: {stat:+}")
            
            if aucun_changement:
                dessinateur.send("    aucune")
            
            # On pourrait faire un if...else mais c'est mieux de séparer les deux blocs
            if not aucun_changement:
                duree = self._attaque._modif_stats_lanceur_duree
                if adversaire:
                    duree = self._attaque._modif_stats_cible_duree
                
                if duree == -1:
                    dessinateur.send(f"    effectif pour tout le combat")
                elif duree == 0:
                    dessinateur.send(f"    effectif pour le reste du tour")
                else:
                    dessinateur.send(f"    effectif pour {duree} tours")
        
        # Dessin
        dessinateur.send(f"Nom: {self._nom}")
        dessinateur.send(f"Type: {self._attaque.type.name}")
        dessinateur.send(f"Puissance: {self._attaque.puissance}")
        
        dessiner_stats_modifiees(self._attaque.stats_changees_cible, "l'adversaire", True)
        dessiner_stats_modifiees(self._attaque.stats_changees_lanceur, "Esquimot (vous)", False)
    
    def _animation(self, num_couche : int) -> Generator[bool, None, None]:
        """Renvoie un générateur avançant l'animation de la carte."""
        while True:
            if self._anim_etat not in Carte._ANIM_DICO.keys():
                logging.warning(
                    f"On ne reconnait pas l'animation \"{self._anim_etat.name}\", "
                    "On joue \"idle\" à la place."
                )
                self._anim_etat = CarteAnimEtat.IDLE
            
            # Reset et initialisation des variables
            debut_anim         : Duree         = copy(Jeu.duree_execution)
            animation_en_cours : CarteAnimEtat = self._anim_etat
            deplacement        : Deplacement   = self._calcul_deplacement()
            self._finir_anim = False
            
            # Si la durée est de 0, l'anim est déjà finie
            # (on évite aussi les divisions par 0 en dessous)
            if self._anim_infos.duree == Duree(s=0):
                self._pos = deplacement.calculer_valeur(1)
                self.dessiner(num_couche)
                
                yield True
                continue
            
            # On joue l'animation
            animation_ecrasee : bool = False
            while Jeu.duree_execution <= debut_anim + self._anim_infos.duree:
                if self._finir_anim:
                    break
                if animation_en_cours != self._anim_etat:
                    animation_ecrasee = True
                    break   # changement d'animation
                if animation_en_cours == CarteAnimEtat.JOUER:
                    self._dessiner_infos = False
                
                t = (Jeu.duree_execution - debut_anim) / self._anim_infos.duree
                t = clamp(t, 0, 1)
                self._pos = deplacement.calculer_valeur(t, easing_fun=self._anim_infos.easing)
                
                self.dessiner(num_couche)
                yield False
            
            # Ces deux lignes s'assurent que la carte soit au bon endroit
            # avant le return/yield juste après
            self._pos = deplacement.calculer_valeur(1)
            self.dessiner(num_couche)
            
            if animation_en_cours == CarteAnimEtat.JOUER:
                self.jouer_sfx()
                self._attaque.appliquer()
                return      # La carte ne doit plus être dessinée après
           
            if not animation_ecrasee:
                # Quand on finit l'animation, on arrête la carte
                # Si on a pas déjà indiqué son prochain état
                self._anim_etat = CarteAnimEtat.IDLE 
            yield True  # Changement d'animation
    
    def skip_animation(self) -> None:
        self._finir_anim = True
    
    def afficher(self) -> None:
        if self.est_affiche:
            return
        
        self._anim_gen = self._animation(0)
        nouvel_index = Carte.cartes_affichees.search(None)
        if nouvel_index >= 0:
            self._id_affichage = nouvel_index
            Carte.cartes_affichees[nouvel_index] = self
        else:
            self._id_affichage = len(Carte.cartes_affichees)
            Carte.cartes_affichees.append(self)
    
    def cacher(self) -> None:
        if self.est_affiche:
            Carte.cartes_affichees.pop(self._id_affichage)  # type: ignore
            self._id_affichage = None
    
    def dessiner(self, num_couche : int) -> None:
        if not self.est_affiche:
            return
        
        Fenetre.blit_couche(0, self._sprite, self._pos.tuple)
        if self.dessiner_infos:
            self._dessin_infos(num_couche)
        
        if self._attaque._crit:
            milieu_sprite = Vecteur(self._sprite.get_rect().size) // 2
            blit_centre(
                num_couche,
                Carte.CRIT_IMG,
                (self._pos + milieu_sprite).tuple, # on centre l'étoile
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
        self.afficher()     # Aide peut-être?
    
    def jouer_sfx(self) -> None:
        """Joue l'effet sonore approprié au jeu de la carte."""
        if self._attaque._crit:
            Carte.SON_CRIT.play()
        elif self._attaque._type == TypeAttaque.SOIN:
            Carte.SON_HEAL.play()
        else:
            Carte.SON_COUP.play()
    
    def dans_hitbox(self, pos : pos_t) -> bool:
        return self._hitbox.collidepoint(pos_t_vers_tuple(pos))