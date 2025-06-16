# Quelques concepts sur Python
On a evidemment pas et on ne va pas tout apprendre sur Python en NSI. Du coup voici des explications pour se mettre au même niveau.

## 1. les annotations
Python est ce qu'on appelle un langage [typé dynamiquement](https://fr.wikipedia.org/wiki/Typage_dynamique), c'est-à-dire que le type des variables est deviné par l'interpréteur (la chose qui éxécute le code) Python au moment où une valeur y est assigné; des fois, ça peut être utile mais la plupart du temps c'est plus énervant qu'autre chose. Prenons cette signature de fonction:
```Python
def calcul_duree(date_debut, date_fin):
```

On n'a aucune idée de quoi passer en argument des string sous forme `"dd/mm/aa"`? des ints pour des dates [EPOCH](https://fr.wikipedia.org/wiki/Epoch)? des listes/tuples contenant des ints? et les dates doivent-elles inclure une année? On en a aucune idée sans documentation.

Heuresement, il existe des langages [statiquement typés](https://developer.mozilla.org/fr/docs/Glossary/Static_typing) dans lesquels on connait les types, par exemple en C++:
```C++
unsigned int calcul_duree(unsigned int[3] dateDebut, unsigned int[3] dateFin) {
```

On sait directement que la fonction accepte des tableaux (grossièrement la même chose que les listes de Python) contenant 3 entiers positifs chacuns et retourne un entier positif.  
On peut mimer ce comportement en Python, avec ce qu'on appelle _les annotations_:
```Python
def calcul_duree(date_debut : list[int, int, int], date_fin : list[int, int, int]) -> int:
```

Attention, j'ai bien écrit "mimer", en effet là où C++ lancera une erreur au visage du programmeur, Python n'en a rien à faire. **Les annotations sont comme les docstrings**, tu peux faire ce qu'elles disent ou pas.

Exemple:
```Python
def ma_fonction(param : int) -> None:
	...

ma_fonction("Pas un nombre entier du tout")	# OK
```

Pour éviter les comportements innatendus, on peut utiliser `assert` et l'opérateur `is`.
```Python
def ma_fonction(param : int) -> None:
	assert(param is int)

ma_fonction("Pas un nombre entier du tout")		# AssertionError
```
J'en profite pour rappeler que `==` compare les valeurs (`5 == 5`) et que `is` compare les types (`5.0 is float`).


### La syntaxe
La syntaxe est assez simple, il y a 3 règle:
+ Pour annoter une variable, on utilise les deux points `:`.
+ Pour indiquer le type de retour d'une fonction, on utilise la flèche `->` avant les deux points.
+ Si jamais il peut y avoir plusieurs types, on les sépare par l'opérateur de disjonction `|`.

Exemples:
```Python
variable_sans_valeur : bool	# On déclare le variable sans lui donner de valeur (annotation obligatoire)
string_var : str = "string"

def fonction_basique() -> None:	# Si une fonction ne retourne rien, elle retourne None
	...		# alternative à pass

def renvoie_string(nombre : float) -> str:
	return ""

def parametre_par_defaut(p1 : None, p2 : int = 69) -> None:
	...


multi_var : int | None = None	# une int ou None
multi_var = 5

def ou_alors(p1 : int | float) -> str | None:
	...
```

Certaines annotations (comme `list`) peuvent prendre des types en paramètre, pour cela il faut ajouter des crochets `[]` avec un ou des types à l'intérieur.
```Python
ma_simple_liste : tuple # une tuple avec un nombre indéterminé d'éléments de types inconnus

ma_liste : list[bool]	# une liste avec des booléens à l'intérieur
ma_liste : list[int | float]	# une liste avec des int et des float à l'intérieur
ma_tuple : tuple[()]	# une tuple vide
ma_tuple : tuple[float, str]	# une tuple avec une float et une string à l'intérieur
ma_tuple : tuple[float, ...]	# une liste avec des float à l'intérieur
mon_dictionnaire : dict[str, int]	# une dictionnaire avec des strings pour clefs et des entiers pour valeur
```

La PEP 484 introduit d'autre syntaxes comme [les _types comments_](https://peps.python.org/pep-0484/#type-comments) (commentaires de type) et les [strings en guise d'annotation de type](https://peps.python.org/pep-0484/#forward-references), mais les deux sont assez rare à utiliser dans ce projet, sachez que ces méthodes existent.
```Python
facebook : 'str' = "méta string"
les_coms = 23	# type: int
```

### Liste des annotations disponibles
Je ne vais pas faire la liste exhaustive (vous en trouverez une bonne partie [ici](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)) mais retenez que en général, c'est le même nom que le type en anglais.

- Aucune valeur (none): `None`
- booléen (boolean): `bool`
- entier (integer): `int`
- flottant (floating point): `float`
- chaine de caractères (string): `str`
- liste (list): `list`
- tuple (tuple): `tuple`

Il n'y a presque aucune autre annotation de type en _vanilla_ Python, mais il existe la librarie `typing` qui défini plein d'autre types.  
Comme vous le savez peut-être les fonctions peuvent être stockées dans des variables, si on importe `Callable` de `collections.abc`, il est possible de d'annoter des fonctions:
```Python
from  collections.abc import Callable
def fun_to_be_a_function(param : str) -> bool:
	...

def fonction_seconde(p1 : bool, p2 : int, p3 : float) -> None:
	...

def fonction_troisieme(p1 : bool, p2 : bool) -> None:
	...

function : Callable[[str], bool] = fun_to_be_a_function		#pas de parenthèse car on n'appelle pas la fonction, on veut l'objet en lui-même

no_fun : Callable[[bool, int, float], None] = fonction_seconde

multi_fun : Callable[..., None] = fonction_seconde	# Peut importe les arguments
multi_fun = fonction_troiseme
```
### Créer de nouvelles anotations
Les types créés par l'utilisateur (nous) ont leurs annotations:
```Python
class LaClasse:
	...
classieux : LaClasse
```

On peut aussi créer des alias avec le mot-clef `type`, si l'on a importé `TypeAlias` de `typing`:
```Python
from typing import TypeAlias

# Pour Python 3.12
type entier = int
type charactere = str
type string = list[charactere, ...]

# Pour les anciens
meilleure_int : TypeAlias = tuple[int]
meilleure_str = tuple[str]

parler_francais			: entier = 9876
en_python				: string = ['h', 'e', 'y']
c_est_possible			: meilleure_int = (56,)
pour_les_francophones	: meilleure_str = ("Oi!",)
```


C'était un guide assez détaillé, pour plus de possiblilités allez voir la [documentation de `typing`](https://docs.python.org/3/library/typing.html).  
Si jamais, vous voulez des définitions plus formelles allez voir la [PEP 484](https://peps.python.org/pep-0484/)