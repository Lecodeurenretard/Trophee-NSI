# README

Ce fichier est un [fichier markdown](https://www.markdownguide.org/basic-syntax/) ([guide markdown](https://www.markdownguide.org/getting-started/)) qui explique le fonctionnement du projet, il devrait être automatiquement mis en forme sur Github (sinon il existe pleins d'extentions sur VS code).


## Utiliser Github
J'ai rédigé [un fichier](Git.md) pour ça.

## Des notions de Python
Des notions Python que l'on a pas vu en NSI: [Python.md](Python.md)

## Comment marche le jeu

Le jeu utilise la POO pour fonctionner, les classes principales sont:
+ [`Stat`](Stat.py): Représente les statistiques d'une entitée.
+ [`Attaque`](Attaque.py): Toute action qui puisse influer sur cette ou une autre entitée.
+ [`Monstre`](Monstre.py): 1er type d'entitée, tout ennemi au joueur.
+ [`Joueur`](Joueur.py): 2nd type d'entitée, le personnage que contôle le joueur.

### Détail fichier par fichier
+ [Attaque.py](Attaque.py) contient (explications dans la [section correspondante](#les-attaques)):
	- `TypeAttaque` (énum)
	- `EffetAttaque` (enum ou alias de `int`)
	- `Attaque` (classe)
+ [Bouton.py](Bouton.py) contient:
	- `Bouton` (classe): Gère les boutons de l'écran titre.
+ [dessin.py](dessin.py) contient:
	- Quelques fonctions de dessin.
+ [fonction_combat.py](fonction_combat.py) contient:
	- Des fonctions gerant les attaques des entitées
+ [fonctions_boutons.py](fonctions_boutons.py)
	- Les fonctions utilisées par les boutons de Bouton.py.
+ [import_var](import_var.py) a pour but:
	- d'importer les variables de variables_globales.py en assurant les modifications inter-modules (fichiers).
+ [Joueur.py](Joueur.py) contient:
	- `Joueur` (classe): explications dans la [section correspondante](#joueur).
	- `joueur` (objet `Joueur`): Le joueur dans les combats.
+ [main.py](main.py) a pour but:
	- D'être le point de départ du programme.
+ [Monstre.py](Monstre.py) contient (explications dans la [section correspondante](#monstre)):
	- `TypeMonstre` (énum)
	- `Monstre` (classe)
+ [Stat.py](Stat.py) contient:
	- `Stat` (classe: )explications dans la [section correspondante](#les-stats)
	- L'import de:
		* `enum.Enum` (classe)
		* `enum.auto()` (fonction)
+ [UI.py](UI.py) contient:
	- Des fonctions relatives à la GUI (notament l'écran titre).
	- Quleques fonctions qui dessine l'écran
+ [variables_globales.py](variables_globales.py) contient:
	- Toutes les variables globales
	- Les alias de types
	- Tous les imports externes (sauf les imports du module `enum`).

### Les entitées
Une entitée est un personnage indépendant (avec ses stats, attaques, ...) pouvant intervenir pendant le combat.  
Toutes les entitées sont enregistrées dans la liste globale `entitees_vivantes[]` (leurs IDs étant leurs index dans celle-ci).

Les entitées ont un comportement personnalisé pour l'opérateur:
+ `del()`: Enlève l'entitée de `entitees_vivantes[]`.

Chaque entitée est attendue d'avoir des méthodes avec ces signatures:
>```Python
> def attaquer(self, id_cible : int, attaque : Attaque) -> bool
>```
Attaque l'entitée avec l'ID `id_cible` avec `attaque`, renvoie si l'attaque à tué l'entitée.

>```Python
> def subir_attaque(self, attaque : Attaque, stats_attaquant : Stat) -> bool
>```
Applique les effets de `attaque` sur l'entitée courante, renvoie si l'entitée est morte.

> ```Python
> def dessiner(self, surface : pygame.Surface, pos_x : int, pos_y : int) -> None
> ```
Dessine l'objet sur `surface` aux positions indiquées.

>```Python
> def dessiner_attaque(self, surface : pygame.Surface, clef_attaque : str|Attaque) -> None
>```
Dessine l'attaque avec pour clef `clef_attaque` (peut-être une attaque dans sa liste d'attaque, dans ce cas ce sera une `Attaque`).

>```Python
> def dessiner_barre_de_vie(self, surface : pygame.Surface, pos_x : int, pos_y : int) -> None
>```
Dessine la barre de vie à la position demandée.

#### `Joueur`
Les fonctions concernant la classe `Joueur` sont séparées dans 2 fichiers [Joueur.py](Joueur.py) et [fonction_combat.py](fonction_combat.py), celles étant dans le second fichiers le sont car elles s'appuient sur la fonction `rafraichir_ecran()` qui à besoin de beaucoup d'autres choses pour fonctionner.

Il n'y a qu'un seul objet joueur, c'est la variable `joueur` (déclarée dans [Joueur.py](Joueur.py)).  
Il n'y a pas besion d'appeler de fonction pour l'ajouter ou l'enlever de `entitees_vivantes[]` car le constructeur et le destructeur (`__init__()` et `__del__()`) s'en chargent automatiquement.

#### `Monstre`
Toutes les fonctions concernant les monstres sont dans [Monstre.py](Monstre.py).  
Tous les monstres sont automatiquement ajoutés à la liste `Monstre.monstres_en_vie[]` et à `entitees_vivantes[]`.

Les monstres fonctionnent par types, un type de monstre est un monstre préfait: il aura ses stats et ses attaques propres. Les types sont gérés par l'énumération `TypeMonstre` (définie dans [Monstre.py](Monstre.py)).  
Voici les types implémentés:
+ Blob (attaques physiques)
+ Sorcier (attaques magiques)

Il est préférable de créer les nouveaux monstres par `Monstre.nouveau_monstre()` pour initialiser l'instance à un type plutôt que des stats précises.  
Il faut effacer les monstres morts nous même avec `del()`.

### Les stats
Pour représenter les stats d'une entitées, on utilise une instance de `Stat` (classe définie dans [Stat.py](Stat.py)).

Pour le moment il y a sept stats:
- `vie`: La vie restante à l'entitée détenant l'objet.
- `vie_max`: La valeur maximum que la vie puisse avoir.
- `force`: La puissance d'attaque physique.
- `defense`: La défense pour les attaques physiques.
- `magie`: La puissance d'attaque magiques.
- `defense_magique`: La défense pour les attaques magiques.
- `vitesse`: influera sur l'ordre des attaques (non implémenté).
- `crit_puissance`: Une valeur ajoutée au coups critiques.
- `crit_resistance`: Une résitance aux dégats critiques.

Chaque objets à en plus un attribut:
- `est_initialise`: Si l'objet à des valeurs pouvant être lues. Si `False` il faut considérer les valeurs des autres attributs comme incorrectes.

Les objets `Stat` ont un comportement personnalisé pour les opérateurs:
+ `==`: Renvoie `True` si les deux objets ne sont **pas** initialisés ou si leurs autres variables membres sont les mêmes.
+ `!=`: Négationne (porte `not`) l'opérateur `==`.
+ `str()`: Renvoie une string de débogage informant sur les attributs de l'objet.
+ `copy()` (du module `copy`): Copie tous les attributs de l'objet.

Je considère que la classe `Stat` est une _structure_ (terme inexistant pour le Python mais je n'ai rien de mieux), c'est-à-dire que la classe ne respecte pas l'[encapsulation](Python.md#lencapsulation) et ses membres sont prévus pour n'être accédés que par une classe contenant un objet `Stat` qui lui sera privé.

### Les attaques
Chaque attaque est représentée par un objet `Attaque` (classe définie dans [Attaque.py](Attaque.py)).  
Une attaque constituée des variables membres:
+ `_nom`: Le nom de l'attaque.
+ `_desc`: Une courte description.
+ `_puissance`: La puissance de l'attaque, sera utilisé pour calculer les dégats causés par l'attaque avec les stats du lanceur et de la victime.
+ `_type_attaque`: Le type de dommages causés par l'attaque (sera détaillé plus en bas.)
+ `_effet`: Le ou les effet.s causé.s de l'attaque (sera détaillé plus tard) (non utilisé).
+ `_crit_prob`: La chance de faire un coup critique, doit être sur $[0; 1]$.
+ `_friendly_fire`: Si l'attaque peut toucher le lanceur ou ses alliés.
+ `_ennemy_fire`: Si l'attaque peut toucher l'adversaire au lanceur ou ses alliés.
+ `_nom_surf`: Une surface contenantle nom de l'attaque rendered pour être dessiné à l'écran.
+ `_couleur`: La couleur dans laquelle l'attaque sera déssinée une fois lancée, changera sûrement en `Sprite` dans le futur.

Il y a aussi les attributs statiques:
+ `toujours_crits`: Outil de déboggage, permet de garantir un crit à chaque attaque.
+ `_PUISSANCE_CRIT`: Comment un crit devrait monter les dégats.
+ `_CRIT_IMG`: Une surface avec l'icône de crit déjà chargée.

Les objets `Attaque` ont un comportement personnalisé pour les opérateurs:
+ `==`: Compare les noms des attaques.
+ `!=`: Négationne (porte `not`) l'opérateur `==`.
+ `str()`: Renvoie une string de débogage informant sur les attributs de l'objet.

Les attaques ne se chargent pas d'infliger les dégats, elles sont chargées de seulement calculer les dégats infligés avec `Attaque.calculer_degats()`.  
Toutes les attaques prédéfinies sont dans le dictionnaire `ATTAQUES_DISPONIBLES[]` (défini dans [Attaque.py](Attaque.py)).

Les attaques ont des types et des effets.  
les types sont membres de l'énumeration `TypeAttaque` (définie dans [Attaque.py](Attaque.py)) et dirigent la façon dont les dégats seront calculés et comment doit être traité.  
Les effets seront les modifications de statut appliqués au destinataire, ils ne sont pas encore implémentés.