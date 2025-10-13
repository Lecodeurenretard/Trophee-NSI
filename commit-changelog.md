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
## Petit bugfix
+ Changements majeurs
+ Sur plusieurs fichiers
	- Renommage de l'état `FIN_JEU` en `GAME_OVER`.
		* La fonction correspondante à aussi été renommée.
+ Structure de fichier
+ READMEs et documentation
+ Interactions joueur/testeur
+ Correction de bugs
	- La vie et le numéro de combat sont correctements resets après un game over.
	- Le joueur ne verra plus la frame de trop à la fin du temps de chargement.
	- Correction d'une erreur d'_overflow_ quand on défile à travers les monstres en mode débug.
	- Correction d'une erreur d'_overflow_ quand on défile à travers les combats en mode débug.

_________________________________
note: promis je rédige la documentation pour le prochain commit.