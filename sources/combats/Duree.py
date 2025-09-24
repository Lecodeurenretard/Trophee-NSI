from imports import *

@total_ordering
class Duree:
    def __init__(self, *, ms : int = 0, s : float = 0):
        if ms != 0 and s != 0 and ms != s * 1000:
            raise ValueError(f"Les paramètres `ms` ({ms}) et `s` ({s}) se contredisent.")
        
        self._ms : int = 0
        if ms != 0:
            self._ms = ms
        elif s != 0:
            self._ms = round(s * 1000)
        self._check_si_negatif()
    
    def __eq__(self, val : 'Duree|int'):
        if type(val) is Duree:
            return self.millisecondes == val.millisecondes
        return self.millisecondes == val
    
    def __lt__(self, val : 'Duree|int'):
        if type(val) is Duree:
            return self.millisecondes < val.millisecondes
        if type(val) is int:
            return self.millisecondes < val
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
        return Duree(ms=self.millisecondes * val)
    def __floordiv__(self, val : int) -> 'Duree':
        return Duree(ms=self.millisecondes // val)
    # On ne défini pas truediv pour rester dans les ints
    
    def __repr__(self):
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
            logging.warning("Une durée ne peut être négative, changement en durée nulle.")
            self._ms = 0