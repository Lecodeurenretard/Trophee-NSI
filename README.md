# L'ascension d'Esquimot
L'ascension d'Esquimot est un RPG/Roguelite tour par tour inspiré de PokéRogue.
Toutes les attaques se font par des cartes.
Le joueur a aussi accès à un shop qui lui permet d'acheter des items pouvant modifier ses statistiques (attaque, défense, ...). A la fin de chacun des trois étages, Esquimot affronte un boss ayant une mécanique unique.

## Jouer au jeu
Pour jouer au jeu, il faut avoir Python les dépendances installées comme indiqué dans [la prochaine section](#configuration-minimum), si vous savez pas comment faire suivez les indications dans [Installer.md](Installer.md).

Une faois prêt, lancer le jeu en double-cliquant sur [sources/main.py](sources/main.py) ou en le lançant depuis la ligne de commande si Tkinter n'est pas disponible (il l'est sur Windows et mac).

## Configuration minimum
+ [Python 3.14.2](https://www.python.org/downloads/release/python-3142/) ou plus récent
	- TKinter, installé par défaut sur Windows, Mac et _la plupart_ des systèmes UNIX.
		* Si Tkinter n'est pas disponible (sur Linux Mint par exemple), il faudra le jeu dans le terminal car certaines informations seront communiquées par la console.
+ [Pygame 2.6](https://www.pygame.org/news) ou plus récent

Pas de configuration minimum pour les composants du PC à moins que ce soit littéralement une patate.

## Les touches
Les touches sont dans [Touches.md](Touches.md).

## Crédits
Jeu produit pour Les Trophées de NSI par:
+ **[LeRetardatN](https://github.com/Lecodeurenretard)**: Le code et la documentation.
+ **[Dooheli](https://github.com/Dooheli)**: Les graphismes.
+ **[hibou509](https://github.com/hibou509)**: Système de combat, béta-test et équilibrage.

## Usage de l'IA
L'utilisation de LLM est restriente au débogage. Nous entendons par "débogage" l'aide utilisée pour résoudre un problème empêchant de jouer au jeu (plantage, erreur, ...).