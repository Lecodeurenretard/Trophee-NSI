# Le système de boss

Les classes décrites dans ce fichier sont:
+ [`Boss`](../sources/Boss.py): Un boss.
+ [`BossJSON`](../sources/Boss.py): La représentation JSON d'un boss.

## La classe `Boss`
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

## L'interface
Tout le code utilisant l'interface est dans [fonctions_boss.py](../sources/fonctions_boss.py).

Pour plus de flexibilité, les boss peuvent exécuter des fonctions en dehors de leurs méthodes, c'est _l'interface des boss_. Ces fonctions doivent être conçue comme des méthodes de `Monstre`, par conséquent, elles doivent avoir un attribut `self` (typé).  
Pour transferer des données entre fonctions ou juste en sauvegarder entre appels, les méthodes peuvent modifier le dictionnaire `attributs_supplementaires` (passé sous le nom `attr` ci-dessous).

Il est possible de programmer trois callbacks differents:
```Python
def nouveau_tour(self : Monstre, attr : dict[str, Any]) -> None:
    pass
```
Est exécuté à chaque début de tour (avant le tour du joueur).

```Python
def choisir_atk(self : Monstre, attr : dict[str, Any]) -> int:
    pass
```
Séléctionne une attaque dans la main du monstre, renvoie l'index de la carte à utiliser dans la main (la main est accessible via `self._cartes_main[]`).

_note:_ Si ce callback est utilisé pour juste exécuter du code avant le choix de l'attaque, l'expression `Monstre.choisir_index_carte_main(self)` renvoie l'index qui serait normalement choisit.

```Python
def subir_dmg(self : Monstre, degats_recu : int, attaque_cause : Attaque, attr : dict[str, Any]) -> None:
    pass
```
Est exécuté à chaque fois que le boss reçoit une attaque (ou soin, dans ce cas `degat_recu` sera négatif).

_note:_ L'instruction `Monstre.recoit_degats(self, degats_recu, attaque_cause)` permet de recevoir les dégats comme ils le seraient normalement.

____________________________________________________________________________

Ces méthodes sont toutes à mettre dans un objet `BossInterfaceMethodes` qu'il faut mettre dans le dictionnaire à la fin du fichier avec pour clef le même nom que dans [boss.json](../data/boss.json).  
Si un attribut de l'objet `BossInterfaceMethodes` est `None` (non renseigné), le programme appellera la version de la méthode définie dans `Monstre`.