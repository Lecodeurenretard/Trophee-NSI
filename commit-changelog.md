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
## Amélioration de la fonction `afficher_gif()` et ajout exemple.
+ Changements majeurs
	- dans `afficher_gif()`
		* Ajout de paramètres pour que le gif loop indéfiniement et pour qu'il soit scale 
		* Fusion des paramètres `chemin_dossier`, `debut_nom ` et `extention` en `pattern`.
		* La fonctions est maintenant un générateur pour ne pas interrompre l'état.
		* La fonction ne blit plus forcément sur `fenetre` mais sur une surface passée en argument.
		* Les gifs ne sont plus skippables.
	- Ajout d'un exemple pour utiliser `dessiner_gif()`.
+ Sur plusieurs fichiers
	- Déplacement de `afficher_gif()` de [UI.py](sources/UI.py) vers [dessin.py](sources/dessin.py).
		- Renommage en `dessiner_gif()`.
+ Structure de fichier
	- Renommage du répertoire annim/ en [anim/](data/anim/).
	- Renommage des frames du dossier pour qu'elles suivent le pattern `frame X.png`.
	- Ajout de frames pour l'exemple.
+ READMEs et documentation
+ Interactions joueur/testeur
	- Le testeur peut maintenant skip les animations des attaques.
+ Correction de bugs
+ [Chemins.py](sources/Constantes/Chemins.py)
	- Ajout de `DOSSIER_ANIM`.

_________________________________
note: promis je rédige la documentation pour le prochain commit.