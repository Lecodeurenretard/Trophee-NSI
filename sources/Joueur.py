from Entite import *

class Joueur(Entite):
    _CARTES_DE_DOS           : bool = False
    _CARTE_MAIN_PREMIERE_POS : Pos  = Jeu.pourcentages_coordonnees(40, 60)
    
    # Pas la peine de créer un JSON juste pour ça
    STATS_DE_BASE : Stat = Stat(45, 32, 37, 22, 32, 1.3, 1).reset_vie()
    
    _nom_derniere_carte_piochee : str = ''
    
    
    @override
    def __init__(self, deck : Sequence[str], inventaire : list[Item] = []) -> None:
        super().__init__(
            "",
            Joueur.STATS_DE_BASE,
            deck,
            6,
            f"{Chemins.IMG}joueur.png",
            inventaire,
        )
        self._nombre_pieces : int = 0
    
    
    @property
    def nb_pieces(self) -> int:
        return self._nombre_pieces
    
    @property
    def pos_sprite_centree(self) -> Pos:
        return Jeu.pourcentages_coordonnees(31, 75)
    
    
    @override
    def recoit_degats(self, degats_recu : int, attaque_cause : Attaque) -> None:
        """Prend en charge les dégats prits et retourne si un crit est retourné."""
        # joueur_invincible n'empèche pas les soins
        if bool(params.joueur_invincible) and degats_recu >= 0:
            return
        
        Entite.recoit_degats(self, degats_recu, attaque_cause)
    
    @override
    def reset(self) -> None:
        Entite.reset(self)      # Appelle la version de Entite au lieu de cette override
        self._stats = copy(Joueur.STATS_DE_BASE)
    
    def index_carte_du_dessus(self, pos_souris : pos_t) -> Optional[int]:
        """
        Détermine quelle est la carte de la main s'affichant au dessus à la position `pos`.
        Renvoie l'index (dans la main) de la carte, si aucune carte n'est à cette position, renvoie None.
        """
        pos_a_verifier : Pos = pos_t_vers_Pos(pos_souris)
        index_cliquee : Optional[int] = None
        
        # ordre inverse de celui de dessin
        # les cartes dessinées avant sont en dessous
        iteration_inversee = range(len(self._cartes_main)-1, -1, -1)    # I miss C-style loops
        for i in iteration_inversee:
            if self._cartes_main[i].dans_hitbox(pos_a_verifier):
                index_cliquee = i
                break
        
        return index_cliquee
    
    def lever_carte_du_dessus(self, pos_souris : pos_t) -> None:
        if not self._main_dans_ecran:
            return
        
        # Baisse les cartes
        for c in self._cartes_main:
            c.anim_etat = CarteAnimEtat.REVENIR
        
        # Lève celle qui est survolée
        i = self.index_carte_du_dessus(pos_souris)
        if i is not None:
            self._cartes_main[i].anim_etat = CarteAnimEtat.EN_SURVOL
    
    def gerer_dessin_infos_cartes(self) -> None:
        for c in self._cartes_main:
            c.dessiner_infos = False
        
        if Jeu.duree_execution - Jeu.dernier_mouvement_souris < Duree(s=Jeu.parametres["temps min affichage info"]):
            return
        i = self.index_carte_du_dessus(pygame.mouse.get_pos())
        if i is not None:
            self._cartes_main[i].dessiner_infos = True
    
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