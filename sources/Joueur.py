from Carte import *
from Item  import Item

class Joueur:
    _CARTE_MAIN_PREMIERE_POS : Pos = Jeu.pourcentages_coordonees(24, 60)
    _CARTES_MAIN_ESPACEMENT  : Vecteur = Vecteur(30, 0)
    
    STATS_DE_BASE : Stat = Stat(45, 32, 37, 22, 32, 50, 1.3, 1).reset_vie()
    DIMENSIONS_SPRITE : tuple[int, int] = (200, 200)
    
    _nom_derniere_carte_piochee : str = ''
    
    
    def __init__(self, moveset : list[str]|tuple[str, ...], inventaire : list[Item] = []) -> None:
        self._stats           : Stat        = copy(Joueur.STATS_DE_BASE)
        self._pseudo          : str         = ""
        self._moveset         : list[str]   = list(moveset)
        self._inventaire      : list[Item]  = copy(inventaire)
        self._nombre_pieces   : int         = 0
        self._max_cartes_main : int         = 6
        self._cartes_main     : list[str] = []
        
        self.afficher : bool = True
        
        self._sprite : Surface = pygame.transform.scale(
            pygame.image.load(f"{Constantes.Chemins.IMG}/joueur.png"),
            Joueur.DIMENSIONS_SPRITE
        )
        
        self._id : int = premier_indice_libre_de_entites_vivantes()
        if self._id >= 0:
            globales.entites_vivantes[self._id] = self
            return
        
        self._id = len(globales.entites_vivantes)
        globales.entites_vivantes.append(self)
    
    def __del__(self):
        # Appelé quand l'objet est détruit (plus utilisé ou détruit avec del())
        if self._id > 0 and globales.entites_vivantes is not None:
            self.meurt()
    
    @property
    def _deck(self) -> list[Carte]:
        return [
            Carte(nom, Joueur._CARTE_MAIN_PREMIERE_POS + i * Joueur._CARTES_MAIN_ESPACEMENT)
            for i, nom in enumerate(self._moveset)
        ]
    
    @property
    def est_mort(self) -> bool:
        return self._stats.est_mort
    
    @property
    def pseudo(self) -> str:
        return self._pseudo
    @property
    def dbg_nom(self) -> str:
        return self.pseudo
    
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
    def nb_pieces(self) -> int:
        return self._nombre_pieces
    
    @property
    def inventaire(self) -> list[Item]:
        return copy(self._inventaire)
    
    @property
    def noms_cartes_deck(self) -> tuple[str, ...]:
        return tuple(self._moveset)
    
    @property
    def max_cartes_main(self) -> int:
        return self._max_cartes_main
    
    @property
    def longueur_barre_de_vie(self) -> int:
        ratio = max(0, self._stats.vie / self._stats.vie_max)
        return round(ratio * Constantes.UI_LONGUEUR_BARRE_DE_VIE)
    
    # propriété car la position pourrait changer suivant la position du ou des joueurs
    @property
    def pos_attaque(self) -> Pos:
        return Jeu.pourcentages_coordonees(16, 46)
    
    @property
    def pos_curseur(self) -> Pos:
        return Pos(0, 0)
    
    @pseudo.setter
    def pseudo(self, value : str) -> None:
        self._pseudo = value
    
    @max_cartes_main.setter
    def max_cartes_main(self, value : int) -> None:
        self.max_cartes_main = value
    
    # J'ai essayé de faire une fonction qui groupe les cartes par nom mais elle ne fonctionne pas
    # #def _inserer_carte_main(self, nom_carte : str) -> None:
    # #    assert(nom_carte in self._moveset), f"La carte \"{nom_carte}\" n'est pas dans le deck."
    # #    
    # #    print('\n')
    # #    if len(self._cartes_main) == 0:
    # #        self._cartes_main.append(Carte(
    # #            nom_carte,
    # #            Joueur._CARTE_POS
    # #        ))
    # #        return
    # #    
    # #    i : int     # On déclare i dans le scope de la fonction
    # #                # On peut faire sans en Python mais C mieux ainsi
    # #    for i, c in enumerate(self._cartes_main):
    # #        if nom_carte == c.nom:
    # #            break
    # #    i += 1
    # #    
    # #    print(i, self._cartes_main[i - 1].pos_defaut)
    # #    pos_carte = Joueur._CARTE_POS
    # #    if i - 1 >= 0:
    # #        pos_carte = self._cartes_main[i - 1].pos_defaut + Joueur._CARTE_ESPACEMENT
    # #    
    # #    for c in self._cartes_main[i:]:
    # #        c.decaler_pos_defaut(Joueur._CARTE_ESPACEMENT)
    # #    self._cartes_main.insert(i, Carte(nom_carte, pos_carte))
    # #
    # #    for c in self._cartes_main[:]:
    # #        print(c)
    
    def _get_carte_main(self, index : int) -> Carte:
        if not 0 <= index < len(self._cartes_main):
            raise IndexError(f"L'index {index} n'est pas dans main du joueur.")
        return Carte(self._cartes_main[index], Joueur._CARTE_MAIN_PREMIERE_POS + index * Joueur._CARTES_MAIN_ESPACEMENT)   # suite arithmétique j(°o°)l
    
    def recoit_degats(self, degats_recu : int) -> None:
        """Prend en charge les dégats prits et retourne si un crit est retourné."""
        # joueur_invincible n'empèche pas les soins
        if bool(params.joueur_invincible) and degats_recu >= 0:
            return
        
        self._stats.baisser_vie(degats_recu)
    
    def meurt(self) -> None:
        globales.entites_vivantes[self._id] = None
        self._id = -1
    
    
    def reset(self) -> None:
        self._stats.vie = self._stats.vie_max
        self._stats = copy(Joueur.STATS_DE_BASE)
        self._inventaire.clear()
    
    def attaquer(self, id_cible : int, index_carte : int) -> None:
        carte : Carte = self._get_carte_main(index_carte)
        if carte.peut_attaquer_lanceur:
            id_cible = self.id
        
        carte.enregister_lancement(self._id, id_cible)
        
        self._cartes_main.pop(index_carte)
        self.piocher()  # TODO: à enlever quand les tours serons réimplémentés
        
        carte.anim_nom = "jouer"
    
    def dessiner(self, surface : Surface) -> None:
        blit_centre(surface, self._sprite, Jeu.pourcentages_coordonees(13, 80, ret_pos=False))
    
    def dessine_barre_de_vie(self, surface : Surface, pos : Pos) -> None:
        dessiner_barre_de_vie(surface, pos, self._stats.vie / self._stats.vie_max, self.longueur_barre_de_vie)
    
    def dessiner_main(self, surface : Surface, de_dos : bool = False) -> None:
        for i, nom_carte in enumerate(self._cartes_main):
            self._get_carte_main(i).dessiner(surface, de_dos=de_dos)
    
    def piocher(self) -> None:
        if self.max_cartes_main <= 0:
            return
        
        while len(self._cartes_main) < self._max_cartes_main:
            choisi = random.choice(self._moveset)
            
            if choisi == self._nom_derniere_carte_piochee and len(self._moveset) > 1:
                continue    # repioche, on évite la surpioche de cartes de même type
            
            self._nom_derniere_carte_piochee = choisi
            self._cartes_main.append(choisi)
    
    def repiocher_tout(self) -> None:
        self._cartes_main.clear()
        self._nom_derniere_carte_piochee = ''
        
        self.piocher()
    
    def verifier_pour_attaquer(self, ev : pygame.event.Event) -> Optional[int]:
        """Verifie si le joueur veut attaquer."""
        if ev.type != pygame.MOUSEBUTTONDOWN:
            return None
        
        index_cliquee : Optional[int] = None
        
        # ordre inverse de celui de dessin
        # les cartes dessinées avant sont en dessous
        iteration_inversee = range(len(self._cartes_main)-1, -1, -1)    # I miss C-style loops
        for i in iteration_inversee:
            
            carte : Carte = self._get_carte_main(i) 
            if carte.souris_survole:
                index_cliquee = i
                break
        
        return index_cliquee
    
    def prendre_item(self, item : Item) -> None:
        """Ajoute un item à l'inventaire s'il n'y était pas déjà. Renvoie si l'item à été ajouté."""
        self._inventaire.append(item)
    def lacher_item(self, item : Item) -> bool:
        """Enlève un item à l'inventaire s'il y était. Renvoie si l'item à été enlevé."""
        if item in self._inventaire:
            self._inventaire.remove(item)
            self._stats.soustraire(item.stats_changees)
            return True
        return False
    
    def gagner_pieces(self, gagne : int) -> None:
        """Donne `gagne` pieces au joueur peu importe les options de triches."""
        self._nombre_pieces += gagne
        self._nombre_pieces = max(0, self._nombre_pieces)
        if gagne > 0:
            son_pieces = Sound(f"{Constantes.Chemins.SFX}/argent.wav")
            son_pieces.play()
    
    def paiement(self, prelevement : int, payer_max : bool = True) -> int:
        """
        `gagner_pieces()` mais enlève des pièces et respecte les paramètres de triches.
        Si `payer_max` est n'est pas actif, aucune piece ne sera enlevé au porte-monnaie du joueur s'il ne peut pas payer.
        Si le paramètre "argent infini" est actif, le joueur ne perd pas d'argent et la fonction renvoie 0.
        Renvoie Le nombre de pieces restantes à payer.
        """
        if params.argent_infini.case_cochee:
            return 0
        
        apres_payement : int = self._nombre_pieces - prelevement
        if apres_payement < 0 and not payer_max:
            return prelevement
        if apres_payement < 0:
            self._nombre_pieces = 0
            return -apres_payement
        
        self._nombre_pieces = apres_payement
        return 0
    
    def decrire(self) -> str:
        """Décrit l'objet dans une string."""
        return (
            f"ID d'entité: {self._id}\n"
            f"Statistiques: {self._stats}\n"
            f"Moveset: {self._moveset}\n"
            f"Inventaire: {[item.nom for item in self._inventaire]}\n"
            f"Argent: {self._nombre_pieces}\n"
        )


joueur : Joueur = Joueur([
    "Soin",
    "Torgnole",
    "Magie",
    "Skip",
])