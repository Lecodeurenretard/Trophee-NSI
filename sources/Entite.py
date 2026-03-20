from Carte import *
from Item  import Item
from Pool  import Pool

@dataclass
class EntiteJSON:
    """La représentation d'une entite dans le JSON."""
    INDEX_EXEMPLE : int = field(init=False, default=0, repr=False)
    INDEX_JOUEUR  : int = field(init=False, default=1, repr=False)
    
    id             : int
    nom            : str
    sprite         : str
    nb_cartes_main : int
    deck           : Pool
    stats          : Stat
    
    DONNEES_TYPES : ClassVar[list[dict]] = []
    # ClassVar dit au décorateur que DONNEES_TYPE est statique
    
    def __init__(self, id_ou_nom : int|str, autoriser_exemple : bool = False):
        # Ensure data is loaded before proceeding
        if not EntiteJSON.DONNEES_TYPES:
            EntiteJSON.actualiser_donnees()
        
        if type(id_ou_nom) is str:
            id_ou_nom = EntiteJSON.chercher_nom(id_ou_nom)
        assert(type(id_ou_nom) is int), f"{type(id_ou_nom)}"
        
        if id_ou_nom == EntiteJSON.INDEX_EXEMPLE and not autoriser_exemple:
            raise ValueError("Le monstre d'exemple (id 0) est interdit.")
        donnees : dict = EntiteJSON.DONNEES_TYPES[id_ou_nom]
        
        self.id = id_ou_nom
        self.nom = donnees["nom"]
        
        self.sprite = valeur_par_defaut(
            donnees['sprite'],
            si_non_none=f"{Chemins.IMG}monstres/{donnees['sprite']}",
            si_none=f"{Chemins.IMG}erreur.png",
        )
        
        self.nb_cartes_main = donnees["nombre_cartes_main"]
        self.deck = Pool(donnees["moveset"])
        self.stats = Stat.depuis_dictionnaire_json(donnees["stats"]).reset_vie()
    
    @staticmethod
    def actualiser_donnees() -> None:
        """Actualise DONNEES_TYPES[]."""
        with open(f"{Chemins.JSON}TypesEntite.json", 'r', encoding='utf-8') as fichier:
            EntiteJSON.DONNEES_TYPES = json.load(fichier)
    
    @staticmethod
    def chercher_nom(nom : str) -> int:
        """Cherche un nom et renvoie sont id."""
        for i, dico in enumerate(EntiteJSON.DONNEES_TYPES):
            if nom == dico["nom"]:
                return i
        return -1
    
    @staticmethod
    def exemple() -> EntiteJSON:
        return EntiteJSON(EntiteJSON.INDEX_EXEMPLE)
    @staticmethod
    def joueur() -> EntiteJSON:
        return EntiteJSON(EntiteJSON.INDEX_JOUEUR)
        

class Entite(ABC):
    _CARTES_DE_DOS           : bool    = True           # à changer dans les classes filles
    _CARTE_MAIN_PREMIERE_POS : Pos     = Pos(0, 0)      # à changer dans les classes filles
    _CARTES_MAIN_ESPACEMENT  : Vecteur = Fenetre.pourcentages_fenetre(4, 0)
    _CARTES_MAIN_MAX_DU_MAX  : int     = 10             # Possible de changer dans les classes filles
    _DIFF_LARG_ET_BARRE_SPRITE : int = 100
    
    vivantes : ArrayStable['Entite'] = ArrayStable['Entite'](2)
    
    def __init__(
            self,
            donnees_json    : EntiteJSON,
            inventaire      : Sequence[Item] = [],
            _taille_sprite  : Optional[Vecteur] = None,
        ):
        
        self._nom                        : str         = donnees_json.nom
        self._stats                      : Stat        = donnees_json.stats
        self._cartes_main                : list[Carte] = []
        self._deck_rempli                : Pool        = deepcopy(donnees_json.deck)
        self._deck                       : Pool        = donnees_json.deck
        self._inventaire                 : list[Item]  = list(inventaire)
        self._nom_derniere_carte_piochee : str         = ''
        
        self._modifs_stats : dict[int, Stat] = {}
        
        max_cartes_main = donnees_json.nb_cartes_main
        assert(0 < max_cartes_main <= self.__class__._CARTES_MAIN_MAX_DU_MAX), f"Le maximum de cartes en main ({max_cartes_main}) doit être entre 0 (exclus) et {self.__class__._CARTES_MAIN_MAX_DU_MAX} (inclus)."
        self._cartes_main_max : int = max_cartes_main
        
        self._main_dans_ecran : bool = False
        self._SPRITE_TAILLE : Vecteur = valeur_par_defaut(
            _taille_sprite,
            si_none=Vecteur(Fenetre.pourcentage_largeur(20), Fenetre.pourcentage_largeur(20)),
        )
        self._LONGUEUR_BARRE_DE_VIE : int = int(self._SPRITE_TAILLE.x) - Entite._DIFF_LARG_ET_BARRE_SPRITE
        self._HAUTEUR_BARRE_DE_VIE  : int = 10
        
        chemin_sprite = valeur_par_defaut(donnees_json.sprite, si_none=f"{Chemins.IMG}erreur.png")
        self._sprite : Surface = pygame.transform.scale(pygame.image.load(chemin_sprite), self._SPRITE_TAILLE)
        self._id : int = Entite.vivantes.search(None)
        if self._id < 0:
            self._id = len(Entite.vivantes)
        
        Entite.vivantes[self._id] = self
    
    def __del__(self):
        # Appelé quand l'objet est détruit (quand nous ne pouvons plus accéder à l'objet)
        if (
            self._id > 0
            and Entite.vivantes is not None
        ):
            self.meurt()
    
    
    @staticmethod
    def tuer_les_entites_mortes() -> list['Entite']:
        """
        Appelle la méthode `.meurt()` sur les entites dont la propriété `.plus_de_vie` est True.
        Renvoie la liste des entités morts.
        """
        echafaud : list[Entite] = []   # Quand les entites seront enlevés de la liste, ils seront "exécutés" par le rammasse-miette
        for _, entite in Entite.vivantes.no_holes():
            if not entite.en_vie:
                entite.meurt()
                echafaud.append(entite)
        
        return echafaud
    
    @property
    def _cartes_main_noms(self) -> list[str]:
        return [c._nom for c in self._cartes_main]
    
    @property
    def _pos_barre_de_vie(self) -> Pos:
        barre_de_vie : Rect = Rect(0, 0, self._LONGUEUR_BARRE_DE_VIE, self._HAUTEUR_BARRE_DE_VIE)
        barre_de_vie.x = (
            self.pos_sprite.x
            + Entite._DIFF_LARG_ET_BARRE_SPRITE // 2
        )
        barre_de_vie.bottom = (
            self.pos_sprite.y
            + (self._sprite.get_bounding_rect().y)
            - Fenetre.pourcentage_hauteur(1)
        )
        
        return Pos(barre_de_vie.topleft)
    
    @property
    def en_vie(self) -> bool:
        return not self._stats.est_mort
    
    @property
    def nom(self) -> str:
        return self._nom
    
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def stats_totales(self) -> Stat:
        copie = copy(self._stats)
        
        # Ajoute les modifications de stats et les supprimme si elles sont obsolètes
        for tour_peremption, stats in copy(self._modifs_stats).items():
            if tour_peremption < Jeu.nb_tours_combat and tour_peremption != -1:
                del self._modifs_stats[tour_peremption]
            copie.additionner(stats)
        
        # Ajoute les modifications procurées par les objets
        for item in self._inventaire:
            copie.additionner(item.stats_changees)
        return copie
    
    @property
    def inventaire(self) -> list[Item]:
        return copy(self._inventaire)
    
    @property
    def cartes_deck_noms(self) -> tuple[str, ...]:
        return tuple(self._deck.noms)
    
    @property
    def cartes_main_max(self) -> int:
        return self._cartes_main_max
    
    @property
    def cartes_main_sont_a_pos_defaut(self) -> bool:
        if len(self._cartes_main) == 0:
            return True
        
        # on admet que si l'une est à la position par défaut
        # alors elles le sont toutes
        return self._cartes_main[0].est_a_pos_defaut
    
    @property
    def pos_sprite(self) -> Pos:
        return centrer_pos(self.pos_sprite_centree, self._SPRITE_TAILLE)
    
    @property
    @abstractmethod
    def pos_sprite_centree(self) -> Pos:
        pass
    
    @property
    def pos_attaque(self) -> Pos:
        return self.pos_sprite
    
    @nom.setter
    def nom(self, val : str) -> None:
        self._nom = val
    
    @cartes_main_max.setter
    def cartes_main_max(self, value : int) -> None:
        value = clamp(value, 0, self.__class__._CARTES_MAIN_MAX_DU_MAX)
        
        if value == 0:
            self._cartes_main.clear()
        if 0 < value < self.cartes_main_max:
            self._cartes_main = self._cartes_main[0:value-1]
        
        self._cartes_main_max = value
    
    
    def _calculer_pos_carte(self, index : int) -> Pos:
        return self.__class__._CARTE_MAIN_PREMIERE_POS + index * Entite._CARTES_MAIN_ESPACEMENT
    
    def _recalc_pos_cartes_main(self) -> None:
        for i, carte in enumerate(self._cartes_main):   # enumerate() garde la référence
            carte.pos_defaut = self._calculer_pos_carte(i)
    
    def _ajouter_carte_main(self, nom_carte : str, faire_revenir : bool = True) -> None:
        index = len(self._cartes_main)
        self._cartes_main.append(Carte(
            nom_carte,
            self._calculer_pos_carte(index),
            de_dos=self.__class__._CARTES_DE_DOS,
        ))
        
        carte_ajoutee = self._cartes_main[index]     # passée par référence
        carte_ajoutee.afficher()
        if faire_revenir:
            carte_ajoutee.anim_etat = CarteAnimEtat.REVENIR
        
        self._trier_main()
        self._recalc_pos_cartes_main()
    
    def _enlever_carte_main(self, index : int) -> Carte:
        assert(0 <= index < len(self._cartes_main)), f"L'index '{index}' ne correspond à aucune carte dans la main du joueur."
        
        enleve : Carte = self._cartes_main.pop(index)
        self._recalc_pos_cartes_main()
        # il y a maximum 10 cartes, c'est pas grave si
        # on recalcule des positions plusieurs fois
        
        return enleve
    
    def _vider_main(self) -> None:
        # itère à l'envers pour que les index restent cohérents
        for i in range(len(self._cartes_main) - 1, -1, -1):
            self._cartes_main.pop(i).cacher()
    
    def _trier_main(self) -> None:
        # trie les cartes par ordre alphabetique
        self._cartes_main = sorted(self._cartes_main, key=lambda c: c._nom)
    
    def _reset_deck(self) -> None:
        self._deck = deepcopy(self._deck_rempli)
    
    def _modifs_stats_garantie_clef(self, clef : int) -> None:
        """S'assure que la clef `clef` existe dans `.modifs_stats[]`."""
        if clef not in self._modifs_stats .keys():
            self._modifs_stats[clef] = Stat.remplies_de(0)
    
    def _dessiner_barre_de_vie(self, num_couche : int) -> None:
        ratio_vie = self._stats.vie / self._stats.vie_max
        
        couleur_remplissage : rgb = VERT
        if ratio_vie <= .2:
            couleur_remplissage = ROUGE
        elif ratio_vie <= .5:
            couleur_remplissage = JAUNE
        elif ratio_vie == 1:
            couleur_remplissage = TURQUOISE
        
        dim_remplissage : tuple[int, int] = (int(ratio_vie * self._LONGUEUR_BARRE_DE_VIE), self._HAUTEUR_BARRE_DE_VIE)
        dim_bords       : tuple[int, int] = (                self._LONGUEUR_BARRE_DE_VIE , self._HAUTEUR_BARRE_DE_VIE)
        dessiner_rect(  # remplissage
            num_couche,
            self._pos_barre_de_vie,
            dim_remplissage,
            couleur_remplissage=couleur_remplissage,
            epaisseur_trait=0,
        )
        dessiner_rect(  # bords
            num_couche,
            self._pos_barre_de_vie,
            dim_bords,
            couleur_bords=NOIR,
            epaisseur_trait=2,
            dessiner_interieur=False,
        )
    
    def meurt(self) -> None:
        del Entite.vivantes[self._id]
        self._id = -1
    
    def recoit_degats(self, degats_recu : int, attaque_cause : Attaque) -> None:
        self._stats.baisser_vie(degats_recu)
    
    def reset(self) -> None:
        self._stats.reset_vie()
        self._modifs_stats = {}
        self._inventaire.clear()
        self._vider_main()
        self._reset_deck()
    
    def attaquer(self, id_cible : int, index_carte : int) -> None:
        """Enregistre le lancement de l'attaque."""
        assert(0 <= id_cible < len(Entite.vivantes)), "ID de la cible invalide."
        assert(0 <= index_carte < len(self._cartes_main)), f"Index invalide."
        
        carte : Carte = self._cartes_main[index_carte]
        if carte.peut_attaquer_lanceur:
            id_cible = self.id
        
        self._enlever_carte_main(index_carte)
        
        carte.anim_etat = CarteAnimEtat.JOUER
        carte.enregister_lancement(self._id, id_cible)
    
    def dessiner(self, num_couche : int) -> None:
        Fenetre.blit_couche(num_couche, self._sprite, self.pos_sprite.tuple)
    
    def dessiner_UI(self, num_couche : int) -> None:
        self._dessiner_barre_de_vie(num_couche)
        Fenetre.blit_couche(
            num_couche,
            Fenetre.construire_police(Polices.TITRE, 7).render(self.nom, True, NOIR),
            (self._pos_barre_de_vie - Vecteur(1, 30)).tuple
        )
    
    def piocher(self) -> None:
        """Pioche jusqu'à remplir la main."""
        if self._cartes_main_max <= 0:
            return
        
        def filtre(nom : str) -> bool:
            if len(self._deck_rempli) <= 1:
                return True
            res = (nom != self._nom_derniere_carte_piochee)
            self._nom_derniere_carte_piochee = nom
            return res
        
        noms_cartes = []
        try:
            noms_cartes = self._deck.tirer_n(
                self._cartes_main_max - len(self._cartes_main),
                filtre=filtre,
            )
        except IndexError:   # plus aucune de cartes
            noms_cartes = self._deck.vider()
            self._reset_deck()
            self.piocher()
        
        # Sécurité
        if len(self._cartes_main) + len(noms_cartes) > self.cartes_main_max:
            noms_cartes = noms_cartes[0:self.cartes_main_max- len(self._cartes_main)]
        
        for nom in noms_cartes:
            self._ajouter_carte_main(nom)
    
    def piocher_si_main_vide(self) -> None:
        if len(self._cartes_main) == 0:
            self.piocher()
    
    def repiocher_tout(self) -> None:
        """Vide la main puis la reremplit."""
        self._vider_main()
        self._nom_derniere_carte_piochee = ''
        
        self.piocher()
    
    def main_entrer(self) -> None:
        self._main_dans_ecran = True
        for c in self._cartes_main:
            c.anim_etat = CarteAnimEtat.REVENIR
    
    def main_sortir(self) -> None:
        self._main_dans_ecran = False
        for c in self._cartes_main:
            c.anim_etat = CarteAnimEtat.PARTIR
    
    def prendre_item(self, item : Item) -> None:
        """Ajoute un item à l'inventaire s'il n'y était pas déjà."""
        self._inventaire.append(item)
    
    def lacher_item(self, item : Item) -> bool:
        """Enlève un item à l'inventaire s'il y était. Renvoie si l'item à été enlevé."""
        if item in self._inventaire:
            self._inventaire.remove(item)
            return True
        return False
    
    def decrire_stats(self) -> str:
        """Renvoie une descriptions des cararistiques de l'instance de l'objet dans une string."""
        return (
            f"ID d'entité: {self._id}\n"
            f"Statistiques: {self._stats}\n"
            f"Statistiques effectives: {self.stats_totales}\n"
            f"Deck: {self._deck}\n"
            f"Main: {self._cartes_main_noms}\n"
            f"Inventaire: {[item.nom for item in self._inventaire]}\n"
        )
    
    def ajouter_modif_stats(self, stat : Stat, valide_pendant : int) -> None:
        """Ajoute une modification de stats valable pendant `valide_pendant` tours."""
        tour = Jeu.nb_tours_combat + valide_pendant
        if valide_pendant == -1:
            tour = -1
        
        self._modifs_stats_garantie_clef(tour)
        self._modifs_stats[tour].additionner(stat)
    
    def nouveau_tour(self) -> None:
        pass
    
    def nouveau_combat(self) -> None:
        self._modifs_stats = {}
        self.repiocher_tout()


Attaque.set_arr_entites(Entite.vivantes) # grâce au passage par référence ça marche
                                         # C'est un hack, certes, mais j'ai pas trouvé mieux