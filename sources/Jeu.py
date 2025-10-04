from imports import *
from Duree import Duree
from Constantes import Touches

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

# J'ai commenté le décorateur car il empèche pywright de détecter les membre
# En principe, Le code devrait marcher même avec le décarateur d'activé.
# @staticclass
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
        ATTENTE_NOUVEAU_COMBAT = auto()
        CHOIX_ATTAQUE          = auto()
        AFFICHAGE_ATTAQUES     = auto()
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
    
    @staticmethod
    def pourcentage_hauteur(pourcents : float) -> int:
        """Renvoie pourcentage de la hauteur de l'écran en pixels"""
        return round(Jeu.HAUTEUR * pourcents / 100)
    
    @staticmethod
    def pourcentage_largeur(pourcents : float) -> int:
        """Renvoie pourcentage de la largeur de l'écran en pixels"""
        return round(Jeu.LARGEUR * pourcents / 100)


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

@overload
def testeur_skip_ou_quitte() -> bool:
    """
    Vérifie si un évènement dans la file des evènements est un évènement permettant de sortir, s'il en existe un quitte immédiatement.
    La fonction vérifie aussi si le testeur veut skip, dans ce cas là elle renvoie `True`.
    Vide la file des évènements.
    La décision est prise par la version avec un argument.
    """
    ...
@overload
def testeur_skip_ou_quitte(ev : pygame.event.Event) -> bool:
    """
    Vérifie si `ev` permet de quitter le jeu, il doit respecter au moins une de ces conditions:
    - Être de type `pygame.QUIT`;
    - Représenter l'appui de la touche `TOUCHE_QUITTER`.
    
    La fonction vérifie aussi si le testeur veut skip dans ce cas là elle renvoie `True`.
    """
    ...

def testeur_skip_ou_quitte(ev : Optional[pygame.event.Event] = None) -> bool:
    if ev is not None:
        verifier_pour_quitter(ev)
        return Touches.testeur_skip(ev)
    
    for ev in pygame.event.get():
        if testeur_skip_ou_quitte(ev):
            return True
    return False