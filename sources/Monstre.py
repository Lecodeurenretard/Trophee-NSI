from Carte import *

@dataclass
class MonstreJSON:
    """Les propriétés des types des monstres quand ils sont parse de TypesMonstre.json"""
    DONNEES_TYPES : list[dict] = field(repr=False)
    
    id      : int
    nom     : str
    sprite  : str
    rang    : int
    moveset : tuple[str, ...]
    stats   : Stat
    
    def __init__(self, id_type : int, autoriser_exemple : bool = False):
        if id_type == 0 and not autoriser_exemple:
            raise RuntimeError("Le monstre d'exemple (id 0) est interdit.")
        donnees : dict = MonstreJSON.DONNEES_TYPES[id_type]
        
        self.id = id_type
        self.nom = donnees["nom"]
        
        if donnees['sprite'] is None:
            donnees['sprite'] = f"{Constantes.Chemins.IMG}/erreur.png"
        self.sprite = f"{Constantes.Chemins.IMG}/monstres/{donnees['sprite']}"
        
        self.rang = donnees["rang"]
        self.moveset = tuple(donnees["moveset"])
        self.stats = Stat.depuis_dictionnaire_json(donnees["stats"]).reset_vie()
    
    @staticmethod
    def actualiser_donnees() -> None:
        """Actualise DONNEES_TYPES[]."""
        with open(f"{Constantes.Chemins.DATA}/TypesMonstre.json", 'r', encoding='utf-8') as fichier:
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


class Monstre:
    POSITION : Pos = Jeu.pourcentages_coordonees(70, 15)
    SPRITE_DIM : tuple[int, int] = (150, 150)
    
    # La liste de tous les monstres en vie
    # Peut-être des combats vs plusieurs monstres?
    monstres_en_vie : list['Monstre'] = []
    
    # devrait être utilisé le moins possible, préférer nouveau_monstre()
    def __init__(
            self,
            nom           : str,
            stats         : Stat,
            attaques      : tuple[str, ...],
            chemin_sprite : Optional[str]         = None,
            type       : Optional[MonstreJSON] = None,
        ):
        
        self._nom = nom
        self._stats = stats
        self._moveset = attaques
        self._type = type
        
        if chemin_sprite is None:
            chemin_sprite = f"{Constantes.Chemins.IMG}/erreur.png"
        self._sprite  : Surface = pygame.transform.scale(pygame.image.load(chemin_sprite), Monstre.SPRITE_DIM)
        
        Monstre._ajouter_monstre_a_liste(self)
        self.afficher : bool = True
        
        self._id = premier_indice_libre_de_entites_vivantes()
        if self._id >= 0:
            globales.entites_vivantes[self._id] = self
            return
        
        self._id = len(globales.entites_vivantes)
        globales.entites_vivantes.append(self)
    
    def __del__(self):
        # Appelé quand l'objet est détruit (quand nous ne pouvons plus accéder à l'objet)
        if (
            self._id > 0
            and globales.entites_vivantes is not None
            and Monstre.monstres_en_vie is not None
        ):
            self.meurt()
    
    @staticmethod
    def nouveau_monstre(type_json : MonstreJSON) -> 'Monstre':
        """Crée un nouveau monstre suivant son type"""
        return Monstre(
            type_json.nom,
            copy(type_json.stats),    # Si pas de copie, tous les monstres suivants auront leurs vie à 0
            tuple(type_json.moveset),
            chemin_sprite=type_json.sprite,
            type=type_json
        )
    
    @staticmethod
    def _ajouter_monstre_a_liste(monstre : 'Monstre') -> None:
        Monstre.monstres_en_vie.append(monstre)
    
    @staticmethod
    def _enlever_monstre_a_liste(monstre : 'Monstre') -> None:
        for i, m in enumerate(Monstre.monstres_en_vie):
            if monstre._id == m._id:
                Monstre.monstres_en_vie.pop(i)
                return
        logging.warning("La fonction Monstre._enlever_monstre_a_liste() à été appellée sur un monstre pas dans la liste dans Monstre.monstres_en_vie[].")
    
    @staticmethod
    def tuer_les_monstres_morts() -> list['Monstre']:
        """
        Appelle la méthode `.meurt()` sur les monstres dont la propriété `.est_mort` est True.
        Renvoie la liste des monstres morts.
        """
        echafaud : list[Monstre] = []   # Quand les monstres seront enlevés de la liste, ils seront "exécutés" par le rammasse-miette
        for monstre in Monstre.monstres_en_vie:
            if monstre.est_mort:
                monstre.meurt()
                echafaud.append(monstre)
        
        return echafaud
    
    @staticmethod
    def spawn(proba : list[float]|tuple[float, ...]|None = None) -> 'Monstre':
        """
        Spawn un monstre au hasard (exclut l'exemple).
        Si `proba[]` n'est pas None alors le monstre d'index i aurat une probabilité de porba[i] de spawn.
        """
        poids : Optional[list[float]] = None
        id_types : list[int] = [i for i, _ in enumerate(MonstreJSON.DONNEES_TYPES)]
        id_types.pop(0)
        
        if proba is not None:
            poids = [-1.0] * len(id_types)    # garantit de trouver une clef
            
            for i, type in enumerate(id_types):
                poids[i] = proba[type]
        
        return Monstre.nouveau_monstre(
            MonstreJSON(random.choices(id_types, weights=poids)[0])
        )
    
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def est_mort(self) -> bool:
        return self._stats.est_mort
    
    @property
    def nom(self) -> str:
        return self._nom
    @property
    def dbg_nom(self) -> str:
        return self.nom
    
    @property
    def stats_totales(self) -> Stat:
        return copy(self._stats)
    @property
    def pos_attaque(self) -> Pos:
        return centrer_pos(Monstre.POSITION, Monstre.SPRITE_DIM)
    
    @property
    def pos_curseur(self) -> Pos:
        return Pos(0, 0)
    
    @property
    def rang(self) -> Optional[int]:
        if self._type is not None:
            return self._type.rang
        return None
    
    # même raisonnement que dans Joueur
    def meurt(self) -> None:
        globales.entites_vivantes[self._id] = None
        Monstre._enlever_monstre_a_liste(self)
        self._id = -1
    
    def _vers_type(self, nouveau_type : MonstreJSON) -> None:
        self._nom = nouveau_type.nom
        
        ratio_vie = self._stats.vie / self._stats.vie_max
       
        self._stats = copy(nouveau_type.stats)
        self._stats.vie = round(self._stats.vie_max * ratio_vie)    # Conserve les proportions
        
        self._moveset = nouveau_type.moveset
        
        self._sprite = pygame.transform.scale(pygame.image.load(nouveau_type.sprite), Monstre.SPRITE_DIM)
        self._type = nouveau_type
    
    def choisir_carte(self) -> Carte:
        return Carte(
            random.choice(self._moveset),
        )
    
    def attaquer(self, id_cible : int, nom_attaque : str) -> None:
        """Attaque la cible et retourne si elle a été tuée."""
        assert(globales.entites_vivantes[id_cible] is not None), "La cible est une case vide de globales.entites_vivantes[] dans Monstre.attaquer() (index invalide)."
        assert(nom_attaque in self._moveset), f"L'attaque {nom_attaque} n'est pas dans le moveset du monstre d'identifiant {self.id}."
        
        Carte(nom_attaque).enregister_lancement(self._id, id_cible)
    
    def recoit_degats(self, dommages : int) -> None:
        if bool(params.monstre_invincible) and dommages >= 0:
            return
        
        self._stats.baisser_vie(dommages)
    
    def longueur_barre_de_vie(self) -> int:
        ratio = max(0, self._stats.vie / self._stats.vie_max)
        return round(ratio * Constantes.UI_LONGUEUR_BARRE_DE_VIE)
    
    def dessiner(self, surface : Surface, pos_x : int, pos_y : int) -> None:
        blit_centre(surface, self._sprite, (pos_x, pos_y))
    
    def dessiner_barre_de_vie(self, surface : Surface, pos : Pos):
        dessiner_barre_de_vie(surface, pos, self._stats.vie / self._stats.vie_max, self.longueur_barre_de_vie())
    
    def vers_type_precedent(self) -> bool:
        """Si le monstre à un type, change le type du monstre vers le précédent et renvoie True, sinon renvoie False et ne fait rien."""
        if self._type is None:
            return False
        
        self._vers_type(self._type.type_precedent())
        return True
    
    def vers_type_suivant(self) -> bool:
        """Si le monstre à un type, change le type du monstre vers le suivant et renvoie True, sinon renvoie False et ne fait rien."""
        if self._type is None:
            return False
        
        self._vers_type(self._type.type_suivant())
        return True
    
    def decrire(self) -> str:
        """Décrit l'objet dans une string."""
        return (
            f"ID d'entité: {self._id}\n"
            f"ID du type: {self._type.id if self._type is not None else -1}\n"
            f"Rang: {self.rang}\n"
            f"Moveset: {self._moveset}\n"
            f"Statistiques: {self._stats}\n"
        )