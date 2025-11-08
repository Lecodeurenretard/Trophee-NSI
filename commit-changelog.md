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
## Les attaques ont leur JSON.
+ Changements majeurs
	- Ajout de [attaques.json](data/attaques.json).
	- Ajout de `_depuis_json_dict()`, `actualiser_liste()`
+ Sur plusieurs fichiers
+ Structure de fichiers
+ READMEs et documentation
	- Corrections et ajouts de nouvelles fonctionnalités dans [fight-system.md](doc/fight-system.md).
+ Interactions joueur/testeur
	- Les monstres n'affichent plus que l'ID de leurs types dans l'écran des informations.
	- Ajout de lignes pour séparer les informations des entités.
+ Correction de bugs
+ [Attaque.py](sources/Attaque.py)
	- Ajout de méthodes `.depuis_str()` aux classes `TypeAttaque` et `AttaqueFlag`.
	- Ajout de `IGNORER_DEFENSE` à `AttaqueFlag`.
	- Ajout de `.avec_nom()` à `Attaque`
	- Suppression de `ATTAQUE_ALLIES` et `ATTAQUE_EQUIPE` dans `AttaqueFlag`.
		* Renommage de `Attaque.peut_attaquer_allies()` en `Attaque.peut_attaquer_lanceur()`.
+ entités
	- `moveset[]` est maintenant une liste de noms d'attaques.
+ `Stat`
	- `.VITESSE_MAX` n'est plus dans le `.__repr__()`.