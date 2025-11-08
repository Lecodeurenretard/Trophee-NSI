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
+ Structure de fichiers
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
## Les monstres ont leur JSON.
+ Changements majeurs
	- Ajout de [TypeMonstres.json](data/TypesMonstre.json).
	- Ajout de `MonstreJSON` pour parse le JSON.
		* La classe reprend les méthodes `.type_precedent()` et `.type_suivant()`.
		* Suppression de `TypeMonstre`.
+ Sur plusieurs fichiers
+ Structure de fichiers
	- _blob.png_ et _sorcier.png_ ont été déplacés dans le dossier [monstres/](data/img/monstres/).
	- Ajout d'une [image d'erreur](data/img/erreur.png).
+ READMEs et documentation
+ Interactions joueur/testeur
	- Les carrés pour les persos en mode débug sont enlevés et remplacés par un indicateur en haut à droit de l'écran.
	- Changement des messages des items "Teto maigre" et "Peluche d'Hornet".
	- _Tweak_ des stats des monstres, joueur et de la constante pour la puissance des crits.
	- Un crit ne peut plus baisser les dégats de l'attaque, les dégats serons (sauf cas exceptionnel) toujours augmentés par un facteur d'au moins `PUISSANCE_CRIT` ($1.3$ pour l'insant).
+ Correction de bugs
	- L'étoile s'affiche quand un crit est lancé.
+ [fonctions_vrac.py](sources/fonctions_vrac.py)
	- Ajout de `clamp()` (2 overloads) en raccourcit.
+ `Item`
	- Renommage de la constante statique `TOUT_LES_ITEMS[]` en `DONNEES_ITEMS[]`.
+ [Monstre.py](sources/Monstre.py)
	- Renommage de `Monstre.dimensions_sprites[]` en `Monstre.SPRITE_DIM`.
	- `Monstre.spawn()` pioche dans tous les types du JSON sauf l'exemple.
	- On ne parle plus de la "classe" d'un monstre mais de son "rang".