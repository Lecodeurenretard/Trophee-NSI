# Détail fichier par fichier
+ [Attaque](../sources/Attaque.py) contient (explications dans le [fichier correspondant](fight-system.md)):
	- `TypeAttaque` (énum)
	- `EffetAttaque` (énum ou flag) (pas encore implémenté)
   	- `AttaqueFlag` (flag)
	- `Attaque` (classe): Calcule les dégats infligés.
+ [Bouton](../sources/Bouton.py) contient:
	- `Button` (classe): Gère les boutons.
	- `ButtonCursor` (classe): fusion entre `Button` et `Curseur`.
+ [Curseur](../sources/Curseur.py) contient:
	- `Curseur` (classe): Un petit rond qui se déplace suivant une grille pour la séléction au clavier.
+ [dessin](../sources/dessin.py) contient:
	- Quelques fonctions de dessin.
+ [fonctions_boutons](../sources/fonctions_boutons.py) contient:
	- Les fonctions utilisées par les boutons.
+ [fonctions_main](../sources/fonctions_main.py):
	- Des fonctions qui ne sont utilisées que dans le fichier [fonctions_etats](../sources/fonctions_etats.py).
+ [fonction_vrac](../sources/fonctions_vrac.py)
	- Des fonctions qui n'ont de place nulle part (et donc qui n'ont besoin que des variables/types/fonctions fourni par [imports_var](../sources/imports_var.py)).
+ [import_var](../sources/import_var.py) a rôle:
	- d'importer les dépendances de [imports](../sources/imports.py).
	- d'importer les constantes globales du module [`Constantes`](../sources/Constantes/).
	- d'importer les classes du module [`classes_utiles`](../sources/classes_utiles/).
+ [imports](../sources/imports.py) a rôle:
	- d'importer les dépendances externes (pygame et la bibliothèque standard)
+ [Joueur](../sources/Joueur.py) contient:
	- `Joueur` (classe): explications dans le [fichier correspondant](fight-system.md#les-entit%C3%A9s).
	- `joueur` (objet `Joueur`): Le joueur dans les combats.
+ [main](../sources/main.py) a pour but:
	- D'être le point de départ du programme.
	- De lancer la fonction d'état correspondante.
+ [Monstre](../sources/Monstre.py) contient (explications dans la [section correspondante](#monstre)):
	- `MonstreJSON` (dataclasse)
	- `Monstre` (classe)
+ [Pos](../sources/Pos.py) contient:
	- `Pos` (dataclasse)
+ [Stats](../sources/Stats.py) contient:
	- `Stat` (dataclasse) explications dans la [section correspondante](#les-stats)
+ [UI](../sources/UI.py) contient:
	- Des fonctions relatives à la GUI.
	- `rafraichir_ecran()` et fonctions associées.
+ [globales_variables](../sources/globales_variables.py) contient:
	- `entites_vivantes[]` (variable): Liste contenant toutes les entités.
 	- *Remarque: Le fichier sera éffacer quand la classe `Entite` sera créée.*
