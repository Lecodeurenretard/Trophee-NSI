from imports import dataclass, pygame, Vecteur, Generator

@dataclass
class Pos:
    x : int
    y : int
    
    def __iter__(self) -> Generator[int, None, None]:
        # v. Réponse StackOverflow https://stackoverflow.com/questions/37639363/how-to-convert-an-custom-class-object-to-a-tuple-in-python
        # En court, cette fonction permet de convertir les objets en tuple et en liste.
        yield self.x    # return mais qui peut se faire plusieurs fois
        yield self.y
    
    def __repr__(self):
        return f"({self.x}; {self.y})"
    
    # On traite les pos comme des vecteurs
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
    
    # à NE PAS définir: le signe, la multiplication et division (scalaire ou pos), l'exponentiation.
    # La raison est simple: les positions ne sont pas des vecteurs
    
    @staticmethod
    def a_partir_de_collection(iterable : list[int] | tuple[int, int]) -> 'Pos':
        assert(len(iterable) == 2), "Les positions sont en deux dimensions."
        return Pos(iterable[0], iterable[1])