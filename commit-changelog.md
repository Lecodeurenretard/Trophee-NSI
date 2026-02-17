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
## Les boss customizables avec des fonctions callbacks spéciales.
+ Changements majeurs
	- Ajout d'une mini API pour les boss.
		* Les callbacks ainsi qu'une dataclasse `BossMethodeWrapper` sont dans [fonctions_boss.py](sources/fonctions_boss.py).
	- Les tours d'un combat sont comptés dans `Jeu.nb_tours_combat`.
+ Sur plusieurs fichiers
+ Structure de fichiers
+ READMEs et documentation
+ Interactions joueur/testeur
	- Le roi Blob est mieux placé.
	- Le Blob est fortement nerf.
	- Ajout d'une touche pour le mode debug pour skip jusqu'au boss.
	- La couleur de la barre de vie pleine est maintenant un turquoise assombrit.
+ Correction de bugs
	- Quelques `print()` oubliés ont été enlevés.
+ `Boss`
	- Ajout propriété statique `_AGRANDISSEMENT_SPRITE`.
+ `Carte`
	- Ajout de la méthode statique `vider_cartes_affichees()`.
+ `Entite` (et filles)
	- Correction du code de dessin des barres de vies.
	- Modifications sur l'utilisation et définition des propriétés de positions
		* Ajout de `pos_sprite_centree`.
		* `.pos_sprite` n'est plus abstraite et désigne la position du coin haut gauche.
		* `.pos_attaque` n'est plus abstraite.
	- Les propriétés statiques `_SPRITE_TAILLE`, `_LONGUEUR_BARRE_DE_VIE` et `_HAUTEUR_BARRE_DE_VIE` sont maintenant non statiques.
	- `.recoit_degat()` à un nouveau parametre `attaque_cause` pour la compatibilité avec la version de `Boss`.
+ [fonctions_main.py](sources/fonctions_main.py)
	- Les skips pour le boss et le shop ont été ajoutés/déplacés dans `reagir_appui_touche()` et peuvent être triggered dans plus d'états.