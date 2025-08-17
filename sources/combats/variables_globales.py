from imports import *

from constantes_globales import *
from Stat import *
from Pos import *

pygame.display.set_caption("Menu Principal")

clock : pygame.time.Clock = pygame.time.Clock()

fenetre : pygame.Surface = pygame.display.set_mode((LARGEUR, HAUTEUR))
fenetre.fill(BLANC)


nbr_combat : int = 1
tour_joueur  : bool = True
menu_running : bool = True

# Toutes les entitées (joueurs, monstres ou None) vont dans cette liste
# leurs ID sera leur index dans cette liste
# de type list[Monstre|Joueur|None], le type n'est pas mis car les classes ne sont pas encore définies
entitees_vivantes : list = []

delta : int = 0