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
## Restructuration de [data/](data/) + les cartes se lèvent.
+ Changements majeurs
+ Sur plusieurs fichiers
+ Structure de fichiers
	- Le répertoire [data/](data/) est mieux organisé.
		* Les cartes ont maintenant 1 dossier par carte.
		* Les JSONs ont leurs dossier
+ READMEs et documentation
	- Ajout d'un README dans [data/](data/).
+ Interactions joueur/testeur
	- Les cartes se lèvent quand la souris les survole.
+ Correction de bugs
	- Patch du bug dans `Array`.
+ `Button`
	- Traduction en français.