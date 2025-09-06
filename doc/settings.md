# La gestions des paramètres
Ce fichier contient la description des classes:
- `Parametre` (ainsi que les enums/_wrappers_ en lien)

## L'énumération `TypeParametre`
Cette énumération contient tous les types (ou catégories pour éviter l'ambiguité avec les types de Python) de paramètres implémentés ainsi que leurs données.
Les catégories sont les suivantes:
<!--Je n'ai jamais aimé les tableaux markdown car ils ne sont jamais alignés-->
| Nom dans l'énumération | Nom utilisé |                            Usage                                 | Type de `Parametre._valeur` | implémenté? |
|:----------------------:|:-----------:|:----------------------------------------------------------------:|:---------------------------:|:-----------:|
|     `CASE_A_COCHER`    |  checkbox   | Un paramètre que l'on peut activer et désactiver à souhait.      |             `bool`          |      ✅     |
|         `RADIO`        | bouton radio| Une liste de choix dans laquelle on ne peut faire qu'un seul choix. Il est sûr qu'exactement une case est cochée.   |     `str`   |      ❌      |
|      `CHECKBOXES`      | liste de checkboxes   | Une liste de choix dans laquelle le joueur peut séléctionner autant de choix possibles (y compris aucun). | `list[str]` |      ❌      |
|       `SLIDERF`        | slider (de flottants) | Un flottant étant limité par un maximum et minimum.    |             `float`         |      ❌      |
|       `SLIDERI`        | slider (d'entiers)    | Un entier étant limité par un maximum et minimum.      |              `int`          |      ❌      |
|        `TEXTE`         |  input (de texte)     | Un champ texte permettant au joueur d'écrire du texte. |              `str`          |      ❌      |
|         `INT`          |  input (de entiers)   | Un champ texte permettant au joueur d'écrire un entier (parsé par `int()`). | `int`  |      ❌      |
|        `FLOAT`         | input (de flottants)  | Un champ texte permettant au joueur d'écrire un nombre à virgule (parsé par `float()`)                    |   `float`   |      ❌      |

Elle contient aussi toutes les données ne variant pas dans les instances du même type comme les dimensions pour le dessin ou la hitbox.

## La classe `Parametre`
Cette classe contient tous les paramètres dans le menu. Les paramètres peuvent agir comme des variables globales, à différence près qu'ils peuvent être changés par l'utilisateur. Un exemple est disponible dans [ex_param](../exemples/ex_param.py).

Chaque instance peut être d'une des catégories de `TypeParametre`.

opérateurs définis:
- convertions
	+ vers `bool`:  Renvoie `._valeur` si dans une catégorie le permettant (v. tableau) sinon élève une `TypeError`.
	+ vers `int`:   Renvoie `._valeur` si dans une catégorie le permettant (v. tableau) sinon élève une `TypeError`.
	+ vers `float`: Renvoie `._valeur` si dans une catégorie le permettant (v. tableau) sinon élève une `TypeError`.
	+ vers `str`:   Renvoie `._valeur` si dans une catégorie le permettant (v. tableau) sinon élève une `TypeError`.

