from Monstre import *

@dataclass
class BossJSON:
    """La représentation d'un boss dans le JSON."""
    DONNEES_BOSS : list[dict] = field(repr=False)
    
    nom            : str
    chemin_sprite  : str
    deck_boss      : tuple[str, ...]
    deck_joueur    : Optional[tuple[str, ...]]
    nb_cartes_main : int
    pos_sprite     : Pos
    rang           : int
    stats          : Stat
    
    def __init__(
        self,
        id_type           : int,
        autoriser_exemple : bool = False,
    ):
        if id_type == 0 and not autoriser_exemple:
            raise RuntimeError("Le boss d'exemple (id 0) est interdit.")
        
        donnees : dict = BossJSON.DONNEES_BOSS[id_type]
        self.nom = donnees["nom"]
        
        self.chemin_sprite = valeur_par_defaut(
            donnees['sprite'],
            si_non_none=f"{Chemins.IMG}/boss/{donnees['sprite']}",
            si_none=f"{Chemins.IMG}/erreur.png",
        )
        
        self.nb_cartes_main = donnees["nombre_cartes_main"]
        self.deck_boss   = tuple(donnees["moveset_boss"])
        self.deck_joueur = donnees["moveset_joueur"]
        if self.deck_joueur is not None:
            self.deck_joueur = tuple(self.deck_joueur)
        
        self.pos_sprite = Pos(Jeu.vecteur_pourcentage(
            Pos(
                donnees["pos_sprite"]
            ).vecteur
        ))

        self.rang  = donnees["rang"]
        self.stats = Stat.depuis_dictionnaire_json(donnees["stats"]).reset_vie()
        
    @staticmethod
    def actualiser_donnees() -> None:
        """Actualise DONNEES_TYPES[]."""
        with open(f"{Chemins.DATA}/boss.json", 'r', encoding='utf-8') as fichier:
            BossJSON.DONNEES_BOSS = json.load(fichier)
    
    def vers_MonstreJSON(self) -> MonstreJSON:
        res = MonstreJSON(0, autoriser_exemple=True)
        res.nom = self.nom
        res.sprite = self.chemin_sprite
        res.nb_cartes_main = self.nb_cartes_main
        res.deck = self.deck_boss
        res.rang = self.rang                # formule approximative
        res.stats = self.stats
        
        return res

class Boss(Monstre):
    @override
    def __init__(
            self,
            boss_json  : BossJSON,
            inventaire : Sequence[Item] = (),
        ):
        super().__init__(
            boss_json.vers_MonstreJSON(),
            inventaire=inventaire,
        )
        self._rang        = boss_json.rang
        self._deck_joueur = boss_json.deck_joueur
        self._pos_sprite  = boss_json.pos_sprite
    
    @staticmethod
    def vivant() -> list[Boss]:
        """Renvoie les monstres en vie."""
        # on admet que c'est que des monstres
        return [
            monstre
            for _, monstre in Entite.vivantes.no_holes()
            if isinstance(monstre, Boss)
        ]
    
    @staticmethod
    def spawn_boss(etage : int = Jeu.num_etage() + 1) -> None:
        Boss(BossJSON(etage))
        # Le boss est enregistré dans Entite.vivantes[]
    
    @property
    def pos_sprite(self) -> Pos:
        return self._pos_sprite
    @property
    def pos_attaque(self) -> Pos:
        return self._pos_sprite
    
    # = delete mais c'est du python
    @override
    def _vers_type(self, nouveau_type : MonstreJSON) -> None:
        """Non implémenté pour Boss."""
        raise TypeError("La classe Boss n'a pas de méthode ._vers_type().")
    
    @override
    def vers_type_precedent(self) -> None:
        """Non implémenté pour Boss."""
        raise TypeError("La classe Boss n'a pas de méthode .vers_type_precedent().")
    
    @override
    def vers_type_suivant(self) -> None:
        """Non implémenté pour Boss."""
        raise TypeError("La classe Boss n'a pas de méthode .vers_type_suivant().")

BossJSON.actualiser_donnees()