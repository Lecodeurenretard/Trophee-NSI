from imports import overload, copy, Iterable, Sequence, Iterator
import sys

class Array[T]:
    """
    Une liste mais les valeurs ne peuvent pas changer d'index (pas de décalage).
    Cela impose qu'il existe des index n'ayant pas de valeur,
    la classe se ce comporte comme s'ils contenaient `None`.
    La classe ne supporte pas les slices, tout opération les utilisant renverra `NotImplemented`.
    
    Sauf pour le slicing et la méthode `.insert()`, la classe est une MutableSequence.
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
        
        assert(isinstance(lst_ou_taille, Iterable)), "Mauvais paramètres."
        for i, val in enumerate(lst_ou_taille):
            self._valeurs[i] = val
            
            if i > self._clef_maximum:
                self._clef_maximum = i
    
    def __delitem__(self, key : int):
        self.pop(key)
    
    def __format__(self, format_spec: str):
        res : str = '['
        for clef, val in enumerate(self):
            if val is None:
                continue
            res += format(clef, format_spec) + ': ' + format(val, format_spec) + ', '
        
        return res[:-2] + ']'   # on enlève le ', ' final
    
    def __repr__(self):
        res : str = '['
        for i in range(self._clef_maximum + 1):
            if i in self._valeurs.keys():
                res += repr(self._valeurs[i])
            else:
                res += '_'
            res += ', '
        
        return res[:-2] + ']'   # on enlève le ', ' final
    
    def __getitem__(self, key : int) -> T|None:
        key = self._solve_key(key)
        
        if key not in self._valeurs.keys():
            return None
        return self._valeurs[key]

    def __setitem__(self, key : int, value : T):
        self._valeurs[self._solve_key(key)] = value
    
    def __len__(self):
        return self._clef_maximum + 1
    
    def __iter__(self):
        for i in range(self._clef_maximum + 1):
            yield self[i]
    
    def __contains__(self, item : T):
        if type(item) is not T:
            return False
        return item in self._valeurs.values()
    
    def __add__(self, other : 'Array[T]|Sequence[T]'):
        res = copy(self)
        for val in other:
            res.append(val)
        return res
    
    def __mul__(self, other : int):
        if type(other) is not int:
            raise TypeError("On ne peut multiplier un array par autre chose qu'un entier.")
        
        res = Array(len(self) * other)
        for i, val in enumerate(res):
            for n in range(1, other+1):       # itère de cette manière (pour les index)
                res[i + len(self) * n] = val  # [[0, 3, 6],  [1, 4, 7],  [2, 5, 8]]
        return res
    
    def _solve_key(self, key : int) -> int:
        """Renvoie l'index "canonique" qui sera utilisé par les fonctions (ex: -1 devient le dernier élément de la liste)."""
        if type(key) is slice:
            return NotImplemented
        if type(key) is not int:
            raise TypeError("Le type d'une clef d'un array doit être une int.")
        
        if abs(key) > self._clef_maximum:
            raise IndexError(f"Accès à l'élément d'indice {key} alors que l'array est de longueur {len(self)}.")
        if key < 0:     # les clefs négatives fonctionnent comme dans les listes
            return len(self) + key
        return key
    
    def append(self, val : T|None) -> None:
        """Ajoute un élément à la fin de la liste."""
        self._clef_maximum += 1
        if val is not None:
            self._valeurs[self._clef_maximum] = val
    
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
    
    def resize(self, size : int) -> None:
        """Modifie la taille de la liste pour qu'elle soit de `taille`."""
        if size < 0:
            raise ValueError("La taille ne peut pas être négative.")
        if size == 0:
            self._clef_maximum = 0
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
    
    def index(self, value : T|None, start : int = 0, end : int = sys.maxsize) -> int:
        """
        Renvoie l'index du premier élément étant égal à `value` entre les index `start` et `stop` (inclus),
        élève une `ValueError` sinon.
        """
        return list(self).index(value, start, end)
    
    def search(self, value : T|None, start : int = 0, end : int = sys.maxsize) -> int:
        """Alternative à .index() qui renvoie -1 quand l'élément n'est pas dans la liste au lieu de lancer une exception."""
        # on est civilisés
        try:
            return self.index(value, start=start, end=end)
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
            raise IndexError(f"Index {index} est     soit un trou, soit en dehors de l'array.")
        
        return self._valeurs[true_index]
    
    # Par essence on ne peut pas définir .insert()