from imports import *
from Duree import Duree

def staticclass(cls):   # prend une classe et ressort une autre classe
    """Empèche les classes d'avoir un constructeur, on les force à être 'statiques'."""
    def __init__(self) -> NoReturn:
        # the humble = delete
        # the humble not defining constructor => can't create object
        # J'aime déclarer un décorateur pour une fonctionalité qui devrait être inscrite dans le langage.
        raise TypeError(f"On ne peut pas instancier d'objet de type `{cls.__name__}` car la classe est déclarée comme statique.")
    
    cls.__init__ = __init__
    return cls


Interruption : TypeAlias = Generator[Surface, None, None]

rgb   : TypeAlias = tuple[int, int, int]
rgba  : TypeAlias = tuple[int, int, int, int]
color : TypeAlias = rgb|rgba


@staticclass
class Constantes:
    """Classe spéciale pour les constates."""
    @classmethod
    def init(cls) -> None:
        cls.Polices.init()
        cls.Chemins.init()
    
    @staticclass
    class Touches:  # La méthodes des sous-classes est trop verbeuse, peut-être avec des modules?
        DBG_SKIP : tuple[int, ...] = (
            pygame.K_SPACE,
        )
        VALIDER : tuple[int, ...] = (
            pygame.K_SPACE,
            pygame.K_RETURN,    # entrée (return pour carriage return ou retour chariot sur les machines à écrire)
            pygame.K_KP_ENTER,  # entrée du pavé numérique
        )
        
        DBG_CRIT              : int = pygame.K_c
        DBG_PRECEDENT_COMBAT  : int = pygame.K_s
        DBG_PROCHAIN_COMBAT   : int = pygame.K_z
        
        DBG_PREDECENT_MONSTRE : int = pygame.K_q
        DBG_PROCHAIN_MONSTRE  : int = pygame.K_d
        
        INFOS                 : int = pygame.K_i
        SETTINGS              : int = pygame.K_TAB
        
        QUITTER               : int = pygame.K_ESCAPE
        
        @staticmethod
        def utilisateur_valide_menu(ev : pygame.event.Event) -> bool:
            """Vérifie si l'utilisateur valide dans un menu."""
            return ev.type == pygame.KEYDOWN and ev.key in Constantes.Touches.VALIDER
        
        @staticmethod
        def testeur_skip(ev : pygame.event.Event) -> bool:
            """Si en mode débug, le testeur veut skip."""
            from parametres_vars import mode_debug
            
            return mode_debug.case_cochee and ev.type == pygame.KEYDOWN and ev.key in Constantes.Touches.DBG_SKIP
    
    # @staticclass
    # class Couleurs:
    NOIR    : rgb = (0, 0, 0)
    BLANC   : rgb = (255, 255, 255)
    GRIS    : rgb = (100, 100, 100)
    GRIS_CLAIR : rgb = (145, 145, 145)
    
    ROUGE   : rgb = (255, 0, 0)
    VERT    : rgb = (0, 255, 0)
    BLEU    : rgb = (0, 0, 255)
    BLEU_CLAIR : rgb = (50, 50, 255)
    JAUNE      : rgb = (255, 255, 0)
    
    TRANSPARENT : rgba = (0, 0, 0, 0)
    
    @staticclass
    class Polices:
        TITRE       : pygame.font.Font = pygame.font.Font(None, 36)    # police par défaut de pygame
        TEXTE       : pygame.font.Font = pygame.font.Font(None, 25)
        FOURRE_TOUT : pygame.font.Font = pygame.font.Font(None, 50)
        
        @classmethod
        def init(cls) -> None:
            cls.TITRE.set_underline(True)
            
    
    @staticclass
    class Chemins:
        RACINE : str
        DOSSIER_IMG  : str
        DOSSIER_SAVE : str
        DOSSIER_ETC  : str
        
        @classmethod
        def init(cls):
            cls.RACINE = ''
            if getcwd().endswith("sources"):
                cls.RACINE = "../"    # rudimentaire mais fonctionnel
            else:
                logging.warning("Le dossier n'est pas reconnu, on suppose que l'on est à la racine.")
            
            cls.DOSSIER_IMG  = f"{cls.RACINE}data/img"
            cls.DOSSIER_SAVE = f"{cls.RACINE}data/save"
            cls.DOSSIER_ETC  = f"{cls.RACINE}data/etc"


@staticclass
class Jeu:
    """
    Classe statique gerant le jeu.
    Elle contient les variables globales.
    """
    LARGEUR : int = 800 ;   HAUTEUR : int = 600
    CENTRE_FENETRE : tuple[int, int] = (LARGEUR // 2, HAUTEUR // 2)
    MAX_COMBAT : int = 5
    
    fenetre    : Surface = pygame.display.set_mode((LARGEUR, HAUTEUR))
    menus_surf : Surface = Surface((LARGEUR, HAUTEUR), pygame.SRCALPHA)
    
    num_combat          : int   = 1
    tour_joueur         : bool  = True
    ecran_titre_running : bool  = True
    duree_execution     : Duree = Duree()
    clock               : pygame.time.Clock = pygame.time.Clock()
    
    
    
    # Graphe des états: http://graphonline.top/fr/?graph=ZCaEuQwPStCefLfb
    class Etat(Enum):
        DECISION_ETAT          = auto()
        CHOIX_ATTAQUE          = auto()
        AFFICHAGE_ATTAQUES     = auto()
        ATTENTE_NOUVEAU_COMBAT = auto()
        FIN_DU_JEU             = auto()
        
        ECRAN_TITRE            = auto()
        CREDITS                = auto()
    etat           : Etat = Etat.DECISION_ETAT
    precedent_etat : Etat = Etat.DECISION_ETAT
    
    
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
    def toggle_tour() -> None:
        Jeu.tour_joueur = not Jeu.tour_joueur
    
    @staticmethod
    def changer_etat(nouvel_etat : Etat) -> None:
        """Change l'état du jeu vers `nouvel_etat`."""
        Jeu.precedent_etat = Jeu.etat
        Jeu.etat           = nouvel_etat
    
    @staticmethod
    def commencer_frame(framerate : int = 60) -> None:
        """La fonction à appeler à chaque début de frame."""
        Jeu.duree_execution.millisecondes += Jeu.clock.tick(framerate)

Constantes.init()
Jeu.init()