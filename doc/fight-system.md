# Comment marche le système de combat

Les classes décrites dans ce fichier sont:
+ [`Stat`](../sources/Stats.py): Représente les statistiques d'une entité.
+ [`Attaque`](../sources/Attaque.py) (ainsi que les enums/_wrappers_ en lien): Toute action qui puisse influer sur cette ou une autre entité.
+ [`Joueur`](../sources/Joueur.py): 1<sup>er</sup> type d'entité, le personnage que contrôle le joueur.
+ [`Monstre`](../sources/Monstre.py): 2<sup>nd</sup> type d'entité, tout ennemi au joueur.

## Les entités
Une entité est un personnage indépendant en ce qui concerne le combat et pouvant y prendre part.  
Toutes les entités sont enregistrées dans la liste globale `entites_vivantes[]` (leurs IDs étant leurs index dans celle-ci).

Les entités ont un comportement personnalisé pour l'opérateur:
+ `del()`: Enlève l'entité de `entites_vivantes[]`. <!--Pas vraiment un opérateur mais restons simple.-->

Les entités doivent définir les propriétés suivantes, les niveaux minimum d'accès entre parenthèse (dans l'ordre: lecture seule, lecture-écriture et lecture-écriture-suppression):
+ `.id` (lecture seule): L'index de l'entité dans `entites_vivantes`.
+ `.stats` (lecture seule): Les stats de l'entité.
+ `.dbg_nom` (lecture seule): Les noms des entités utilisés pour le débogage (différent de `.__repr__()` car la méthode désigne tout l'objet et non seulement les noms).
+ `.pos_attaque_x` et `.pos_attaque_y` (lecture seule): la position du dessin de l'attaque de l'entité.

Chaque entité est attendue d'avoir des méthodes avec ces signatures et respectant les descriptions:
>```Python
> def attaquer(self, id_cible : int, nom_attaque : str) -> None
>```
Enregistre l'attaque avec le nom `nom_attaque` dans `Attaque.attaque_du_tour[]`.

>```Python
> def recoit_degats(self, degats_recu : int) -> None
>```
Baisse la vie de l'entité, peu importe sa défense.

> ```Python
> def dessiner(self, surface : pygame.Surface, pos_x : int, pos_y : int) -> None
> ```
Dessine l'objet sur `surface` aux positions indiquées.

>```Python
> def dessiner_barre_de_vie(self, surface : pygame.Surface, pos_x : int, pos_y : int) -> None
>```
Dessine la barre de vie à la position demandée.

>```Python
>def est_mort(self) -> bool:
>```
Renvoie si l'entité ne peut plus combattre.

### `Joueur`
Il n'y a qu'un seul objet joueur, c'est la variable `joueur` (déclarée dans [Joueur.py](../sources/Joueur.py)).  
Il n'y a pas besoin d'appeler de fonction pour l'ajouter ou l'enlever de `entites_vivantes[]` car le constructeur et le destructeur (`__init__()` et `__del__()`) s'en chargent automatiquement.

### `Monstre`
Tous les monstres sont automatiquement ajoutés et enlevés des listes `Monstre.monstres_en_vie[]` et `entites_vivantes[]`.

Les monstres fonctionnent par types, un type de monstre est un monstre préfait: il aura ses stats et ses attaques propres.  
Voici les types implémentés:
+ Blob (attaque physique)
+ Sorcier (attaque magique)

Tous les types de monstres sont définis dans le fichier [TypesMonstre.json](../data/TypesMonstre.json). Chaque type à aussi un "rang", c'est une mesure arbitraire utilisée pour estimer rapidement la puissance d'un monstre; pour l'instant ce n'est utilisé que pour le calcul des pièces gagnées.

Il est préférable de créer les nouveaux monstres par `Monstre.nouveau_monstre()` pour initialiser l'instance à un type.

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

## Les attaques
Chaque attaque est représentée par un objet `Attaque` (classe définie dans [Attaque.py](../sources/Attaque.py)).  
attributs:
+ `._nom`: Le nom de l'attaque.
+ `._desc`: Une courte description à montrer à l'utilisateur.
+ `._puissance`: La puissance de l'attaque, sera utilisé pour calculer les dégats causés par l'attaque avec les stats du lanceur et de la victime.
+ `._type`: Le type de dommages causés par l'attaque (sera détaillé plus en bas).
+ `._lanceur_id` et `._cible_id`: Les IDs du lanceur et de la cible, sont changés lors de la copie, par défaut sont à `-1`.
+ `._prob_crit`: La chance de faire un coup critique, doit être sur $[0; 1]$.
+ `._crit`: Si l'attaque à fait un crit, ne **doit pas** être lu avant le calcul des dégats. Par défaut à `False` et le restera pour une attaque de `ATTAQUES_DISPONIBLES[]`.
+ `._effet`: Le ou les effet.s causé.s de l'attaque (sera détaillé plus tard) (non implémenté).
+ `._drapeaux`: Un flag de type `AttaqueFlags` à assigner à l'attaque.


attributs statiques:
+ `_PUISSANCE_CRIT`: Comment un crit devrait monter les dégats.
+ `toujours_crits`: Outil de déboggage, permet de garantir un crit à chaque attaque.
+ `CRIT_IMG`: Une surface avec l'icône de crit déjà chargée.
+ `attaques_du_tour[]`: Une file triée (ordre croissant) contenant toutes les attaques lancées pendant ce tour. Capacité de 10.

propriétés:
+ `._couleur`: La couleur dans laquelle l'attaque sera déssinée une fois lancée, changera sûrement en `Sprite` dans le futur.
+ `.dbg_str`: ...
+ `._lanceur` et `._cible`: Le lanceur et la cible de l'attaque, leur existance est vérifiée par `assert()`.
+ getters:
	- `.puissance`
	- `.desc`
- `.nom_surface`: Une surface contenant le nom du monstre _rendered_ avec la bonne police de texte.
+ `.friendly_fire`: Si l'attaque peut toucher le lanceur.
+ `.ennemy_fire`: Si l'attaque peut toucher l'adversaire au lanceur.

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

## Un tour expliqué sous différents points de vue
### Du point de vue du joueur
Un tour commence quand le joueur choisit une attaque à lancer. Le monstre en choisira ensuite une autre suivant son type. Les attaques serons ensuite lancées suivant leurs vitesses; si une entité meurt avant que son attaque ne soit lancée, l'attaque sera _skip_.

### Du point de vue des entitées
Le tour commence quand l'entitée récupère son attaque et l'enregistre dans la pile. Peu de temps après, elle doit changer son nombre de PV en appelant `.recoit_degats()`. Si elle survit au dégats infligés, elle peut passer au prochain tour, sinon elle est détruite.

### Du point de vue de l'attaque
Le tour commence quand elle est copiée pour avoir ses membres `._lanceur_id` et `._cible_id` défini puis la copie est insérée dans un objet `AttaquePriorisee` qui est lui-même _push_ dans `Attaque.attaque_du_tour[]`. Après peu, l'attaque priorisée ressort et si le lanceur est toujours vivant et que la cible correspond bien aux drapeaux l'attaque est lancée et les dégats sont envoyés à l'entité cible. Si l'attaque se révèle être un crit, son attribut `._crit` devient `True`. L'attaque est dessinée avec `.dessiner()` et est enfin détruite.
