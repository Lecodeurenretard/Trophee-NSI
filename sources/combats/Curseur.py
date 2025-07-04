from import_var import *

class Curseur:
    def __init__(self, col_dispo : tuple[int, ...], lne_dispo : tuple[int, ...], pos_interdites : tuple[Pos, ...] = ()) -> None:
        # ordonne de gauche à droite et de haut en bas
        self._col_dispo   : tuple[int, ...] = tuple(sorted(col_dispo))
        self._ligne_dispo : tuple[int, ...] = tuple(sorted(lne_dispo))
        self._interdit     : tuple[Pos, ...] = pos_interdites
        
        self._pos_dans_toutes_pos = Pos(0, 0)	# v. doc
        self._pos = Pos(0, 0)
        self._update_pos()
    
    def _update_pos(self, update_col : bool = True, update_lne : bool = True) -> bool:
        """Retourne si la position à été modifiée."""
        ancienne_pos : Pos = self._pos
        if update_lne:
            self._pos.y = self._ligne_dispo[self._pos_dans_toutes_pos.y]
        
        if update_col:
            self._pos.x = self._col_dispo[self._pos_dans_toutes_pos.x]
        
        if not self._est_emplacement_valide(self._pos):
            self._pos = ancienne_pos
            return False
        return True
    
    def _est_ligne_valide(self, lne : int) -> bool:
        return lne in self._ligne_dispo
    def _est_colonne_valide(self, col : int) -> bool:
        return col in self._col_dispo
    def _est_emplacement_valide(self, p : Pos) -> bool:
        return (
            self._est_colonne_valide(p.x)
            and self._est_ligne_valide(p.y)
            and p not in self._interdit
        )
    
    def dessiner(self, surface : Surface, couleur : color, rayon : int = 10) -> None:
        pygame.draw.circle(surface, couleur, tuple(self._pos), rayon)
    
    def _ajouter_a_pdtp_x(self, combien : int):
        self._pos_dans_toutes_pos.x += combien
        self._pos_dans_toutes_pos.x %= len(self._col_dispo)
    def _ajouter_a_pdtp_y(self, combien : int):
        self._pos_dans_toutes_pos.y += combien
        self._pos_dans_toutes_pos.y %= len(self._ligne_dispo)
    
    def monter(self) -> None:
        self._ajouter_a_pdtp_y(-1)
        while not self._update_pos():     # skip les positions interdites
            self._ajouter_a_pdtp_y(-1)
        
    def descendre(self) -> None:
        self._ajouter_a_pdtp_y(1)
        while not self._update_pos():     # skip les positions interdites
            self._ajouter_a_pdtp_y(1)
        
    def aller_gauche(self) -> None:
        self._ajouter_a_pdtp_x(-1)
        while not self._update_pos():     # skip les positions interdites
            self._ajouter_a_pdtp_x(-1)
        
    def aller_droite(self) -> None:
        self._ajouter_a_pdtp_x(1)
        while not self._update_pos():     # skip les positions interdites
            self._ajouter_a_pdtp_x(1)
        

    def get_position_dans_position(self) -> tuple[int, int]:
        return tuple(self._pos_dans_toutes_pos) # type: ignore  # Une tuple de Pos à toujours une longueur de deux
    
    def deplacement_utilisateur(self, ev : pygame.event.Event) -> None:
        if ev.type != pygame.KEYDOWN:
            return
        
        if ev.key == pygame.K_UP:
            self.monter()
            return
        
        if ev.key == pygame.K_DOWN:
            self.descendre()
            return
        
        if ev.key == pygame.K_LEFT:
            self.aller_gauche()
            return
        
        if ev.key == pygame.K_RIGHT:
            self.aller_droite()
            return
        # sinon, ne fait rien