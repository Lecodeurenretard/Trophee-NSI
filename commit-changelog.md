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
## Amélioration de l'API des boss.
+ Changements majeurs
	- Ajout de l'attribut JSON "autres_attributs" pour apporter des données supplémentaire au boss (évite de les hardcoder dans fonctions_boss).
		* Ajout du membre dans `BossJSON` et est servi lors de l'initialisation de `attributs_supplementaires[]`.
+ Sur plusieurs fichiers
+ Structure de fichiers
+ READMEs et documentation
	- Ajout du binaire dans le README.
+ Interactions joueur/testeur
	- Le démon change bien tout les 2 tours.
+ Correction de bugs
	- Les boutons pour cherche le boss et le shop cherchent à partir du combat suivant et n'excluent plus le dernier combat.
+ `Stat`
	- Ajout de la méthode `.copier()` qui permet la copie en place d'un autre objet `Stat`.