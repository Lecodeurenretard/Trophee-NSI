from import_var import *

class Curseur:
    def __init__(self, col_dispo : tuple[int, ...], lne_dispo : tuple[int, ...]) -> None:
        # ordonne de gauche à droite et de haut en bas
        self._col_dispo   : tuple[int, ...] = tuple(sorted(col_dispo))
        self._ligne_dispo : tuple[int, ...] = tuple(sorted(lne_dispo))
        
        self._position_dans_positions = Pos(0, 0)	# v. doc
        self._pos = Pos(0, 0)
        self._update_pos()
    
    
    
    def _update_pos(self, update_col : bool = True, update_lne : bool = True) -> None:
        if update_lne:
            self._pos.y = self._ligne_dispo[self._position_dans_positions.y]
        
        if update_col:
            self._pos.x = self._col_dispo[self._position_dans_positions.x]
    
    def _est_ligne_valide(self, lne : int) -> bool:
        return lne in self._ligne_dispo
    def _est_colonne_valide(self, col : int) -> bool:
        return col in self._col_dispo
    def _est_emplacement_valide(self, p : Pos) -> bool:
        return self._est_colonne_valide(p.x) and self._est_ligne_valide(p.y)
    
    def dessiner(self, surface : pygame.Surface, couleur : color, rayon : int = 10) -> None:
        pygame.draw.circle(surface, couleur, tuple(self._pos), rayon)
    
    
    def monter(self) -> Pos:
        self._position_dans_positions.y -= 1
        self._position_dans_positions.y = self._position_dans_positions.y % len(self._ligne_dispo)

        self._update_pos()
        return self._pos
    def descendre(self) -> Pos:
        self._position_dans_positions.y += 1
        self._position_dans_positions.y = self._position_dans_positions.y % len(self._ligne_dispo)

        self._update_pos()
        return self._pos
    
    def aller_gauche(self) -> Pos:
        self._position_dans_positions.x -= 1
        self._position_dans_positions.x = self._position_dans_positions.x % len(self._col_dispo)
        
        self._update_pos()
        return self._pos
    def aller_droite(self) -> Pos:
        self._position_dans_positions.x += 1
        self._position_dans_positions.x = self._position_dans_positions.x % len(self._col_dispo)
        
        self._update_pos()
        return self._pos
    
    def get_position_dans_position(self) -> tuple[int, int]:
        """
        Retourne une tuple caractérisant la position du curseur si le curseur n'est à aucune position connue, met un NaN sur la coordonée correspondante.
        
        Exemples:
        prenons
            curseur_pos_attendue_x = (60, 80)
            curseur_pos_attendue_y = (70, 90)
        et
            variables_globales.curseur_x = 60
            variables_globales.curseur_y = 90
        
        alors quelle_position_curseur() retournera (0, 1)
        
        
        Si cette fois
            variables_globales.curseur_x = 61
            variables_globales.curseur_y = 70
        
        alors quelle_position_curseur() retournera (NAN, 0)
        """
        
        return tuple(self._position_dans_positions) # type: ignore  # Une tuple de Pos à toujours une longueur de deux
    
    def changer_pos_curseur(self, ev : pygame.event.Event) -> None:
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