"""Contient la classe Joueur et la variable globale joueur."""
from Entite import *

class Joueur(Entite):
    _CARTES_DE_DOS           : bool = False
    _CARTE_MAIN_PREMIERE_POS : Pos  = Fenetre.pourcentages_coordonnees(40, 60)
    
    
    @override
    def __init__(self, inventaire : list[Item] = []) -> None:
        super().__init__(
            EntiteJSON.joueur(),
            inventaire,
        )
        self._nombre_pieces : int = 0
    
    
    @property
    def nb_pieces(self) -> int:
        return self._nombre_pieces
    
    @property
    def pos_sprite_centree(self) -> Pos:
        return Fenetre.pourcentages_coordonnees(31, 75)
    
    
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
        self._stats = copy(EntiteJSON.joueur().stats)
    
    def gerer_dessin_infos_cartes(self) -> None:
        """Si les conditions sont bonnes, affiches les infos de la carte survolée."""
        for c in self._cartes_main:
            c.dessiner_infos = False
        
        # Affiche les infos de la carte du dessus si le joueur la survole assez longtemps
        if Jeu.duree_execution - Jeu.dernier_mouvement_souris < Duree(s=Jeu.parametres["temps min affichage info"]):
            return
        i = self.index_carte_du_dessus(pygame.mouse.get_pos())
        if i is not None:
            self._cartes_main[i].dessiner_infos = True
    
    def ajouter_pieces(self, gagne : int) -> None:
        """Donne `gagne` pieces au joueur peu importe les options de triches."""
        self._nombre_pieces += gagne
        self._nombre_pieces = max(0, self._nombre_pieces)
        if gagne > 0:
            son_pieces = Sound(f"{Chemins.SFX}/argent.wav")
            son_pieces.play()
    
    def paiement(self, prelevement : int, payer_max : bool = True) -> int:
        """
        `ajouter_pieces()` mais enlève des pièces et respecte les paramètres de triches.
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
    
    @override
    def decrire_stats(self) -> str:
        return (
            Entite.decrire_stats(self)
            + f"Argent: {self._nombre_pieces}\n"
        )


joueur : Joueur = Joueur()