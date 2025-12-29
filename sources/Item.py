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
    
    ORDONEE_SPRITE     : int = Jeu.pourcentage_hauteur(32)
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
    
    def __eq__(self, value : 'Item'):
        return self.id == value.id
    
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
                abscisses[i]        - Item.DIMENSIONS_SPRITES[0]//2,
                Item.ORDONEE_SPRITE - Item.DIMENSIONS_SPRITES[1]//2
            )
            hitbox = translation(item.sprite.get_bounding_rect(), decalage)
            
            if hitbox.collidepoint(pygame.mouse.get_pos()):
                return i
        return None
    
    def dessiner(self, surface : Surface, abscisses : int, centre : bool = True, afficher_avertissements : bool = True) -> None:
        LARGEUR_SPRITE : int = self.sprite.get_bounding_rect().width
        HAUTEUR_SPRITE : int = self.sprite.get_bounding_rect().height
        LARGEUR_EFFET  : int = LARGEUR_SPRITE + 50
        LARGEUR_DESC   : int = LARGEUR_SPRITE + 70
        
        nom  : Surface = Polices.TITRE.render(self.nom, True, NOIR)
        prix : Surface = Polices.TEXTE.render(f"{self.prix} pieces", True, JAUNE_PIECE)
        
        pos_sprite : tuple[int, int] = (abscisses, Item.ORDONEE_SPRITE)
        pos_nom    : tuple[int, int] = (abscisses, Jeu.pourcentage_hauteur(50))
        pos_prix   : tuple[int, int] = (
            abscisses + LARGEUR_SPRITE - prix.get_bounding_rect().width + 40,
            Item.ORDONEE_SPRITE - HAUTEUR_SPRITE // 2
        )
        rect_effet : tuple[int, int, int, int] = (
            abscisses, Jeu.pourcentage_hauteur(53),
            LARGEUR_EFFET, Jeu.pourcentage_hauteur(5)
        )
        rect_desc  : tuple[int, int, int, int] = (
            abscisses, Jeu.pourcentage_hauteur(60),
            LARGEUR_DESC, Jeu.pourcentage_hauteur(42)
        )
        
        texte_non_dessine_effet : str = ''
        texte_non_dessine_desc  : str = ''
        if centre:
            blit_centre(surface, self.sprite, pos_sprite)
            blit_centre(surface, nom, pos_nom)
            blit_centre(surface, prix, pos_prix)
            
            texte_non_dessine_effet += dessiner_texte(surface, self.effet_affiche, NOIR, centrer_pos(rect_effet, centrer_y=False), Polices.TEXTE)
            texte_non_dessine_desc += dessiner_texte(surface, self.description  , NOIR, centrer_pos(rect_desc , centrer_y=False), Polices.TEXTE)
        else:
            surface.blit(self.sprite, pos_sprite)
            surface.blit(nom, pos_nom)
            surface.blit(prix, pos_prix)
            
            texte_non_dessine_effet += dessiner_texte(surface, self.effet_affiche, NOIR, rect_effet, Polices.TEXTE)
            texte_non_dessine_desc += dessiner_texte(surface, self.description, NOIR, rect_desc, Polices.TEXTE)
        
        if afficher_avertissements and texte_non_dessine_effet != '':
            logging.debug(f"Le texte suivant n'a pas pu être dessiné (effet d'un  item trop long): {texte_non_dessine_effet}")
        if afficher_avertissements and texte_non_dessine_desc != '':
            logging.debug(f"Le texte suivant n'a pas pu être dessiné (description d'un  item trop longue): {texte_non_dessine_desc}")

Item.actualiser_items()