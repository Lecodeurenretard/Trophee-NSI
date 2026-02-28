from imports import (
    overload, copy,
    Iterable,  Iterator,
    Sequence, MutableSequence,
    Any, sys
)


def iter_slice(s : slice[int, int, int]) -> Iterator[int]:
    """Renvoie un itérateur qui prend les valeurs de la slice."""
    for i in range(s.start, s.stop + 1, s.step):
        yield i

# Python va considérer ArrayStable comme une liste (pas précis du tout mais c'est dans l'esprit)
# Si vous voulez en savoir plus, allez voir l'hérédité et les génériques (on utilise la nouvelle syntaxe de ces génériques)
class ArrayStable[T](MutableSequence[T|None]):
    """
    Une liste mais les valeurs ne peuvent pas changer d'index (pas de décalage).
    Ce design impose qu'il existe des index n'ayant pas de valeur associée, La classe les considère comme `None`.
    
    Bien que la méthode `.insert()` ne soit pas implémentée, la classe est une MutableSequence.
    Voici la documentation: https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range
    """
    
    @overload
    def __init__(self, lst_ou_taille : int = 0): ...
    @overload
    def __init__(self, lst_ou_taille : Iterable[T]): ...
    
    def __init__(self, lst_ou_taille : int|Iterable[T] = 0) -> None:
        self._valeurs      : dict[int, T] = {}
        self._clef_maximum : int = -1   # vide
        
        if type(lst_ou_taille) is int:
            self.resize(lst_ou_taille)
            return
        
        assert(isinstance(lst_ou_taille, Iterable)), f"lst_ou_taille n'est ni un entier, ni un Iterable.."
        for i, val in enumerate(lst_ou_taille):
            self._valeurs[i] = val
            
            if i > self._clef_maximum:
                self._clef_maximum = i
    
    def __delitem__(self, index : int|slice):
        if type(index) is int:
            self.pop(index)
            return
        
        assert(type(index) is slice)    # pywright strikes again
        for i in iter_slice(index):
            del self[i]
    
    def __format__(self, format_spec: str):
        if self._clef_maximum == -1:
            return '[]'
        
        res : str = '['
        for clef, val in enumerate(self):
            if val is None:
                continue
            res += format(clef, format_spec) + ': ' + format(val, format_spec) + ', '
        
        return res[:-2] + ']'   # on enlève le ', ' final
    
    def __repr__(self):
        if self._clef_maximum == -1:
            return '[]'
        
        res : str = '['
        for i in range(self._clef_maximum + 1):
            if i in self._valeurs.keys():
                res += repr(self._valeurs[i])
            else:
                res += '_'
            res += ', '
        
        return res[:-2] + ']'   # on enlève le ', ' final
    
    @overload
    def __getitem__(self, key : int) -> T|None: ...
    @overload
    def __getitem__(self, key : slice) -> list[T|None]: ...
    
    def __getitem__(self, key : int|slice) -> T|None|list[T|None]:
        if type(key) is slice:
            if not (0 <= key.start <= key.stop or key.stop <= key.start <= 0):
                raise ValueError(f"La slice {key} entrainerait une boucle infine.")
            
            return [self[i] for i in iter_slice(key)]
        
        key = self._solve_key(key)
        
        if key not in self._valeurs.keys():
            return None
        return self._valeurs[key]
    
    @overload
    def __setitem__(self, index: int, value: T|None) -> None: ...
    @overload
    def __setitem__(self, index: slice, value: Iterable[T|None]) -> None: ...
    
    def __setitem__(self, index : int|slice, value : T|None|Iterable[T|None]) -> None:
        if type(index) is int and not isinstance(value, Iterable):
            # on assume que le type soit bon vu que l'on a 
            self._valeurs[self._solve_key(index)] = value   # type: ignore
            return
        
        if type(index) is slice and isinstance(value, Iterable):
            for i, elem in zip(iter_slice(index), value):
                self[i] = elem
            return
        
        raise TypeError(
            "Soit l'index doit être une slice et la valeur passée un itérable, "
            "soit l'index passé doit être une int et la valeur passée un élément de type T."
        )
    
    def __len__(self):
        return self._clef_maximum + 1
    
    def __iter__(self):
        for i in range(self._clef_maximum + 1):
            yield self[i]
    
    def __contains__(self, item : object):
        if type(item) is not T:
            return False
        return item in self._valeurs.values()
    
    def __add__(self, other : 'ArrayStable[T]|Sequence[T]'):
        res = copy(self)
        for val in other:
            res.append(val)
        return res
    
    def __mul__(self, other : int):
        if type(other) is not int:
            raise TypeError("On ne peut multiplier un array par autre chose qu'un entier.")
        
        res = ArrayStable(len(self) * other)
        for i, val in enumerate(res):
            for n in range(1, other+1):       # itère de cette manière (pour les index)
                res[i + len(self) * n] = val  # [[0, 3, 6],  [1, 4, 7],  [2, 5, 8]]
        return res
    
    def _solve_key(self, key : int) -> int:
        """Renvoie l'index "canonique" qui sera utilisé par les fonctions (ex: -1 devient le dernier élément de la liste)."""
        if type(key) is not int:
            raise TypeError("Le type d'une clef d'un array doit être une int.")
        
        if abs(key) > self._clef_maximum:
            raise IndexError(f"Accès à l'élément d'indice {key} alors que l'array est de longueur {len(self)}.")
        if key < 0:     # les clefs négatives fonctionnent comme dans les listes
            return len(self) + key
        return key
    
    def append(self, value : T|None) -> None:
        """Ajoute un élément à la fin de la liste."""
        self._clef_maximum += 1
        if value is not None:
            self._valeurs[self._clef_maximum] = value
    
    def pop(self, index : int = -1) -> T|None:
        """Enlève l'élément à l'indice `index` et renvoie sa valeur."""
        index = self._solve_key(index)
        if not (0 <= index < len(self)):
            raise IndexError(f"L'indice {index} n'est pas dans l'array.")
        if index not in self._valeurs.keys():
            return None     # on pop un None
        
        enleve = self._valeurs[index]
        del self._valeurs[index]
        return enleve
    
    def insert(self, index: int, value: T | None) -> None:
        raise TypeError(
            "La classe Array n'implémente pas la méthode .insert().\n"
            "Pour ajouter un élément à l'index i, utilisez .__setitem__()."
        )
    
    def resize(self, size : int) -> None:
        """Modifie la taille de la liste pour qu'elle soit de `taille`."""
        if size < 0:
            raise ValueError("La taille ne peut pas être négative.")
        if size == 0:
            self._clef_maximum = -1
            self._valeurs.clear()
            return
        
        if size < len(self):
            # Supprime toutes les clefs au dessus du nouveau max
            for i in self._valeurs.keys():
                if i >= size:
                    del self._valeurs[i]
        self._clef_maximum = size - 1
    
    def trim_end(self) -> None:
        """Enlève les cases vides à la fin."""
        for i, elem in enumerate(reversed(self)):
            if elem is not None:
                self.resize(i + 1)
                return
    
    def clear(self) -> None:
        """Vide l'array."""
        self._valeurs.clear()
        self._clef_maximum = -1
    
    def count(self, value : T|None) -> int:
        """
        Compte le nombre de fois que `value` apparait
        ou le nombre d'emplacemements vides si `value` est None.
        """
        return list(self).count(value)
    
    def index(self, value : Any, start : int = 0, stop : int = sys.maxsize) -> int:
        """
        Renvoie l'index du premier élément étant égal à `value` entre les index `start` et `stop` (inclus),
        élève une `ValueError` sinon.
        """
        return list(self).index(value, start, stop)
    
    def search(self, value : T|None, start : int = 0, end : int = sys.maxsize) -> int:
        """Alternative à .index() qui renvoie -1 quand l'élément n'est pas dans la liste au lieu de lancer une exception."""
        # on est civilisés
        try:
            return self.index(value, start=start, stop=end)
        except ValueError:
            return -1
    
    def no_holes(self) -> Iterator[tuple[int, T]]:
        """Renvoie un itérateur itérant parmis les index des valeurs non None."""
        for i, val in enumerate(self):
            if val is not None:
                yield (i, val)
    
    def index_exists(self, key : int) -> bool:
        """Vérifie que l'index soit correct dans les limites de l'array et que la valeur correspondante ne soit pas None."""
        try:
            return self[key] is not None
        except IndexError:
            return False
    
    def at(self, index : int, accept_negative : bool = True) -> T:
        true_index = index
        if true_index < 0 and accept_negative:
            true_index = len(self) + index
        else:
            raise ValueError("Index négatif passé alors que `accept_negative` est False.")
        
        if true_index not in self._valeurs.keys():
            raise IndexError(f"L'index {index} est soit un trou, soit en dehors de l'array.")
        
        return self._valeurs[true_index]
    
    # Par essence on ne peut pas définir .insert()