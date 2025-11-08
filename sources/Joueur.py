from Attaque import *
from Item import Item

class Joueur:
    STATS_DE_BASE : Stat = Stat(45, 37, 37, 22, 32, 50, 1.3, 1).reset_vie()
    DIMENSIONS_SPRITE : tuple[int, int] = (160, 160)
    
    def __init__(self, moveset : list[str]|tuple[str, ...], chemin_vers_sprite : Optional[str] = None, inventaire : list[Item] = []) -> None:
        self._stats   : Stat             = copy(Joueur.STATS_DE_BASE)
        self._pseudo  : str              = ""
        self._moveset : list[str]        = list(moveset)
        self._inventaire    : list[Item] = copy(inventaire)
        self._nombre_pieces : int        = 0
        
        self.afficher : bool = True
        
        if chemin_vers_sprite is None:
            chemin_vers_sprite = f"{Constantes.Chemins.IMG}/erreur.png"
        
        self._sprite : Surface = pygame.transform.scale(
            pygame.image.load(chemin_vers_sprite),
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
    def stats(self) -> Stat:
        return copy(self._stats)
    
    @property
    def nb_pieces(self) -> int:
        return self._nombre_pieces
    
    @property
    def inventaire(self) -> list[Item]:
        return copy(self._inventaire)
    
    @property
    def noms_attaques(self) -> tuple[str, ...]:
        return tuple(self._moveset)
    
    @property
    def longueur_barre_de_vie(self) -> int:
        ratio = max(0, self._stats.vie / self._stats.vie_max)
        return round(ratio * Constantes.UI_LONGUEUR_BARRE_DE_VIE)
    
    # propriété car la position pourrait changer suivant la position du ou des joueurs
    @property
    def pos_attaque(self) -> Pos:
        return Pos(Jeu.largeur // 4, Jeu.pourcentage_hauteur(60))
    
    @property
    def pos_curseur(self) -> Pos:
        return Pos(0, 0)
    
    @pseudo.setter
    def pseudo(self, value : str) -> None:
        self._pseudo = value
    
    
    def recoit_degats(self, degats_recu : int) -> None:
        """Prend en charge les dégats prits et retourne si un crit est retourné."""
        if bool(params.joueur_invincible) and degats_recu >= 0:   # joueur_invincible n'empèche pas les soins
            return
        
        self._stats.baisser_vie(degats_recu)
    
    def meurt(self) -> None:
        globales.entites_vivantes[self._id] = None
        self._id = -1
    
    def get_attaque_surface(self, nom_attaque : str) -> Surface:
        if nom_attaque not in self.noms_attaques:
            raise ValueError(f"Le nom {nom_attaque} n'est pas dans `_moveset[]`.")
        
        return Attaque.avec_nom(nom_attaque).nom_surface
    
    def attaque_peut_toucher_lanceur(self, nom_attaque : str) -> bool:
        if nom_attaque not in self.noms_attaques:
            raise ValueError(f"Le nom {nom_attaque} n'est pas dans `_moveset[]`.")
        
        return Attaque.avec_nom(nom_attaque).peut_attaquer_lanceur
    
    def attaque_peut_toucher_ennemis(self, nom_attaque : str) -> bool:
        if nom_attaque not in self.noms_attaques:
            raise ValueError(f"Le nom {nom_attaque} n'est pas dans `_moveset[]`.")
        
        return Attaque.avec_nom(nom_attaque).peut_attaquer_adversaires
    
    def reset(self) -> None:
        self._stats.vie = self._stats.vie_max
        self._stats = copy(Joueur.STATS_DE_BASE)
    
    def attaquer(self, id_cible : int, nom_attaque : str) -> None:
        if nom_attaque not in self.noms_attaques:
            raise ValueError(f"Le nom {nom_attaque} n'est pas dans `_moveset[]`.")
        
        if self.attaque_peut_toucher_lanceur(nom_attaque):
            id_cible = self.id
        
        Attaque.avec_nom(nom_attaque).enregister_lancement(self._id, id_cible)
    
    def dessiner(self, surface : Surface) -> None:
        blit_centre(surface, self._sprite, (Jeu.largeur // 4, Jeu.pourcentage_hauteur(60)))
    
    def dessine_barre_de_vie(self, surface : Surface, pos_x : int, pos_y : int) -> None:
        dessiner_barre_de_vie(surface, pos_x, pos_y, self._stats.vie / self._stats.vie_max, self.longueur_barre_de_vie)
    
    
    def dessine_prochaine_frame(self, surface : Surface) -> None:
        if not self.afficher:
            return
        self.dessiner(surface)
    
    def dessine_prochaine_frame_UI(self, surface : Surface) -> None:
        self.dessine_barre_de_vie(surface, Jeu.pourcentage_largeur(70), Jeu.pourcentage_hauteur(65))
    
    def prendre_item(self, item : Item) -> bool:
        """Ajoute un item à l'inventaire s'il n'y était pas déjà. Renvoie si l'item à été ajouté."""
        if item not in self._inventaire:
            self._inventaire.append(item)
            self._stats.additionner(item.stats_changees)
            return True
        return False
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
            f"ID d'entité: {self._id}\n"
            f"Argent récolté: {self._nombre_pieces}\n"
        )


joueur : Joueur = Joueur([
    "Soin",
    "Torgnole",
    "Magie",
    "Skip",
], chemin_vers_sprite=f"{Constantes.Chemins.IMG}/joueur.png")