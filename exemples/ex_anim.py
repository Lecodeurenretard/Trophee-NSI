import sys
from pathlib import Path
sys.path.insert(0, str(next(Path(__file__).parent.parent.glob('sources/'))))
# La ligne du dessus fais croire à Python que l'on se trouve dans `sources/` au  lieu de `exemple`
# Pourquoi doit-on écrire du spagetti code pour une chose aussi simple qu'importer depuis un autre dossier?



# VsCode n'aime pas la magie noire, il reporte 4 erreurs
import pygame
from Jeu                            import Jeu, verifier_pour_quitter
from Constantes.Couleurs            import BLANC, NOIR, BLEU_CLAIR
from classes_utiles.Animation       import MultiDeplacement
from classes_utiles.EasingConstants import FADE


diamant_gen = MultiDeplacement(
	[
		[Jeu.pourcentage_largeur(25), Jeu.pourcentage_largeur(50), Jeu.pourcentage_largeur(75), Jeu.pourcentage_largeur(50), Jeu.pourcentage_largeur(25)],	# x va boucler à travers ces valeurs
		[Jeu.pourcentage_hauteur(50), Jeu.pourcentage_hauteur(25), Jeu.pourcentage_hauteur(50), Jeu.pourcentage_hauteur(75), Jeu.pourcentage_hauteur(50)]	# y va boucler à travers ces valeurs
	],
	[
		[1/4, 1/2, 3/4],	# x atteindra 50 pourcents au quart (.25) de l'animation et 75 pourcents à la moitié (.50) de l'animation, ...
		[1/4, 1/2, 3/4]		# y atteindra 75 pourcents au quart (.25) de l'animation et 50 pourcents à la moitié (.50) de l'animation, ...
	]
).generateur(Jeu.framerate * 3, easing=FADE, loop=True)		# On crée un générateur pour facilement pouvoir animer à l'infini
															# On aurait aussi pu faire avec .caluler_valeur()

# vu qu'on a un générateur on aurait pu mettre une boucle for mais ça aurait été source de confusion
# for pos_rond in triangle_gen:
while True:
	Jeu.commencer_frame()
	verifier_pour_quitter()
	
	pos_rond = next(diamant_gen)
	Jeu.fenetre.fill(BLANC)
	
	# dessin diamant
	pygame.draw.polygon(
		Jeu.fenetre,
		BLEU_CLAIR,
		(
			(Jeu.pourcentage_largeur(25), Jeu.pourcentage_hauteur(50)),
			(Jeu.pourcentage_largeur(50), Jeu.pourcentage_hauteur(75)),
			(Jeu.pourcentage_largeur(75), Jeu.pourcentage_hauteur(50)),
			(Jeu.pourcentage_largeur(50), Jeu.pourcentage_hauteur(25)),
		),
		width=2
	)
	
	# dessin rond et affichage
	pygame.draw.circle(Jeu.fenetre, NOIR, pos_rond.tuple, 20)
	pygame.display.flip()