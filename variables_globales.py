import pygame
import sys
import time
import random


pygame.init()
pygame.display.set_caption("Menu Principal")

clock = pygame.time.Clock()

LARGEUR = 800 ;   HAUTEUR = 600
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))

NOIR    = (0, 0, 0)
BLANC   = (255, 255, 255)
GRIS    = (100, 100, 100)

ROUGE   = (255, 0, 0)
VERT    = (0, 255, 0)
BLEU    = (0, 0, 255)
BLEU_CLAIR = (50, 50, 255)

MAX_COMBAT = 5	# combat maximum (nbr_combat <= MAX_COMBAT)

INVICIBLE_PLAYER = False    # [titlecard]
INVICIBLE_ENNEMI = False

UI_LONGUEUR_BARRE_DE_VIE = 200

police = pygame.font.SysFont(None, 50)
fenetre.fill(BLANC)

nbr_combat = 1

police_ecriture  = pygame.font.Font(None, 36)
police_ecriture2 = pygame.font.Font(None, 25)

texte_gagner        = police_ecriture.render("Vous avez gagné !", True, NOIR)
texte_perdu         = police_ecriture.render("Vous avez perdu !", True, NOIR)
texte_torgnole      = police_ecriture.render("Torgnole"         , True, BLANC)
texte_soin          = police_ecriture.render("Soin"             , True, BLANC)
texte_magique       = police_ecriture.render("Att. magique"     , True, BLANC)
texte_input_ligne1  = police_ecriture2.render("SPACE : utiliser", True, BLANC)
texte_input_ligne2  = police_ecriture2.render("I : info"        , True, BLANC)

tour_joueur = True
charge_puissance = 20
att_magique_puissance = 45

barre_vie_remplie_adversaire, barre_vie_remplie_joueur = UI_LONGUEUR_BARRE_DE_VIE, UI_LONGUEUR_BARRE_DE_VIE

perso_stat   = {"vie": 50, "force": 35, "defense": 40, "magie": 20, "defense_magique": 30, "vitesse": 50}
blob_stat    = {"vie": 40, "force": 30, "defense": 45, "magie": 0 , "defense_magique": 25, "vitesse": 30}
sorcier_stat = {"vie": 30, "force": 10, "defense": 30, "magie": 15, "defense_magique": 80, "vitesse": 60}
monstre_stat = {}

curseur_x, curseur_y = 50, (13*(HAUTEUR//16))

joueur_vie  = perso_stat["vie"]
monstre_vie = 0

menu_running = True
couleur = NOIR

nom_adversaire = ""
pseudo_joueur = ""