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
## Ajout de pools de monstres.
+ Changements majeurs
	- Ajout du système de Pool à la Isaac.
		* Les blobs, les sorciers et Corbobo restent dans les plaines et Corbobo et Secoupe sont dans l'église satanique.
		* Ajout de `Jeu.pools_monstres[]` et `Jeu.pool_monstres_etage[]`.
	- Ajout de la classe `Pool` qui n'est pas restreinte aux monstre.
+ Sur plusieurs fichiers
+ Structure de fichiers
+ READMEs et documentation
+ Interactions joueur/testeur
	- Magie et Torgnole enlèvent de la défense physique et magique respectivement.
	- Les skips jusqu'au shop et au boss affichent de nouveau un message dans la console.
+ Correction de bugs
+ [fonctions_main.py](sources/fonctions_main.py)
	- Suppression du paramètre `numero_combat` dans `initialiser_nouveau_combat()` car inutile.
+ [Jeu.py](sources/Jeu.py)
	- Ajout de `Jeu.NOMBRE_ETAGES`.
	- Le numéro d'étape précédente est maintenant sauvegardé.
		* Ajout de `Jeu.num_etape_precedente`, `Jeu.avancer_etape()` et `Jeu.aller_etape()`.
	- Ajout de `Jeu.rafraichir_pools()`.
	- Déplacement de tout le contenu graphique dans une nouvelle classe `Fenetre`.
		* `Jeu.fenetre` devient `Fenetre.surface`.
- `MonstreJSON`
	- Ajout d'une overload pour le constructeur.
	- Ajout de `chercher_nom()`.
- `Monstre` (donc descendants)
	- `spawn()` prend maintenant une pool en paramètre et pioche dedans.




____________
Pleins de fichiers ont dû changer `Jeu.X` en `Fenetre.X` d'où tous les fichiers modifiés.