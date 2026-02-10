from Entite import *

@dataclass
class MonstreJSON:
    """La représentation d'un monstre dans le JSON."""
    DONNEES_TYPES : list[dict] = field(repr=False)
    
    id             : int
    nom            : str
    sprite         : str
    rang           : int
    nb_cartes_main : int
    deck           : tuple[str, ...]
    stats          : Stat
    
    def __init__(self, id_type : int, autoriser_exemple : bool = False):
        if id_type == 0 and not autoriser_exemple:
            raise RuntimeError("Le monstre d'exemple (id 0) est interdit.")
        donnees : dict = MonstreJSON.DONNEES_TYPES[id_type]
        
        self.id = id_type
        self.nom = donnees["nom"]
        
        self.sprite = valeur_par_defaut(
            donnees['sprite'],
            si_non_none=f"{Chemins.IMG}/monstres/{donnees['sprite']}",
            si_none=f"{Chemins.IMG}/erreur.png",
        )
        
        self.rang = donnees["rang"]
        self.nb_cartes_main = donnees["nombre_cartes_main"]
        self.deck = tuple(donnees["moveset"])
        self.stats = Stat.depuis_dictionnaire_json(donnees["stats"]).reset_vie()
    
    @staticmethod
    def actualiser_donnees() -> None:
        """Actualise DONNEES_TYPES[]."""
        with open(f"{Chemins.DATA}/TypesMonstre.json", 'r', encoding='utf-8') as fichier:
            MonstreJSON.DONNEES_TYPES = json.load(fichier)
    
    def type_precedent(self, autoriser_exemple : bool = False) -> 'MonstreJSON':
        if self.id == 0 or (not autoriser_exemple and self.id == 1):
            return MonstreJSON(len(MonstreJSON.DONNEES_TYPES) - 1)
        return MonstreJSON(self.id - 1)
    
    def type_suivant(self, autoriser_exemple : bool = False) -> 'MonstreJSON':
        if self.id == len(MonstreJSON.DONNEES_TYPES) - 1:
            return MonstreJSON(0 if autoriser_exemple else 1)
        return MonstreJSON(self.id + 1)

MonstreJSON.actualiser_donnees()


class Monstre(Entite):
    _CARTES_DE_DOS           : bool = True
    _CARTE_MAIN_PREMIERE_POS : Pos  = Jeu.pourcentages_coordonnees(33, 3)
    POSITION                 : Pos  = Jeu.pourcentages_coordonnees(72, 42)
    
    @override
    def __init__(
            self,
            type       : MonstreJSON,
            inventaire : Sequence[Item] = (),
        ):
        super().__init__(
            type.nom,
            type.stats,
            type.deck,
            type.nb_cartes_main,
            chemin_sprite=type.sprite,
            inventaire=inventaire,
        )
        self._type = type
    
    
    @staticmethod
    def spawn(proba : list[float]|tuple[float, ...]|None = None) -> 'Monstre':
        """
        Spawn un monstre au hasard (exclut l'exemple).
        Si `proba[]` n'est pas None alors le monstre d'index i aurat une probabilité de porba[i] de spawn.
        """
        poids : Optional[list[float]] = None
        id_types : list[int] = [i for i, _ in enumerate(MonstreJSON.DONNEES_TYPES)]
        id_types.pop(0)     # l'exemple n'est pas pris en compte
        
        if proba is not None:
            poids = [-1.0] * len(id_types)    # garantit de trouver une clef
            
            for i, type in enumerate(id_types):
                poids[i] = proba[type]
        
        monstre = Monstre(
            MonstreJSON(random.choices(id_types, weights=poids)[0]),
        )
        monstre.piocher()
        return monstre
    
    @staticmethod
    def vivants() -> list['Monstre']:
        """Renvoie les monstres en vie."""
        # on admet que c'est que des monstres
        return [
            monstre
            for clef, monstre in Entite.vivantes.no_holes()
            if isinstance(monstre, Monstre)
        ]
    
    @staticmethod
    def massacre() -> None:
        """Tue tous les monstres vivants."""
        for monstre in Monstre.vivants():
            monstre.meurt()
        Entite.tuer_les_entites_mortes()
    
    
    @property
    def pos_sprite(self) -> Pos:
        return centrer_pos(Monstre.POSITION, Monstre._SPRITE_TAILLE)
    @property
    def pos_attaque(self) -> Pos:
        return Monstre.POSITION - Vecteur(Carte._HAUTEUR_SPRITE, Carte._HAUTEUR_SPRITE)
    
    @property
    def rang(self) -> int:
        return self._type.rang
    
    
    def _vers_type(self, nouveau_type : MonstreJSON) -> None:
        self._nom = nouveau_type.nom
        
        ratio_vie = self._stats.vie / self._stats.vie_max
       
        self._stats = copy(nouveau_type.stats)
        self._stats.vie = round(self._stats.vie_max * ratio_vie)    # Conserve les proportions
        
        self._deck = list(nouveau_type.deck)
        
        self._sprite = pygame.transform.scale(pygame.image.load(nouveau_type.sprite), Monstre._SPRITE_TAILLE)
        self._type = nouveau_type
    
    def choisir_index_carte_main(self) -> int:
        assert(len(self._cartes_main) > 0), f"La main du monstre d'ID {self._id} (un {self._nom}) est vide!"
        return random.randint(0, len(self._cartes_main)-1)
    
    def vers_type_precedent(self) -> None:
        """Change le type du monstre vers le précédent."""
        self._vers_type(self._type.type_precedent())
    
    def vers_type_suivant(self) -> None:
        """Change le type du monstre vers le suivant."""
        self._vers_type(self._type.type_suivant())
    
    @override
    def decrire_stats(self) -> str:
        """Décrit l'objet dans une string."""
        return (
            Entite.decrire_stats(self)
            + f"ID du type: {self._type.id}\n"
            + f"Rang: {self.rang}\n"
        )