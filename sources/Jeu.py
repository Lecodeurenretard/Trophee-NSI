from imports import *
from classes_utiles import Duree, Pos, pos_t, pos_t_vers_tuple
from Constantes import Touches, Chemins
from Constantes.Couleurs import TRANSPARENT, ROUGE
from Constantes.Polices import FOURRE_TOUT, pixels_vers_taille_police
from Pool import Pool


Interruption : TypeAlias = Generator[None, None, None]
class Jeu:
    """
    Classe statique gerant le jeu.
    Elle contient les variables globales.
    """
    _CHEMIN_FICHIER_PARAMETRES : str = f"{Chemins.SAVE}parametres.txt"
    _TYPE_PREFIXES             : dict[type, str] = {
        int: 'i',
        float: 'f',
        str: 's',
    }
    
    ETAPE_PAR_ETAGE   : int = 10
    NOMBRE_ETAGES     : int = 2
    COMBAT_MAX        : int = NOMBRE_ETAGES * ETAPE_PAR_ETAGE
    ATTAQUES_PAR_TOUR : int = 3
    
    num_etape                 : int  = 1
    num_etape_precedente      : int  = num_etape
    
    attaques_restantes_joueur : int  = ATTAQUES_PAR_TOUR
    nb_tours_combat           : int  = 0
    a_gagne                   : bool = False
    
    
    duree_execution : Duree = Duree(s=0)
    clock           : pygame.time.Clock = pygame.time.Clock()
    framerate       : int = 60
    
    dernier_mouvement_souris : Duree = copy(duree_execution)
    
    volume_musique : float = 1
    parametres : dict[str, Any] = {}
    
    # Associe numéros étages et les pools de monstres
    pools_monstres      : dict[int, Pool] = {}
    pool_monstres_etage : Pool = Pool([])
    
    
    
    # Graphe des états: http://graphonline.top/fr/?graph=OMlRPwRCzhQxYjcl
    class Etat(Enum):
        DECISION_ETAT           = auto()
        ATTENTE_PROCHAINE_ETAPE = auto()
        CHOIX_ATTAQUE           = auto()
        AFFICHAGE_ATTAQUE       = auto()
        GAME_OVER               = auto()
        SHOP                    = auto()
        
        ECRAN_TITRE             = auto()
        CREDITS                 = auto()
        PREPARATION             = auto()
    etat           : Etat = Etat.DECISION_ETAT
    precedent_etat : Etat = Etat.DECISION_ETAT
    
    
    @staticmethod
    def num_etage(etape : Optional[int] = None) -> int:
        """Renvoie le numéro de l'étage pour l'étape `etape`, si etape est None renvoie pour l'étage courant."""
        if etape is None:
            etape = Jeu.num_etape
        # Pour que les étages multiples de Jeu.ETAPE_PAR_ETAGE (aka étages de boss)
        # soient dans l'étage inférieur.
        return (etape - 1) // Jeu.ETAPE_PAR_ETAGE
    
    @staticmethod
    def nom_etage(etape : Optional[int] = None) -> str:
        """Renvoie le nom de l'étage pour l'étape `etape`, si etape est None renvoie pour l'étage courant."""
        match(Jeu.num_etage(etape=etape)):
            case 0:
                return "plaines"
            case 1:
                return "eglise_satanique"
            case _:
                return "le_vide"
    
    @staticmethod
    def _application_contraintes_etape() -> None:
        # on s'assure que 0 < num_etape <= Jeu.COMBAT_MAX
        Jeu.num_etape %= Jeu.COMBAT_MAX
        if Jeu.num_etape == 0:
            Jeu.num_etape = Jeu.COMBAT_MAX
    
    @staticmethod
    def avancer_etape(n : int) -> None:
        """Ajoute n à num_etape."""
        Jeu.num_etape_precedente = Jeu.num_etape
        Jeu.num_etape += n
        Jeu._application_contraintes_etape()
    
    @staticmethod
    def aller_etape(etape : int) -> None:
        """Met num_etape à etape."""
        Jeu.num_etape_precedente = Jeu.num_etape
        Jeu.num_etape = etape
        Jeu._application_contraintes_etape()
    
    @staticmethod
    def etape_est_shop() -> bool:
        return Jeu.decision_shop(Jeu.num_etape)
        
    @staticmethod
    def etape_est_boss() -> bool:
        return Jeu.decision_boss(Jeu.num_etape)
    
    @staticmethod
    def decision_boss(num_combat : int) -> bool:
        """Décide si le combat est un combat de boss."""
        if num_combat == Jeu.COMBAT_MAX:    # un boss doit être le dernier niveau
            return True
        return num_combat % 10 == 0
    
    @staticmethod
    def decision_shop(num_combat : int) -> bool:
        """Décide si le combat est un shop."""
        if Jeu.decision_boss(num_combat):    # un shop ne peut pas être pendant un boss
            return False
        return num_combat % 5 == 0
    
    @classmethod
    def decision_etat_en_cours(cls) -> bool:
        return Jeu.etat == Jeu.Etat.DECISION_ETAT
    
    @classmethod
    def reset_etat(cls) -> None:
        """Indique que l'état du jeu doit être changé sous peu."""
        Jeu.etat = Jeu.Etat.DECISION_ETAT   # on ne veut pas enregistrer DECISION_ETAT dans precedent_etat
    
    @classmethod
    def changer_etat(cls, nouvel_etat : Etat) -> None:
        """Change l'état du jeu vers `nouvel_etat`."""
        cls.precedent_etat = cls.etat
        cls.etat           = nouvel_etat
    
    @staticmethod
    def commencer_frame() -> Duree:
        """La fonction à appeler à chaque début de frame. Renvoie le temps écoulé depuis la dernière frame."""
        delta = Jeu.clock.tick(Jeu.framerate)
        Jeu.duree_execution.millisecondes += delta
        
        for ev in pygame.event.get():
            verifier_pour_quitter(ev)
            if ev.type == pygame.MOUSEMOTION:
                Jeu.dernier_mouvement_souris = copy(Jeu.duree_execution)
            
            pygame.event.post(ev)    # remet les évènements dans la file des évènements
        
        return Duree(ms=delta)
    
    @staticmethod
    def jouer_musique(fichier : str, volume : Optional[float] = None) -> None:
        pygame.mixer.music.load(fichier)
        
        pygame.mixer.music.set_volume(
            volume
            if volume is not None
            else Jeu.volume_musique
        )
        pygame.mixer.music.play()
    
    @staticmethod
    def interrompre_musique() -> None:
        pygame.mixer.music.stop()
    
    @staticmethod
    def _creer_fichier_parametre() -> None:
        CHEMIN_PARAM_DEFAUT = f"{Chemins.ETC}parametres_defaut.txt"
        if not os.path.isfile(CHEMIN_PARAM_DEFAUT):
            raise FileNotFoundError(f"{CHEMIN_PARAM_DEFAUT} non trouvé, veuillez le retélécharger de Github.")
        shutil.copy(CHEMIN_PARAM_DEFAUT, Jeu._CHEMIN_FICHIER_PARAMETRES)
    
    @staticmethod
    def ecrire_parametres() -> None:
        with open(Jeu._CHEMIN_FICHIER_PARAMETRES, "w", encoding="utf-8") as f:
            for nom, val in Jeu.parametres.items():
                prefixe = Jeu._TYPE_PREFIXES[type(val)]
                f.write(f"{prefixe}{nom}={val}\n")
    
    @staticmethod
    def lire_parametres() -> None:
        Jeu.parametres = {}
        if not os.path.isfile(Jeu._CHEMIN_FICHIER_PARAMETRES):
            logging.warning(f"Le fichier {Jeu._CHEMIN_FICHIER_PARAMETRES} n'a pas été trouvé, on en recrée un.")
            Jeu._creer_fichier_parametre()
        
        with open(Jeu._CHEMIN_FICHIER_PARAMETRES, "r", encoding="utf-8") as f:
            # Lit chaque ligne et remplit 
            for ligne in f.readlines():
                nom, val = ligne.split('=', maxsplit=1)
                type_val = recherche_map(nom[0], Jeu._TYPE_PREFIXES, type(None))
                
                if type_val is None:
                    raise RuntimeError(
                        f"Préfixe '{nom[0]}' inconnu,"
                        " le fichier {Jeu.CHEMIN_FICHIER_PARAMETRES} est mal-formé."
                    )
                Jeu.parametres[nom[1:]] = type_val(val)     # functional cast comme pour int()
    
    @staticmethod
    def rafraichir_pools() -> None:
        # rafraichit aussi les autres pools
        Jeu.pools_monstres = {
            int(i): pool
            for i, pool in Pool.parse_fichier_pools(f"{Chemins.POOLS}monstres.json").items()
        }






class Fenetre:
    surface : Surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    
    largeur, hauteur = pygame.display.get_surface().get_size()  # type: ignore # la fenêtre à été créée du coup ce n'est jamais None
    centre_fenetre : tuple[int, int] = (largeur // 2, hauteur // 2)
    
    
    # on pourrait automatiser la création de surfaces avec
    # une compréhension de liste mais c'est brouillon.
    NB_COUCHES_GRAPHIQUES : int = 3
    couches_graphiques : tuple[Surface, ...] = (
        Surface((largeur, hauteur), pygame.SRCALPHA),
        Surface((largeur, hauteur), pygame.SRCALPHA),
        Surface((largeur, hauteur), pygame.SRCALPHA),
    )
    
    @classmethod
    def init(cls) -> None:
        """Initialise la classe, doit être appelé avant de l'utiliser."""
        cls.set_texte_fenetre("Menu Principal")
    
    @staticmethod
    def get_texte_fenetre() -> str:
        # https://www.pygame.org/docs/ref/display.html#pygame.display.get_caption
        return pygame.display.get_caption()[0]
    
    @staticmethod
    def set_texte_fenetre(val : str) -> None:
        pygame.display.set_caption(val)
    
    @staticmethod
    def get_couche(numero_couche : int) -> Surface:
        """
        Renvoie la couche avec le numéro correspondant, plus le numéro est élevé, plus la couche est dessinée tard.
        Ainsi les couches avec les plus haut numéro sont au dessus de celles avec de plus bas.
        La seule exeption est la couche de debogage qui est dessinée en dernière et à pour numéro -1.
        """
        if numero_couche == -1:
            return Fenetre.get_couche_debug()
        if not 0 <= numero_couche <= Fenetre.NB_COUCHES_GRAPHIQUES-1:
            raise ValueError(f"Le numéro de couche doit être positif et en dessous ou égal à {Fenetre.NB_COUCHES_GRAPHIQUES-1} ou égal à -1.")
        
        if numero_couche == 0:
            return Fenetre.surface
        return Fenetre.couches_graphiques[numero_couche-1]
    
    @staticmethod
    def get_couche_debug() -> Surface:
        return Fenetre.couches_graphiques[-1]
    
    @staticmethod
    def blit_couche(
        numero_couche : int,
        surface : Surface,
        dest : pos_t = (0, 0),
        area : tuple[int, int, int, int]|None = None,
        special_flags : int = 0,
    ) -> Rect:
        """
        Blit surface sur la couche numero_couche.
        Les autres arguments sont passés à surface.blit().
        Renvoie un Rect sur la zone de l'écran affectée.
        """
        return Fenetre.get_couche(numero_couche).blit(
            surface,
            dest=pos_t_vers_tuple(dest),
            area=area,
            special_flags=special_flags
        )
        
    @staticmethod
    def pourcentage_hauteur(pourcents : float) -> int:
        """Renvoie pourcentage de la hauteur de l'écran en pixels"""
        return round(Fenetre.hauteur * pourcents / 100)
    
    @staticmethod
    def pourcentage_largeur(pourcents : float) -> int:
        """Renvoie pourcentage de la largeur de l'écran en pixels"""
        return round(Fenetre.largeur * pourcents / 100)
    
    @overload
    @staticmethod
    def pourcentages_coordonnees(pc_largeur : float, pc_hauteur : float, ret_pos : Literal[True] = True) -> Pos:
        """Raccourcit pour Pos(Fenetre.pourcentage_largeur(pc_largeur), Fenetre.pourcentage_largeur(pc_hauteur))"""
    
    @overload
    @staticmethod
    def pourcentages_coordonnees(pc_largeur : float, pc_hauteur : float, ret_pos : Literal[False]) -> tuple[int, int]:
        """Raccourcit pour (Fenetre.pourcentage_largeur(pc_largeur), Fenetre.pourcentage_largeur(pc_hauteur))"""
    
    @staticmethod
    def pourcentages_coordonnees(pc_largeur : float, pc_hauteur : float, ret_pos : bool = True) -> pos_t:
        if ret_pos:
            return Pos(Fenetre.pourcentages_coordonnees(pc_largeur, pc_hauteur, ret_pos=False))
        return (Fenetre.pourcentage_largeur(pc_largeur), Fenetre.pourcentage_hauteur(pc_hauteur))
    
    @overload
    @staticmethod
    def pourcentages_fenetre(pc_largeur : float, pc_hauteur : float, ret_vec : Literal[True] = True) -> Vecteur:
        """Raccourcit pour Vecteur(Fenetre.pourcentage_largeur(pc_largeur), Fenetre.pourcentage_largeur(pc_hauteur))"""
    
    @overload
    @staticmethod
    def pourcentages_fenetre(pc_largeur : float, pc_hauteur : float, ret_vec : Literal[False]) -> tuple[int, int]:
        """Raccourcit pour (Fenetre.pourcentage_largeur(pc_largeur), Fenetre.pourcentage_largeur(pc_hauteur))"""
    
    @staticmethod
    def pourcentages_fenetre(pc_largeur : float, pc_hauteur : float, ret_vec : bool = True) -> Vecteur|tuple[int, int]:
        if ret_vec:
            return Vecteur(Fenetre.pourcentages_coordonnees(pc_largeur, pc_hauteur, ret_pos=False))
        return (Fenetre.pourcentage_largeur(pc_largeur), Fenetre.pourcentage_hauteur(pc_hauteur))
    
    @staticmethod
    def vecteur_pourcentage(v : Vecteur) -> Vecteur:
        """pourcentages_fenetre() mais prend un vecteur en entrée."""
        return Vecteur(*Fenetre.pourcentages_fenetre(v.x, v.y))
    
    @staticmethod
    def pourcentage_hauteur_police(pourcents : float) -> int:
        """Renvoie pourcentage de la hauteur de l'écran en pixels pour une police."""
        return pixels_vers_taille_police(Fenetre.pourcentage_hauteur(pourcents))
    
    @staticmethod
    def construire_police(
            chemin  : Optional[str],
            hauteur : float,
            gras     : bool = False,
            italique : bool = False,
            souligne : bool = False,
            barre    : bool = False,
        ) -> Font:
        """Construit un objet Font avec une taille de police de `hauteur`% la taille de l'écran."""
        res = Font(chemin, Fenetre.pourcentage_hauteur_police(hauteur))
        res.set_bold(gras)
        res.set_italic(italique)
        res.set_underline(souligne)
        res.set_strikethrough(barre)
        return res
    
    @staticmethod
    def changer_taille_fenetre(nouvelle_taille : tuple[int, int]) -> None:
        """Change la taille de la fenetre."""
        pygame.display.set_mode(nouvelle_taille)
        
        Fenetre.largeur, Fenetre.hauteur = nouvelle_taille
        Fenetre.centre_fenetre = (Fenetre.largeur // 2, Fenetre.hauteur // 2)
    
    @staticmethod
    def display_flip() -> None:
        """Met à jour le display et si `reset_menu` est actif, remplit `menus_surf` avec de la transparence."""
        import parametres_vars as p
        if bool(p.mode_debug):
            surf : Surface = Fenetre.construire_police(FOURRE_TOUT, 10).render("Débug", True, ROUGE)
            Fenetre.blit_couche(
                2,
                surf,
                (Fenetre.largeur - surf.get_rect().width, 0)
            )
        
        for couche in Fenetre.couches_graphiques:
            Fenetre.surface.blit(couche)
        pygame.display.flip()
        
        for couche in Fenetre.couches_graphiques:
            couche.fill(TRANSPARENT)







# Le système d'overload est à la fois une bénédiction pour la fonctionnalité
# et une malédiction pour sa syntaxe.
@overload
def verifier_pour_quitter() -> None:
    """
    Vérifie si un évènement dans la file des evènements est un évènement permettant de sortir, s'il en existe un quitte immédiatement.
    Vide la file des évènements.
    La décision est prise par la version surchargée avec un évènement.
    """
    ...

@overload
def verifier_pour_quitter(ev : pygame.event.Event) -> None:
    """
    Vérifie si `ev` permet de quitter le jeu, il doit respecter au moins une de ces conditions:
    - Être de type `pygame.QUIT`;
    - Représenter l'appui de la touche `TOUCHE_QUITTER`.
    """
    ...

def verifier_pour_quitter(ev : Optional[pygame.event.Event] = None) -> None:
    if ev is not None:
        if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == Touches.QUITTER):
            quit()
        return
    
    for event in pygame.event.get():
        verifier_pour_quitter(event)




# La fonction ci-dessous devrait être dans fonction_vrac.py mais est requise par Jeu
def recherche_map[K, V](element : V, map : Mapping[K, V], si_pas_trouve : K) -> K:
    """
    Trouve la clef correspondante à `element` dans `map` ou `si_pas_trouve` s'il n'est pas dans la map.
    Si les valeurs du dictionnaire ne sont pas uniques, le résultat pourrait être imprévisible.
    Cette fonction n'est pas mémoisée car les dict ne sont pas hashables.
    """
    for clef, valeur in map.items():
        if valeur == element:
            return clef
    return si_pas_trouve