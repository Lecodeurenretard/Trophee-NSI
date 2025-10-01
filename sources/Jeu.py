from imports import *
from Duree import Duree

def staticclass(cls : type) -> type:
    """Empèche les classes d'avoir un constructeur, on les force à être 'statiques'."""
    def __init__(self, *autre : Any, **autres : Any) -> NoReturn:   # Englobe toutes les fonctions possibles dans Python
        """Lance une TypeError."""
        # the humble = delete
        # the humble not defining constructor => can't create object
        # J'aime déclarer un décorateur pour une fonctionalité qui devrait être inscrite dans le langage.
        raise TypeError(f"On ne peut pas instancier d'objet de type `{cls.__name__}` car la classe est déclarée comme statique.")
    
    cls.__init__ = __init__
    return cls


Interruption : TypeAlias = Generator[Surface, None, None]

# @staticclass # empèche pywright de typer les membres
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
    
    @classmethod
    def toggle_tour(cls) -> None:
        cls.tour_joueur = not cls.tour_joueur
    
    @classmethod
    def changer_etat(cls, nouvel_etat : Etat) -> None:
        """Change l'état du jeu vers `nouvel_etat`."""
        cls.precedent_etat = cls.etat
        cls.etat           = nouvel_etat
    
    @classmethod
    def commencer_frame(cls, framerate : int = 60) -> None:
        """La fonction à appeler à chaque début de frame."""
        cls.duree_execution.millisecondes += cls.clock.tick(framerate)

Jeu.init()