from import_local import *

@dataclass
class Item:
    """Un item parsé de items.json."""
    TOUT_LES_ITEMS   : list[dict] = field(repr=False)
    
    nom            : str
    description    : str
    sprite         : Surface
    prix           : int
    effet_affiche  : str
    stats_changees : Stat
    
    ORDONEE_SPRITE     : int = Jeu.pourcentage_hauteur(32)
    DIMENSIONS_SPRITES : tuple[int, int] = (200, 200)
    
    
    def __init__(self, id : int, permissif : bool = False, interdire_0 : bool = True):
        """Si `permissif` est actif, corrige l'id."""
        if permissif:
            id = max(1, id) if interdire_0 else max(0, id)
            id = min(len(Item.TOUT_LES_ITEMS)-1, id)
        elif not (0 <= id < len(Item.TOUT_LES_ITEMS)):
            raise OverflowError("id soit négatif, soit trop grand.")
        elif interdire_0 and id == 0:
            raise ValueError("L'item d'indice 0 (l'exemple) n'est pas autorisé par défaut par le constructeur de Item.")
        
        item : dict = Item.TOUT_LES_ITEMS[id]
        
        self.id          = id
        self.nom         = item["nom"]
        self.description = item["description"]
        self.sprite      = pygame.image.load(f"{Constantes.Chemins.IMG}/items/{item["sprite"]}")
        self.sprite      = pygame.transform.scale(self.sprite, self.DIMENSIONS_SPRITES)
        self.prix        = item["prix"] if item["prix"] is not None else 0
        
        self.effet_affiche  = item["effets"]["message utilisateur"]
        self.stats_changees = Stat.depuis_dictionnaire_json(item["effets"]["stats"], valeur_par_defaut=0)   # sera ajouté/enlevé aux stats correspondantes du joueur.
    
    def __str__(self):
        return self.nom
    
    def __eq__(self, value : 'Item'):
        return self.id == value.id
    
    @staticmethod
    def actualiser_items() -> None:
        """Ouvre item.json et prend tous les objets trouvés."""
        with open(f"{Constantes.Chemins.DATA}/items.json", 'r', encoding='utf-8') as fichier:
            Item.TOUT_LES_ITEMS = json.load(fichier)
            fichier.seek(0)
    
    @staticmethod
    def depuis_nom(nom_item : str) -> 'Item':
        """Initialise un objet Item avec les attributs de l'objet ayant le même nom dans le JSON."""
        for id, item in enumerate(Item.TOUT_LES_ITEMS):
            if nom_item == item["nom"]:
                return Item(id)
        raise ValueError(f"Le nom \"{nom_item}\" n'a pas été trouvé.")
    
    @staticmethod
    def item_aleatoire() -> 'Item':
        return Item(random.randint(1, len(Item.TOUT_LES_ITEMS) - 1))
    @staticmethod
    def generateur_items() -> 'Generator[Item, None, None]':
        while True:
            try:
                yield Item.item_aleatoire()
            except GeneratorExit:
                break
    
    @staticmethod
    def item_survole(liste_item : 'list[Item]|tuple[Item, ...]', abscisses : list[int]|tuple[int, ...]) -> Optional[int]:
        """Renvoie l'index de l'item survolé ou None si aucun ne l'est."""
        for i, item in enumerate(liste_item):
            decalage = Vecteur(
                abscisses[i]        - Item.DIMENSIONS_SPRITES[0]//2,
                Item.ORDONEE_SPRITE - Item.DIMENSIONS_SPRITES[1]//2
            )
            hitbox = translation(item.sprite.get_bounding_rect(), decalage)
            
            if hitbox.collidepoint(pygame.mouse.get_pos()):
                return i
        return None
    
    def dessiner(self, surface : Surface, abscisses : int, centre : bool = True) -> None:
        LARGEUR_SPRITE : int = self.sprite.get_bounding_rect().width
        HAUTEUR_SPRITE : int = self.sprite.get_bounding_rect().height
        
        nom  : Surface = Constantes.Polices.TITRE.render(self.nom, True, NOIR)
        prix : Surface = Constantes.Polices.TEXTE.render(f"{self.prix} pieces", True, JAUNE_PIECE)
        
        pos_sprite : tuple[int, int] = (abscisses, Item.ORDONEE_SPRITE)
        pos_nom    : tuple[int, int] = (abscisses, Jeu.pourcentage_hauteur(50))
        pos_prix   : tuple[int, int] = (
            abscisses + LARGEUR_SPRITE - prix.get_bounding_rect().width + 25,
            Item.ORDONEE_SPRITE - HAUTEUR_SPRITE // 2
        )
        rect_effet : tuple[int, int, int, int] = (
            abscisses, Jeu.pourcentage_hauteur(53),
            LARGEUR_SPRITE, Jeu.pourcentage_hauteur(5)
        )
        rect_desc  : tuple[int, int, int, int] = (
            abscisses, Jeu.pourcentage_hauteur(60),
            LARGEUR_SPRITE, Jeu.pourcentage_hauteur(40)
        )
        
        if centre:
            blit_centre(surface, self.sprite, pos_sprite)
            blit_centre(surface, nom, pos_nom)
            blit_centre(surface, prix, pos_prix)
            
            dessiner_texte(surface, self.effet_affiche, NOIR, centrer_pos(rect_effet, centrer_y=False), Constantes.Polices.TEXTE)
            dessiner_texte(surface, self.description  , NOIR, centrer_pos(rect_desc , centrer_y=False), Constantes.Polices.TEXTE)
        else:
            surface.blit(self.sprite, pos_sprite)
            surface.blit(nom, pos_nom)
            surface.blit(prix, pos_prix)
            
            dessiner_texte(surface, self.effet_affiche, NOIR, rect_effet, Constantes.Polices.TEXTE)
            dessiner_texte(surface, self.description, NOIR, rect_desc, Constantes.Polices.TEXTE)

Item.actualiser_items()