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
## Meilleur [fight-system.md](doc/fight-system.md).
+ Changements majeurs
	- Actualisation de [fight-system.md](doc/fight-system.md).
+ Sur plusieurs fichiers
	- Plus de commentaires et de docstrings
	- Transfer des fonctions `.index_carte_du_dessus()` et `.lever_carte_du_dessus()` de `Joueur` vers `Entite`.
+ Structure de fichiers
+ READMEs et documentation
+ Interactions joueur/testeur
	- Si une entité à plus que sa vie maximum, affiche sa barre de vie en jaune pièce (pour l'instant impossible).
+ Correction de bugs
+ `Attaque`
	- Les modifications de stats peuvent être `null` dans le JSON.
+ `Carte`
	- Suppression de `_DUREE_INTER_JEU` (inutilisé).
+ `Entite` (et descendantes)
	- Ajout de `vivants()` qui renvoie toutes les entités vivantes de même type ou de type fils à la classe quil'a appelé.
		* Par exemple, `Monstre.vivants()` renvoie tous les objets `Monstre` et `Boss`.
		* Suppression de `Monstre.vivants()` et `Boss.vivants_boss()` qui avaient ce but.
		* `vivantes` est maintenant	non publique.
	- Différentiation entre un reset _hard_ et _soft_ du deck.
		* `._reset_deck()` devient `._reset_deck_soft()`