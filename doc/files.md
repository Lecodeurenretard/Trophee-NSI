# Détail fichier par fichier
+ [Attaque](../sources/combats/Attaque.py) contient (explications dans la [section correspondante](#les-attaques)):
	- `TypeAttaque` (énum)
	- `EffetAttaque` (énum ou flag) (pas encore implémenté)
	- `Attaque` (classe)
	- `AttaquePriorisee` (classe): Enveloppe pour classer les attaques suivant leurs vitesses.
+ [Bouton](../sources/combats/Bouton.py) contient:
	- `Button` (classe): Gère les boutons de l'écran titre.
	- `ButtonCursor` (classe): fusion entre `Button` et `Curseur`.
+ [constantes_globales](../sources/combats/constantes_globales.py) contient:
	- Toutes les constantes globales.
+ [Curseur](../sources/combats/Curseur.py) contient:
	- `Curseur` (classe): Un petit rond qui se déplace suivant une grille pour la séléction au clavier.
+ [dessin](../sources/combats/dessin.py) contient:
	- Quelques fonctions de dessin.
+ [fonctions_boutons](../sources/combats/fonctions_boutons.py) contient:
	- Les fonctions utilisées par les boutons.
+ [fonctions_main](../sources/combats/fonctions_main.py):
	- Des fonctions qui ne sont utilisées que dans le fichier [main](../sources/combats/main.py).
+ [fonction_vrac](../sources/combats/fonctions_vrac.py)
	- Des fonctions qui n'ont de place nulle part (et donc qui n'ont besion que du contexte fourni par [imports_var](../sources/combats/imports_var.py)).
+ [import_var](../sources/combats/import_var.py) a rôle:
	- d'importer les dépendances externes de [imports](../sources/combats/imports.py).
	- d'importer les variables et constantes globales.
	- d'importer les classes beaucoup utilisées (comme `Pos` ou `Stats`).
	- de faire les raccourcits (comme `Surface` au lieu de `pygame.Surface`).
+ [imports](../sources/combats/imports.py) a rôle:
	- d'importer les dépendances externes (pygame et la bibliothèque standard)
+ [Joueur](../sources/combats/Joueur.py) contient:
	- `Joueur` (classe): explications dans la [section correspondante](#joueur).
	- `joueur` (objet `Joueur`): Le joueur dans les combats.
+ [liste_boutons](../sources/combats/liste_boutons.py) contient:
	- Des listes de boutons pour les menus.
+ [main](../sources/combats/main.py) a pour but:
	- D'être le point de départ du programme pour le mode boss rush.
	- Itèrer parmis les combats
+ [Monstre](../sources/combats/Monstre.py) contient (explications dans la [section correspondante](#monstre)):
	- `TypeMonstre` (énum)
	- `Monstre` (classe)
+ [Pos](../sources/combats/Pos.py) contient:
	- `Pos` (classe)
+ [Stats](../sources/combats/Stats.py) contient:
	- `Stat` (classe) explications dans la [section correspondante](#les-stats)
+ [UI](../sources/combats/UI.py) contient:
	- Des fonctions relatives à la GUI (notament l'écran titre).
	- Quelques fonctions qui dessinent l'écran
+ [variables_globales](../sources/combats/variables_globales.py) contient:
	- Toutes les variables globales saufs constantes.
	- Les alias de types