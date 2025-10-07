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
## Création module [classes_utiles](sources/classes_utiles/).
+ Changements majeurs
	- Déplacement des fichiers:
		* Animation.py
		* Duree.py
		* EasingFunctions.py
		* Pos.py
	- `Easing` n'est maintenant utilisé que pour les consantes dans [EasingConstants.py](sources/classes_utiles/EasingConstants.py)
+ Sur plusieurs fichiers
	- Les constantes de [EasingFunctions.py](sources/classes_utiles/EasingFunctions.py) sont déplacées dans [EasingConstants.py](sources/classes_utiles/EasingConstants.py)
+ Structure de fichier
+ READMEs et documentation
+ Interactions utilisateur