# Détail fichier par fichier
## Détail de [sources/](../sources/)
+ [Attaque](../sources/Attaque.py) contient (explications dans le [fichier correspondant](fight-system.md)):
	- `TypeAttaque` (énum)
	- `EffetAttaque` (énum ou flag) (pas encore implémenté)
   	- `AttaqueFlag` (flag)
	- `Attaque` (classe): Calcule les dégats infligés.
+ [Bouton](../sources/Bouton.py) contient:
	- `Button` (classe): Gère les boutons.
	- `ButtonCursor` (classe): fusion entre `Button` et `Curseur`.
+ [Carte](../sources/Carte.py) contient (explications dans le [fichier correspondant](fight-system.md)):
	- `CarteAnimInfo` (dataclasse)
	- `Carte` (classe)
+ [Curseur](../sources/Curseur.py) contient:
	- `Curseur` (classe): Un petit rond qui se déplace suivant une grille pour la séléction au clavier.
+ [dessin](../sources/dessin.py) contient:
	- Des fonctions de dessin.
+ [Entite](../sources/Entite.py) contient (explications dans le [fichier correspondant](fight-system.md)):
	- `Entite` (classe)
+ [fonctions_boutons](../sources/fonctions_boutons.py) contient:
	- `menu_parametres()` (fonction): Une interruption se chargeant de l'écran des paramètres.
+ [fonctions_main](../sources/fonctions_main.py):
	- Des fonctions qui ne sont utilisées que dans le fichier [fonctions_etats](../sources/fonctions_etats.py).
+ [fonction_vrac](../sources/fonctions_vrac.py)
	- Des fonctions qui n'ont de place nulle part (et donc qui n'ont besoin que des variables/types/fonctions fourni par [imports_var](../sources/imports_var.py)).
+ [import_var](../sources/import_var.py) a pour rôle:
	- d'importer les dépendances de [imports](../sources/imports.py).
	- d'importer les constantes globales du module [`Constantes`](../sources/Constantes/).
	- d'importer les classes du module [`classes_utiles`](../sources/classes_utiles/).
+ [import_local](../sources/import_local.py) a pour rôle:
	- de rassembler tous les fichiers indépendants dans la cascade d'imports.
+ [imports](../sources/imports.py) a pour rôle:
	- d'importer les dépendances externes (pygame et la bibliothèque standard)
+ [Item](../sources/Jeu.py) contient (explications dans la [section correspondante](fight-system.md#monstre)):
	- Item (dataclasse)
+ [Jeu](../sources/Jeu.py) contient:
	- `Jeu` (classe): Fait une interface avec les états et les éléments de jeu de haut niveau (fenêtre)
		* `Jeu.Etat` (enum): Tous les états possibles.
	- `verifier_pour_quitter()` (fonction): Vérifie si un évènement est une évènement demandant de fermer le jeu.
	- `testeur_skip_ou_quitte()` (fonction): Vérifie si un évènement est une évènement demandant de fermer le jeu ou demande de skip.
+ [Joueur](../sources/Joueur.py) contient:
	- `Joueur` (classe): explications dans le [fichier correspondant](fight-system.md#les-entit%C3%A9s).
	- `joueur` (objet `Joueur`): Le joueur dans les combats.
+ [main](../sources/main.py) a pour but:
	- D'être le point de départ du programme.
	- De lancer la fonction d'état correspondante.
+ [Monstre](../sources/Monstre.py) contient (explications dans la [section correspondante](fight-system.md#monstre)):
	- `MonstreJSON` (dataclasse)
	- `Monstre` (classe)
+ [Parametre](../sources/Parametres.py) contient:
	- `TypeParametre` (enum)
	- `Parametre` (classe)
+ [Stats](../sources/Stats.py) contient:
	- `Stat` (dataclasse) explications dans la [section correspondante](#les-stats)
+ [UI](../sources/UI.py) contient:
	- Des fonctions relatives à la GUI.
	- `rafraichir_ecran()` et fonctions associées.

## Détails des sous-dossiers de [sources](../sources/)
### [classes_utiles/](../sources/classes_utiles/)
+ [Animation](../sources/classes_utiles/Animation.py) contient (voir [fichier correspondant](Jeu.md#2-les-animations)):
	- `valeurs_regulieres_entre_01()` (fonction)
	- `_generer_generateur()` (fonction)
	- `_generer_generateur_multi()` (fonction)
	- `SensLecture` (enum)
	- `InterpolationLineaire` (classe) et dérivées:
		* `Gradient` (classe)
		* `Deplacement` (classe)
	- `MultiInterpolation` (classe) et dérivées:
		* `MultiGradient` (classe)
		* `MultiDeplacement` (classe)
+ [Duree](../sources/classes_utiles/Duree.py) contient:
	- `Duree` (classe): Permet de ne pas s'embrouiiler avec les unités.
+ [EasingConstants](../sources/classes_utiles/EasingConstants.py) contient:
	- Les fonction d'easing souvent utilisées.
+ [EasingFunctions](../sources/classes_utiles/EasingFunctions.py) contient:
	- `EasingType` (classe): Apporte les méthode pour renvoyer les fonction d'easing.
+ [Pos](../sources/classes_utiles/Pos.py) contient:
	- `Pos`: Une position 2D.
### [Constantes/](../sources/Constantes/)
Apporte les constantes globales.