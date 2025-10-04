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
## Implémentation de gradients et amélioration des outils sur les fonctions d'easing.
+ Changements majeurs
	- Création de la classe `Gradient`.
	- Création de `EasingType`, `ecraser_easing()` et `inversement_ease()`.
+ Sur plusieurs fichiers
	- Déplacements des fonctions d'easing (`easing_square`, `easing_circular`, ...) vers l'enum `EasingType` dans [EasingFunctions.py](sources/EasingFunctions.py).
		* Suppression du prefixe `easing_` et mise en constantes.
	- `tour_joueur` n'est plus une variable globale.
+ Structure de fichier
	- Nouveau fichier [EasingFunctions.py](sources/EasingFunctions.py).
+ READMEs et documentation
+ Interactions utilisateur
	- Amélioration du faux chargement.
		* Ajout de contours à la barre.
		* Ajout de gradient à la barre: elle varie de rouge à vert suivant son niveau d'accomplissement.
		* Le temps de chargement est maintenant précis.
	- Baisse du temps du faux chargement: 7s -> 2s.
+ `InterpolationLineaire`
	- Correction de la logique pour `.generateur()`.
+ [fonctions_etats.py](sources/fonctions_etats.py)
	- Début d'implémentation de l'état `afficher_attaques()`.
	- Implémentation de l'état `FIN_JEU` bien qu'il soit innacéssible pour l'instant.

+ [fonctions_vrac.py](sources/fonctions_vrac.py)
	- Réimplémentation de la fonction `attendre()`, cette fois-ci elle joue que prenait `time.sleep()`.
+ `Jeu`
	- Ajout de la variable globale `a_gagne`.
	- Modification de `commencer_frame()` pour qu'elle retourne la durée de la dernière frame.
	- Suppression de `toggle_tour()`.
+ [UI.py](sources/UI.py)
	- Réécriture de `faux_chargement()`. v. Interactions utilisateur