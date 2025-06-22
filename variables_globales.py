import pygame
import sys
import time
import random
from math import isnan
from typing import TypeAlias, Callable, TypeVar, NoReturn, Any
from copy import copy, deepcopy

from Stat import *

pygame.init()
pygame.display.set_caption("Menu Principal")

LARGEUR : int = 800 ;   HAUTEUR : int = 600

color : TypeAlias = tuple[int, int, int]
NOIR    : color = (0, 0, 0)
BLANC   : color = (255, 255, 255)
GRIS    : color = (100, 100, 100)

ROUGE   : color = (255, 0, 0)
VERT    : color = (0, 255, 0)
BLEU    : color = (0, 0, 255)
BLEU_CLAIR : color = (50, 50, 255)
JAUNE   : color = (255, 255, 0)

MAX_COMBAT : int = 5	# combat maximum (nbr_combat <= MAX_COMBAT)

INVICIBLE_ENNEMI : bool = False

UI_LONGUEUR_BARRE_DE_VIE : int = 200

POLICE_GRAND : pygame.font.Font = pygame.font.Font(None, 36)
POLICE_PETIT : pygame.font.Font = pygame.font.Font(None, 25)

TEXTE_VICTOIRE      : pygame.Surface = POLICE_GRAND.render("Vous avez gagné !", True, NOIR)
TEXTE_DEFAITE       : pygame.Surface = POLICE_GRAND.render("Vous avez perdu !", True, NOIR)
TEXTE_INFO_UTILISER : pygame.Surface = POLICE_PETIT.render("SPACE : utiliser", True, BLANC)
TEXTE_INFO_INFO     : pygame.Surface = POLICE_PETIT.render("I : info"        , True, BLANC)

# Un nombre indéterminé, comme None mais exclusivement pour les nombres
# N'est égal à aucun nombre, même lui-même (NAN != NAN)
# Pour vérifier si un nombre est nan, utiliser `math.isnan(x)`
NaN : TypeAlias = float
NAN : NaN = float("nan")


clock : pygame.time.Clock = pygame.time.Clock()

fenetre : pygame.Surface = pygame.display.set_mode((LARGEUR, HAUTEUR))
fenetre.fill(BLANC)

police : pygame.font.Font = pygame.font.SysFont(None, 50)

nbr_combat : int = 1
tour_joueur : bool = True

pos : TypeAlias = tuple[int, int]
curseur_pos_attendue_x : pos= (50, 350)
curseur_pos_attendue_y : pos= (13 * HAUTEUR // 16, 13 * HAUTEUR // 16 + 70)
curseur_x, curseur_y = curseur_pos_attendue_x[0], curseur_pos_attendue_y[0]

assert(len(curseur_pos_attendue_x) == len(curseur_pos_attendue_y))	# filet de sécurité

menu_running : bool = True

# Toutes les entitées (joueurs, monstres ou None) vont dans cette liste
# leurs ID sera leur index dans cette liste
entitees_vivantes : list = []