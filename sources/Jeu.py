from imports import *
from classes_utiles import Duree
from Constantes import Touches
from Constantes.Couleurs import TRANSPARENT, ROUGE
from Constantes.Polices import FOURRE_TOUT

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
    largeur : int = 800 ;   hauteur : int = 600
    centre_fenetre : tuple[int, int] = (largeur // 2, hauteur // 2)
    MAX_COMBAT : int = 10
    DECISION_SHOP : Callable[[int], bool] = lambda num_combat: num_combat % 5 == 0 and num_combat != Jeu.MAX_COMBAT
    
    fenetre    : Surface = pygame.display.set_mode((largeur, hauteur))
    menus_surf : Surface = Surface((largeur, hauteur), pygame.SRCALPHA)
    infos_surf : Surface = Surface((largeur, hauteur), pygame.SRCALPHA)
    
    num_etape          : int   = 1
    a_gagne             : bool = False
    
    duree_execution     : Duree = Duree()
    clock               : pygame.time.Clock = pygame.time.Clock()
    framerate           : int = 60
    
    volume_musique : float = 1
    volume_sfx     : float = 1
    volume_global  : float = 1
    
    
    # Graphe des états: http://graphonline.top/fr/?graph=OMlRPwRCzhQxYjcl
    class Etat(Enum):
        DECISION_ETAT          = auto()
        ATTENTE_PROCHAINE_ETAPE = auto()
        CHOIX_ATTAQUE          = auto()
        AFFICHAGE_ATTAQUES     = auto()
        GAME_OVER              = auto()
        SHOP                   = auto()
        
        ECRAN_TITRE            = auto()
        CREDITS                = auto()
        PREPARATION            = auto()
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
        
        return Duree(ms=delta)
    
    @staticmethod
    def pourcentage_hauteur(pourcents : float) -> int:
        """Renvoie pourcentage de la hauteur de l'écran en pixels"""
        return round(Jeu.hauteur * pourcents / 100)
    
    @staticmethod
    def pourcentage_largeur(pourcents : float) -> int:
        """Renvoie pourcentage de la largeur de l'écran en pixels"""
        return round(Jeu.largeur * pourcents / 100)
    
    @staticmethod
    def changer_taille_fenetre(nouvelle_taille : tuple[int, int]) -> None:
        """Change la taille de la fenetre."""
        pygame.display.set_mode(nouvelle_taille)
        
        Jeu.largeur, Jeu.hauteur = nouvelle_taille
        Jeu.centre_fenetre = (Jeu.largeur // 2, Jeu.hauteur // 2)
    
    @staticmethod
    def display_flip(reset_menu : bool = True, reset_infos : bool = True) -> None:
        """Met à jour le display et si `reset_menu` est actif, remplit `menus_surf` avec de la transparence."""
        import parametres_vars as p
        if bool(p.mode_debug):
            surf : Surface = FOURRE_TOUT.render("Débug", True, ROUGE)
            Jeu.infos_surf.blit(
                surf,
                (Jeu.largeur - surf.get_rect().width, 0)
            )
        
        Jeu.fenetre.blit(Jeu.menus_surf, (0, 0))
        Jeu.fenetre.blit(Jeu.infos_surf, (0, 0))
        pygame.display.flip()
        
        if reset_menu:
            Jeu.menus_surf.fill(TRANSPARENT)
        if reset_infos:
            Jeu.infos_surf.fill(TRANSPARENT)
    
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