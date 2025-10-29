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
## Fin de la documentation (pour l'instant).
+ Changements majeurs
	- Ajout titre et section "Retour sur les classes" dans [Jeu.md](doc/Jeu.md)
+ Sur plusieurs fichiers
+ Structure de fichier
+ READMEs et documentation
+ Interactions joueur/testeur
	- Le texte du haut de fenètre change suivant la partie du jeu dans lequel le joueur se trouve.
	- Les pseudo ne peuvent plus être que des espaces ou contenir deux caractères blancs côte à côtes.
+ Correction de bugs
+ [Animation.py](sources/classes_utiles/Animation.py)
	- Ajout à toutes les classes de méthodes statiquess ou non pour qu'elles aie toutes un constructeur, un `.__repr__()`, et les méthodes `generateur_s()`, `calculer_valeur_s()`, `.generateur()`, `.calculer_valeur()`.
		* Modification de [ex_anim.py](exemples/ex_anim.py) pour inclure les nouvelles méthodes.
	- Regroupement de la logique des méthodes `.generateur()` dans la fonction `_generer_generateur()` (et `_generer_generateur_multi()`).