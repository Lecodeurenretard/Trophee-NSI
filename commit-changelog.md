Ce fichier contient tous les changements faits dans les commits. Il est rafraichit à chaque commits.
Un bon moyen de savoir si le changement devrait être écrit ici, c'est de se demander si il changera la façcon d'interagir sur la fonction/classe.

<!--
format:
## [message du commit]
+ Changements majeurs
	- [Changements à la base du but du commit?]
+ Sur plusieurs fichiers
	- [Autres changements?]
+ Structure de fichier
	- [changements sur la structure de ficher?]
+ READMEs et documentation
	- [changements dans la doc?]
+ Interaction joueur/testeur
	- [Changement touches/dialogue/...]
+ [fichier/classe]
	- [changements...]
+ [...]


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
## Centralisation des variables (et constantes) globales
+ Changements majeurs
	- Ajout des classes `Jeu` et `Constantes`.
+ Sur plusieurs fichiers
	- Déplacements des variables globales dans la classe `Jeu`.
		- Déplacements des fonctions directements reliées comme `changer_etat()`.
		- Déplacement de l'enum `EtatJeu` et renommage en `Etat`.
+ Structure de fichier
	- Création de [Jeu.py](sources/Jeu.py)
+ READMEs et documentation
+ Interactions utilisateur