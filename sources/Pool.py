from imports import random, dataclass, copy, json

class Pool:
    @dataclass
    class PoolObj:
        nom         : str
        poids       : float
        soustraire  : float
    
    def __init__(self, donnees_json : list) -> None:
        self.pool : list[Pool.PoolObj] = []
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
    def parse_fichier_pools(chemin_fichier : str) -> dict[str, Pool]:
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
    
    def tirer_n(self, n : int) -> list[str]:
        """Tire n éléments de la pool."""
        indices_tires = random.choices(range(len(self.noms)), weights=self._poids, k=n)
        tirages = []
        
        pool = copy(self.pool)  # shallow copy pour éviter les problèmes de décalage d'indice
        for i in indices_tires:
            obj = pool[i]
            obj.poids -= obj.soustraire     # baisse la probabilité d'apparaitre
            
            if obj.poids <= 0:
                self.pool.pop(i)
            tirages.append(pool[i].nom)
        
        return tirages