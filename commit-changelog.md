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
## Les decks sont des pools.
+ Changements majeurs
+ Sur plusieurs fichiers
+ Structure de fichiers
	- Renommage de TypeMonstre.py en [TypesEntite.json](data/JSON/TypesEntite.json).
+ READMEs et documentation
+ Interactions joueur/testeur
+ Correction de bugs
+ [Entite.py](sources/Entite.py)
	- Ajout de `EntiteJSON`.
		* Transfert des fonctionalités de `MonstreJSON`.
	- Ajout de `Entite._reset_deck()`.
	- Changer `Entite.cartes_main_max` peut enlever des cartes à la main.
	- Supression de `Entite._cartes_deck`.
+ `Pool`
	- Ajout de filtre lors de `.tirer_n()`.
	- Ajout de `.vider()`.
+ `Joueur`
	- Suppression de `STATS_DE_BASE`.