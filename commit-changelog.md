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
+ [fichier/classe]
	- [...]

--------------template--------------
## 
+ Changements majeurs
+ Sur plusieurs fichiers
+ Structure de fichier
+ READMEs et documentation
+ Interactions utilisateur
+ 
	- 
------------------------------------
-->
<!--
Nils: J'utilise l'ordre Ajout, Renommage, Déplacement, Modification, Effacement/Destruction, Autre.
-->
_____
## Meilleure répartition des méthodes
+ Changements majeurs
+ Sur plusieurs fichiers
	- Déplacements des fonctions de convertions de couleurs (`rgb_to_rgba()`, `color_to_rgb()`, ...) dans [Constantes.Couleurs](sources/Constantes/Couleurs.py).
	- Déplacements des fonctions `pourcentage_hauteur()` et `pourcentage_largeur()` dans la classe `Jeu`.
+ Structure de fichier
+ READMEs et documentation
+ Interactions utilisateur
	- La barre de vie est maintenant cyan quand elle est au max.
	- Les etats/interruptions utilisant `image_vers_generateur()` permettent maintenant de quitter le jeu.
	- Les iterruptions affichent maintenant des messages dans la console.
+ [dessin.py](sources/dessin.py)
	- Ajouts des paramètres `gerer_evenements` et `derniere_etape` à `image_vers_generateur()`.