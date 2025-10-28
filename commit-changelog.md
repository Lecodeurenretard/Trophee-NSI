Ce fichier contient tous les changements faits dans les commits. Il est rafraichit à chaque commits.
Un bon moyen de savoir si le changement devrait être écrit ici, c'est de se demander si il changera la façcon d'interagir sur la fonction/classe.

<!--
format:
## [message du commit]
+ Changements majeurs
	- [Changements à la base du but du commit]
+ Sur plusieurs fichiers
	- [Autres changements?]
+ Structure de fichier
	- [Changements sur la structure de ficher]
+ READMEs et documentation
	- [Changements dans la doc?]
+ Interaction joueur/testeur
	- [Changement touches/dialogue/...]
+ Correction de bug
	- [Interaction joueur/testeur mais pour les corrections de bugs]
+ [fichier/classe]
	- [...]

--------------template--------------
## 
+ Changements majeurs
+ Sur plusieurs fichiers
+ Structure de fichier
+ READMEs et documentation
+ Interactions joueur/testeur
+ Correction de bugs
+ []()
	- 
------------------------------------
-->
<!--
Nils: J'utilise l'ordre Ajout, Renommage, Déplacement, Modification, Effacement/Destruction, Autre.
-->
_____
## Encore plus de méthodes d'animations + nouvel état.
+ Changements majeurs
	- Ajout de classes pour interpoler entre plus que deux valeurs:
		* `MultiInterpolation`
		* `MultiGradient`
		* `MultiDeplacement`
	- Ajout état `PREPARATION`.
		* Ajout `preparation()` dans [fonctions_etats.py](sources/fonctions_etats.py).
		* Suppression `lancer_jeu()` dans [fonctions_boutons](sources/fonctions_boutons.py).
+ Sur plusieurs fichiers
+ Structure de fichier
	- Ajout documentation [Jeu.md](doc/Jeu.md).
	- Ajout exemple [ex_anim.py](exemples/ex_anim.py).
+ READMEs et documentation
	- Début documentation sur le jeu et les méthodes d'animaations.
+ Interactions joueur/testeur
+ Correction de bugs
+ [Animation.py](sources/classes_utiles/Animation.py)
	- Ajout paramètre `loop` aux méthodes `.generateur()` des classess.
+ [Couleurs.py](sources/Constantes/Couleurs.py)
	- Ajout fonctions `iterable_to_color()`, `iterable_to_rgb()` et `iterable_to_rgba()` pour assert un type de couleur sur une valeur.
+ [fonctions_boutons.py](sources/fonctions_boutons.py)
	- Un seul point de sortie pour `menu_parametres()`.
	- `menu_parametres()` écoute maintenant pour des `GeneratorExit` (on peut l'arrêter avec `.close()`).
+ [fonctions_main.py](sources/fonctions_main.py)
	- `nouveau_combat()` ne renvoie plus l'image de nouveau combat.
	- Renommage de `nouveau_combat()` --> `initialiser_nouveau_combat()`.
+ `Jeu`
	- Nouvel attriibut statique `framerate`.
	- Ajout méthode `changer_taille_fenetre()`.
	- Les attributs statiques `HAUTEUR` et `LARGEUR` ne sont plus constants.
		* Renommage vers `hauteur` et `largeur`.s