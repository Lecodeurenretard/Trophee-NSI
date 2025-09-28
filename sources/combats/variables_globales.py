from imports import *
from constantes_globales import *
from Duree import Duree

pygame.display.set_caption("Menu Principal")

clock : pygame.time.Clock = pygame.time.Clock()

fenetre : Surface = pygame.display.set_mode((LARGEUR, HAUTEUR))
fenetre.fill(BLANC)

menus_surf : Surface = Surface((LARGEUR, HAUTEUR), pygame.SRCALPHA)

nbr_combat : int = 1
tour_joueur  : bool = True
menu_running : bool = True

# Toutes les entitées (joueurs, monstres ou None) vont dans cette liste
# leurs ID sera leur index dans cette liste
# de type list[Monstre|Joueur|None], le type n'est pas mis car les classes ne sont pas encore définies
entites_vivantes : list = []

temps_de_jeu : Duree = Duree()


# Graphe des états: http://graphonline.top/fr/?graph=ZCaEuQwPStCefLfb
class EtatJeu(Enum):
    DECISION_ETAT          = auto()
    CHOIX_ATTAQUE          = auto()
    AFFICHAGE_ATTAQUES     = auto()
    ATTENTE_NOUVEAU_COMBAT = auto()
    FIN_DU_JEU             = auto()
    
    ECRAN_TITRE            = auto()
    CREDITS                = auto()

etat_jeu           : EtatJeu = EtatJeu.DECISION_ETAT
precedent_etat_jeu : EtatJeu = EtatJeu.DECISION_ETAT