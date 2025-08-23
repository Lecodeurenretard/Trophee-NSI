from import_var import *

class Curseur:
    def __init__(self, col_dispo : list[int], lne_dispo : list[int], pos_interdites : list[Pos] = []) -> None:
        # ordonne de gauche à droite et de haut en bas
        self._col_dispo   : list[int] = list(sorted(col_dispo))
        self._lne_dispo : list[int] = list(sorted(lne_dispo))
        self._interdit    : list[Pos] = pos_interdites
        
        self._pos_dans_toutes_pos = Pos(0, 0)	# v. doc
        self._pos = Pos(0, 0)
        self._update_pos()
    
    def _update_pos(self, update_col : bool = True, update_lne : bool = True) -> bool:
        """Retourne si la position à été modifiée."""
        ancienne_pos : Pos = self._pos
        if update_lne:
            self._pos.y = self._lne_dispo[self._pos_dans_toutes_pos.y]
        
        if update_col:
            self._pos.x = self._col_dispo[self._pos_dans_toutes_pos.x]
        
        if not self.est_emplacement_valide(self._pos):
            self._pos = ancienne_pos
            return False
        return True
    
    def _interdir_col_sauf(self, colonne : int, exception_ligne : int) -> None:
        assert(colonne in self._col_dispo), "La colonne n'a pas été ajoutée auparavant au curseur dans Curseur.interdir_col_sauf()."
        assert(exception_ligne in self._lne_dispo), "La ligne à éviter n'a pas été ajoutée auparavant au curseur dans Curseur.interdir_col_sauf()."
        for lne in self._lne_dispo:
            if lne != exception_ligne:
                self.ajouter_interdit(Pos(colonne, lne))
    
    def _interdir_lne_sauf(self, ligne : int, exception_colonne : int) -> None:
        assert(ligne in self._lne_dispo), "La colonne n'a pas été ajoutée auparavant au curseur dans Curseur.interdir_ligne_sauf()."
        assert(exception_colonne in self._col_dispo), "La ligne à éviter n'a pas été ajoutée auparavant au curseur dans Curseur.interdir_ligne_sauf()."
        for col in self._col_dispo:
            if col != exception_colonne:
                self.ajouter_interdit(Pos(col, ligne))
    
    def _lever_interdiction(self, pos_interdite : Pos) -> None:
        self._interdit.remove(pos_interdite)    # lève une ValueError si ne trouve pas
    
    def _ajouter_a_pdtp_x(self, combien : int):
        self._pos_dans_toutes_pos.x += combien
        self._pos_dans_toutes_pos.x %= len(self._col_dispo) # Empèche le curseur d'aller Out of Bound
    def _ajouter_a_pdp_y(self, combien : int):
        self._pos_dans_toutes_pos.y += combien
        self._pos_dans_toutes_pos.y %= len(self._lne_dispo)
    
    def coordonees_globales_vers_coordonees_curseur(self, coord_globales : Pos) -> Pos:
        res : Pos = Pos(-1, -1)
        res.x = self._col_dispo.index(coord_globales.x)
        res.y = self._lne_dispo.index(coord_globales.y)
        
        return res
    
    def verifie_ligne_existe(self, lne : int) -> bool:
        return lne in self._lne_dispo
    def verifie_colonne_existe(self, col : int) -> bool:
        return col in self._col_dispo
    
    def verifie_emplacement_existe(self, p : Pos) -> bool:
        return (
            self.verifie_colonne_existe(p.x)
            and self.verifie_ligne_existe(p.y)
        )
    def est_emplacement_valide(self, p : Pos) -> bool:
        return (
            self.verifie_emplacement_existe(p)
            and p not in self._interdit
        )
    
    def dessiner(self, surface : Surface, couleur : color, rayon : int = 10) -> None:
        pygame.draw.circle(surface, couleur, tuple(self._pos), rayon)
    
    def monter(self) -> None:
        self._ajouter_a_pdp_y(-1)
        while not self._update_pos():     # skip les positions interdites
            self._ajouter_a_pdp_y(-1)
        
    def descendre(self) -> None:
        self._ajouter_a_pdp_y(1)
        while not self._update_pos():
            self._ajouter_a_pdp_y(1)
        
    def aller_gauche(self) -> None:
        self._ajouter_a_pdtp_x(-1)
        while not self._update_pos():
            self._ajouter_a_pdtp_x(-1)
        
    def aller_droite(self) -> None:
        self._ajouter_a_pdtp_x(1)
        while not self._update_pos():
            self._ajouter_a_pdtp_x(1)
        

    @property
    def position_dans_positions(self) -> Pos:
        return self._pos_dans_toutes_pos
    
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
    
    
    def ajouter_colonne(self, x_coord : int) -> None:
        if x_coord not in self._col_dispo:
            insort(self._col_dispo, x_coord)    # Garde _col_dispo triée
    
    def ajouter_ligne(self, y_coord : int) -> None:
        if y_coord not in self._lne_dispo:
            insort(self._lne_dispo, y_coord)
    
    def ajouter_interdit(self, a_interdir : Pos) -> None:
        if a_interdir not in self._interdit:
            self._interdit.append(a_interdir)
    
    def ajouter_pos(self, position : Pos) -> None:
        assert(not self.est_emplacement_valide(position)), f"Une position est déjà active à {position} dans Curseur.ajouter_pos()."
        
        if self.verifie_emplacement_existe(position):
            self._lever_interdiction(position)
            return
        
        if self.verifie_colonne_existe(position.x):
            self.ajouter_ligne(position.y)
            self._interdir_lne_sauf(position.y, position.x)
            return
        
        if self.verifie_ligne_existe(position.y):
            self.ajouter_colonne(position.x)
            self._interdir_col_sauf(position.x, position.y)
            return
        raise(RuntimeError("La logique de Curseur.ajouter_pos() est mauvaise."))