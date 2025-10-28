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
## Avancement doc + suppresion imports inutiles
+ Changements majeurs
	- Avancement de [Jeu.md](doc/Jeu.md).
+ Sur plusieurs fichiers
+ Structure de fichier
	- Suppression du suffixe `_placeholder` pour les sprites.
+ READMEs et documentation
+ Interactions joueur/testeur
+ Correction de bugs
+ [ex_anim.py](exemples/ex_anim.py)
	- Ajout de couleur gradient.
+ [fonctions_vrac.py](sources/fonctions_vrac.py)
	- Ajout `valeurs_regulieres()`.