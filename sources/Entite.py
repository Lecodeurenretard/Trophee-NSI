from Carte import *
from Item  import Item

class Entite(ABC):
    _CARTES_DE_DOS           : bool    = True           # à changer dans les classes filles
    _CARTE_MAIN_PREMIERE_POS : Pos     = Pos(0, 0)      # à changer dans les classes filles
    _CARTES_MAIN_ESPACEMENT  : Vecteur = Jeu.pourcentages_fenetre(4, 0)
    _CARTES_MAIN_MAX_DU_MAX  : int     = 10
    
    _SPRITE_DIM : tuple[int, int] = (400, 400)
    
    _LONGUEUR_BARRE_DE_VIE : int = _SPRITE_DIM[0] - 100
    _HAUTEUR_BARRE_DE_VIE  : int = 10
    
    vivantes : dict[int, 'Entite'] = {}
    
    def __init__(
            self,
            nom             : str,
            stats           : Stat,
            deck            : Sequence[str],
            max_cartes_main : int,
            chemin_sprite   : Optional[str]  = None,
            inventaire      : Sequence[Item] = [],
        ):
        
        self._nom                        : str         = nom
        self._stats                      : Stat        = stats
        self._cartes_main                : list[Carte] = []
        self._deck                       : list[str]   = list(deck)
        self._inventaire                 : list[Item]  = list(inventaire)
        self._nom_derniere_carte_piochee : str         = ''
        
        assert(0 < max_cartes_main <= self.__class__._CARTES_MAIN_MAX_DU_MAX), f"Le maximum de cartes en main ({max_cartes_main}) doit être entre 0 (exclus) et {self.__class__._CARTES_MAIN_MAX_DU_MAX} (inclus)."
        self._cartes_main_max : int = max_cartes_main
        
        chemin_sprite = valeur_par_defaut(chemin_sprite, si_none=f"{Chemins.IMG}/erreur.png")
        self._sprite : Surface = pygame.transform.scale(pygame.image.load(chemin_sprite), Entite._SPRITE_DIM)
        
        # Ajoute l'entite à la liste
        self._id : int = premier_indice_libre(Entite.vivantes)
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
        for entite in list(Entite.vivantes.values()):
            if not entite.en_vie:
                entite.meurt()
                echafaud.append(entite)
        
        return echafaud
    
    
    @property
    def _cartes_deck(self) -> list[Carte]:
        return [
            Carte(nom, self._calculer_pos_carte(i), de_dos=self.__class__._CARTES_DE_DOS)
            for i, nom in enumerate(self._deck)
        ]
    
    @property
    def _cartes_main_noms(self) -> list[str]:
        return [c._nom for c in self._cartes_main]
    
    @property
    def _pos_barre_de_vie(self) -> Pos:
        return self.pos_sprite - Vecteur(self._SPRITE_DIM) / 2 - Vecteur(0, 20)
    
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
        for item in self._inventaire:
            copie.additionner(item.stats_changees)
        return copie
    
    @property
    def inventaire(self) -> list[Item]:
        return copy(self._inventaire)
    
    @property
    def cartes_deck_noms(self) -> tuple[str, ...]:
        return tuple(self._deck)
    
    @property
    def cartes_main_max(self) -> int:
        return self._cartes_main_max
    
    # propriété car la position pourrait changer suivant la position du ou des joueurs
    @property
    @abstractmethod
    def pos_sprite(self) -> Pos:
        pass
    
    @property
    @abstractmethod
    def pos_attaque(self) -> Pos:
        pass
    
    @nom.setter
    def nom(self, val : str) -> None:
        self._nom = val
    
    @cartes_main_max.setter
    def cartes_main_max(self, value : int) -> None:
        self._cartes_main_max = clamp(value, 0, Entite._CARTES_MAIN_MAX_DU_MAX)
    
    
    def _calculer_pos_carte(self, index : int) -> Pos:
        return self.__class__._CARTE_MAIN_PREMIERE_POS + index * Entite._CARTES_MAIN_ESPACEMENT
    
    def _recalc_pos_cartes_main(self) -> None:
        for i, carte in enumerate(self._cartes_main):   # enumerate() garde la référence
            carte.pos_defaut = self._calculer_pos_carte(i)
    
    def _inserer_carte_main(self, nom_carte : str) -> None:
        index = len(self._cartes_main)
        self._cartes_main.append(Carte(
            nom_carte,
            self._calculer_pos_carte(index),
            de_dos=self.__class__._CARTES_DE_DOS,
        ))
        self._cartes_main[index].afficher(Jeu.fenetre)
        
        self._trier_main()
        self._recalc_pos_cartes_main()
    
    def _enlever_carte_main(self, index : int) -> Carte:
        assert(0 <= index < len(self._cartes_main)), f"L'index '{index}' ne correspond a aucune carte dans la main du joueur."
        
        enleve : Carte = self._cartes_main.pop(index)
        self._recalc_pos_cartes_main()
        # il y a maximum 10 cartes, c'est pas grave si
        # on recalcule des positions plusieurs fois
        
        return enleve
    
    def _trier_main(self) -> None:
        # trie les cartes par ordre alphabetiques
        self._cartes_main = sorted(self._cartes_main, key=lambda c: c._nom)
    
    def meurt(self) -> None:
        del Entite.vivantes[self._id]
        self._id = -1
    
    def recoit_degats(self, degats_recu : int) -> None:
        self._stats.baisser_vie(degats_recu)
    
    def reset(self) -> None:
        self._stats.reset_vie()
        self._inventaire.clear()
        self._cartes_main.clear()
    
    def attaquer(self, id_cible : int, index_carte : int) -> None:
        """Enregistre le lancement de l'attaque."""
        assert(id_cible in Entite.vivantes.keys()), "ID de la cible invalide."
        assert(0 <= index_carte < len(self._cartes_main)), f"Index invalide."
        
        carte : Carte = self._cartes_main[index_carte]
        if carte.peut_attaquer_lanceur:
            id_cible = self.id
        
        self._enlever_carte_main(index_carte)
        if len(self._cartes_main) == 0:
            self.piocher()
        
        carte.enregister_lancement(self._id, id_cible)
        carte.anim_nom = "jouer"
    
    def dessiner(self, surface : Surface) -> None:
        blit_centre(surface, self._sprite, self.pos_sprite.tuple)
    
    def dessiner_barre_de_vie(self, surface : Surface) -> None:
        ratio_vie = self._stats.vie / self._stats.vie_max
        
        couleur_remplissage : rgb = VERT
        if ratio_vie <= .2:
            couleur_remplissage = ROUGE
        elif ratio_vie <= .5:
            couleur_remplissage = JAUNE
        elif ratio_vie == 1:
            couleur_remplissage = CYAN
        if bool(params.mode_debug):
            couleur_remplissage = GRIS
        
        dim_remplissage : tuple[int, int] = (int(ratio_vie * Entite._LONGUEUR_BARRE_DE_VIE), Entite._HAUTEUR_BARRE_DE_VIE)
        dim_bords       : tuple[int, int] = (                Entite._LONGUEUR_BARRE_DE_VIE , Entite._HAUTEUR_BARRE_DE_VIE)
        dessiner_rect(  # remplissage
            surface,
            self._pos_barre_de_vie,
            dim_remplissage,
            couleur_remplissage=couleur_remplissage,
            epaisseur_trait=0,
        )
        dessiner_rect(  # bords
            surface,
            self._pos_barre_de_vie,
            dim_bords,
            couleur_bords=NOIR,
            epaisseur_trait=2,
            dessiner_interieur=False,
        )
    
    def dessiner_UI(self, surface : Surface) -> None:
        self.dessiner_barre_de_vie(surface)
        Jeu.menus_surf.blit(
            Polices.TITRE.render(self.nom, True, NOIR),
            (self._pos_barre_de_vie - Vecteur(1, 30)).tuple
        )
    
    def piocher(self) -> None:
        if self.cartes_main_max <= 0:
            return
        
        while len(self._cartes_main) < self._cartes_main_max:
            choisi = random.choice(self._deck)
            
            if choisi == self._nom_derniere_carte_piochee and len(self._deck) > 1:
                continue    # repioche, on évite la surpioche de cartes de même type
            
            self._nom_derniere_carte_piochee = choisi
            self._inserer_carte_main(choisi)
    
    def repiocher_tout(self) -> None:
        self._cartes_main.clear()
        self._nom_derniere_carte_piochee = ''
        
        self.piocher()
    
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
            f"Deck: {self._deck}\n"
            f"Main: {self._cartes_main_noms}\n"
            f"Inventaire: {[item.nom for item in self._inventaire]}\n"
        )

Attaque.set_dico_entites(Entite.vivantes) # grâce au passage par référence ça marche
                                          # C'est un hack, certes, mais j'ai pas trouvé mieux