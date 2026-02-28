from import_var import *
from Curseur    import Curseur

class Bouton:
    SON_APPUI  : Sound         = Sound(f"{Chemins.SFX}/select.mp3")
    NOM_POLICE : Optional[str] = None
    
    def __init__(
            self,
            dim            : tuple[int, int, int, int],
            txt            : str                       = '',
            img            : Optional[str]             = None,
            action         : Callable[[], None] | None = None,
            epaisseur_ligne : int                      = 1,
            coul_bg        : color                     = GRIS,
            coul_ligne     : color                     = NOIR
    ):
        self._rect   : Rect = Rect(*dim)
        self._texte  : str  = txt
        self._image  : Optional[Surface] = None
        if img is not None:
            self._image = pygame.image.load(img).convert_alpha()
            self._image = pygame.transform.scale(self._image, (dim[2], dim[3]))
        
        self._coul_ligne : rgba = color_to_rgba(coul_ligne)
        self._coul_bg    : rgba = color_to_rgba(coul_bg)
        
        self._taille_ligne : int = epaisseur_ligne
        
        self._action : Callable[[], None]|None = action
    
    @property
    def rect(self) -> Rect:
        return copy(self._rect)
    
    def dessiner(self, num_couche : int, point_size : int) -> None:
        toile = Jeu.get_couche(num_couche)
        
        pygame.draw.rect(toile, self._coul_bg, self._rect)
        if self._taille_ligne > 0:
            pygame.draw.rect(toile, self._coul_ligne, self._rect, width=self._taille_ligne)
        
        
        if self._image is not None:
            toile.blit(self._image, self._rect)
            return
        
        police : pygame.font.Font = pygame.font.SysFont(Bouton.NOM_POLICE, point_size)
        surf = police.render(self._texte, True, BLANC)
        toile.blit(surf, surf.get_rect(center=self._rect.center))
    
    def check_click(self, pos_click : pos_t, jouer_son : bool = True) -> bool:
        """Vérifie si le clic était dans le bouton, si oui joue le son et appelle le callback et return true."""
        if self.dans_hitbox(pos_click):
            if jouer_son:
                self.jouer_sfx()
            
            if self._action is not None:
                self._action()
            return True
        return False
    
    def dans_hitbox(self, pos : pos_t) -> bool: # peak name has been lost in translaztion :(
        """Vérifie que la souris est dans la hitbox du bouton ("sur" le bouton)."""
        return self._rect.collidepoint(pos_t_vers_tuple(pos))
    
    def jouer_sfx(self) -> None:
        Bouton.SON_APPUI.play()
    
    def changer_pos(self, new_pos : Pos) -> None:
        self._rect = Rect(new_pos.tuple, self._rect.size)