from imports import dataclass

@dataclass
class Pos:
    x : int
    y : int
    
    def __iter__(self):
        # v. Réponse StackOverflow https://stackoverflow.com/questions/37639363/how-to-convert-an-custom-class-object-to-a-tuple-in-python
        # La réponse en court est que cette fonction permet de convertir les objets en tuple et en liste.
        yield self.x	# return mais qui peut se faire plusieurs fois
        yield self.y
    
    def __repr__(self):
        return f"({self.x}; {self.y})"
    
    @staticmethod
    def a_partir_de_liste(iterable : list[int] | tuple[int, int]) -> 'Pos':
        assert(len(iterable) == 2), "Les positions sont en deux dimensions."
        return Pos(iterable[0], iterable[1])