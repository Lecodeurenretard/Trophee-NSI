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
## $2^\text{me}$ étape de l'implémentation des cartes (injouable).
+ Changements majeurs
	- Pleins de changements dans `Carte` (v. section correspondante) pour les animer (fonctionnalités non testées ni utilisées).
	- Pleins de changements dans `Joueur`(v. section correspondante) pour afficher les cartes de la main.
		* Ajout de la notion de "deck" et de "main".
+ Sur plusieurs fichiers
+ Structure de fichiers
+ READMEs et documentation
	- Suppression du tableau dans le [README de la racine](README.md).
	- Petits changements dans le [README de source/](sources/README.md).
+ Interactions joueur/testeur
	- Ajout d'une touche (dans le mode débug) pour reroll les cartes.
		* Ajout de la constante `DBG_REROLL_CARTES`.
	- Le jeu ne change les cartes mais ne permet pas d'attaquer.
+ Correction de bugs
+ [Animation.py](sources/classes_utiles/Animation.py)
	- Ajout de l'énum `SensLecture`.
	- Ajout d'options pour jouer les animations à l'envers.
+ [Pos.py](sources/classes_utiles/Pos.py)
	- Ajout de `.__str__()`.
	- Ajout alias `pos_t` et `pos_pygame` (le second n'est pas importé dans les autres fichiers).
		* Ajout de fonctions pour convertir les types entre eux. 	
+ `Attaque`
	- Les instances stockent maintenant le nom de l'attaque.
+ `Carte`
	- Ajout des constantes statiques suivantes:
		* `_SURVOL_DECALAGE`,
		* `_ANIM_GARDER_POS`,
		* `_ANIM_CHANGER_POS`,
		* `_ANIM_DICO[]`,
		* `_SPRITE_DOS`
	- Ajout des attributs non statiques:
		* `._pos_defaut`,
			+ Ajout du paramètre `pos_defaut` à tous les overloads du constructeur.
		* `._pos`,
		* `._anim_nom`,
		* `._anim_sens`,
		* `._TAILLE_SPRITE`
	- Ajout d'un `.__repr__()`.
	- Ajout des propriétés (en lecture seule):
		* `._hitbox`,
		* `._anim_destination`,
		* `._anim_duree`,
		* `._anim_easing`,
		* `.pos_defaut`,
		* `.souris_survole`,
		* `.anim_nom` (lecture-écriture)
	- Ajout de la méthode `._set_deplacement()`.
	- Ajout de la méthode `.decaler_pos_defaut()`.
	- Remplacement de `._jouer_animation()` par `.jouer_animation()`.
	- Renommage de `_DUREE_INTER_ANIMATION` en `_DUREE_INTER_JEU`.
	- la méthode `._dessiner()` devient publique.
	- Suppression de l'attribut `._autoriser_animation`
	- Suppression de `.jouer()`.
		- Suppression de `.pos_anim_attaque()`.
+ [fonctions_combats](sources/fonction_combat.py)
	- Suppression de `joueur_attaque()`.
+ [fonctions_vrac](sources/fonctions_vrac.py)
	- Ajout de `etirer_garder_ratio()`.
+ [imports.py](sources/imports.py)
	- Définition des vecteurs `v_x` et `v_y`.
+ `Jeu`
	- Ajout d'overload/argument à `pourcentages_coordonees()`. Si ret_pos est vrai, renvoieun objet `Pos` sinon une tuple.
+ `Joueur`
	- Ajout des constantes statiques `_CARTE_MAIN_PREMIERE_POS` et `_CARTES_MAIN_ESPACEMENT`.
	- Ajout de l'attribut statique `_nom_derniere_carte_piochee`.
	- Ajout des attributs non statiques `._max_cartes_main` et `._cartes_main[]`.
		* Ajouts de getters et/ou setters.
	- Ajout de la notion de "deck" et de "main".
		* Ajout de `.dessiner_main()`.
		* Renommage de `noms_cartes` en `noms_cartes_deck`.
	- Ajout de `.piocher()` et `.repiocher_tout()`.
	- Ajout de `.verifier_pour_attaquer()`.
	- Le chemin vers le sprite n'est plus argument du constructeur.
	- Suppression de `.dessine_prochaine_frame()` et `.dessine_prochaine_frame_UI()`.

+ [UI.py](sources/UI.py)
	- Suppression de `dessiner_boutons_attaques()`.
______
Plus jamais je fais de commit aussi gros.

Impossible de passer à l'état `AFFICHAGE_ATTAQUES` pour l'instant.
J'ai aussi l'impression qu'il y a un lag pour cliquer sur les cartes TOFIX?