# Comment marche le système de combat

Les classes décrites dans ce fichier sont:
+ [`Stat`](../sources/Stats.py): Représente les statistiques d'une entité.
+ [`Entite`](../sources/Entite.py) (et descendants): Tout acteur dans un combat, c'est-à-dire le joueur, les monstres et les boss.
+ [`Attaque`](../sources/Attaque.py) (ainsi que les enums/_wrappers_ en lien): S'assure du calcul de dégats.
+ [`Item`](../sources/Item.py): Un objet avec un effet passif.

Les interfaces de [`Item`](interfaces.md#linterface-des-items), [`Carte`](interfaces.md#linterface-des-cartes), [`Boss`](interfaces.md#linterface-des-boss) sont décrites dans [interfaces.md](interfaces.md).

## Les entités
Une entité est un personnage pouvant prendre part au combat et  y étant indépendant.  

Les entités ont un comportement personnalisé pour l'opérateur:
+ `del()`: Enlève l'entité de `entites_vivantes[]`.

Concrètement, une entite est une instance de `Entite` ou d'un de ses classes filles: `Joueur`, `Monstre` ou `Boss`.  
Quand une classe hérite de `Entite`, il faut qu'elle définisse:
- `_CARTE_MAIN_PREMIERE_POS : Pos` (statique): La postion de la première carte (celle la plus à gauche) de la main de l'entite.
- `_CARTES_DE_DOS : bool` (statique): Si les cartes de la main doivent être dessinées de dos par défaut.
- `.pos_sprite_centree : Pos` (propriété _getter_): La position du centre du sprite sur l'écran.

Elle est aussi en mesure de changer:
- `_CARTES_MAIN_MAX_DU_MAX : int` (statique): La valeur maximum que peut prendre `._cartes_main_max` donc la longueur maximum de `._cartes_main`.

Toutes les instances de `Entite` (et filles) sont enregistrées dans la liste statique `Entite.vivantes[]`, chacune est aussi dotée d'un id qui correspond à son indice dans `Entite.vivantes[]`.

Les données JSON des entités (de [data/JSON/TypesEntite.json](../data/JSON/TypesEntite.json)) sont stockées dans des objets `EntiteJSON`, ceci ne devraient pas être modifiés après construction.

### `Entite`
C'est la classe mère pour toutes les entités.

### `Joueur`
Il n'y a qu'un seul objet joueur, c'est la variable `joueur` (déclarée dans [Joueur.py](../sources/Joueur.py)), admise comme étant d'ID `EntiteJSON.INDEX_JOUEUR`.  
Cette classe se charge aussi de la gestion de l'argent du joueur.

#### Héritage
`Joueur` hérite de toutes les méthodes et propriétés publiques (les non-publiques ne sont pas couvertes dans cette documentation) de `Entite`.  
Tous les attributs, propriétés et fonctions de `Entite` sont hérités.

#### Overrides
- Le constructeur ne prend pas d'instance `EntiteJSON`.
- `.recoit_degats()` n'a aucun effet si `params.joueur_invincible` est `True` et que les dégats sont négatifs.
- `.reset()` reset aussi les stats.
- `.decrire_stats()` Ajoute l'argent à la description.

#### Ajouts
- `.gerer_dessin_infos_cartes()` Décide quelle carte doit avoir ses infos (la fenêtre quand on survole une carte) de dessinées.
- `.ajouter_pieces()` Ajoute ou enlève les pièces à l'argent du joueur peu importe toutes conditions extérieur.
- `.paiement()` Enlève les pièces mais respecte les paramètres de triche et a des sécurités au cas où le joueur n'aurait pas de quoi payer.

### `Monstre`
Les monstres fonctionnent par types, un type de monstre est un monstre préfait: il a ses stats et ses attaques propres.  
Les types sont répertoriés avec le joueur dans [data/JSON/TypesEntite.json](../data/JSON/TypesEntite.json).

Chaque type à aussi un "rang", c'est une mesure arbitraire utilisée pour estimer rapidement la puissance d'un monstre; pour l'instant ce n'est utilisé que pour le calcul des pièces gagnées.

#### Héritage
`Monstre` hérite de toutes les méthodes et propriétés publiques (les non-publiques ne sont pas couvertes dans cette documentation) de `Entite`.  
Tous les attributs, propriétés et fonctions de `Entite` sont hérités.

#### Overrides
- Le constucteur prend un objet `MonstreJSON` au lieu d'un `EntiteJSON`.
- `.decrire_stats()` qiu ajoute l'ID du type et le rang du monstre.

#### Ajouts
- `spawn()` Tire un monstre d'une pool et le construit.
- `adversaire()` Renvoie l'adversaire principal du joueur (celui qui est dans le combat depuis le plus longtemps).
- `massacre()` Appelle `meurt()` sur tous les monstres en vie.
- `.vers_type_precedent()`/`.vers_type_suivant()` Change le type du monstre.
- `.choisir_index_carte_main()` choisi la carte à être jouer.

## `Boss`
### Héritage
En tant que fille de `Monstre`, `Boss` hérite de toutes les méthodes et propriétés publiques (les non-publiques ne sont pas couvertes dans cette documentation) à l'exception de ces deux méthodes qui élèverons une `TypeError`:
- `.vers_type_precedent()`
- `.vers_type_suivant()`

### Overrides
Implémentations des [de l'interface](#linterface):
* `.choisir_index_carte_main()`
* `.recoit_degats()`

Le constructeur est aussi override pour prendre un objet `BossJSON` en entrée.

### Ajouts
- `vivants_boss()` (statique): Renvoie les boss en vie.
- `spawn_boss()` (statique): fait spawn le boss correspondant à l'étage en argument.
- `.callbacks` (propriété): Renvoie l'objet `BossMethodeWrapper` correspondant au boss.
- `.nouveau_tour()`: Exécute le prédicat `nouveau_tour()` du boss s'il existe

## Les stats
Pour représenter les stats d'une entités, on utilise une instance de `Stat` (classe définie dans [Stat.py](../sources/Stats.py)).

Le jeu comprend 8 stats différentes:
- `.vie`: La vie restante à l'entité détenant l'objet.
- `.vie_max`: La valeur maximum que la vie puisse avoir (ceci n'est pas enforcé par la classe `Stat`).
- `.force`: La puissance d'attaque physique.
- `.defense`: La défense pour les attaques physiques.
- `.magie`: La puissance d'attaque magiques.
- `.defense_magique`: La défense pour les attaques magiques.
- `.crit_puissance`: Une valeur ajoutée au coups critiques (se multiplie avec les dégats de crits finaux).
- `.crit_resistance`: Une résitance aux dégats critiques (se divise avec les dégats de crits finaux).

`Stat` est une dataclasse, ce qui veut dire que l'encapsulation ne s'applique pas dessus.  
Du fait de l'absence de constructeur manuellement définit, `.vie` sera initialisé à un nombre négatif, pour y remédier, utiliser `.reset_vie()`.

Si chaque attribut doit être initialisé à la même valeur, la méthode statique `Stat.remplir_de()` pourra être utilisée.

## Les cartes
Une instance de `Carte` correspond à une carte dans le jeu.  
Chaque carte est directement prise dans [data/JSON/cartes.json](../data/JSON/cartes.json). Comme chaque carte contient un objet `Attaque`, chaque objet JSON de carte contient aussi les informations de l'attaque correspondante, ces informations sont utilisées par la classe `Attaque`.

### Le système d'animation
La classe détient un dictionnaire statique `_ANIM_DICO[]` qui associe à chaque nom d'animation une instance de `CarteAnimInfo` qui contient les informations de l'animation:
- La destination (ou position à la fin)
- La durée (une durée de 0s indique que l'animation est instantanément finie et on considère que t=1).
- La fonction d'easing.
- Si la carte doit être dessinée de dos. Est prioritaire par rapport à `Carte._de_dos_defaut`.

`CarteAnimInfo.destination` et `CarteAnimInfo.de_dos` peuvent contenir les constantes statiques `CarteAnimInfo.GARDER` et `CarteAnimInfo.CHANGER` qui indique respectivement qu'il faut soit utiliser les informations de la carte, soit qu'il faut utiliser une valeur que l'on a pas encore. Ainsi, si `de_dos = GARDER` alors lors de l'animation, la carte sera dessinée suivant `Carte._de_dos_defaut`, de même si `destination = GARDER`, la destination sera la position actuelle de la carte. L'interprétation exacte de `CHANGER` est déterminée par l'animation jouée.

## Les attaques
Chaque attaque est représentée par un objet `Attaque` (classe définie dans [Attaque.py](../sources/Attaque.py)).  
attributs:

Les objets `Attaque` ont un comportement personnalisé pour les opérateurs:
+ `==`: Compare les noms des attaques.
+ `!=`: Renvoie l'inverse de l'opérateur `==`.

Les attaques ont des types et des effets.  
les types sont membres de l'énumeration `TypeAttaque` (définie dans [Attaque.py](../sources/Attaque.py)) et dirigent la façon dont les dégats seront calculés et comment doit être traité.  
Les effets seront les modifications de statut appliqués au destinataire, ils ne sont pas encore implémentés.

La classe `Attaque` possède `attaques_du_tour[]` (on peut y référer par la file des attaques). Cette file accueille des `AttaquePriorisee` et les classe suivant leurs vitesse.

### Depuis le JSON
Toutes les attaques sont _parse_ depuis le fichier [cartes.json](../data/cartes.json).  
Voici une table de correspondance entre les clefs du JSON et les attributs des instances `Attaque`:
+ `nom` ---> `._nom`
+ `puissance` ---> `._puissance`
+ `type` ---> `._type`, prend l'une de ces valeurs (insensible à la casse):
	- `"physique"`,
	- `"magique"`,
	- `"soin"`,
	- `"charge"`,
	- `"divers"`
+ `probabilité_crit` (optionnel) ---> `._prob_crit`
	- Valeur par défaut `.1`
+ `flags[]` (optionnel) ---> `._drapeaux`, Chaque élément du tableau peut prendre une de ces valeurs (insensible à la casse):
	- `"ignore defense"`,
	- `"ignore stats"`,
	- `"cible lanceur"`,
	- `"cible ennemis"` ou `"cible adversaire"`
+ `nom_ajustement` (optionnel) ---> `._ajustement_degats`.
	- L'ID est la clef de la fonction d'ajustement dans `Attaque._AJUSTEMENTS[]`.
	- Valeur par défaut: `0`
+ `Modif stat cible`/`Modif stat lanceur` (optionnel) ---> `_modif_stats_cible`/`_modif_stats_lanceur`, la clef "duree" est assignée à `_modif_stats_cible_duree`/`_modif_stats_lanceur_duree`.
	- Cette duree est le nombre de tours les effets vont durer.
		* Un tour est le joueur joue trois cartes puis le monstre joue trois cartes.
		* Une durée de `0` indique que les effets durerons seulement pour le reste du tour.
	- Valeur par défaut `{"duree": 0, "attaque": 0, ..., "crit_resistance": 0}`

## Les objets passifs
Une instance d'`Item` est un objet passif qui modifie les stats du joueur lorsqu'il est équipé. Le seul moyen de s'en procurer (pour l'instant) est le shop.  
Les instances représentent à la fois les items tels qu'ils sont dans le shop et tels qu'ils sont dans l'inventaire du joueur.

Les items sont parsés de [items.json](../data/items.json), l'objet `"stats"` aura ses attributs additionnés aux stats de l'entité quand elle le prendra.