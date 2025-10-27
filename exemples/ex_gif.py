import sys
from pathlib import Path
sys.path.insert(0, str(next(Path(__file__).parent.parent.glob('sources/'))))
# La ligne du dessus fais croire à Python que l'on se trouve dans `sources/` au  lieu de `exemple/`

# Etonnamment cet exemple n'affiche qu'une seule erreur sur VS Code


from dessin import dessiner_gif, pygame, Duree, verifier_pour_quitter, Jeu, Constantes

# Création du générateur
dessin_gif = dessiner_gif(Jeu.fenetre, "exemples/gif/frames/*.png", Duree(ms=30), Jeu.CENTRE_FENETRE, loop=True, scale=True)

print("Exemple: Comment dessiner un gif.")
while True:
	Jeu.commencer_frame()	# Le générateur s'appuie sur l'horloge interne, il est nécéssaire le l'actualiser
	verifier_pour_quitter()
	
	next(dessin_gif)		# Dessine le gif
	pygame.display.flip()