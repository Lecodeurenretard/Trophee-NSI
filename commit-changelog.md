Ce fichier contient tous les changements faits dans les commits. Il est rafraichit à _à peu près_ chaque commit (si le commit est assez petit, c'est pas très grave si le fichier n'est pas mis-à-jour).

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
+ Structure de fichiers
+ READMEs et documentation
+ Interactions joueur/testeur
+ Correction de bugs
+ []()
	- 
------------------------------------
-->
_____
## Nouvelles dynamiques + Meilleure UI.
+ Changements majeurs
	- Le joueur est découragé d'utiliser tout le temps les mêmes attaques car l'adverdaire devient résilient.
+ Sur plusieurs fichiers
+ Structure de fichiers
+ READMEs et documentation
+ Interactions joueur/testeur
	- Une défense négative augmente les dégats prits, il n'y a plus de défense minimale.
	- Les infos sont dessinées audessus des cartes pour ne plus être cachées par les autres cartes.
	- Les stats ont maintenant un joli nom (user friendly).
		* Ajout de `Stat.joli_nom()`.
+ Correction de bugs
	- Les stats temporaires sont reset aux game overs