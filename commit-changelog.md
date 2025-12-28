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
_____
## Implémentation de la classe Entite (dernière étape de l'implémentation des cartes).
+ Changements majeurs
	- Ajout de la classe `Entite`, mère de `Joueur` et de `Monstre`
		* Refactorisations
+ Sur plusieurs fichiers
+ Structure de fichiers
	- Suppression de globales_variables.py
+ READMEs et documentation
+ Interactions joueur/testeur
	- Le joueur a un reset des cartes à chaque début de combat et repioche à chaque début de tour.
	- On peut enfin jouer!
+ Correction de bugs
+ `Attaque`
	- Nouvel attribut statique `_dico_entites[]` pour avoir une référence sur `Entite.vivantes[]` pendan le runtime.
		* setter `set_dico_entites()`
+ `Entite` et descendants
	- Création de la classe abstraite `Entite`.
		* Toutes les méthodes redondantes entre `Joueur` et `Monstre` y ont été déplacé.
	- Beaucoups de renommages.
	- 187 lignes de moins dans [Joueur.py](sources/Joueur.py) et 102 de moins dans [Monstre.py](sources/Monstre.py).
+ `MonstreJSON`
	- Ajout d'un attribut oublié: `nb_cartes_main`.
+ `Stat`
	- `depuis_dictionnaire_json()` lance une erreur quand elle rencontre une clef inconnue.


_______________
Tout marche correctement sauf le lancer de carte qui lag toujours.