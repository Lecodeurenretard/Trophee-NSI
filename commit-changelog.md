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
## $3^\text{me}$ étape de l'implémentation des cartes (injouable).
+ Changements majeurs
	- Gros changement dans `Carte` (v. section associée).
		- Ajout d'un système d'animation (une carte peut passer d'une animation A vers une animation B alors que A n'est pas finie).
+ Sur plusieurs fichiers
	- Plus besoin d'écrire `Constantes.` pour accéder à ses modules.
+ Structure de fichiers
+ READMEs et documentation
	- La liste des touches à été déplacée dans [Touches.md](Touches.md).
+ Interactions joueur/testeur
	- Le testeur peut skip avec les boutons entrée.
	- Le joueur pioche en début de tour au lieu du début de l'état `CHOIX_ATTAQUE`.
		* On n'est pas à un piont ou, une différence est faite.
+ Correction de bugs
+ `Carte`
	- Les cartes dessinées à l'écran sont contenues dans `cartes_affichees[]`.
		* L' "ID d'affichage" est la clef de l'instance dans le dico.
	- Nouvelles propriétés pour avoir la vie facile:
		* `.est_de_dos` (vérifie si la carte doit être dessinée de dos suivant l'animation en cours)
		* `.est_affiche` (fait un assert en plus)
		* Quelques autres qui ne font pas grand chose
	- Ajout d'un système d'animation
		* générateur pour animations `._animation()` qui centralise les déplacements et dessin de l'instance.
		* les méthodes `.afficher()` et `.cacher()` qui se cahragent du dessin.
		* Supression de `.jouer_animation()`.
	- Les cartes storent leurs animations dans `._anim_gen`.
	- Renommage de `_ANIM_GARDER_POS` et `_ANIM_CHANGER_POS` en `_ANIM_GARDER` et `_ANIM_CHANGER`.
	- Renommage `._set_deplacement()` en `._calcul_deplacement()`.
	- Les animations doivent spécifier aussi si la carte doit être de dos.
	- Suppression de `.decaler_pos_defaut()` et de `_SPRITE_DOS` car inutiles.
+ [fonctions_etats.py](sources/fonctions_etats.py)
	- Réduction de la longueur du code de `shop()` (plus un export mais même chose)
		* La radio est maintenant gérée par un générateur externe.
		* La génération d'items random est maintenant faite dans une sous fonction.
		* Déplacemment de code vers `reagir_appui_touche_shop()`.
		* Tout le code de dessin est à part dans `rafraichir_ecran_shop()`.
+ [fonctions_vrac.py](sources/fonctions_vrac.py)
	- Remplacement de `premier_indice_libre_de_entites_vivantes()` par `premier_indice_libre()` (2 overloads) qui est plus général.
	- Inversion des overloads de `clamp()` pour que le _type checker_ s'y retrouve.
+ `Item`
	- `generateur_items()` admet un nouvel argument `consecutifs_differents` qui permet de limiter le nombre de fois qu'un même item puisse apparaitre.
+ `Joueur`
	- Ajout de `_CARTES_MAIN_MAX_DU_MAX` pour limiter le maximum d ecarte que le joueur puisse avoir en main.
	- Ajout de méthode pour gérer la main du joueur:
		* `._recalculer_positions_cartes()`,
		* `._inserer_carte_main()`,		<!--Qu'est-ce que j'ai souffert sur cette méthode-->
		* `._enlever_carte_main()`
	- `._cartes_main[]` est maintenant une liste de cartes.
		- Suppression de `._get_carte_main()`.
	- Suppression de `.dessiner_main()` (Les cartes se chargent elles-mêmes de se décider).
+ [UI.py](sources/UI.py)
	- `rafraichir_ecran()` s'occuppe de dessiner les cartes.
	- Les fonctions `dessiner_nombre_pieces()` et `dessiner_inventaire()` sont maintenant ici.
	- Ajout de `rafraichir_ecran_shop()`.

______
Le monstre ne peut pas encore attaquer.
Maintenant c'est le lancement de carte qui lag. TOFIX