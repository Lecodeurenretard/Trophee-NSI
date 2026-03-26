"""
Contient la classe Item.
projet : L'ascension de Esquimot
auteur : Dooheli, Lecodeurenretard, hibou509
"""
from import_local import *
from Carte        import Carte, Attaque

@dataclass
class ItemInterfaceMethodes:
    nouveau_tour : None|Callable[[Item            , dict[str, Any]], None] = None
    nouvel_etage : None|Callable[[Item            , dict[str, Any]], None] = None
    nouveau_shop : None|Callable[[Item, list[Item], dict[str, Any]], None] = None
    
    carte_jouee          : None|Callable[[Item, Carte       , dict[str, Any]], None] = None
    porteur_subit_dmg    : None|Callable[[Item, Attaque, int, dict[str, Any]], None] = None
    adversaire_subit_dmg : None|Callable[[Item, Attaque, int, dict[str, Any]], None] = None    # on attend un id
    
    attributs_supplementaires : dict[str, Any] = field(default_factory=dict)

class Item:
    """Un item passif ayant un effet sur le joueur/gameplay."""
    DONNEES_ITEMS      : ClassVar[list[dict]]      = []
    ORDONEE_SPRITE     : ClassVar[int]             = Fenetre.pourcentage_hauteur(10)
    DIMENSIONS_SPRITES : ClassVar[tuple[int, int]] = (350, 350)
    REDUCTION_PROMO    : ClassVar[float]           = .8
    
    callbacks : dict[str, ItemInterfaceMethodes] = {}       # v. fonctions_item.py
    
    def __init__(self, id : int, permissif : bool = False, interdire_exemple : bool = True):
        """Si `permissif` est actif, corrige l'id."""
        assert(len(Item.DONNEES_ITEMS) > 0), "Item.DONNEES_ITEMS est vide, il faut appeler Item.actualiser_items() avant de créer un objet."
        if permissif:
            id = clamp(
                    id,
                    int(interdire_exemple),     # 1 if interdire_exemple else 0,
                    len(Item.DONNEES_ITEMS) - 1
                )
        elif not (0 <= id < len(Item.DONNEES_ITEMS)):
            raise OverflowError("id soit négatif, soit trop grand.")
        elif interdire_exemple and id == 0:
            raise ValueError("L'item d'indice 0 (l'exemple) n'est pas autorisé par défaut par le constructeur de Item.")
        
        item : dict = Item.DONNEES_ITEMS[id]
        
        self.id          = id
        self.nom         = item["nom"]
        self.description = item["description"]
        
        chemin : str = f"{Chemins.IMG}"
        chemin += valeur_par_defaut(
            item['sprite'],
            si_non_none=f"items/{item['sprite']}",
            si_none="erreur.png"
        )
        self.sprite      = pygame.image.load(chemin)
        self.sprite      = pygame.transform.scale(self.sprite, self.DIMENSIONS_SPRITES)
        
        self._prix        = valeur_par_defaut(item["prix"], 0)
        
        self.interface : ItemInterfaceMethodes = ItemInterfaceMethodes()
        if self.nom in Item.callbacks.keys():
            self.interface = Item.callbacks[self.nom]
        
        self.effet_affiche  = item["effets"]["message utilisateur"]
        self.stats_changees = Stat.depuis_dictionnaire_json(item["effets"]["stats"], valeur_par_defaut=0)
        # .stats_changees sera ajouté/enlevé aux stats correspondantes du joueur.
        
        self.en_promo = False
    
    def __str__(self):
        return self.nom
    
    def __repr__(self):
        return (
            "Item("
            f"id={self.id}, "
            f"nom={self.nom}"
            ")"
        )
    
    def __eq__(self, obj : object):
        assert(type(obj) is Item), "On ne peut comparer un item qu'avec un autre item."
        return self.id == obj.id
    
    @staticmethod
    def actualiser_items() -> None:
        """Ouvre item.json et prend tous les objets trouvés."""
        with open(f"{Chemins.JSON}items.json", 'r', encoding='utf-8') as fichier:
            Item.DONNEES_ITEMS = json.load(fichier)
    
    @staticmethod
    def depuis_nom(nom_item : str) -> 'Item':
        """Initialise un objet Item avec les attributs de l'objet ayant le même nom dans le JSON."""
        for id, item_json in enumerate(Item.DONNEES_ITEMS):
            if nom_item == item_json["nom"]:
                return Item(id)
        raise ValueError(f"Le nom \"{nom_item}\" n'a pas été trouvé.")
    
    @staticmethod
    def item_aleatoire() -> 'Item':
        assert(len(Item.DONNEES_ITEMS) > 0), "Item.DONNEES_ITEM[] est vide!"
        return Item(random.randint(1, len(Item.DONNEES_ITEMS) - 1))
    
    @staticmethod
    def generateur_items(consecutifs_differents : bool = False) -> 'Generator[Item, None, None]':
        """
        Génère des items randoms.
        Si `consecutifs_differents` est coché, ne gènere pas deux fois le même item d'affilée.
        """
        dernier_item_id : int = -1
        while True:
            res : Item = Item.item_aleatoire()
            if consecutifs_differents and res.id == dernier_item_id:
                continue
            dernier_item_id = res.id
            
            try                 : yield res
            except GeneratorExit: break
    
    @staticmethod
    def item_survole(liste_item : 'list[Item]|tuple[Item, ...]', abscisses : list[int]|tuple[int, ...]) -> Optional[int]:
        """Renvoie l'index de l'item survolé ou None si aucun ne l'est."""
        for i, item in enumerate(liste_item):
            decalage = Vecteur(
                abscisses[i] - Item.DIMENSIONS_SPRITES[0]//2,
                Item.ORDONEE_SPRITE
            )
            hitbox = translation(item.sprite.get_bounding_rect(), decalage)
            
            if hitbox.collidepoint(pygame.mouse.get_pos()):
                return i
        return None
    
    @property
    def prix(self) -> int:
        prix = self._prix
        if self.en_promo:
            prix = int(prix * Item.REDUCTION_PROMO)
        return prix
    
    @prix.setter
    def prix(self, val : int) -> None:
        self._prix = val
    
    def dessiner(self, num_couche : int, abscisses : int, afficher_avertissements : bool = True) -> None:
        HAUTEUR_POLICE_NORMALE : int = 7
        RECT_GLOBAL : Rect = Rect(
            abscisses - self.DIMENSIONS_SPRITES[0] // 2,
            0,
            self.DIMENSIONS_SPRITES[0],
            Fenetre.hauteur,
        )
        
        couleur_prix = ROUGE if self.en_promo else JAUNE_PIECE
        
        nom  : Surface = (
            Fenetre.construire_police(Polices.TITRE, 12)
                .render(self.nom, True, NOIR)
        )
        prix : Surface = (
            Fenetre.construire_police(Polices.TEXTE, 10)
                .render(f"{self._prix} pieces", True, couleur_prix)
        )
        
        rect_sprite : Rect = Rect(
            (abscisses, Item.ORDONEE_SPRITE),
            self.sprite.get_rect().size,
        )
        rect_nom    : Rect = Rect(
            (abscisses, rect_sprite.bottom),
           nom.size,
        )
        pos_prix   : Pos = Pos(
            abscisses + rect_sprite.width // 2 + Fenetre.pourcentage_largeur(1),
            rect_sprite.y,
        )
        rect_effet : Rect = Rect(
            abscisses,
            rect_nom.bottom + Fenetre.pourcentage_hauteur(2),
            rect_sprite.width,
            Fenetre.pourcentage_hauteur(HAUTEUR_POLICE_NORMALE)
        )
        rect_desc  : Rect = Rect(
            abscisses,
            rect_effet.bottom + Fenetre.pourcentage_hauteur(4),
            rect_sprite.width,
            Fenetre.pourcentage_hauteur(42)
        )
        
        police = Fenetre.construire_police(Polices.TEXTE, HAUTEUR_POLICE_NORMALE)
        
        blit_centre_rect(num_couche, self.sprite, RECT_GLOBAL, centre_rect_y=False, pos=Pos(-1, rect_sprite.centery))
        blit_centre_rect(num_couche, nom        , RECT_GLOBAL, centre_rect_y=False, pos=Pos(-1, rect_nom.centery))
        blit_centre(num_couche, prix, pos_prix.tuple)
        
        rect_effet.centerx = RECT_GLOBAL.centerx
        rect_desc.centerx  = RECT_GLOBAL.centerx
        
        texte_non_dessine_effet = dessiner_texte(num_couche, self.effet_affiche, NOIR, rect_to_tuple(rect_effet), police)
        texte_non_dessine_desc  = dessiner_texte(num_couche, self.description  , NOIR, rect_to_tuple(rect_desc), police)
        
        if afficher_avertissements and texte_non_dessine_effet != '':
            logging.debug(f"Le texte suivant n'a pas pu être dessiné (effet d'un  item trop long): {texte_non_dessine_effet}")
        if afficher_avertissements and texte_non_dessine_desc != '':
            logging.debug(f"Le texte suivant n'a pas pu être dessiné (description d'un  item trop longue): {texte_non_dessine_desc}")
    
    def nouveau_tour(self) -> None:
        callback = self.interface.nouveau_tour
        if callback is not None:
            callback(self, self.interface.attributs_supplementaires)
    
    def nouvel_etage(self) -> None:
        callback = self.interface.nouvel_etage
        if callback is not None:
            callback(self, self.interface.attributs_supplementaires)
    
    def nouveau_shop(self, items_du_shop : list[Item]) -> None:
        """Appelé a chaque nouveau combat même le shop."""
        callback = self.interface.nouveau_shop
        if callback is not None:
            callback(self, items_du_shop, self.interface.attributs_supplementaires)
    
    def carte_jouee(self, carte : Carte) -> None:
        callback = self.interface.carte_jouee
        if callback is not None:
            callback(self, carte, self.interface.attributs_supplementaires)
    
    def porteur_subit_dmg(self, attaque : Attaque, id_porteur : int) -> None:
        callback = self.interface.porteur_subit_dmg
        if callback is not None:
            callback(self, attaque, id_porteur, self.interface.attributs_supplementaires)
    
    def adversaire_subit_dmg(self, attaque : Attaque, id_adversaire : int) -> None:
        callback = self.interface.adversaire_subit_dmg
        if callback is not None:
            callback(self, attaque, id_adversaire, self.interface.attributs_supplementaires)
