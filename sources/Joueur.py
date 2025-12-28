from Entite import *

class Joueur(Entite):
    _CARTES_DE_DOS           : bool = False
    _CARTE_MAIN_PREMIERE_POS : Pos  = Jeu.pourcentages_coordonees(24, 60)
    _POS_BARRE_VIE           : Pos  = Pos(500, 400)
    
    STATS_DE_BASE : Stat = Stat(45, 32, 37, 22, 32, 50, 1.3, 1).reset_vie()
    DIMENSIONS_SPRITE : tuple[int, int] = (200, 200)
    
    _nom_derniere_carte_piochee : str = ''
    
    
    @override
    def __init__(self, deck : Sequence[str], inventaire : list[Item] = []) -> None:
        super().__init__(
            "",
            Joueur.STATS_DE_BASE,
            deck,
            6,
            f"{Chemins.IMG}/joueur.png",
            inventaire
        )
        self._nombre_pieces : int = 0
    
    
    @property
    def nb_pieces(self) -> int:
        return self._nombre_pieces
    
    @property
    def pos_sprite(self) -> Pos:   # on ne met pas de @override car le membre est abstrait (pur)
        return Jeu.pourcentages_coordonees(13, 80)
    
    @property
    def pos_attaque(self) -> Pos:
        return Jeu.pourcentages_coordonees(16, 46)
    
    
    @override
    def recoit_degats(self, degats_recu : int) -> None:
        """Prend en charge les dégats prits et retourne si un crit est retourné."""
        # joueur_invincible n'empèche pas les soins
        if bool(params.joueur_invincible) and degats_recu >= 0:
            return
        
        Entite.recoit_degats(self, degats_recu)
    
    @override
    def reset(self) -> None:
        Entite.reset(self)
        self._stats = copy(Joueur.STATS_DE_BASE)
    
    def verifier_pour_attaquer(self, ev : pygame.event.Event) -> Optional[int]:
        """Verifie si le joueur veut attaquer."""
        if ev.type != pygame.MOUSEBUTTONDOWN:
            return None
        
        index_cliquee : Optional[int] = None
        
        # ordre inverse de celui de dessin
        # les cartes dessinées avant sont en dessous
        iteration_inversee = range(len(self._cartes_main)-1, -1, -1)    # I miss C-style loops
        for i in iteration_inversee:
            
            carte : Carte = self._cartes_main[i]
            if carte.souris_survole:
                index_cliquee = i
                break
        
        return index_cliquee
    
    def gagner_pieces(self, gagne : int) -> None:
        """Donne `gagne` pieces au joueur peu importe les options de triches."""
        self._nombre_pieces += gagne
        self._nombre_pieces = max(0, self._nombre_pieces)
        if gagne > 0:
            son_pieces = Sound(f"{Chemins.SFX}/argent.wav")
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
    
    def decrire_stats(self) -> str:
        return (
            Entite.decrire_stats(self)
            + f"Argent: {self._nombre_pieces}\n"
        )


joueur : Joueur = Joueur([
    "Soin",
    "Torgnole",
    "Magie",
    "Skip",
])