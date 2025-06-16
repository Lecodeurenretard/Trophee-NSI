# Quelques concepts sur Python
On a evidemment pas et on ne va pas tout apprendre sur Python en NSI. Du coup voici des explications pour se mettre au même niveau.

## 0. Les bonnes pratiques
Il est facile de créer un code qui fait ce qu'on veut mais il est un peu plus compliqué d'écrire un code compréhensible facilement. Heureusement, des développeurs bien plus expérimenté que nous se sont penchés sur la question et nous ont apporté des conseils pour rendre le code plus lisible et instinctif. J'insiste sur le fait que ce sont des **conseils** et peuvent ce révéler dans certains cas plus contre-productifs qu'autre chose, c'est donc au développeur de réfléchir si il est pertinent d'écrire de cette façon.

### Le ZEN de Python
La [PEP 20](https://peps.python.org/pep-0020/) nous indique que Tim Peters (qui à beaucoup contribué au langage) à énoncé 20 directives qu'il faudrait suivre pour le design du langage Python, en voici la traduction des principales:
```
Explicite c'est meilleur qu'implicite.
Simple c'est meilleur que complexe.
Complexe c'est meilleur que compliqué.
Plat c'est meilleur qu'indenté.
Clairsemé c'est meilleur que dense.
La lisibilié compte.
Les cas spéciaux ne sont pas assez spéciaux pour briser les règles.
Les erreurs ne devrait jamais être silenciées.
A moins que ce le soit explicitement.
Maintenant c'est mieux que jamais.
```

Je vous laisse vous en inspirer.

### Le principe DRY
Le principe _D.R.Y._ est simple: _Don't Repeat Yourself_ (ne te répète pas). Dans un code parfais, il ne devrait pas avoir deux lignes qui se ressemble: tout doit être regroupé. Pourquoi?  
Pour répondre à cette question, prenons un exemple qu était dans le code avant refactorisation:
```Python
pygame.quit()
sys.exit()
```
Elles ont une fonction bien précise: quitter le programme et en oublier une ou se tromper dans l'ordre peut potentiellement causer un comportement innatendu du programme. Même en copiant et en collant, c'est un problème; imaginons que pour déboguer l'on veuille ajouter un `print()` à chaque fois que le programme s'arrète, doit-on faire `Ctrl + F` pour chaque fichier et y ajouter son `print()`? Puis quand on veut l'enlever, rebelotte? non, il y a plus simple.

La solution est simplement de créer une fonction prenant ces deux lignes:
```Python
def quit():
	pygame.quit()
	sys.exit()
```
Maintenant s'il faut ajouter un `print()`, on l'ajoute dans la fonction, chaque sortie aura son `print()`.

Il est même pertinent de créer des fonctions même si le code n'est répété car c'est souvent plus propre que de le voir au milieu d'un autre blob de code et rien que le nom de la fonction peut faire office de commentaire vu qu'il explique ce que fait la fonction.

### Evitez de trop indenter
Idéalement, l'indentation ne devrait pas dépasser 4 en tout point du code et cette indentation de 4 doit être occasionnelle. La raison est simple: plus un script est nesté (à de `if`, `for`, etc imbriqués), plus ce script est compliqué à lire car il faut se souvenir de chaque condition qu'il a fallut pour y arriver.

Pour dénester le code, il existe 2 technique prominente: la mise en fonction et l'inversion. La première est facile à comprendre: on met le code dans une fonction; la deuxième est un peut plus compliquée, prenons:
```Python
def fonction():
	if condition:
		fait_qql_chose()
```
L'inverser donnerait
```Python
def fonction():
	if not condition:
		return	# Retourne None
	
	# On est sûrs que condition est vraie
	# car return finit l'éxécution de la fonction
	fait_qql_chose()
```

Il est aussi possible de le faire dans des boucles avec `continue`/`break`:
```Python
for nombre in (1, 2, 3, 4):
	if nombre == 1:
		le_un()
```
```Python
for nombre in (1, 2, 3, 4):
	if nombre != 1:
		continue

	# On est sûrs que nombre == 1
	le_un()
```

Comme exercice, vous pouvez refactoriser ceci:
```Python
liste = [1, 2, 3, 4]

jusqu_au_pairs = []
for nombre in liste:
	if nombre % 2 == 0:		# pair
		jusqu_au_pairs.append([])
		for nb in range(1, nombre+1):	# [1, 2, ..., nombre]
			jusqu_au_pairs[-1].append(nb)

# jusqu_au_pairs = [
# 	[1, 2],
# 	[1, 2, 3, 4],
# ]
```
______
**solution**
```Python
def ajouter_jusqua(n):
	resultat = []
	for nb in range(1, n+1):	# [1, 2, ..., nombre]
		resultat.append(nb)
	
	return resultat

liste = [1, 2, 3, 4]
jusqu_au_pairs = []
for nombre in liste:
	if nombre % 2 != 0:
		continue
	
	jusqu_au_pairs.append(ajouter_jusqua(nombre))

# jusqu_au_pairs = [
# 	[1, 2],
# 	[1, 2, 3, 4],
# ]
```

C'est, certes, plus long mais beaucoup facile à lire.

Souvenez-vous que l'objectif est que le plus grand nombre de ligne soit au plus petit niveau d'indentation.

### Les commentaires peuvent mentir
Certains développeurs avancent qu'il ne faudrait jamais utiliser de commentaire (à quelques exceptions près). Bein que je ne soit pas d'accord, j'approuve leur argument principal: **il est facile d'oublier de modifier un commentaire**, ce qui provoque un décalage entre le commentaire et le code, ce qui n'est jamais bon.

Il n'y a pas vraiment de solution à ça mais on peut réfléchir au but des commentaires en premier lieu: un commentaire ne doit pas expliquer _ce que fait_ le code, mais **pourquoi** le code est ainsi pour pas que les autres développeurs ou vous du futur fassent une erreur en le modifiant.

Attention, cela ne veut pas dire qu'il faut néscéssairement abandonner tout commentaire expliquant le code, il faut juste les limiter car les codeurs savent lire du Pythons.

### Le principe de la boite noire
Ce principe dit que toute structure (classe, fonction) doit-être vu comme une [boite noire](https://fr.wikipedia.org/wiki/Bo%C3%AEte_noire_(syst%C3%A8me)); autrement dit: quand on utilise une fonction, on se fiche de comment elle accomplit sa tâche, on n'est intéressé que par ce qu'il lui faut donner en entrée et ce qu'elle renvoie en sortie et rien d'autre. C'est notament parce que quelq'un peut changer l'intérieur dans une mise-à-jour future.

### La PEP 8
On sait tous à quoi sert la [PEP 8](https://peps.python.org/pep-0008/), c'est un assemblage de règles qui permet d'écrire du Python plus élégament, même si certaines règles sont contestables comme les [lignes de 79 caractères maximum](https://peps.python.org/pep-0008/#maximum-line-length). Il faudrait essayer d'y adhérer le plus possible.

### Autres recomandations
Cette section est pour des suggestions autres.

Si vous parlez assez bien anglais, allez voir [CodeAesthetics](https://www.youtube.com/@codeaesthetic), il fait des vidéos de quelques minutes sur comment organiser le code.

## 1. Les annotations
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

Le module `typing` donne accès aux annotations `Any` et `NoReturn` qui ne représentent pas de type en particuler.  
`Any` représente une union de tous les types qui existent, il ne faut **pas** l'utiliser si le type d'une variable n'est pas connu (on ne met pas d'annotation dans ce cas), il faut l'utiliser seulement quand une variable peut être (et probablement sera) de n'importe quel type.  
`NoReturn` ne s'utilise qu'en type de retour d'une fonction et indique que soit la fonction lancera une erreur, soit la fonction fera quitter le programme mais ne doit **jamais** utiliser de `return` explicite ou implicite.  
Exemple:
```Python
from typing import Any, NoReturn
tous_type : Any
tous_type = 1	# int
tous_type = 1.0	# float
tous_type = "s"	# str
tous_type = {}	# dict
tous_type = max # fonction

def retourne_implicitement() -> None:
	print("Je retourne None")
	# Retourne implicitiment None

def ne_retourne_pas(lancer) -> NoReturn:
	if lancer:
		raise Exception("Je suis une erreur")	# Quitte la fonction par une erreur
	
	from sys import exit
	exit(1)		# Quitte la fonction en fermant le programme
	# retour implicite jamais atteint
```

### Créer de nouvelles annotations
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
meilleure_int : TypeAlias = tuple[int]	# avec annotation
meilleure_str = tuple[str]				# sans annotation

parler_francais			: entier = 9876
en_python				: string = ['h', 'e', 'y']
c_est_possible			: meilleure_int = (56,)
pour_les_francophones	: meilleure_str = ("Oi!",)
```


C'était un guide assez détaillé, pour plus de possiblilités allez voir la [documentation de `typing`](https://docs.python.org/3/library/typing.html).  
Si jamais, vous voulez des définitions plus formelles allez voir la [PEP 484](https://peps.python.org/pep-0484/)


## 2. La programation orientée objet
La programmation orientée objet (POO ou OOP en anglais) est l'un des styles majeurs de _design_ de code avec l'impératif et le fonctionnel. Pour résumer, ce style repose sur la définition de plans pour construire des _objets_ qui peuvent être utilisés pour faire des actions.

### Introduction
Disons que nous sommes dans une usines de chaises et qu'il faut coder les machines pour fabriquer des chaises. Pour cela, il nous faut définir les caractéristiques que chaque chaise a, il nous faut:
- le nombre de pieds
- si la chaise à des roullettes
- les dimensions de la chaise


### Le constructeur
Il nous faut définir une _classe_ "chaise" qui définira ce qu'auront chaque chaises puis à partir de cette classe nous allons construire des _objets_ (ou instances) qui représenterons une chaise à fabriquer avec les machines. Dans la classe, il doit y avoir une fonction qui "construit" les objets, elle s'appelle le _constructeur_ et est la fonction `__init__()`.  
Voici la synatxe en Python:
```Python
class Chaise:
	# On définit le constructeur de Chaise
	def __init__(self, nb_pied : int, a_roullettes : bool, dimensions : tuple[float, float, float]):
		self.nb_pied : int = nb_pied
		self.a_des_roues : int = a_roullettes
		self.dim : tuple[float, float, float] = dimensions

ma_chaise : Chaise = Chaise(4, False, (.5, .5, 1))
```

L'exemple ci-dessus, définit le constructeur puis l'appelle pour créer une chaise.  
A partir de la ligne 5, on définit des variables comme `self.nb_pied`, ce sont des variables qui appartiennent à l'objet. Notez, que la fonction `__init__()` est **la seule** fonction à pouvoir déclarer des variables qui appartiennent à `self`.  
Nous pouvons voir que le premier argument `self`, est **ignoré** lors de l'appel du constructeur; il représente l'objet que l'on est en train de construire, c'est pour cela que les variables définie appartiennent à `self`, c'est des variables inhérentes à l'objet.

A la dernière ligne, la variable `ma_chaise` est définie, elle est de type `Chaise` et pour qu'elle soit une chaise, on appelle le constructeur qui est, pour l'instant, le seul moyen d'obtenir une chaise. De part les paramètre du constructeur, on en déduit que:
```Python
ma_chaise.nb_pied	== 4
ma_chaise.a_des_roues	== False
ma_chaise.dim		== (.5, .5, 1)
```

Pour résumer, les constructeurs sont les moyens principaux de créer des objets, définissent les variables des instances et peuvent être appelés avec le nom de la classe qu'ils contruisent.

### Parenthèse vocabulaire
Petit point lexique:

Les variables appartenants aux objets sont appelés _variables membre_ ou alors _attributs_.  
Les fonctions définies dans une classe sont des _fonctions membre_ ou _méthodes_.

_Instance d'une classe_ désigne la même chose qu'un objet.

### Créer des méthodes
Créer une méthode, c'est créer une fonction normale mais on indente pour qu'elle appartienne à la classe, toute méthode prend comme premier paramètre `self`, qui représente l'objet qui fait l'appel de la méthode. Pour les utiliser, c'est comme les méthodes des listes (`.append()`, `.pop()`, ...).

Dans notre scénarion, nous pourrions avoir des méthodes qui gère la fabrication de la chaise:
```Python
class Chaise:
	# On définit le constructeur de Chaise
	def __init__(self, nb_pied : int, a_roullettes : bool, dimensions : tuple[float, float, float]):
		self.nb_pied : int = nb_pied
		self.a_des_roues : int = a_roullettes
		self.dim : tuple[float, float, float] = dimensions
	
	def placer_pieds(self) -> None:
		demander_pieds(self.nb_pieds)	# demande le bon nombre de pieds
		...	# fait autre chose
	
	def placer_dossier(self) -> None:
		pass
	
	def placer_assise(self) -> None:
		pass

	def construire(self, combien : int) -> None:
		for _ in range(combien):	# fait combien itérations (aucune variable)
			self.placer_pieds()
			self.placer_assise()
			self.placer_dossier()
			...

ma_chaise : Chaise = Chaise(4, False, (.5, .5, 1))
ma_chaise.construire(5)		# Construit 5 chaise avec les propriétés de ma_chaise
```

Certaines méthodes ont des noms qui commencent et terminent par deux underscores `__`, ce sont les _méthodes magiques_, il y en a pas mal et elles ne sont pas utiles pour ce projet du coup, je ne les détaillerais pas mais vous pouvez allez les voir vous même à [la documentation](https://docs.python.org/3.13/reference/datamodel.html#special-method-names).

### L'encapsulation
L'encapsulation est un concept similaire à celui de la [boite noire](https://fr.wikipedia.org/wiki/Bo%C3%AEte_noire_(syst%C3%A8me)). Le principe est de considérer un objet comme une capsule opaque, creuse et avec des bouttons dessus qui représentent les méthodes, à l'intérieur il y a des données (attributs) qui sont innacessibles à l'utilisateur de la classe qui ne peut qu'appuyer sur les boutons à la surface.  
En somme, la seule façon de modifier et lire les attributs d'un objet doit être par ses méthodes; malheureusement, en Python il n'existe pas de moyen de s'assurer que c'est respecté mais il y a des conventions, on verra plus tard.

Je me souviens que quand j'ai appris ce concept pour la première fois, je n'y croyais pas beaucoup non plus alors pourquoi devrait-on respecter l'encapsulation en premier lieu? La réponse que j'ai reçu, c'est qu'il ne faut pas submerger l'utilisateur de choix; cependant je ne suis pas convaincu par cette explication, surtout en Python où les variables ne sont pas protègées; ma réponse est qu'avec cette approche, on peut forcer l'utilisateur à utiliser d'une certaine façon.  
Par exemple, il est possible pour la fabrication de chaises de ne vouloir que de l'extérieur, on ne sache que le type de chaise construite.

Comme on ne peut pas directement prendre une variable, il existe des méthodes conçues uniquement pour récupérer la valeur d'un attribut, on les appelle les fonctions _getters_, de même une fonction conçue uniquement pour changer la valeur d'un attribut s'appelle une fonction _setter_.

Tous ceci est bien mais il nous manque un élément crucial pour pouvoir mettre en place l'encapsulation: un moyen de dire à l'utilisateur de ne pas accéder à un membre d'une classe / d'un objet.  
Dans un langage de programation orienté objet standard, on trouve deux types de membres: les membres _privés_ et _publics_; les premiers ne peuvent être accédés seulement par une méthode membre de la même classe dont ils sont, les seconds peuvent être accédés depuis n'importe où.  
Comme je l'ai écrit plus haut, il est impossible en Python de s'assurer qu'un membre soit privé, il existe cependant une convention installée par la [PEP 8](https://peps.python.org/pep-0008/#method-names-and-instance-variables): les attributs non publics commencent par un seul underscore `_`. Comme Python n'a pas d'attribut privés à proprement parler, la [PEP 8](https://peps.python.org/pep-0008/#designing-for-inheritance) indique qu'il ne faudrait pas parler d'attribut "privés" mais "non publics".

Voici une veresion de `Chaise` respectant l'encapsulation:
```Python
class Chaise:
	# On définit le constructeur de Chaise
	def __init__(self, nb_pied : int, a_roullettes : bool, dimensions : tuple[float, float, float]):
		self._nb_pied : int = nb_pied
		self._a_des_roues : int = a_roullettes
		self._dim : tuple[float, float, float] = dimensions

	# getter pour _nb_pied
	def get_nb_pied(self) -> int:
		return self._nb_pied
	
	# getter pour _dim
	def get_nb_pied(self) -> int:
		return self._dim
	
	# Pas de getter pour _a_des_roues, peut-être que ce n'est pas pertinent

	# Pas de setter du tout, une chaise doit rester constante

	# Les méthodes non publiques existent aussis
	def _est_chaise_gamer(self) -> bool:
		pass

	def est_comfortable(self, reponse_honnete : bool = False) -> bool:
		return True		# Toutes les chaises fabriquées sont comfortables

ma_chaise : Chaise = Chaise(4, False, (.5, .5, 1))
print(ma_chaise.est_comfortable())		# pas d'erreur et autorisé
print(ma_chaise._est_chaise_gamer())	# pas d'erreur mais va à l'encontre des développeurs de la classe
```