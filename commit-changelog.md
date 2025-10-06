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
+ [fichier/classe]
	- [...]

--------------template--------------
## 
+ Changements majeurs
+ Sur plusieurs fichiers
+ Structure de fichier
+ READMEs et documentation
+ Interactions utilisateur
+ 
	- 
------------------------------------
-->
<!--
Nils: J'utilise l'ordre Ajout, Renommage, Déplacement, Modification, Effacement/Destruction, Autre.
-->
_____
## Implémentation de l'état AFFICHAGE_ATTAQUES
+ Changements majeurs
	- Implémentation de `afficher_attaques()`
		- Renommage en `affichage_attaques()`.
+ Sur plusieurs fichiers
+ Structure de fichier
+ READMEs et documentation
+ Interactions utilisateur
+ [ex_curseur.py](exemples/ex_curseur.py)
	- Ajout de rounds gris pour indiquer les emplacements interdits
	- Réparation de l'exemple
+ [ex_param.py](exemples/ex_param.py)
	- Réparation de l'exemple
+ [Animation.py](sources/Animation.py)
	- Ajout d'une classe `Deplacement`.
	- Les arguments positionnels dans les `.calculer_valeur()` sont maintenant limités à `t` (et `self`).
	- Suppression de l'alias `ColorEasing`.
+ `Attaque`
	- Ajout d'une animation de glissade quand les attaques sont dessinées.
	- Ajout d'une propriété `._deplacement`.
	- Ajout d'une méthode `.pos_anim_attaque()`.
	- Renommage de `_DUREE_AFFICHAGE` et `_DUREE_VIDE` en `_DUREE_ANIMATION` et `_DUREE_ENTRE_ATTAQUES`.
	- Renommage de `.friendly_fire` et `.ennemy_fire` en `.peut_attaquer_allies` et `.peut_attaquer_adversaires`.
	- Le `.__repr__()` est maintenant mieux formaté.
	- Réécriture de `lancer_toutes_les_attaques_gen()`.
	- `.dessiner()` est maintenant non public et prend une position en entrée.
+ `Duree`
	- Ajout d'opérateurs de divisions de durées à durées.
	- Ajout d'une méthode `.__str__()`
		* Elle reprend la sortie qu'avait `.__repr__()`.
		* `.__repr__()` à une nouvelle sortie.
+ [EasingFunctions.py](sources/EasingFunctions.py)
	- `EasingType.ease_in()`, `EasingType.ease_out()` et `EasingType.ease_in_out()` accèpte maintenant les entiers.
+ [fonctions_vrac.py](sources/fonctions_vrac.py)
	- Réparation de `avancer_generateurs()`.
+ entitées
	- Fusion de `.pos_attaque_x` et de `.pos_attaque_y` en `pos_attaque`.
	- Fusion de `.pos_curseur_x` et de `.pos_curseur_y` en `pos_curseur`.
+ `Monstre`
	- Ajout d'une constante statique `POSITION`.
+ `Pos`
	- Ajout d'une overload au constructeur pour simplifier les calculs avec les vecteurs.
	- Ajout d'une méthode `milieu()`