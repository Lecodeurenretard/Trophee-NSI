# Détail fichier par fichier
+ [Attaque](../sources/Attaque.py) contient (explications dans la [section correspondante](#les-attaques)):
	- `TypeAttaque` (énum)
	- `EffetAttaque` (énum ou flag) (pas encore implémenté)
	- `Attaque` (classe)
	- `AttaquePriorisee` (classe): Enveloppe pour classer les attaques suivant leurs vitesses.
+ [Bouton](../sources/Bouton.py) contient:
	- `Button` (classe): Gère les boutons de l'écran titre.
	- `ButtonCursor` (classe): fusion entre `Button` et `Curseur`.
+ [constantes_globales](../sources/constantes_globales.py) contient:
	- Toutes les constantes globales.
+ [Curseur](../sources/Curseur.py) contient:
	- `Curseur` (classe): Un petit rond qui se déplace suivant une grille pour la séléction au clavier.
+ [dessin](../sources/dessin.py) contient:
	- Quelques fonctions de dessin.
+ [fonctions_boutons](../sources/fonctions_boutons.py) contient:
	- Les fonctions utilisées par les boutons.
+ [fonctions_main](../sources/fonctions_main.py):
	- Des fonctions qui ne sont utilisées que dans le fichier [main](../sources/main.py).
+ [fonction_vrac](../sources/fonctions_vrac.py)
	- Des fonctions qui n'ont de place nulle part (et donc qui n'ont besion que du contexte fourni par [imports_var](../sources/imports_var.py)).
+ [import_var](../sources/import_var.py) a rôle:
	- d'importer les dépendances externes de [imports](../sources/imports.py).
	- d'importer les variables et constantes globales.
	- d'importer les classes beaucoup utilisées (comme `Pos` ou `Stats`).
	- de faire les raccourcits (comme `Surface` au lieu de `pygame.Surface`).
+ [imports](../sources/imports.py) a rôle:
	- d'importer les dépendances externes (pygame et la bibliothèque standard)
+ [Joueur](../sources/Joueur.py) contient:
	- `Joueur` (classe): explications dans la [section correspondante](#joueur).
	- `joueur` (objet `Joueur`): Le joueur dans les combats.
+ [liste_boutons](../sources/liste_boutons.py) contient:
	- Des listes de boutons pour les menus.
+ [main](../sources/main.py) a pour but:
	- D'être le point de départ du programme pour le mode boss rush.
	- Itèrer parmis les combats
+ [Monstre](../sources/Monstre.py) contient (explications dans la [section correspondante](#monstre)):
	- `TypeMonstre` (énum)
	- `Monstre` (classe)
+ [Pos](../sources/Pos.py) contient:
	- `Pos` (classe)
+ [Stats](../sources/Stats.py) contient:
	- `Stat` (classe) explications dans la [section correspondante](#les-stats)
+ [UI](../sources/UI.py) contient:
	- Des fonctions relatives à la GUI (notament l'écran titre).
	- Quelques fonctions qui dessinent l'écran
+ [variables_globales](../sources/variables_globales.py) contient:
	- Toutes les variables globales saufs constantes.
	- Les alias de types