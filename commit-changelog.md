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
## Ajout de sound effects.
+ Changements majeurs
	- Des SFX ont été ajoutés pour:
		* Les boutons
		* Les attaques
		* Le gain/la perte d'argent
	- Ajout de dossier [sfx/](data/sfx/) dans [data/](data/).
		* Ajout da la constante `SFX` dans [Chemins.py](sources/Constantes/Chemins.py).
+ Sur plusieurs fichiers
+ Structure de fichiers
+ READMEs et documentation
+ Interactions joueur/testeur
	- Quand l'attaque fatale pour le monstre est skip, la barre de vie est bien actualisée.
	- On ne peut plus payer si l'item est déjà dans l'inventaire.
+ Correction de bugs
+ `Attaque`
	- Ajout des constantes statiques `SON_COUP`, `SON_HEAL` et `SON_CRIT`.
	- Ajout de la méthode `.jouer_sfx()`.
+ `Button`
	- Ajout de la constante statique `SON_APPUI`.
	- Ajout de la méthode `.jouer_sfx()`.



_______
Il faudra changer les SFX plus tard.