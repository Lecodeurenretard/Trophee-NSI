# Comment marche le système de combat

Les classes décrites dans ce fichier sont:
+ [`Stat`](../sources/Stats.py): Représente les statistiques d'une entité.
+ [`Entite`](../sources/Entite.py) (et descendants): Tout acteur dans un combat, c'est-à-dire le joueur et les monstres.
	- la classe `Boss` à [son propre fichier](boss.md).
+ [`Carte`](../sources/Carte.py): Une carte en elle-même.
+ [`Attaque`](../sources/Attaque.py) (ainsi que les enums/_wrappers_ en lien): S'assure du calcul de dégats.
+ [`Item`](../sources/Item.py): Un objet avec un effet passif.

## Les entités
Une entité est un personnage indépendant en ce qui concerne le combat et pouvant y prendre part.  
Toutes les entités sont enregistrées dans la liste statique `Entite.vivantes[]` (leurs IDs étant leurs index dans celle-ci).

Les entités ont un comportement personnalisé pour l'opérateur:
+ `del()`: Enlève l'entité de `entites_vivantes[]`. <!--Pas vraiment un opérateur mais restons simple.-->

Concrètement, une entite est une instance de `Entite` ou d'un de ses classes filles: `Joueur` et `Monstre`.  
Quand une classe hérite de `Entite`, il faut qu'elle définisse:
- `_CARTE_MAIN_PREMIERE_POS : Pos` (statique): La postion de la première carte (celle la plus à gauche) de la main de l'entite.
- `_CARTES_DE_DOS : bool` (statique): Si les cartes de la main doivent être dessinées de dos par défaut.
- `.pos_sprite : Pos` (propriété _getter_): La position du centre du sprite sur l'écran.
- `.pos_attaque : Pos` (propriété _getter_): La position sur laquelle les attaques devraient arriver.

### `Entite`
C'est la classe mère pour toutes les entités.

### `Joueur`
Il n'y a qu'un seul objet joueur, c'est la variable `joueur` (déclarée dans [Joueur.py](../sources/Joueur.py)), admis comme étant d'ID 0.

### `Monstre`
Les monstres fonctionnent par types, un type de monstre est un monstre préfait: il aura ses stats et ses attaques propres.  
Voici les types implémentés:
+ Blob (attaque physique)
+ Sorcier (attaque magique)

Tous les types de monstres sont définis dans le fichier [TypesMonstre.json](../data/TypesMonstre.json).  
Chaque type à aussi un "rang", c'est une mesure arbitraire utilisée pour estimer rapidement la puissance d'un monstre; pour l'instant ce n'est utilisé que pour le calcul des pièces gagnées.

## Les stats
Pour représenter les stats d'une entités, on utilise une instance de `Stat` (classe définie dans [Stat.py](../sources/Stats.py)).

Pour le moment il y a sept stats:
- `.vie`: La vie restante à l'entité détenant l'objet.
- `.vie_max`: La valeur maximum que la vie puisse avoir.
- `.force`: La puissance d'attaque physique.
- `.defense`: La défense pour les attaques physiques.
- `.magie`: La puissance d'attaque magiques.
- `.defense_magique`: La défense pour les attaques magiques.
- `.crit_puissance`: Une valeur ajoutée au coups critiques.
- `.crit_resistance`: Une résitance aux dégats critiques.

`Stat` est une dataclasse, ce qui veut dire que l'encapsulation ne s'applique pas dessus.  
Du fait de l'absence de constructeur manuellement définit, `.vie` sera initialisé à un nombre négatif, pour y remédier, utiliser `.reset_vie()`.

## Les cartes
Une instance de `Carte` correspond à une carte dans le jeu.  
Chaque carte est directement prise dans [cartes.json](../data/cartes.json). Comme chaque carte contient un objet Attaque, chaque objet JSON de carte contient aussi les informations de l'attaque correspondante, ces informations sont utilisées par la classe `Attaque`.

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
Toutes les attaques sont _parse_ depuis le fichier [attaques.json](../data/attaques.json). Les clefs des objets correspondent aux paramètres du constructeur, c'est-à-dire:
+ `nom` ---> `._nom`
+ `description` ---> `._desc`
+ `puissance` ---> `._puissance`
+ `vitesse` ---> `._vitesse`
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
	- L'ID est la clef de la fonction d'ajustement dans `_AJUSTEMENTS[]`.
	- Valeur par défaut: `0`
+ `animer` (optionnel) ---> `_animation`
	- Valeur par défaut: `true`

## Les objets passifs
Une instance d'`Item` est un objet passif qui modifie les stats du joueur lorsqu'il est équipé. Le seul moyen de s'en procurer (pour l'instant) est le shop.

Les items sont parsés de [items.json](../data/items.json), l'objet `"stats"` aura ses attributs additionnés aux stats de l'entité quand elle le prendra.