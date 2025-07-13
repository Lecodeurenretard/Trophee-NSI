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
Plat c'est meilleur qu'indenté (nesté en VO).
Clairsemé c'est meilleur que dense.
La lisibilié compte.
Les cas spéciaux ne sont pas assez spéciaux pour briser les règles.
Les erreurs ne devrait jamais être silenciées.
A moins que ce le soit explicitement.
Maintenant c'est mieux que jamais.
```

Je vous laisse vous en inspirer.

### Le principe DRY
Le principe _D.R.Y._ est simple: _Don't Repeat Yourself_ (ne te répète pas). Dans un code parfais, il ne devrait pas avoir deux lignes qui se ressemblent, tout doit être regroupé. Pourquoi?  
Pour répondre à cette question, prenons un exemple qu était dans le code avant refactorisation:
```Python
pygame.quit()
sys.exit()
```
Elles ont une fonction bien précise: quitter le programme; en oublier une ou se tromper dans l'ordre peut potentiellement causer un comportement innatendu du programme. Même en copiant et en collant, c'est un problème; imaginons que pour déboguer l'on veuille ajouter un `print()` à chaque fois que le programme se ferme, doit-on faire `Ctrl + F` pour chaque fichier et y ajouter son `print()`? Puis quand on veut l'enlever, rebelotte? non, il y a plus simple.

La solution est simplement de créer une fonction prenant ces deux lignes:
```Python
def quit():
	pygame.quit()
	sys.exit()
```
Maintenant quand on veut quitter le programme, on appelle `quit()`; s'il faut ajouter un `print()`, on l'ajoute dans la fonction et on est content car il n'y a qu'une ligne de changée.

Il est même pertinent de créer des fonctions même si le code n'est pas nécessairement répété car c'est souvent plus propre que de le voir au milieu d'un autre blob de code. En fait, rien que le nom de la fonction peut faire office de commentaire vu qu'il explique le but du bout de code.

### Evitez de trop indenter
Idéalement, le niveau de l'indentation ne devrait pas dépasser 4 en tout point du code et ce niveau de 4 devrait être occasionnel. La raison est simple: plus un script est nesté (a de `if`, `for`, etc... imbriqués les uns dans les autres), plus ce script est compliqué à lire du fait qu'il faut se souvenir de chaque condition qu'il a fallut pour y arriver.

Pour dénester le code, il existe 2 technique prédominantes: la mise en fonction et l'inversion. La première est facile à comprendre: on met le code dans une fonction; la deuxième est un peut plus complexe, prenons:
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

Il est aussi possible de le faire dans des boucles avec `continue` ou `break`:
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
def ajouter_jusqua(n):	# mise en fonction
	resultat = []
	for nb in range(1, n+1):	# [1, 2, ..., nombre]
		resultat.append(nb)
	# On aurait pu aussi faire
	# return list(range(1, n+1))
	# ou return [nb for nb in range(1, n+1)]
	
	return resultat

liste = [1, 2, 3, 4]
jusqu_au_pairs = []
for nombre in liste:
	if nombre % 2 != 0:	# inversion
		continue
	jusqu_au_pairs.append(ajouter_jusqua(nombre))

# jusqu_au_pairs = [
# 	[1, 2],
# 	[1, 2, 3, 4],
# ]
```

C'est, certes, plus long mais beaucoup plus compréhensible instictivement.

Souvenez-vous que l'objectif est que le plus grand nombre de ligne soit au plus petit niveau d'indentation.

### Les commentaires peuvent mentir
Certains développeurs avancent qu'il ne faudrait jamais utiliser de commentaire (à quelques exceptions près). Bien que je ne soit pas d'accord, j'approuve leur argument principal: **il est facile d'oublier de modifier un commentaire** lors d'une modification du code, ce qui provoque un décalage entre le commentaire et le code, ce qui n'est jamais bon.

Il n'existe pas vraiment de solution à ce problème mais on peut réfléchir au but des commentaires en premier lieu: un commentaire ne devrait pas expliquer _ce que fait_ le code, mais **pourquoi** le code est ainsi pour pas que les autres développeurs ou vous du futur fassent une erreur en le modifiant.  
Attention, cela ne veut pas dire qu'il faut nécessairement abandonner tout commentaire expliquant le code, il faut juste les limiter car les codeurs savent lire du Python.

### Le principe de la boite noire
Ce principe dit que toute structure (classe, fonction) doit-être vu comme une [boite noire](https://fr.wikipedia.org/wiki/Bo%C3%AEte_noire_(syst%C3%A8me)); autrement dit: quand on utilise une fonction, on se fiche de comment elle accomplit sa tâche, on n'est seulement intéressé des entrées et des sorties et rien d'autre.

### La PEP 8
On sait tous à quoi sert la [PEP 8](https://peps.python.org/pep-0008/), c'est un assemblage de règles qui permet d'écrire du Python plus élégament, même si certaines règles sont contestables comme les [lignes de 79 caractères maximum](https://peps.python.org/pep-0008/#maximum-line-length).

Il faudrait essayer d'y adhérer le plus possible.

### Autres recomandations
Cette section est pour des suggestions autres.

Si vous parlez assez bien anglais, allez voir [CodeAesthetics](https://www.youtube.com/@codeaesthetic), il fait des vidéos de quelques minutes sur comment organiser le code.

## 1. Les annotations
### Pourquoi utiliser les annotations ?
Python est ce qu'on appelle un langage [typé dynamiquement](https://fr.wikipedia.org/wiki/Typage_dynamique), c'est-à-dire que le type des variables est deviné par l'interpréteur (la chose qui éxécute le code) Python au moment où une valeur y est assigné; des fois, ça peut être utile mais la plupart du temps c'est plus énervant qu'autre chose.

Prenons cette signature de fonction:
```Python
def calcul_duree(date_debut, date_fin):
```

On n'a aucune idée de quoi passer en argument: des string sous forme `"dd/mm"`? des ints pour des dates [EPOCH](https://fr.wikipedia.org/wiki/Epoch)? des listes/tuples contenant des ints? et les dates doivent-elles inclure une année? On en a aucune idée sans documentation.

Heureusement, il existe des langages [statiquement typés](https://developer.mozilla.org/fr/docs/Glossary/Static_typing) dans lesquels on connait les types, par exemple en C++:
```C++
unsigned int calcul_duree(unsigned int[3] dateDebut, unsigned int[3] dateFin) {
```

On sait directement que la fonction accepte des tableaux (grossièrement la même chose que les listes de Python) contenant 3 entiers positifs chacuns et retourne un entier positif.  
On peut mimer ce comportement en Python, avec ce qu'on appelle _les annotations_:
```Python
def calcul_duree(date_debut : list[int, int, int], date_fin : list[int, int, int]) -> int:
```

Attention, j'ai bien écrit "mimer", en effet là où C++ vous lancera une erreur au visage, Python n'en a rien à faire: **les annotations sont ignorées lors de l'éxécution du programme**.

Exemple:
```Python
def ma_fonction(param : int) -> None:
	...

ma_fonction("Pas un nombre entier du tout")	# OK pour Python
```

Pour éviter les comportements innatendus, on peut utiliser `assert` et l'opérateur `is`.
```Python
def ma_fonction(param : int) -> None:
	assert(type(param) is int)

ma_fonction("Pas un nombre entier du tout")		# AssertionError
```
J'en profite pour rappeler que `==` compare les valeurs (`5 == 5`) et que `is` compare les locations des variables. Quand on teste pour un type ou `None`, il faut utiliser `is` (bien que dans l'écrasante majorité des cas les deux sont équivalents); si vous voulez connaitre la raison voici [une explication (relativement) longue](https://jaredgrubb.blogspot.com/2009/04/python-is-none-vs-none.html) et [une autre plus courte](https://stackoverflow.com/questions/3257919/what-is-the-difference-between-is-none-and-none).

Même si dans la [PEP 484](https://peps.python.org/pep-0484/#non-goals) les auteurs indiquent en gras qu'ils _"ne désirent pas rendre les annotations obligatoire, même par convention"_. Bien que dans les trois PEPs sur les annotations, ils ne précisent jamais pourquoi c'est le cas; je pense que c'est pour respecter la règle _"simple est meilleur que complexe"_ (si c'est le cas ça contredit "Explicite est meilleur qu'implicite").  
Dans tous les cas, mon point de vue est celui du [standard C++](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#reason-16): _"Types are the simplest and best documentation"_ (Les types sont la meilleur documentation).

### La syntaxe
La syntaxe est assez simple, il y a 3 règle:
+ Pour annoter une variable, on utilise les deux points `:`.
+ Pour indiquer le type de retour d'une fonction, on utilise la flèche `->` avant les deux points commençant la fonction.
+ Si jamais il peut y avoir plusieurs types, on les sépare par l'opérateur de disjonction `|`.

Exemples:
```Python
variable_sans_valeur : bool	# On déclare le variable sans lui donner de valeur (annotation obligatoire dans ce cas là)
string_var : str = "string"

def fonction_basique() -> None:	# Si une fonction ne retourne rien, elle retourne None
	...	# alternative à pass

def conversion_en_string(nombre : float) -> str:
	"""Convertit `nombre` en string"""
	return str(nombre)

def parametre_par_defaut(p1 : None, p2 : int = 69) -> None:
		...


multi_var : int | None = None	# une int ou None
multi_var = 5		# Pas d'annotation

def ou_alors(p1 : int | float) -> str | None:
	...
```

Certaines annotations (comme `list`) peuvent prendre des types en paramètre, pour cela il faut ajouter des crochets `[]` avec un ou des types à l'intérieur.
```Python
ma_simple_liste : list # une liste avec un nombre indéterminé d'éléments de types inconnus

ma_liste : list[bool]		# une liste avec des booléens à l'intérieur
ma_liste : list[int | float]	# une liste avec des int et des float à l'intérieur
ma_tuple : tuple[()]		# une tuple vide
ma_tuple : tuple[float, str]	# une tuple avec exactement une float et une string à l'intérieur
ma_tuple : tuple[float, ...]	# une liste avec des float à l'intérieur
mon_dictionnaire : dict[str, int]	# une dictionnaire avec des strings pour clefs et des entiers pour valeur
```

La [PEP 484](https://peps.python.org/pep-0484/#designing-for-inheritance) introduit d'autre syntaxes comme [les _types comments_](https://peps.python.org/pep-0484/#type-comments) (commentaires de type) et les [strings en guise d'annotation de type](https://peps.python.org/pep-0484/#forward-references), mais les deux ont un usage occasionnel. Sachez que ces méthodes existent.
```Python
# Les string en annotation
# Le type doit être dans une string litérale, sutout utilisé en POO
facebook : 'str' = "méta string"

meta_str : str = 'str'
une_string : meta_str = ''	 # invalide => le type de la variable est inconnu
```

```Python
# Le type est dans un commentaire
# C'est surtout utilisé dans des cas plus complexe, comme des unpack de conteneurs ou des boucles for
# Allez voir la PEP 484 pour plus d'exemple d'utilisation
les_coms = 23	# type: int

# Empèche le vérificateur de type de lancer une erreur
mauvais_type1 : float = False	# type: ignore

mauvais_type2 : int = True # type: ignore # Commentaire après le commentaire de type
bon_type = 1 # type: int # Commentaire après le commentaire de type
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

Il n'y a presque aucune autre annotation de type en _vanilla_ Python, mais il existe la librarie `typing` qui définie plein d'autre types.


Comme vous le savez peut-être les fonctions peuvent être stockées dans des variables, si on importe `Callable` de `collections.abc`, il est possible de d'annoter des fonctions:
```Python
from  collections.abc import Callable
def fun_to_be_a_function(param : str) -> bool:
	...

def fonction_seconde(p1 : bool, p2 : int, p3 : float) -> None:
	...

def fonction_troisieme(p1 : bool, p2 : bool) -> None:
	...

function : Callable[[str], bool] = fun_to_be_a_function		# pas de parenthèse car on n'appelle pas la fonction, on veut l'objet en lui-même

no_fun : Callable[[bool, int, float], None] = fonction_seconde

multi_fun : Callable[..., None] = fonction_seconde	# Peut importe les arguments
multi_fun = fonction_troiseme
```

___
Le module `typing` donne aussi accès aux annotations `Any` et `NoReturn` qui ne représentent pas de type en particuler.  
`Any` représente une union de tous les types qui existent, il ne faut **pas** l'utiliser si le type d'une variable n'est pas connu (on ne met pas d'annotation dans ce cas), il faut l'utiliser seulement quand une variable peut être (et probablement sera) de n'importe quel type.  
`NoReturn` ne s'utilise qu'en type de retour d'une fonction et indique que soit la fonction lancera une erreur, soit la fonction fermera le programme mais ne doit **jamais** atteindre de `return` explicite ou implicite.  
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

from sys import exit
def ne_retourne_pas(lancer : bool) -> NoReturn:
	if lancer:
		raise Exception("Je suis une erreur")	# Quitte la fonction par une erreur
	
	exit(1)		# Quitte la fonction en fermant le programme
	# retour implicite jamais atteint

def OK_mais_moyen() -> NoReturn:
	if False:
		return	# retourne None mais n'est jamais atteint donc c'est bon
	exit()		# Même si une vraie fonction ne devrait pas faire ça
```

### Créer de nouvelles annotations
Les types créés par l'utilisateur (nous) ont leurs annotations:
```Python
class LaClasse:
	...
classieux : LaClasse
```
<sub>v. [la section sur la POO](#2-la-programation-orientée-objet) pour les classes.</sub>

On peut aussi créer des alias de type	 avec le mot-clef `type`, si l'on a importé `TypeAlias` de `typing`:
```Python
from typing import TypeAlias

# Pour Python 3.12
type entier = int
type charactere = str
type string = list[charactere, ...]

# Pour les anciens
meilleure_int : TypeAlias = tuple[int]	# avec annotation
meilleure_str = tuple[str]		# sans annotation

parler_francais		: entier = 9876
en_python		: string = ['h', 'e', 'y']
c_est_possible		: meilleure_int = (56,)
pour_les_francophones	: meilleure_str = ("Oi!",)
```


Pour plus de possiblilités allez voir la [documentation de `typing`](https://docs.python.org/3/library/typing.html).  
Si jamais, vous voulez des définitions plus formelles allez voir la [PEP 484](https://peps.python.org/pep-0484/).


## 2. La programation orientée objet
La programmation orientée objet (POO ou OOP en anglais) est l'un des styles majeurs de _design_ de code avec l'impératif et le fonctionnel. Grossièrement ce style repose sur la définition de plans (les _classes_) pour construire des _objets_ qui représentent une composante du programme.  
L'avantage de la POO c'est qu'lle nous permet de penser à notre programme comme des objets, plus ou moins tangibles; contrairement aux autres styles qui sont un emboitement d'instructions.

### Le fil rouge
Disons que nous sommes dans une usines de chaises et qu'il faut coder les machines pour fabriquer des chaises. Pour cela, il nous faut définir les caractéristiques que chaque chaise a, il nous faut donc:
- le nombre de pieds
- si la chaise à des roulettes
- les dimensions de la chaise


### Les constructeurs
Il nous faut définir une _classe_ "chaise" qui définira ce qu'auront chaque chaises puis, à partir de cette classe nous allons construire des _objets_ qui représenterons des chaises à fabriquer avec les machines.  
Dans la classe, il doit y avoir une fonction qui "construit" les objets, on l'appelle le _constructeur_ et en Python ce sera toujours la fonction `__init__()`.  

L'exemple ci-dessous, définit le constructeur de la class `Chaise` puis l'appelle pour créer une objet `Chaise`.  
```Python
class Chaise:
	# On définit le constructeur de Chaise
	def __init__(self, nb_pied : int, a_roulettes : bool, dimensions : tuple[float, float, float]):
		self.nb_pied	 : int = nb_pied
		self.a_des_roues : int = a_roulettes
		self.dim		 : tuple[float, float, float] = dimensions

ma_chaise : Chaise = Chaise(4, False, (.5, .5, 1))
```

A partir de la ligne 5, on définit des variables comme `self.nb_pied`, ce sont des variables qui appartiennent à l'objet. Notez que la fonction `__init__()` est **la seule** fonction à pouvoir déclarer des variables qui appartiennent à `self`.  
A la dernière ligne, `self` est **ignoré** lors de l'appel du constructeur. C'est parce qu'il représente l'objet que l'on est en train de construire et est automatiquement assigné. C'est aussi pour cela que les variables que l'on déclare appartiennent à `self`, c'est des variables inhérentes à l'objet.

A la dernière ligne, la variable `ma_chaise` est définie, elle est de type `Chaise` car on lui assigne le résulat du constructeur constructeur qui est, pour l'instant, le seul moyen d'obtenir une chaise.  
En regardant les arguments du constructeur, on conclue les égalités suivantes.
```Python
ma_chaise.nb_pied		== 4
ma_chaise.a_des_roues		== False
ma_chaise.dim			== (.5, .5, 1)
```

Pour résumer, les constructeurs sont les moyens principaux de créer des objets, définissent les variables des instances et peuvent être appelés avec le nom de la classe qu'ils contruisent.
### Parenthèse vocabulaire
Petit point lexique:  
Les variables appartenants aux objets sont appelés _variables membre_ ou alors _attributs_. Dans les sphères anglophones, on peut aussi trouver _properties_ mais en francçais, c'est rare.  
Les fonctions définies dans une classe sont des _fonctions membre_ ou _méthodes_.  
Si l'on ne précise pas la nature d'un _membre_, l'on parle à la fois d'un attribut et d'une méthode.

Une _instance_ (de la classe X) est juste un objet (de la classe X).

### Créer des méthodes
Créer une méthode, c'est comme créer une fonction normale mais on indente pour qu'elle appartienne à la classe. Toute méthode prend comme premier paramètre `self`, qui représente l'objet qui fait l'appel de la méthode. Pour les utiliser, c'est comme les méthodes des listes (`.append()`, `.pop()`, ...).

Dans notre scénario, nous pourrions avoir des méthodes qui gère la fabrication de la chaise:
```Python
class Chaise:
	# On définit le constructeur de Chaise
	def __init__(self, nb_pied : int, a_roulettes : bool, dimensions : tuple[float, float, float]):
		self.nb_pied	 : int	= nb_pied
		self.a_des_roues : int	= a_roulettes
		self.dim : tuple[float, float, float] = dimensions
	
	def placer_pieds(self) -> None:
		demander_pieds(self.nb_pieds)	# demande le bon nombre de pieds
		...	# fait autre chose
	
	def placer_dossier(self) -> None:
		pass
	
	def placer_assise(self) -> None:
		pass

	def fabriquer(self, combien : int) -> None:
		for _ in range(combien):	# fait `combien` itérations (aucune variable)
			self.placer_pieds()
			self.placer_assise()
			self.placer_dossier()
			...

ma_chaise : Chaise = Chaise(4, False, (.5, .5, 1))
ma_chaise.fabriquer(5)		# Fabrique 5 chaises avec les propriétés de ma_chaise
```

Certaines méthodes ont des noms qui commencent et terminent par deux underscores `__`, ce sont les _méthodes magiques_, il y en a pas mal mais elles ne sont pas utiles pour ce projet, du coup je ne les détaillerais pas mais vous pouvez allez les voir vous même dans [la documentation](https://docs.python.org/3.13/reference/datamodel.html#special-method-names) (il y en a d'autre suivant les modules installés).

### L'encapsulation
#### Le cas général
L'encapsulation est un concept similaire à celui de la [boite noire](https://fr.wikipedia.org/wiki/Bo%C3%AEte_noire_(syst%C3%A8me)). Le principe est de considérer un objet comme une capsule opaque, creuse et avec des boutons dessus; à l'intérieur il y a des données (attributs) qui sont innacessibles à l'utilisateur de la classe qui ne peut qu'appuyer sur les boutons à la surface en appelant des méthodes.  
En somme, la seule façon de modifier et lire les attributs d'un objet doit être par ses méthodes. Malheureusement, en Python, il n'existe pas de moyen de s'assurer que ce soit respecté mais il y a des conventions pour montrer que faire aux développeurs, nous les verrons plus tard.

Je me souviens que quand j'ai vu ce concept pour la première fois, je n'y croyais pas beaucoup non plus alors pourquoi devrait-on respecter l'encapsulation en premier lieu? La réponse que j'ai reçu, c'est qu'il ne faut pas submerger l'utilisateur de la classe de choix avec trop de façon de faire la même chose (notion qui est inscrit dans le [ZEN](#le-zen-de-python) de Python); cependant je ne suis pas convaincu par cette explication, surtout en Python où les variables ne sont pas protégées; ma réponse est qu'avec cette approche, on peut forcer l'utilisateur à utiliser la classe d'une certaine façon.  
Par exemple, il est possible pour la fabrication de chaises de ne vouloir, que de l'extérieur, on ne puisse savoir seulement le type de chaise construite sans de caractéristiques précises.

Avec ce design on ne peut pas directement lire une variable, il faut définir des méthodes conçues uniquement pour récupérer la valeur d'un attribut, on les appelle les fonctions _getters_. De même pour une fonction conçue uniquement pour changer la valeur d'un attribut s'appelle une fonction _setter_.

Il ne nous manque plus qu'un élément crucial pour pouvoir mettre en place l'encapsulation: un moyen de dire à l'utilisateur de ne pas accéder à un membre d'une classe ou d'un objet.  
Dans un langage de programation orienté objet standard, on trouve deux types de membres: les membres _privés_ et les membres _publics_; les premiers ne peuvent être accédés seulement par une méthode membre de la même classe, les seconds peuvent être accédés depuis n'importe où.  
Comme je l'ai écrit plus haut, il est impossible en Python de s'assurer qu'un membre soit privé, il existe cependant une convention installée par la [PEP 8](https://peps.python.org/pep-0008/#method-names-and-instance-variables): les attributs non publics commencent par un seul underscore `_`. Comme Python n'a pas d'attribut privés à proprement parler, la [PEP 8](https://peps.python.org/pep-0008/#designing-for-inheritance) indique qu'il ne faudrait pas parler d'attribut "privés" mais "non publics".

Voici une version de `Chaise` respectant l'encapsulation:
```Python
class Chaise:
	# On définit le constructeur de Chaise
	def __init__(self, nb_pied : int, a_roulettes : bool, dimensions : tuple[float, float, float]):
		# Tous les membres sont privés
		self._nb_pied : int = nb_pied
		self._a_des_roues : int = a_roulettes
		self._dim : tuple[float, float, float] = dimensions

	# getter pour _nb_pied
	def get_nb_pied(self) -> int:
		return self._nb_pied
	
	# Un getter n'est pas obligé de retourner un attribut existant
	def get_nb_roulettes(self) -> int:
		return self._nb_pied if self._a_des_roues else 0
	
	# Il devrait y avoir le moins de getters possibles

	# setter pour _dim
	# on aurait pu l'appeler autrement mais
	# la convention veut indiquer les setters par le préfixe `set_`
	def set_nb_pied(self, nouvelle_valeur : tuple[float, float, float]) -> int:
		self._dim = nouvelle_valeur
	
	# Pas de setter pour les autres attributs

	# Les méthodes non publiques existent aussis
	def _est_chaise_gamer(self) -> bool:
		pass

	def est_comfortable(self, reponse_honnete : bool = False) -> bool:
		return True		# Toutes les chaises fabriquées sont comfortables

ma_chaise : Chaise = Chaise(4, False, (.5, .5, 1))
print(ma_chaise.est_comfortable())		# pas d'erreur et autorisé
print(ma_chaise._est_chaise_gamer())	# pas d'erreur mais va à l'encontre des développeurs de la classe
```

#### Le cas de Python
Dans un langage classique, nous nous serions arrêté ici mais nous codons en Python et, Python n'aime pas le concept de getter et de setter. Ce langage à une propriété <!--pun not intended--> que d'autre n'ont pas: créer des attributs virtuels.  
Ce que j'appelle "attribut virtuel" (pas du tout un terme officiel), c'est des méthodes qui sont accédées comme des attributs. On les déclare avec le décorateur `@property`.

exemple:
```Python
class Chaise:
	def __init__(self, nb_pied : int, a_roulettes : bool, dimensions : tuple[float, float, float]):
		self._nb_pied : int = nb_pied
		self._a_des_roues : int = a_roulettes
		self._dim : tuple[float, float, float] = dimensions
	
	def set_a_des_roulettes(self, val : bool) -> None:
		self._a_des_roues = val

	@property
	def nb_roulettes(self) -> int:
		if self._a_des_roues:
			return self._nb_pied
		return 0

ma_chaise : Chaise = Chaise(4, False, (.5, .5, 1))
print(ma_chaise.nb_roulettes)		#-> 0

ma_chaise.set_a_des_roulettes(True)
print(ma_chaise.nb_roulettes)		#-> 4
```

Ces propriétés servent de getter, pour les setters on utilise un décorateur différent: `@nom_proprietee.setter`, toujours une fonction.
```Python
class Chaise:
	def __init__(self, nb_pied : int, a_roulettes : bool, dimensions : tuple[float, float, float]):
		self._nb_pied : int = nb_pied
		self._a_des_roues : int = a_roulettes
		self._dim : tuple[float, float, float] = dimensions
	
	@property		# Obligatoire pour définir le setter
	def nb_roulettes(self) -> int:
		if self._a_des_roues:
			return self._nb_pied
		return 0
	
	@nb_roulettes.setter
	def nb_roulettes(self, valeur) -> None:
		self._a_des_roues = True
		self._nb_pied = valeur


ma_chaise : Chaise = Chaise(4, False, (.5, .5, 1))
print(ma_chaise.nb_roulettes)		#-> 0

ma_chaise.nb_roulettes = 4
print(ma_chaise.nb_roulettes)		#-> 4
```
___

Si quelque chose est confus, voici [le post StackOverflow](https://stackoverflow.com/questions/2627002/whats-the-pythonic-way-to-use-getters-and-setters#upvote-btn-36943813) que j'ai suivi ainsi que la [documentation](https://docs.python.org/3/library/functions.html#property).

### Les membres statiques
Un membre statique est un membre qui appartient à la classe et non à une instance de la classe. Les attributs statiques représentent une valeur lié à ce que représente la classe; les méthodes statiques sont en général, soit des actions souvent utilisées par la classe mais impropre aux objets individuels soit une action sur les attributs statiques.  
Les attributs statiques doivent au maximum respecter l'encapsulation, bien que l'on soit moins strict dessus que pour les attributs non statiques.

Pour créer un attribut statique, il faut le déclarer dans la classe. Quant aux méthodes statiques, ont utilise le décorateur `@staticmethod` (on peut aussi utiliser [`@classmethod`](https://docs.python.org/3/library/functions.html#classmethod) qui fait la même chose pour plus de caractères).  
Pour accéder à un membre statique, on fait comme pour les membres classiques mais on met le nom de la classe à la place d'une variable.

```Python
class Chaise:
	nom_usine : str = "NSI factory"	# nom_usine est statique
	_emplacement_usine: tuple[float, float] = (48.639101, 1.821532)

	def __init__(self, nb_pied : int, a_roulettes : bool, dimensions : tuple[float, float, float]):
		self._nb_pied : int = nb_pied
		self._a_des_roues : int = a_roulettes
		self._dim : tuple[float, float, float] = dimensions
	
	@staticmethod
	def fabriquer_fauteuils(combien : int) -> None:	# pas de `self` car il n'y a pas d'objet
		pass
	
	@classmethod
	def fabriquer_fauteuil(cls) -> None:	# `cls` remplace `self` et désigne la classe (ici `	`)
		cls.fabriquer_fauteuils(1)

print(Chaise.nom_usine)		#-> NSI factory
Chaise.fabriquer_fauteuils(5)
```

Toutes les méthodes non-statiques peuvent accéder aux méthodes statiques mais l'inverse n'est pas possible.

```Python
class Chaise:
	# ...
	
	def fabriquer_fauteuil(self) -> None:
		Chaise.fabriquer_fauteuils(1)
	
	@staticmethod
	def erreur() -> None:
		self.fabriquer_fauteuil()	# self n'est pas défini
```

<!-- Je ne pense pas que se soit utile maintenant
### La déscendance (inheritance)
### Préférez la composition à la déscendance
-->

### Détails sur les objets
#### Passage par référence
A l'instar des tuples et des listes, les objets sont passés par références. Celà veut dire que les objets ne sont pas copiés quand passés d'une variable à une autre.  
Pour régler le problème, il faut créer une méthode `__copy__()` ou `__deepcopy__()` qui puis appeler `copy()` ou `deepcopy()` du module `copy`. Pour d'autres questions allez voir [cette réponse stackOverflow](https://stackoverflow.com/questions/4794244/how-can-i-create-a-copy-of-an-object-in-python#answer-46939443).

Exemple:
```Python
class ClasseSansCopie:
	def __init__(self, attr1, attr2):
		self.un = attr1
		self.deux = attr2

objet = ClasseSansCopie(3, [4])
autre_objet = objet

objet.un = 10
print(autre_objet.un)	#-> 10


from copy import copy, deepcopy
class ClasseAvecCopie:
	def __init__(self, attr1, attr2):
		self.un = attr1
		self.deux = attr2
	
	def __copy__(self):
		return ClasseAvecCopie(self.un, self.deux)
	
	def __deepcopy__(self, memo):
		# memo est un dictionnaire id -> None?
		# pour être honnête même avec test je ne comprend pas
		# son fonctionnement
		if memo.get(id(copy)) is not None:	# je recopie stackOverflow
			return None
		
		return ClasseAvecCopie(
			deepcopy(self.un),
			deepcopy(self.deux),
		)


objet = ClasseSansCopie(3, [4])
autre_objet = copy(objet)

objet.un = 10
objet.deux.append(5)
print(autre_objet.un)	#-> 3
print(autre_objet.deux)	#-> [4, 5], copy() n'a pas copié la liste

objet = ClasseSansCopie(3, [4])
autre_objet = deepcopy(objet)

objet.un = 10
objet.deux.append(5)
print(autre_objet.un)	#-> 3
print(autre_objet.deux)	#-> [4]
```

## 3. Les énumérations
Une énumération est un type qui ne peut prendre que certaines valeurs. Par exemple, pour une application météo il ne peut faire que: soleil, pluie, nuages.

Pour créer une énumération, il faut créer une classe qui hérite (prend toutes les méthodes et attributs) de `Enum` du module `enum`, on peut ensuite créer des variables globales qui seront les cas de l'énumération.  
Pour ma météo:
```Python
from enum import Enum
class Meteo(Enum):
	SOLEIL = "ensoleillé"
	NUAGES = "nuageux"
	PLUIE = "pluvieux"
```

On peut ensuite les comparer avec des variables:
```Python
from enum import Enum
class Meteo(Enum):
	SOLEIL = "ensoleillé"
	NUAGES = "nuageux"
	PLUIE = "pluvieux"

temps_hier : METEO = METEO.SOLEIL
temps_aujourdhui : METEO = METEO.PLUIE

if temps_hier == temps_aujourdhui:
	print(f"Il à fait {temps_hier.name} hier et aujourd'hui.")
else:
	print(f"Il à fait {temps_hier.name} hier alors qu'aujourd'hui il a fait {temps_aujourdhui.name}.")
```

On peut aussi utiliser la fonction `auto()` du même module pour ne pas se préoccupper des valeurs de chaque cas.

Il existe deux sous classes de `Enum` définie dans le même module: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum) et [`IntEnum`](https://docs.python.org/3/library/enum.html#enum.IntEnum) qui ne peuvent contenir que des membres de types `str` et `int`.

## 4. Autres concepts non spécifiques à Python
### Les bitmasks
Un bitmask c'est comme une liste de booléens qui décrivent chacuns des états indépendants les uns des autres, par exemple les livres peuvent à la fois être grands et contenir la couleur jaune mais le livre peut aussi être petit et quand même contenir la couleur jaune.  
En Python on traduis cette situation avec un type dérivé de `Flag`:
```Python
from enum import Flag, auto

class EtatsLivre(Flag):
	GRAND = auto()
	JAUNE = auto()

un_livre = EtatLivre.GRAND			# Le livre est grand mais pas jaune
un_autre_livre = EtatLivre.JAUNE	# l'opposé
# on peut se représenter ces variables comme:
# un_livre = [True, False]
# un_autre_livre = [False, True]

# Attention: même si c'est comme une liste de booléens,
# on ne peut pas accéder aux éléments avec les crochets []
```

Quand on manipule un bitmask, on le fait avec des opérateurs dits _["bitwise"](https://fr.wikipedia.org/wiki/Op%C3%A9ration_bit_%C3%A0_bit)_:

- `|` (OR/OU): Associe les booléens de manière à ce que tous les `True` présents dans les deux bitmasks soient présents dans le résultat.
- `&` (AND/ET): Associe les booléens de manière à ce qu'il ne reste que les `True` présents dans les deux opérandes à la fois.
- `~` (NOT/NON): Inverse tous les booléens du bitmask.
- `^` (XOR): Teste si chaque booléen est différent de celui de l'autre opérande.

ex:
```Python
from enum import Flag, auto

class EtatLivre(Flag):
	GRAND = auto()
	JAUNE = auto()

un_livre = EtatLivre.GRAND
un_autre_livre = EtatLivre.JAUNE
# un_livre = [True, False]
# un_autre_livre = [False, True]

grand_et_jaune = EtatLivre.GRAND | EtatLivre.JAUNE
# grand_et_jaune = [True or False, False or True] -> [True, True]

seulement_grand = grand_et_jaune & EtatLivre.GRAND
# seulement_grand = [True and True, True and False] -> [True, False]

rien_du_tout = ~grand_et_jaune
# rien_du_tout = [not True, not True] -> [False, False]

soit_grand_soit_jaune = EtatLivre.JAUNE ^ seulement_grand
# soit_grand_soit_jaune = [False != True, False != False] -> [True, False]
```

Dans la pratique, on utilise l'opérateur `|` pour ajouter des bitmasks ensemble, l'opérateur `&` pour filtrer des valeurs.  
Voici la syntaxe pour vérifier si un masque en contient un autre vérification:
```Python
# ...

masque = EtatLivre.GRAND
if masque & EtatLivre.GRAND:	# on isole la valeur EtatLivre.GRAND
	print("masque contient GRAND")

if masque & EtatLivre.JAUNE:
	print("masque contient JAUNE")	# n'est pas affiché

# masque & EtatLivre.GRAND = [True and True, False and False] -> [True, False]
# masque & EtatLivre.JAUNE = [True and False, False and True] -> [False, False]
```

Et cette méthode marche même avec plusieurs valeurs
```Python
grand_et_jaune = EtatLivre.GRAND | EtatLivre.JAUNE
masque = EtatLivre.GRAND

if grand_et_jaune & masque :
	print("grand_et_jaune contient masque")

# grand_et_jaune & masque = [True, False]
```

Seulement vu que l'on est en Python, il est possible d'utiliser le mot-clef `in` qui à l'avantage de ne pas être commutatif.
```Python
grand_et_jaune = EtatLivre.GRAND | EtatLivre.JAUNE
masque = EtatLivre.GRAND

if grand_et_jaune in masque:		# Faux
	print("masque contient grand_et_jaune")

if masque in grand_et_jaune:		# Vrai
	print("grand_et_jaune contient masque")
```

La documentation de [`Flag`](https://docs.python.org/3/library/enum.html#enum.Flag)
_____

Pour notre petit projet, il n'est pas très utile d'en connaitre plus mais savoir comment les choses fonctionnent est toujours interressant.  
Si on cherche à revenir aux bases du concept, un bitmask n'est rien d'autres qu'un cas particulier d'`int` <!--On pourrait répondre que tous les autres types auusi mais c'est hors sujet-->. Alors pourquoi et comment, le "pourquoi" est simple: dans les premières versions de C (et dans les autres languages de l'époques) il n'y avait qu'un seul type: les `int` et le "type" était déterminé par la façon dont les valeurs étaient utilisées; et c'est resté de cette façon dans la majorité des languages modernes car il n'existe pas de raisons de changer.  
Le "comment" est aussi simple une fois intégré. Vous savez que les ordinateurs représentent les nombres en binaires avec chaque chiffre représenté par un bit, les bitmasks vont juste associer arbitrairement chaque bit avec une signification.

Voici une représentation plus rudimentaire de la classe d'avant:
```Python
ETAT_LIVRE_GRAND = 0b1		# binaire
ETAT_LIVRE_JAUNE = 0b10
# Si on peut ajouter d'autres états:
# ETAT_LIVRE_DECHIRE = 0b100
# ETAT_LIVRE_EN_FEU =  0b1000
# ...
```

Les opérations _bitwise_ prennent plus de sens vu que c'est juste les portes logiques appliquées à chaque bit:
```Python
0b01 | 0b10 == 0b11
0b11 & 0b00 == 0b00
0b11 ^ 0b01 == 0b10
~0b10       == 0b01
```

La [version plus rigoureuse](https://fr.wikipedia.org/wiki/Masquage) de mon explication.