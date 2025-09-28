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
> def attaquer(self, id_cible : int, attaque : Attaque) -> None
>```
> ou
>```Python
> def attaquer(self, id_cible : int, clef_attaque : str) -> None
>```
Enregistre l'attaque dans `Attaque.attaque_du_tour[]`.

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
Tous les monstres sont automatiquement ajoutés à la liste `Monstre.monstres_en_vie[]` et à `entites_vivantes[]`.

Les monstres fonctionnent par types, un type de monstre est un monstre préfait: il aura ses stats et ses attaques propres. Les types sont gérés par l'énumération `TypeMonstre` (définie dans [Monstre.py](../sources/Monstre.py)).  
Voici les types implémentés:
+ Blob (attaque physique)
+ Sorcier (attaque magique)

Il est préférable de créer les nouveaux monstres par `Monstre.nouveau_monstre()` pour initialiser l'instance à un type plutôt que des stats précises.  
Pour détruire le monstre, il faut appeler `.meurt()`.

## Les stats
Pour représenter les stats d'une entités, on utilise une instance de `Stat` (classe définie dans [Stat.py](../sources/Stats.py)).

Pour le moment il y a sept stats:
- `.vie`: La vie restante à l'entité détenant l'objet.
- `.vie_max`: La valeur maximum que la vie puisse avoir.
- `.force`: La puissance d'attaque physique.
- `.defense`: La défense pour les attaques physiques.
- `.magie`: La puissance d'attaque magiques.
- `.defense_magique`: La défense pour les attaques magiques.
- `.vitesse`: influera sur l'ordre des attaques (non implémenté).
- `.crit_puissance`: Une valeur ajoutée au coups critiques.
- `.crit_resistance`: Une résitance aux dégats critiques..

`Stat` est une "structure" (terme que j'ai importé du C++), ce qui veut dire que l'encapsulation ne s'applique pas dessus.  
Dû à l'absence de constructeur manuellement définit, `.vie` sera initialisé à un nombre négatif, pour y remédier, utiliser `.reset_vie()`.

## Les attaques
Chaque attaque est représentée par un objet `Attaque` (classe définie dans [Attaque.py](../sources/Attaque.py)).  
attributs:
+ `._nom`: Le nom de l'attaque.
+ `._desc`: Une courte description à montrer à l'utilisateur.
+ `._puissance`: La puissance de l'attaque, sera utilisé pour calculer les dégats causés par l'attaque avec les stats du lanceur et de la victime.
+ `._vitesse`: La vitesse de l'attaque, sera combinée avec celle du lanceur lors du classement.
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
	- `.vitesse`
	- `.desc`
- `.nom_surface`: Une surface contenant le nom du monstre _rendered_ avec la bonne police de texte.
+ `.friendly_fire`: Si l'attaque peut toucher le lanceur ou ses alliés.
+ `.ennemy_fire`: Si l'attaque peut toucher l'adversaire au lanceur ou ses alliés.

Les objets `Attaque` ont un comportement personnalisé pour les opérateurs:
+ `==`: Compare les noms des attaques.
+ `!=`: Renvoie l'inverse de l'opérateur `==`.

Les attaques se chargent d'infliger les dégats.  
Les attaques prédéfinies sont dans le dictionnaire `ATTAQUES_DISPONIBLES[]` (défini dans [Attaque.py](../sources/Attaque.py)) puis sont copiées dans un objet .

Les attaques ont des types et des effets.  
les types sont membres de l'énumeration `TypeAttaque` (définie dans [Attaque.py](../sources/Attaque.py)) et dirigent la façon dont les dégats seront calculés et comment doit être traité.  
Les effets seront les modifications de statut appliqués au destinataire, ils ne sont pas encore implémentés.

## Un tour expliqué sous différents points de vue
### Du point de vue du joueur
Un tour commence quand le joueur choisit une attaque à lancer. Le monstre en choisira ensuite une autre suivant son type. Les attaques serons ensuite lancées suivant leurs vitesses; si une entité meurt avant que son attaque ne soit lancée, l'attaque sera _skip_.

### Du point de vue des entitées
Le tour commence quand elle copie une attaque de son moveset pour l'insérer un objet `AttaquePriorisee` contenant l'attaque à lancer dans la file `Attaque.attaque_du_tour[]`. Peu de temps après, elle doit changer son nombre de PV du fait d'appels de `.recoit_degats()`. Si elle survit au dégats infligés, elle peut passer au prochain tour, sinon elle est détruite.

### Du point de vue de l'attaque
Le tour commence quand elle est copiée pour avoir ses membres `._lanceur_id` et `._cible_id` défini puis la copie est insérée dans un objet `AttaquePriorisee` qui est lui-même _push_ dans `Attaque.attaque_du_tour[]`. Après peu, l'attaque priorisée ressort et si le lanceur est toujours vivant et que la cible correspond bien aux drapeaux l'attaque est lancée et les dégats sont envoyés à l'entité cible. Si l'attaque se révèle être un crit, son attribut `._crit` devient `True`. L'attaque est dessinée avec `.dessiner()` et est enfin détruite.