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
## Adaptation des textes au plein écran.
+ Changements majeurs
	- La taille des textes est maintenant calculée dynamiquement suivant la taille de la fenêtre.
		* Les constantes dans [Polices.py](sources/Constantes/Polices.py) sont maintenant soit des strings indiquant les noms de police soit `None` (pour la police par défaut de Pygame).
		* Ajout de `Jeu.construire_police()` qui permet de construire une police suivant sa hauteur sur l'écran.
+ Sur plusieurs fichiers
+ Structure de fichiers
+ READMEs et documentation
+ Interactions joueur/testeur
	- Les tailles sont maintenant calculées suivant les dimensions de l'écran (ça peut introduire des _mixels_ mais problème pour futur nous).
	- Les barres de vies sont maintenant centrées sur les sprites de leurs entités et suivent leurs tailles.
	- Changement de tailles de certains textes.
	- Agrandissement des boites dans les paramètres.
+ Correction de bugs
	- Réparation du lag sur le lancer de carte.
	- Les cartes se retournent bien au lancement.
	- Les mains après le shop sont correctement affichées.
+ `Attaque`
	- Suppression de `.nom_surface` car inutile.
+ `Carte`
	- La propriété `._sprite` à été scindée en deux:
		* La partie qui fait le travail lent est cachée et mise dans la méthode `._preparation_sprite()`.
		* `.sprite` se contente de l'appeler avec les bons arguments.
+ `Entite` et filles
	- `_SPRITE_DIM` est renommée en `_SPRITE_TAILLE` est est devenue un `Vecteur`.
	- `.dessiner_barre_de_vie()` devient privée.
+ [fonctions_vrac.py](sources/fonctions_vrac.py)
	- Ajout de `blit_centre_rect()`.
	- Ajout d'une overload à `centrer_pos()` avec un `Vecteur`.
	- Ajout de `centrer_rect()` (2 overload).
	- Ajout de `rect_to_tuple()`.
+ `Jeu`