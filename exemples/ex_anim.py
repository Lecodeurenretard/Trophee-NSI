import sys
from pathlib import Path
sys.path.insert(0, str(next(Path(__file__).parent.parent.glob('sources/'))))
# La ligne du dessus fais croire à Python que l'on se trouve dans `sources/` au  lieu de `exemple`
# Pourquoi doit-on écrire du spagetti code pour une chose aussi simple qu'importer depuis un autre dossier?



# VsCode n'aime pas la magie noire, il reporte 5 erreurs
import pygame
from Jeu                            import Jeu, Fenetre, verifier_pour_quitter
from Constantes.Couleurs            import BLANC, NOIR, BLEU_CLAIR, BLEU, ROUGE, VERT, GRIS
from classes_utiles.Animation       import MultiDeplacement, MultiGradient
from classes_utiles.EasingConstants import FADE
from classes_utiles.Pos import Pos


diamant_gen = MultiDeplacement.generateur_s(
	[
		Fenetre.pourcentages_coordonnees(25, 50),
		Fenetre.pourcentages_coordonnees(50, 25),
		Fenetre.pourcentages_coordonnees(75, 50),
		Fenetre.pourcentages_coordonnees(50, 75),
		Fenetre.pourcentages_coordonnees(25, 50),
	],
	[	# sur une fenêtre carrée de 100 pixel de côté, le rond atteindra (50, 25) au quart (.25) de l'animation, (75, 50) à la moitié (.50) de l'animation, ...
		1/4,
		1/2,
		3/4
	],
	Jeu.framerate * 3,
	easing_fun=FADE,
	loop=True,
)		# On crée un générateur pour facilement pouvoir animer à l'infini
															# On aurait aussi pu faire avec .caluler_valeur()

# on pourrat aussi faire comme en haut et utiliser generateur_s() (les temps ne seraient plus falcutatifs)
couleur_gen = MultiGradient(
	[
		GRIS,
		ROUGE,
		VERT,
		BLEU,
		GRIS,
	]
	# les temps sont facultatifs
).generateur(Jeu.framerate * 3 , easing_fun=FADE, loop=True)	

# vu qu'on a un générateur on aurait pu mettre une boucle for mais ça aurait été source de confusion
# for pos_rond in triangle_gen:
while True:
	Jeu.commencer_frame()
	verifier_pour_quitter()
	
	pos_rond = next(diamant_gen)
	coul_rond = next(couleur_gen)
	Fenetre.surface.fill(BLANC)
	
	# dessin diamant
	pygame.draw.polygon(
		Fenetre.surface,
		BLEU_CLAIR,
		(
			Fenetre.pourcentages_coordonnees(25, 50, ret_pos=False),
			Fenetre.pourcentages_coordonnees(50, 75, ret_pos=False),
			Fenetre.pourcentages_coordonnees(75, 50, ret_pos=False),
			Fenetre.pourcentages_coordonnees(50, 25, ret_pos=False),
		),
		width=2
	)
	
	# dessin rond et affichage
	pygame.draw.circle(Fenetre.surface, coul_rond, pos_rond.tuple, 20)
	pygame.display.flip()