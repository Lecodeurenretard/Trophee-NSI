from import_local import *

@dataclass
class Item:
    """Un item parsé de items.json."""
    DONNEES_ITEMS   : list[dict] = field(repr=False)
    
    nom            : str
    description    : str
    sprite         : Surface
    prix           : int
    effet_affiche  : str
    stats_changees : Stat
    
    ORDONEE_SPRITE     : int = Jeu.pourcentage_hauteur(10)
    DIMENSIONS_SPRITES : tuple[int, int] = (350, 350)
    
    
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
        
        chemin : str = f"{Chemins.IMG}/"
        chemin += valeur_par_defaut(
            item['sprite'],
            si_non_none=f"items/{item['sprite']}",
            si_none="erreur.png"
        )
        self.sprite      = pygame.image.load(chemin)
        self.sprite      = pygame.transform.scale(self.sprite, self.DIMENSIONS_SPRITES)
        
        self.prix        = valeur_par_defaut(item["prix"], 0)
        
        self.effet_affiche  = item["effets"]["message utilisateur"]
        self.stats_changees = Stat.depuis_dictionnaire_json(item["effets"]["stats"], valeur_par_defaut=0)
        # .stats_changees sera ajouté/enlevé aux stats correspondantes du joueur.
    
    def __str__(self):
        return self.nom
    
    def __eq__(self, obj : object):
        assert(type(obj) is Item), "On ne peut comparer un item qu'avec un autre item."
        return self.id == obj.id
    
    @staticmethod
    def actualiser_items() -> None:
        """Ouvre item.json et prend tous les objets trouvés."""
        with open(f"{Chemins.DATA}/items.json", 'r', encoding='utf-8') as fichier:
            Item.DONNEES_ITEMS = json.load(fichier)
    
    @staticmethod
    def depuis_nom(nom_item : str) -> 'Item':
        """Initialise un objet Item avec les attributs de l'objet ayant le même nom dans le JSON."""
        for id, item in enumerate(Item.DONNEES_ITEMS):
            if nom_item == item["nom"]:
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
    
    def dessiner(self, surface : Surface, abscisses : int, afficher_avertissements : bool = True) -> None:
        HAUTEUR_POLICE_PC : int = 7
        RECT_GLOBAL : Rect = Rect(
            abscisses - self.DIMENSIONS_SPRITES[0] // 2,
            0,
            self.DIMENSIONS_SPRITES[0],
            Jeu.hauteur,
        )
        
        nom  : Surface = Jeu.construire_police(Polices.TITRE, 12).render(self.nom, True, NOIR)
        prix : Surface = Jeu.construire_police(Polices.TEXTE, 10).render(f"{self.prix} pieces", True, JAUNE_PIECE)
        
        rect_sprite : Rect = Rect(
            (abscisses, Item.ORDONEE_SPRITE),
            self.sprite.get_rect().size,
        )
        rect_nom    : Rect = Rect(
            (abscisses, rect_sprite.bottom),
           nom.size,
        )
        pos_prix   : Pos = Pos(
            abscisses + rect_sprite.width // 2 + Jeu.pourcentage_largeur(1),
            rect_sprite.y,
        )
        rect_effet : Rect = Rect(
            abscisses,
            rect_nom.bottom + Jeu.pourcentage_hauteur(2),
            rect_sprite.width,
            Jeu.pourcentage_hauteur(HAUTEUR_POLICE_PC)
        )
        rect_desc  : Rect = Rect(
            abscisses,
            rect_effet.bottom + Jeu.pourcentage_hauteur(4),
            rect_sprite.width,
            Jeu.pourcentage_hauteur(42)
        )
        
        police = Jeu.construire_police(Polices.TEXTE, HAUTEUR_POLICE_PC)
        
        blit_centre_rect(surface, self.sprite, RECT_GLOBAL, centre_rect_y=False, pos=Pos(-1, rect_sprite.centery))
        blit_centre_rect(surface, nom        , RECT_GLOBAL, centre_rect_y=False, pos=Pos(-1, rect_nom.centery))
        blit_centre(surface, prix, pos_prix.tuple)
        
        rect_effet.centerx = RECT_GLOBAL.centerx
        rect_desc.centerx  = RECT_GLOBAL.centerx
        
        texte_non_dessine_effet = dessiner_texte(surface, self.effet_affiche, NOIR, rect_to_tuple(rect_effet), police)
        texte_non_dessine_desc  = dessiner_texte(surface, self.description  , NOIR, rect_to_tuple(rect_desc), police)
        
        if afficher_avertissements and texte_non_dessine_effet != '':
            logging.debug(f"Le texte suivant n'a pas pu être dessiné (effet d'un  item trop long): {texte_non_dessine_effet}")
        if afficher_avertissements and texte_non_dessine_desc != '':
            logging.debug(f"Le texte suivant n'a pas pu être dessiné (description d'un  item trop longue): {texte_non_dessine_desc}")

Item.actualiser_items()