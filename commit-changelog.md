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
## Adaptation de l'interface des boss pour les cartes et les items.
+ Changements majeurs
	- Ajout de `CarteInterfaceMethodes`.
		* Ajout de `Carte.callbacks`.
		* Ajout de `carte.interface`
	- Même chose pour Item.
+ Sur plusieurs fichiers
	- Création de [fonctions_cartes.py](sources/fonctions_cartes.py).
+ Structure de fichiers
+ READMEs et documentation
+ Interactions joueur/testeur
	- Correction de fautes d'orthographes/grammaire.
+ Correction de bugs
+ `Item`
	- Les items peuvent être en promotion.