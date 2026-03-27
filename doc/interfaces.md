# Les interfaces
Pour rendre le développement de certaines parites du jeu plus accessibles, il existe les interfaces qui permettent une insertion de comportements personalisés sans avoir à comprendre l'entièreté des classes/système de combat.

Les fonctions utilisants les interfaces si dessous sont à mettre dans les fichiers indiqués puis doivent être passées dans le dictionnaire `callbacks[]` qui se trouve en bas du fichier. Les valeurs de ce dictionnaires sont des instances de `XInterfaceMethodes` où le X est remplacé par le nom de l'interface, ces objets ont pour rôle de contenir les fonctions utilisant les interfaces. Passer `None` ou omettre un argument revient à passer une fonction ayant aucun effet. Les clefs du dictionnaire doivent correspondre au nom de la chose dans le JSON sinon les méthodes ne seront jamais exécutées.

## Elements communs
Le fonctionnement général des interfaces est identique: Une fonction est passée et cette fonction est exécutée **comme une méthode**. En effet, ces fonctions sont autorisées à accéder aux membres non publics des objets et prennent `self` en premier paramètre (même si ce `self` doit être annoté pour aider le _type checker_).

Si une de ces méthodes a besoin de stocker des données persistant entre les appels, elle peuvent le faie dans le dictionnaire `attr` (pour attributs) passé en dernier paramètre.  
Prenez par exemple:
```Python
def ma_methode(self : Item, attr : dict[str, Any]) -> None:
    if "compteur" not in attr.keys():   # setup pour le premier appel
        attr["compteur"] = 0
    
    attr["compteur"] += 1
    print("Cette fonction a été appelée", attr["compteur"], "fois.")
```
Affiche le nombre de fois qu'elle a été appelée.

Bien qu'en Python il soit possible de créer des attributs dynamiquement, la solution du dictionnaire est meilleure car elle s'assure que tous les instances d'une même classe aient les mêmes membres.


## L'interface des boss
Utilisée dans [fonctions_boss.py](../sources/fonctions_boss.py).

Il est possible de programmer trois callbacks differents:
```Python
def nouveau_tour(self : Monstre, attr : dict[str, Any]) -> None:
```
Est exécuté à chaque début de tour (avant le tour du joueur).

```Python
def choisir_atk(self : Monstre, attr : dict[str, Any]) -> int:
```
Séléctionne une attaque dans la main du monstre, renvoie l'index de la carte à utiliser dans la main (la main est accessible via `self._cartes_main[]`).

> _note:_ Si ce callback est utilisé pour juste exécuter du code avant le choix de l'attaque, l'expression `Monstre.choisir_index_carte_main(self)` renvoie l'index qui serait normalement choisit.

```Python
def subir_dmg(self : Monstre, degats_recu : int, attaque_cause : Attaque, attr : dict[str, Any]) -> None:
```
Est exécuté à chaque fois que le boss reçoit une attaque (ou soin, dans ce cas `degat_recu` sera négatif).

> _note:_ L'instruction `Monstre.recoit_degats(self, degats_recu, attaque_cause)` permet de recevoir les dégats comme ils le seraient normalement.

## L'interface des cartes
Utilisée dans [fonctions_cartes.py](../sources/fonctions_cartes.py).

Il est possible de programmer un seul callbacks:
```Python
def jouee(self : Carte, attr : dict[str, Any]) -> None:
```
Est exécuté juste après l'application des dégats sur l'entité cible.

## L'interface des items
Utilisée dans [fonctions_items.py](../sources/fonctions_items.py).

Les callbacks sont traités dans l'ordre de rammassages des items de la part de l'entité. Prenons pour instance, une situation où le joueur achète item1 puis item2 au shop, les callbacks d'item1 serons appelés avant ceux d'item2.

Il est possible de programmer six callbacks differents:
```Python
def nouveau_tour(self : Item, attr : dict[str, Any]) -> None:
```
Est exécuté au début d'un tour juste après son équivalent dans `Boss`.

```Python
def nouvel_etage(self : Item, attr : dict[str, Any]) -> None:
```
Est exécuté à chaque nouvel étage, juste après que l'entité détenteur de l'item ait repioché.

```Python
def nouveau_shop(self : Item, items_du_shop : list[Item], attr : dict[str, Any]) -> None:
```
Est exécuté avant que le joueur rentre dans le shop.
`items_du_shop` est une référence sur la liste des items du shop, ainsi modifier un de ces items modifiera celui qui sera dans le shop.

```Python
def carte_jouee(self : Item, carte : Carte, attr : dict[str, Any]) -> None:
```
Est exécuté juste avant que le porteur de l'item joue sa carte.
Encore une fois, `carte` est passée par référence.

```Python
def porteur_subit_dmg(self : Item, attaque : Attaque, id_porteur : int, attr : dict[str, Any]) -> None:
```
Quand le porteur de l'item reçoit une attaque.
Le paramètre `attaque` est copié.

> _rappel:_ On peut obtenir une entité depuis son ID avec `Entite.vivants()[id]`.  
Le joueur est toujours d'ID `EntiteJSON.INDEX_JOUEUR` et on peut y accéder par la variable globale `joueur` mais attention le joueur n'est pas forcément le porteur de l'item et il devrait marcher pareil peut importe son porteur. Il serait légitime de séprarer seulement si l'item fait une opération propre au joueur comme la gestion d'argent.

```Python
def adversaire_subit_dmg(self : Item, attaque : Attaque, id_adversaire : int, attr : dict[str, Any]) -> None:
```
Même chose que `porteur_subit_dmg()` mais est appelé quand le porteur frappe un adversaire.

> _note:_ Si le lanceur s'attaque lui-même (avec un soin par exemple), cette fonction sera quand même appelée et sera exécutée après `porteur_subit_dmg()`.