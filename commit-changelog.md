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
## Ajout de d'une popup d'infos pour les cartes + Ajout de paramètres extérieurs + Ajout système de couches graphiques
+ Changements majeurs
	+ Nouvelle méthode pour `Carte`: `._dessin_infos()`.
	+ Le jeu lit un fichier externe pour les paramètres.
		- Nouvelles méthodes: `Jeu.ecrire_parametres()` et `Jeu.lire_parametres()`.
+ Sur plusieurs fichiers
	- Les surfaces "toiles" (sur lequelles on dessine) ne sont plus directement passées aux fonctions de dessins, à la place le numéro de couche y est passé.
	- Les Interruptions doivent maintenant directement dessiner sur l'écran.
+ Structure de fichiers
	- Le répertoire [data/](data/) est mieux organisé.
		* Les cartes ont maintenant 1 dossier par carte.
		* Les JSONs ont leurs dossier
+ READMEs et documentation
	- Ajout d'un README dans [data/](data/).
+ Interactions joueur/testeur
	- Les cartes se lèvent quand la souris les survole.
+ Correction de bugs
	- Patch du bug dans `Array`.
	- Si une erreur SDL/Pygame survient, prévient l'utilisateur.
+ `Attaque`
	- Ajout des propriétés `.type`, `.stats_changees_cible` et `.stats_changees_lanceur`.
+ `Button`
	- Traduction en français.
+ Suppression de `ButtonCursor`.
+ [dessin.py](sources/dessin.py)
	- Remplacement de `image_vers_generateur()` par `blit_generateur()`.
+ `Entite` (donc descendantes)
	- Ajout de l'attribut non statique `._main_dans_ecran`.
+ [Jeu.py](sources/Jeu.py)
	- Nouvelle fonction `recherche_map()` qui fait une recherche dans un élément de type `Mapping`.
+ `Joueur`
	- Nouvelle méthode `.gerer_dessin_infos_cartes()`.
+ [UI.py](sources/UI.py)
	- `demander_pseudo()` et `faux_chargement()` ne demandent plus d'arguments.