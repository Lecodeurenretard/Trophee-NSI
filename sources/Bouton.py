from import_var import *
from Curseur    import Curseur

class Button:
    SOUND_PRESSED : Sound         = Sound(f"{Chemins.SFX}/select.mp3")
    FONT_NAME     : Optional[str] = None
    
    def __init__(
            self,
            dim            : tuple[int, int, int, int],
            text           : str                       = '',
            img            : Optional[str]             = None,
            action         : Callable[[], None] | None = None,
            line_thickness : int                       = 1,
            bg_color       : color                     = GRIS,
            line_color     : color                     = NOIR
    ):
        self._rect  : Rect = Rect(*dim)
        self._text  : str  = text
        self._image : Optional[Surface] = None
        if img is not None:
            self._image = pygame.image.load(img)
            self._image = pygame.transform.scale(self._image, (dim[2], dim[3]))
        
        self._line_color : rgba = color_to_rgba(line_color)
        self._bg_color   : rgba = color_to_rgba(bg_color)
        
        self._line_size : int = line_thickness
        
        self._action : Callable[[], None] | None = action
    
    @property
    def rect(self) -> Rect:
        return self._rect
    
    def draw(self, surface : Surface, point_size : int) -> None:
        pygame.draw.rect(surface, self._bg_color, self._rect)
        if self._line_size > 0:
            pygame.draw.rect(surface, self._line_color, self._rect, width=self._line_size)
        
        
        if self._image is not None:
            surface.blit(self._image, self._rect)
            return
        
        police : pygame.font.Font = pygame.font.SysFont(Button.FONT_NAME, point_size)
        surf = police.render(self._text, True, BLANC)
        surface.blit(surf, surf.get_rect(center=self._rect.center))
    
    def check_click(self, pos_click : pos_t, jouer_son : bool = True) -> bool:
        """Vérifie si le clic était dans le bouton, si oui joue le son et appelle le callback et return true."""
        if self.mouse_on_butt(pos_click):
            if jouer_son:
                self.jouer_sfx()
            
            if self._action is not None:
                self._action()
            return True
        return False
    
    def mouse_on_butt(self, pos_mouse : pos_t) -> bool: # peak naming
        """Vérifie que la souris est dans la hitbox du bouton ("sur" le bouton)."""
        return self._rect.collidepoint(pos_t_vers_tuple(pos_mouse))
    
    def jouer_sfx(self) -> None:
        Button.SOUND_PRESSED.play()
    
    def change_pos(self, new_pos : Pos) -> None:
        self._rect = Rect(new_pos.tuple, self._rect.size)

class ButtonCursor(Button):
    """La classe n'est plus maintenue, et ne doit PAS être utilisée."""
    _CURSOR_OFFSET : int = 10
    _cursor_radius : int = 12
    
    # Prefixed by static to avoid name conflict with propreties
    _static_group_count    : dict[str, int]     = {}    # group's name -> # of buttons in the group
    _static_group_cursors  : dict[str, Curseur] = {}    # group's name -> group's cursor
    _static_group_colors   : dict[str, rgba]    = {}    # group's name -> group's color
    _static_group_is_drawn : dict[str, bool]    = {}    # group's name -> should the group be drawn
    
    def __init__(
            self,
            text: str, dim : tuple[int, int, int, int],
            group_name : str, group_color : color = NOIR,
            line_thickness : int = 1, bg_color : color = GRIS, line_color : color = NOIR,
            action: Callable[[], None] | None = None
        ):
        """
        Ctor for CursorButton.  
        Takes same arguments as Button's ctor except for:
            - `group_name`: the group's name, if the group doesn't exists creates it
            - `group_color`: defines the color of the group's cursor (ignored if `group` already exists)
        """
        super().__init__(dim=dim, text=text, action=action, line_thickness=line_thickness, line_color=line_color, bg_color=bg_color)
        self._group_name = group_name
        
        cursor_pos : Pos = Pos(
            self._rect.x - ButtonCursor._cursor_radius - ButtonCursor._CURSOR_OFFSET,
            self._rect.y + self._rect.h // 2
        )
        
        # The cursor position from where it's able to select this button
        if ButtonCursor._group_exists(group_name):
            ButtonCursor._add_to_group(self, cursor_pos)
        else:
            ButtonCursor._create_group(cursor_pos, self._group_name, group_color)
        
        self._cursor_pos : Pos = self.cursor.coordonees_globales_vers_coordonees_curseur(cursor_pos)
    
    def __del__(self):
        ButtonCursor._static_group_count[self._group_name] -= 1
        if ButtonCursor._static_group_count[self._group_name] <= 0:    # no more Button in the group
            del ButtonCursor._static_group_count[self._group_name]
            del ButtonCursor._static_group_cursors[self._group_name]
            del ButtonCursor._static_group_colors[self._group_name]
            del ButtonCursor._static_group_is_drawn[self._group_name]
    
    @staticmethod
    def _create_group(cursor_position : Pos, group_name : str, group_color : color) -> None:
        cursor = Curseur([cursor_position.x], [cursor_position.y])
        cursor.interdir_col_sauf(cursor_position.x, cursor_position.y)    # Since it's new there's only one position available
        cursor.interdir_lne_sauf(cursor_position.y, cursor_position.x)
        
        ButtonCursor._static_group_count[group_name] = 1
        ButtonCursor._static_group_cursors[group_name] = cursor
        ButtonCursor._static_group_colors[group_name] = color_to_rgba(group_color)
        ButtonCursor._static_group_is_drawn[group_name] = False
    
    @staticmethod
    def _add_to_group(curse_butt : 'ButtonCursor', cursor_pos : Pos) -> None:
        curse_butt.cursor.ajouter_pos(cursor_pos)
        
        ButtonCursor._static_group_count[curse_butt._group_name] += 1
    
    @staticmethod
    def _group_exists(group_to_test : str) -> bool:
        return group_to_test in ButtonCursor._static_group_cursors.keys()
    
    @staticmethod
    def draw_cursors(surface : Surface) -> None:
        for group_name in ButtonCursor._static_group_cursors:
            if not ButtonCursor._static_group_is_drawn[group_name]:
                continue
            
            color = ButtonCursor._static_group_colors[group_name]
            group = ButtonCursor._static_group_cursors[group_name]
            
            group.dessiner(surface, color, ButtonCursor._cursor_radius)
    
    @staticmethod
    def handle_inputs(butt_seq : 'list[ButtonCursor]|tuple[ButtonCursor, ...]', ev : pygame.event.Event) -> bool:
        """
        Gère les inputs des boutons dans `butt_seq` ainsi que leurs groupes respectifs.  
        Renvoie True si `action()` à été éxecuté au moins une fois.
        """
        groups_having_moved_cursor : list[str] = []
        
        action_executed : bool = False
        for butt in butt_seq:
            if butt._group_name not in groups_having_moved_cursor:
                butt.cursor.deplacement_utilisateur(ev)
                groups_having_moved_cursor.append(butt._group_name)
            
            if Touches.utilisateur_valide_menu(ev) and butt._do_cursor_select_button:
                butt.jouer_sfx()
                if butt._action is None:
                    continue
                
                butt._action()
                action_executed = True
                continue
            
            if ev.type == pygame.MOUSEBUTTONDOWN:
                action_executed |= butt.check_click(ev.pos)
        
        return action_executed
    
    @property
    def _group_is_drawn(self) -> bool:
        return ButtonCursor._static_group_is_drawn[self._group_name]
    @property
    def _group_count(self) -> int:
        return ButtonCursor._static_group_count[self._group_name]
    @property
    def _group_cursor(self) -> Curseur:
        return ButtonCursor._static_group_cursors[self._group_name]
    @property
    def _group_color(self) -> rgba:
        return ButtonCursor._static_group_colors[self._group_name]
    
    @property
    def _do_cursor_select_button(self) -> bool:
        return self.cursor.position_dans_positions == self._cursor_pos
    
    @property
    def cursor(self) -> Curseur:
        return self._group_cursor
    
    @staticmethod
    def enable_drawing(group_name : str) -> None:
        assert(group_name in ButtonCursor._static_group_is_drawn.keys()), "Mauvais nom de groupe."
        ButtonCursor._static_group_is_drawn[group_name] = True
    
    @staticmethod
    def disable_drawing(group_name : str) -> None:
        assert(group_name in ButtonCursor._static_group_is_drawn.keys()), "Mauvais nom de groupe."
        ButtonCursor._static_group_is_drawn[group_name] = False
    
    def change_pos(self, new_pos : Pos) -> None:
        # La méthode demanderait de modifier la position dans le groupe aussi
        # (donc la position des autres membres), je laisse ça à plus tard.
        raise NotImplementedError("La méthode `.change_pos()` n'est pas implémentée pour la classe ButtonCursor.")