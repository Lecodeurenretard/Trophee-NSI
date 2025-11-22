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
## Ajustements
+ Changements majeurs
	- Le joueur peut prendre plusieurs fois le même item, l'effet sera amplifié à chaque doublon.
	- Nouveau bouton "actualiser données" qui évite de tout le temps ouvrir/fermer le jeu lors d'un équilibrage.
	- Equilibrage
		* Les attaques "Soin", "Magie" et "Torgbole" ont leurs puissances fortement baissées.
		* L'objet "Teto maigre" a été nerf.
		* L'objet "Peluche d'Hornet" a été fortement nerf.
		* Les blobs sont plus résistants face à la magie.
		* Les sorciers ont leur défense (physique et magique) nerf. Leur résistance aux crit baissée aussi.
+ Sur plusieurs fichiers
+ Structure de fichiers
+ READMEs et documentation
+ Interactions joueur/testeur
	- Le nom d'utilisateur ne peut plus être juste des caractère blancs.
+ Correction de bugs
+ `Attaque`
	- Nouvelle méthode `.actualiser()`.
+ `Button`
	- Nouvelle propriété `.rect`.
	- Nouvelle méthode `.change_pos()`.
		* Elève une `NotImplementedError` dans la version de `ButtonCursor`.
	- Renommage de `.in_butt_hit()` en `.mouse_on_butt()`.
	- `.check_click()` joue un son et renvoie `True` même s'il n'y a pas de callback.
+ [fonctions_boutons.py](sources/fonctions_boutons.py)
	- La boucle d'évènement de `menu_parametres()` a été déplacée dans sa fonction `_evenements_parametres()`.
+ [fonctions_vrac.py](sources/fonctions_vrac.py)
	- La boucle infinie dans `centrer_pos()` n'est plus.
+ Entitées
	- La propriété `.stats` est remplacée par `.stats_totales` qui prend en compte les objets de l'inventaire.