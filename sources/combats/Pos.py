class Pos:
	# Encore une fois, Pos est une "structure" => pas d'encapsulation
	def __init__(self, x : int, y : int):
		self.x = x
		self.y = y
	
	def __eq__(self, autre_pos : 'Pos'):
		return self.x == autre_pos.x and self.y == autre_pos.y
	
	def __str__(self):
		return f"({self.x}; {self.y})"
	def __iter__(self):
		# v. Réponse StackOverflow https://stackoverflow.com/questions/37639363/how-to-convert-an-custom-class-object-to-a-tuple-in-python
		# La réponse en court est que cette fonction permet de convertir les objets en tuple et en liste.
		yield self.x	# return mais en bizarre
		yield self.y
	
	@staticmethod
	def a_partir_de_liste(iterable : list[int] | tuple[int, int]) -> 'Pos':
		assert(len(iterable) == 2), "Les positions sont en deux dimensions."
		return Pos(iterable[0], iterable[1])