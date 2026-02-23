from imports import total_ordering, overload, logging

@total_ordering
class Duree:
    @overload
    def __init__(self, *, ms : int): ...
    @overload
    def __init__(self, *, s : float): ...
    
    def __init__(self, *, ms : int = 0, s : float = 0):
        if (ms != 0 and s != 0) and ms != s * 1000:
            raise ValueError(f"Les paramètres {ms=} et {s=} se contredisent.")
        
        self._ms : int = 0
        if ms != 0:
            self._ms = ms
        elif s != 0:
            self._ms = round(s * 1000)
        self._check_si_negatif()
    
    def __eq__(self, val : object):  # on devrait mettre juste Duree
        if type(val) is Duree:       # mais il faut que l'opérateur accepte tous les objets
            return self.millisecondes == val.millisecondes
        raise TypeError(     # on pourrais renvoyer False mais on est pas en JS ici
            f"On ne compare les durées qu'avec d'autres durées pas avec des {type(val).__name__}."
        )
    
    def __lt__(self, val : 'Duree'):
        if type(val) is Duree:
            return self.millisecondes < val.millisecondes
        raise TypeError(
            f"On ne compare les durées qu'avec d'autres durées pas avec des {type(val).__name__}."
        )
    # gt, le, et ge sont générées automatiquement par total_ordering
    
    def __add__(self, val : 'Duree') -> 'Duree':
        if type(val) is Duree:
            return Duree(ms=self.millisecondes + val.millisecondes)
        raise TypeError(f"Le paramètre 'val' est de type '{type(val)}' alor que la fonction attend une Duree ou une int.")
    def __sub__(self, val : 'Duree') -> 'Duree':
        if type(val) is Duree:
            return Duree(ms=self.millisecondes - val.millisecondes)
        raise TypeError(f"Le paramètre 'val' est de type '{type(val)}' alor que la fonction attend une durée ou une int.")
    
    def __mul__(self, val : int) -> 'Duree':
        return Duree(s=self.secondes * val)
    
    @overload
    def __floordiv__(self, val : int) -> 'Duree': ...
    @overload
    def __floordiv__(self, val : 'Duree') -> int: ...   # secondes sur des secondes => pas d'unité
    
    def __floordiv__(self, val : 'int|Duree') -> 'Duree|int':
        if type(val) is int:
            return Duree(ms=self.millisecondes // val)
        if type(val) is Duree:
            return self.millisecondes // val.millisecondes
        raise TypeError("Mauvais type pour une division avec {self}.")
    
    def __truediv__(self, other : 'Duree') -> float:
        return self.millisecondes / other.millisecondes
    
    def __repr__(self):
        return f"Duree(ms={self._ms})"
    def __str__(self):
        return f"{self._ms}ms"
    
    @property
    def secondes(self) -> float:
        return self._ms / 1000
    
    @property
    def millisecondes(self) -> int:
        return self._ms
    
    @secondes.setter
    def secondes(self, val : float) -> None:
        self._ms = round(val * 1000)
        self._check_si_negatif()
    
    @millisecondes.setter
    def millisecondes(self, val : int) -> None:
        self._ms = val
        self._check_si_negatif()
    
    def _check_si_negatif(self) -> None:
        if self._ms < 0:
            logging.warning(f"Une durée ne peut être négative, changement en durée nulle (valeur précédente: {self._ms}ms).")
            self._ms = 0