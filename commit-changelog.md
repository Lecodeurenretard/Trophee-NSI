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
## Adaptation au plein écran.
+ Changements majeurs
	- Le jeu est maintenant adapté au plein écran (du moins sur le mien).
		* Agrandissement des interfaces et des polices.
		* La quasi totalité des mesures de distance/longueur sont maintenant faites par rappot à l'écran.
	- Les curseurs ne sont plus implémentés dans le jeu.
		* `ButtonCursor` aussi.
+ Sur plusieurs fichiers
	- Déplacement de `dessiner_barre_de_vie()` dans [Entite.py](sources/Entite.py).
	- Suppression des derniers fossiles de la stat `vitesse`.
+ Structure de fichiers
+ READMEs et documentation
+ Interactions joueur/testeur
	- Meilleur équilibrage pour Corbobo et Secoupe.
	- Nouvelle touche en mode débug pour cacher les cartes.
	- Nouvel écran de chargement: la barre part du milieu et s'allonge des deux côtés en même temps.
	- Les barres de vies sont affichées au dessus des entités et sont allongées.
	- Le texte de nombre d'attaques à été changé et change de couleur suivant le nombre d'attaques restantes.
	- Suppression du paramètre `monstre_invincible` car il ne servait pas (et était inutilisable depuis le commit pécédent).
+ Correction de bugs
	- Lorsque l'on essaye de revenir au combat précédent dans un shop, le bloaquage est enlevé.
+ [Couleurs.py](sources/Constantes/Couleurs.py)
	- Renommage des `iterable_to_*` en `sequence_to_*`.
+ `Bouton`
	- Ajout de l'attribut statique `FONT_NAME`.
	- Renommage de `SON_APPUI` en `SOUND_PRESSED`.
	- `.draw()` admet un nouvel argument (obligatoire) `point_size` qui représente la taille du texte.
+ `Carte`
	- `._get_sprite()` obtient le cache LRU de functools
		* C'est une propriété maintenant.
		* Renommage en `_sprite`.
+ `Entite` et déscendants
	- Remplacement de la constante `_POS_BARRE_VIE` par la propriété `._pos_barre_de_vie`.
	- `SPRITE_DIM` devient non public.
	- Remplacement de `.plus_de_vie` par `.en_vie`.
	- `.dessiner_UI()` ne prend plus qu'un seul argument: la surface.
+ `Jeu`
	- Ajout de la méthode `pourcentages_fenetre()` (3 overload) qui fait la même chose que `pourcentages_coordonees()` mais pour les distances (renvoie donc un `Vecteur`).



_______________
Le lancer de carte lag encore.