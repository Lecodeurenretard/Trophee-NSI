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
## Plus de cartes dans les mains.
+ Changements majeurs
+ Sur plusieurs fichiers
+ Structure de fichiers
+ READMEs et documentation
	- Le survol de carte est documenté.
+ Interactions joueur/testeur
	- Ajout de paramètres booléens pour sauvegarder le mode débug.
	- Ajout d'un nouveau monstre: Cangros (rang 1).
	- Les Corbobos spawn moins dans l'église satanique.
	- Les cartes jouées sont montrées, le joueur peut voir les cartes lancées par le monstre.
	- easter egg
+ Correction de bugs
	- Les attaques de types `DIVERS` de puissance `0` (aka Skip) ne font plus de dégats.
	- Le jeu ne crash plus quand un adversaire à une résistance aux crit de 0.
+ `Carte`
	- Ajout de la méthode statique `ordre_dessin()`.
+ [fonctions_vrac.py](sources/fonctions_vrac.py)
	- Ajout de `valeur_par_defaut_map()`.
+ `Monstre` (et descendantes)
	- Ajout de `.adversaire()` pour camoufler un nombre magique.




____________
Les monstres avec plus de deux cartes dans la main peuvent parfois faire freeze le Jeu (les évènements sont quand même actifs).
Ce qui semble se passer c'est que ces cartes sont mal spawn mais je trouve pas ce qu'il y a de mal (v. `print()` commentés pour plus d'infos).

Aussi, La bande verte en haut à gauche des plaines est remarquée mais aucun fix immédiat n'a été trouvé.