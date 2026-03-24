"""
projet : L'ascension de Esquimot
auteur : Dooheli, Lecodeurenretard, hibou509
"""

from imports import random, dataclass, copy, json, overload, Callable, math

class Pool:
    """
    Structure de donnée permettant de piocher des choses de manière aléatoire.
    Il est possible de comparer ceci à une boite remplie de papiers,
    le poids de ces bouts de papiers étant leurs nombre.
    """
    @dataclass
    class PoolObj:
        nom         : str
        poids       : float
        soustraire  : float
    
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, donnees_json : list) -> None: ...
    
    def __init__(self, donnees_json : list|None = None) -> None:
        self.pool : list[Pool.PoolObj] = []
        if donnees_json is not None:
            self._depuis_donnees_json(donnees_json)
    
    def __len__(self):
        return len(self.pool)
    
    def __iter__(self):
        for obj in self.pool:
            yield (obj.nom, obj.poids)
    
    def __str__(self) -> str:
        res = 'Pool('
        for t in self:
            res += f"{t}; "
        res += ')'
        return res
    
    @staticmethod
    def parse_fichier_pools(chemin_fichier : str) -> 'dict[str, Pool]':
        donnees : dict[str, list[dict]]
        with open(chemin_fichier, encoding="utf-8") as f:
            donnees = json.load(f)
        
        return {
            clef: Pool(donnee)
            for clef, donnee in donnees.items()
        }
    
    @property
    def _poids(self) -> list[float]:
        return [obj.poids for obj in self.pool]
    
    @property
    def noms(self) -> list[str]:
        return [obj.nom for obj in self.pool]
    
    def _depuis_donnees_json(self, liste_json : list[dict]) -> None:
        SOUSTRAIT_DEFAUT : float= 1
        self.pool = [
            Pool.PoolObj(
                dico["nom"],
                dico["poids"],
                dico["soustraire"] if dico["soustraire"] is not None else SOUSTRAIT_DEFAUT,
            )
            for dico in liste_json
        ]
    
    def tirer_n(self, n : int, filtre : Callable[[str], bool]|None = None) -> list[str]:
        """
        Tire n éléments de la pool, si filtre() est fournie ne tire une carte c que si filtre(c) == True.
        S'il n'y a pas assez d'élément dans la pool, élève une IndexError.
        """
        if n <= 0:
            return []
        if filtre is None:
            filtre = lambda nom: True # Accepte tout
        
        # filtre() n'est pas garantit de renvoyer le même résultat
        # s'il est appelé plusieurs fois avec les même arguments.
        obj_filtres = [
            (i, obj.poids)
            for i, obj in enumerate(self.pool)
            if filtre(obj.nom)
        ]
        index_filtres = [idex  for idex, _  in obj_filtres]
        poids_filtres = [poids for _, poids in obj_filtres]
        
        try:
            indices_tires = random.choices(index_filtres, weights=poids_filtres, k=n)
        except IndexError:   # La pool n'a pas assez d'objets
            raise IndexError(f"La pool n'a pas assez d'éléments pour le tirage.")
        
        tirages = []
        pool = copy(self.pool)  # shallow copy pour éviter les problèmes de décalage d'indice
        for i in indices_tires:
            obj = pool[i]
            
            obj.poids -= obj.soustraire     # baisse la probabilité d'apparaitre
            if obj.poids <= 0:
                self.pool.pop(i)
            tirages.append(pool[i].nom)
        
        return tirages
    
    def vider(self) -> list[str]:
        res = []
        for obj in self.pool:
            res.extend(
                # nom répété le nombre de fois qu'il aurait pu être tiré.
                [obj.nom] * math.floor(obj.poids / obj.soustraire)
            )
        
        self.pool = []
        return res
    