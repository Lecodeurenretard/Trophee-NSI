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
## Ajout d'un shop primitif
+ Changements majeurs
	- Ajout du fichier pour objets [items.json](data/items.json).
	- Ajout d'une classe `Item`.
		* Ajout du fichier [Item.py](sources/Item.py).
	- Ajout état `shop`.
+ Sur plusieurs fichiers
	- Renommage de l'état `attente_nouveau_combat` vers `attente_prochaine_etape`.
+ Structure de fichiers
	- Ajout des sprites des items id [1](data/img/items/placeholder1.png), [2](data/img/items/placeholder2.png) et [3](data/img/items/placeholder3.png).
	- Ajout des images de boutons [croix.png](data/img/croix.png) et [retour.png](data/img/retour.png).
+ READMEs et documentation
+ Interactions joueur/testeur
	- Ajout d'une image de croix au lieu du X.
	- Ajout la touche 'p' skip jusqu'au prochain shop.
	- Ajout d'un shop tous les 5 combats (un shop ne peut pas être le dernier combat).
	- Le dernier combat est le 10<sup>me</sup>
+ Correction de bugs
+ [Chemins.py](sources/Constantes/Chemins.py)
	- Suppression du préfixe `DOSSIER_` sur les constantes de chemin.
+ [Touches.py](sources/Constantes/Touches.py)
	- Ajout de la constante `DBG_SHOP`.
+ `Button`
	- Modification de la classe pour qu'elle supporte l'affichage d'image.
+ [fonctions_vrac.py](sources/fonctions_vrac.py)
	- Ajout des paramètres `centrer_x` et `centrer_y` à tous les _overloads_ de `centrer_pos()`.
	- Ajout de `dessiner_texte()` qui permet d'afficher du texte avec du _line wrapping_.
+ `Jeu`
	- Ajout variable `DECISION_SHOP`.
	- Ajout méthode `reset_etat()`.
	- Ajout méthode `display_flip()` pour que `menu_surf` soit toujours render.
+ `Joueur`
	- Ajout d'un inventaire.
		* Ajout attribut `._inventaire[]` et méthodes `.prendre_item()` et `.lacher_item()`.
+ `Stat`
	- Ajout méthode `depuis_dictionnaire_json()` permettant de transformer un dictionnaire en objet `Stat`.