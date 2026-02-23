from imports import dataclass, overload, Vecteur, TypeAlias

@dataclass
class Pos:
    x : int
    y : int
    
    @overload
    def __init__(self, x_ou_pos : int, y : int): ...
    @overload
    def __init__(self, x_ou_pos : tuple[int, int]|list[int]): ...
    @overload
    def __init__(self, x_ou_pos : Vecteur): ...
    
    def __init__(self, x_ou_pos : int|tuple[int, int]|list[int]|Vecteur, y : int = -1):
        # J'ai déja dit à quel point je n'aime pas ce système de surchargement des fonctions?
        self.x : int; self.y : int
        if type(x_ou_pos) is int:
            self.x = x_ou_pos; self.y = y
            return
        
        if type(x_ou_pos) is Vecteur:
            self.x = round(x_ou_pos.x); self.y = round(x_ou_pos.y)
            return
        
        if type(x_ou_pos) is not tuple and type(x_ou_pos) is not list:
            raise TypeError(f"Mauvais type ({type(x_ou_pos).__name__}) du premier paramètre du constructeur de Pos.")
        if len(x_ou_pos) != 2:
            raise ValueError("Les positions sont en deux dimensions.")
        self.x, self.y = x_ou_pos[0], x_ou_pos[1]
    
    def __repr__(self):
        return f"Pos({self.x}; {self.y})"
    def __str__(self):
        return f"({self.x}; {self.y})"
    
    def __add__(self, other : 'Pos|Vecteur') -> 'Pos':
        if type(other) is Vecteur:
            return Pos(self.x + int(other.x), self.y + int(other.y))
        if type(other) is Pos:  # pas necessaire mais le typechecker...
            return Pos(self.x + other.x, self.y + other.y)
        
        raise TypeError("On ne peut ajouter un objet pos qu'a un vecteur (de pygame) ou une autre instance de Pos.")
    
    def __sub__(self, other : 'Pos|Vecteur') -> 'Pos':
        if type(other) is Vecteur:
            return Pos(self.x - int(other.x), self.y - int(other.y))
        if type(other) is Pos:
            return Pos(self.x - other.x, self.y - other.y)
        
        raise TypeError("On ne peut ajouter un objet pos qu'a un vecteur (de pygame) ou une autre instance de Pos.")
    
    # à NE PAS définir: le signe, la multiplication et division (scalaire ou pos), l'exponentiation.
    # La raison est simple: les positions ne sont pas des vecteurs
    # Si l'addition et la soustraction sont permis, c'est pour avoir moins à écrire.
    
    @staticmethod
    def milieu(p1 : 'Pos|Vecteur', p2 : 'Pos|Vecteur') -> 'Pos':
        """Retourne le milieu du segment allant de p1 à p2."""
        if type(p1) is Pos:
            p1 = p1.vecteur
        if type(p2) is Pos:
            p2 = p2.vecteur
        
        assert(type(p1) is Vecteur and type(p2) is Vecteur) # on réassure le type checker
        return Pos((p1 + p2) / 2)
    
    @property
    def tuple(self) -> tuple[int, int]:
        return (self.x, self.y)
    
    @property
    def vecteur(self) -> Vecteur:
        return Vecteur(self.x, self.y)

pos_pygame : TypeAlias = tuple[int, int]|list[int]
pos_t      : TypeAlias = Pos|pos_pygame

def pos_t_vers_Pos(p : pos_t) -> Pos:
    from copy import copy
    
    if type(p) is Pos:
        return copy(p)
    
    # I love pywright--------------------
    # (on sait déjà que c'est l'un des deux)
    assert(type(p) is tuple or type(p) is list) 
    return Pos(p)

def pos_t_vers_tuple(p : pos_t) -> tuple[int, int]:
    return pos_t_vers_Pos(p).tuple