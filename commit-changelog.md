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
## Bugfix no1
+ Changements majeurs
+ Sur plusieurs fichiers
+ Structure de fichiers
+ READMEs et documentation
	- Ajout d'un guide de lancement.
	- Meilleur README pour les trophées.
+ Interactions joueur/testeur
	- Les stats sont arrondies aux joueur.
+ Correction de bugs
	- Les attaques ne changeant aucunes stats n'enlèvent plus 100 aux stats.
	- Les logs sont activés dès le départ quand le mode débug est lancé de base.
+ `ListeStable`
	- `.__contains__()` peut renvoyer true.
+ `Carte`
	- Meilleur `.__repr__()`
+ `Jeu`
	- Ajout de `verifier_parametre()` pour avoir un meilleur message d'erreur en cas deparamètre non trouvé.