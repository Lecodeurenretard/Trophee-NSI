from imports import dataclass, overload, Vecteur, Generator

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
    
    def __iter__(self) -> Generator[int, None, None]:
        # v. Réponse StackOverflow https://stackoverflow.com/questions/37639363/how-to-convert-an-custom-class-object-to-a-tuple-in-python
        # En court, cette fonction permet de convertir les objets en tuple et en liste.
        # Techniquement, grâce à elle on pourrait itérer à travers une position avec une boucle for
        # mais personne ne fera ceci, n'est-ce pas?
        yield self.x    # return mais qui peut se faire plusieurs fois
        yield self.y
    
    def __repr__(self):
        return f"({self.x}; {self.y})"
    
    def __add__(self, other : 'Pos|Vecteur') -> 'Pos':
        if type(other) is Vecteur:
            return Pos(self.x + int(other.x), self.y + int(other.y))
        if type(other) is Pos:  # pas necessaire, mais Pylance ne veut pas me lacher sinon
            return Pos(self.x + other.x, self.y + other.y)
        
        raise TypeError("On ne peut ajouter un objet pos qu'a un vecteur (de pygame) ou une autre instance de Pos.")
    def __sub__(self, other : 'Pos|Vecteur') -> 'Pos':
        if type(other) is Vecteur:
            return Pos(self.x - int(other.x), self.y - int(other.y))
        if type(other) is Pos:
            return Pos(self.x - other.x, self.y - other.y)
        
        raise TypeError("On ne peut ajouter un objet pos qu'a un vecteur (de pygame) ou une autre instance de Pos.")
    
    @staticmethod
    def milieu(p1 : 'Pos|Vecteur', p2 : 'Pos|Vecteur') -> 'Pos':
        """Retourne le milieu du segment allant de p1à p2."""
        p1 = Vecteur(tuple(p1)) # conversion en vecteur
        p2 = Vecteur(tuple(p2))
        
        return Pos((p1 + p2) / 2)
    
    # à NE PAS définir: le signe, la multiplication et division (scalaire ou pos), l'exponentiation.
    # La raison est simple: les positions ne sont pas des vecteurs
    # Si l'addition et la soustraction sont permis, c'est pour avoir moins à écrire.