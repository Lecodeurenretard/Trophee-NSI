Ce fichier contient tous les changements faits dans les commits. Il est rafraichit à chaque commits.
Un bon moyen de savoir si le changement devrait être écrit ici, c'est de se demander si il changera la façcon d'interagir sur la fonction/classe.

<!--
format:
## [message du commit]
+ Changements majeurs
	- [Changements à la base du but du commit?]
+ Sur plusieurs fichiers
	- [Autres changements?]
+ Structure de fichier
	- [changements sur la structure de ficher?]
+ READMEs et documentation
	- [changements dans la doc?]
+ Interaction joueur/testeur
	- [Changement touches/dialogue/...]
+ [fichier/classe]
	- [changements...]
+ [...]


--template:--
## 
+ Changements majeurs
+ Sur plusieurs fichiers
+ Structure de fichier
+ READMEs et documentation
+ Interactions utilisateur
+ 
	- 
-->
<!--
Nils: J'utilise l'ordre Ajout, Renommage, Déplacement, Modification, Effacement/Destruction, Autre.
-->
_____
## Début refactorisation moteur graphique + implémentation animations _in game_ + merge
+ Changements majeurs
	- Création de la classe `InterpolationLineaire`.
	- Création de fonctions de easing.
	- Ajout d'états au jeu.
		* Implémentation rudimentaire
+ Changements mineurs
	- Ajout de `Duree` pour éviter la confusion entre les unités.
+ Sur plusieurs fichiers
+ Structure de fichier
+ READMEs et documentation
+ Interactions utilisateur
+ `Attaque`
	- Ajout des constantes statiques `_DUREE_AFFICHAGE` et `_DUREE_VIDE`.
	- Ajout du membre statique `._etat_graphique[]`.
	- Modification de `lancer_toutes_les_attaques()`:
		* Ajout du paramètre `surface`.
		* Renommage en `lancer_toutes_les_attaques_gen()`.
		* La fonction renvoie maintenant Un générateur qui exécute et dessine une par une.
		* Suppression du paramètre `reset_ecran`.
+ [dessin.py](sources/combats/dessin.py)
	- Ajout de la fonction `image_vers_generateur()` qui renvoie un générateur renvoyant l'image pendant un temps défini.
+ [fonctions_main](sources/combats/fonctions_main.py)
	- `nouveau_combat()` est maintant un générateur.
+ [fonctions_vrac](sources/combats/fonctions_vrac.py)
	- Jaout des fonctions `avancer_generateurs()` et `terminer_generateur()`.
+ Entités
	- Ajout d'un dictionnaire `_etat_graphique[]`.
	- Ajout des méthodes `.dessine_prochaine_frame()` et `.dessine_prochaine_frame_UI()`.
	- `.recoit_degats()` ne retourne plus rien.
	- `.est_mort` est une propriété désormais.
+ `Monstre`
	- Renommage de `._attaques_disponibles[]` en `._moveset[]` pour une unicité dans les entités.
+ `Stat`
	- `.est_mort` est une propriété désormais.
+ [UI.py](sources/combats/UI.py)
	- `afficher_nombre_combat()` devient `ecran_nombre_combat()` et retourne un générateur qui donne l'écran pour chaque frames.
	- `rafraichir_ecran()` à été adapté au fonctionnement avec les générateurs.
		* Elle prend deux listes de générateurs en entrée et va les exécuter à chaque frames.
+ [variables_globales.py](sources/combats/variables_globales.py)
	- Ajout de `menus_surf` qui contient tous les graphiques des menus.
	- Remplacement de `delta` par `temps_de_jeu` (le delta timing des animations se fait nativement pour les animations).