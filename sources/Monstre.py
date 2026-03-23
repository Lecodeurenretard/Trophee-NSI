"""Contient la classe Mostre et MonstreJSON."""
from Entite import *
from Pool import Pool

@dataclass
class MonstreJSON(EntiteJSON):
    """La représentation d'un monstre dans le JSON."""
    rang : int # pyright: ignore[reportGeneralTypeIssues]   # Il aime pas le ClassVar de EntiteJSON
    
    @overload
    def __init__(self, id_ou_nom : int, autoriser_exemple : bool = False): ...
    @overload
    def __init__(self, id_ou_nom : str, autoriser_exemple : bool = False): ...
    
    @override
    def __init__(self, id_ou_nom : int|str, autoriser_exemple : bool = False):
        if type(id_ou_nom) is str:
            id_ou_nom = EntiteJSON.chercher_nom(id_ou_nom)
        assert(type(id_ou_nom) is int), f"{type(id_ou_nom)}"
        
        
        try:
            super().__init__(id_ou_nom, autoriser_exemple=autoriser_exemple)
            donnees : dict = EntiteJSON.DONNEES_TYPES[id_ou_nom]
            self.rang = donnees["rang"]
        except KeyError as err:
            raise RuntimeError(f"La clef {err.args[0]} n'est pas définie dans le JSON.")
    
    def type_precedent(self) -> 'MonstreJSON':
        if self.id <= EntiteJSON.INDEX_JOUEUR + 1:
            return MonstreJSON(len(MonstreJSON.DONNEES_TYPES) - 1)
        return MonstreJSON(self.id - 1)
    
    def type_suivant(self) -> 'MonstreJSON':
        if self.id <= len(MonstreJSON.DONNEES_TYPES) - 1:
            return MonstreJSON(EntiteJSON.INDEX_JOUEUR)
        return MonstreJSON(self.id + 1)


class Monstre(Entite):
    _CARTES_DE_DOS           : bool = True
    _CARTE_MAIN_PREMIERE_POS : Pos  = Fenetre.pourcentages_coordonnees(33, 3)
    POSITION_CENTREE         : Pos  = Fenetre.pourcentages_coordonnees(60, 23)
    
    @override
    def __init__(
            self,
            type       : MonstreJSON,
            inventaire : Sequence[Item] = (),
            _taille_sprite : Optional[Vecteur] = None,
        ):
        super().__init__(
            type,
            inventaire=inventaire,
            _taille_sprite=_taille_sprite,
        )
        self._type = type
    
    
    @staticmethod
    def spawn(pool : Pool) -> 'Monstre':
        """
        Tire un monstre dans la pool et le spawn.
        """
        if len(pool) == 0:
            raise ValueError("La pool est vide.")
        nom_monstre = pool.tirer_n(1)
        
        monstre = Monstre(
            MonstreJSON(
                nom_monstre[0]
            ),
        )
        monstre.piocher()
        return monstre
    
    @staticmethod
    def adversaire() -> Optional[Monstre]:
        """Renvoie l'adversaire principal du combat."""
        for _, m in Monstre.vivants().no_holes():   # no_holes() est un itérateur, pas de __getitem__
            return m     # Le premier monstre à être ajouté au combat
        return None
    
    @staticmethod
    def massacre() -> None:
        """Tue tous les monstres vivants."""
        for _, monstre in Monstre.vivants().no_holes():
            monstre.meurt()
    
    
    @property
    def pos_sprite_centree(self) -> Pos:
        return Monstre.POSITION_CENTREE
    
    @property
    def rang(self) -> int:
        return self._type.rang
    
    
    def _vers_type(self, nouveau_type : MonstreJSON) -> None:
        self._type = nouveau_type
        self._nom = nouveau_type.nom
        self._deck = nouveau_type.deck
        
        ratio_vie = self._stats.vie / self._stats.vie_max
       
        self._stats = copy(nouveau_type.stats)
        self._stats.vie = round(self._stats.vie_max * ratio_vie)    # Conserve les proportions
        
        self._sprite = pygame.transform.scale(
            pygame.image.load(nouveau_type.sprite),
            self._SPRITE_TAILLE
        )
    
    def vers_type_precedent(self) -> None:
        """Change le type du monstre vers le précédent."""
        self._vers_type(self._type.type_precedent())
    
    def vers_type_suivant(self) -> None:
        """Change le type du monstre vers le suivant."""
        self._vers_type(self._type.type_suivant())
    
    def choisir_index_carte_main(self) -> int:
        assert(len(self._cartes_main) > 0), f"La main du monstre d'ID {self._id} (un {self._nom}) est vide!"
        return random.randint(0, len(self._cartes_main)-1)
    
    @override
    def decrire_stats(self) -> str:
        """Décrit l'objet dans une string."""
        return (
            Entite.decrire_stats(self)
            + f"ID du type: {self._type.id}\n"
            + f"Rang: {self.rang}\n"
        )