from Curseur import *
from fonctions_vrac import utilisateur_valide_menu

class Button:
    def __init__(
        self,
        text : str, dim : tuple[int, int, int, int],
        action : Callable[[], None] | None = None,
        line_thickness : int = 1, bg_color : color = GRIS, line_color : color = NOIR
    ):
        self._rect : Rect = Rect(*dim)
        self._text : str = text
        
        self._line_color : color = line_color
        self._bg_color : color = bg_color
        self._line_size : int = line_thickness
        
        self._action : Callable[[], None] | None = action
    
    def draw(self, surface : Surface) -> None:
        pygame.draw.rect(surface, self._bg_color, self._rect)
        if self._line_size > 0:
            pygame.draw.rect(surface, self._line_color, self._rect, width=self._line_size)
        
        text_surf : Surface = globales.POLICE_FOURRE_TOUT.render(self._text, True, BLANC)
        text_rect : Rect = text_surf.get_rect(center=self._rect.center)
        
        surface.blit(text_surf, text_rect)

    def check_click(self, pos_click : Pos) -> bool:
        if self._rect.collidepoint(tuple(pos_click)) and self._action is not None:
            self._action()
            return True
        return False

class ButtonCursor(Button):
    _cursor_radius : int = 12
    _cursor_offset : int = 10
    
    _group_count   : dict[str, int]     = {}    # group's name -> # of buttons in the group
    _group_cursors : dict[str, Curseur] = {}    # group's name -> group's cursor
    _group_colors  : dict[str, color]   = {}    # group's name -> group's color
    
    def __init__(
            self,
            text: str, dim : tuple[int, int, int, int],
            group_name : str, group_color : color = NOIR,
            line_thickness : int = 1, bg_color : color = GRIS, line_color : color = NOIR,
            callback: Callable[[], None] | None = None
        ):
        """
        Ctor for CursorButton.  
        Takes same arguments as Button's ctor except for:
            - `group_name`: the group's name, if the group doesn't exists creates it
            - `group_color`: defines the color of the group's cursor (ignored if `group` already exists)
            and some others taht will be used for drawing.
        """
        super().__init__(text, dim, action=callback, line_thickness=line_thickness, line_color=line_color, bg_color=bg_color)
        self._group_name = group_name
        
        cursor_pos : Pos = Pos(
            self._rect.x - ButtonCursor._cursor_radius - ButtonCursor._cursor_offset,
            self._rect.y + self._rect.h // 2
        )
        
        if ButtonCursor._group_exists(group_name):
            self._get_cursor().ajouter_pos(cursor_pos)
            self._cursor_pos : Pos = self._get_cursor().coordonee_globale_vers_coordonee_curseur(cursor_pos)
            ButtonCursor._group_count[self._group_name] += 1
            return
        
        cursor = Curseur([cursor_pos.x], [cursor_pos.y])
        cursor._interdir_col_sauf(cursor_pos.x, cursor_pos.y)
        cursor._interdir_ligne_sauf(cursor_pos.y, cursor_pos.x)
        
        ButtonCursor._group_count[self._group_name] = 1
        ButtonCursor._group_cursors[group_name] = cursor
        ButtonCursor._group_colors[group_name] = group_color
        
        self._cursor_pos : Pos = self._get_cursor().coordonee_globale_vers_coordonee_curseur(cursor_pos)
    
    def __del__(self):
        ButtonCursor._group_count[self._group_name] -= 1
        if ButtonCursor._group_count[self._group_name] <= 0:    # no more Button in the group
            del ButtonCursor._group_count[self._group_name]
            del ButtonCursor._group_cursors[self._group_name]
            del ButtonCursor._group_colors[self._group_name]
    
    @staticmethod
    def _group_exists(group_to_test : str) -> bool:
        return group_to_test in ButtonCursor._group_cursors.keys()
    
    @staticmethod
    def draw_cursors(surface : Surface) -> None:
        for group_name in ButtonCursor._group_cursors:
            color_ = ButtonCursor._group_colors[group_name]
            group = ButtonCursor._group_cursors[group_name]
            
            group.dessiner(surface, color_, ButtonCursor._cursor_radius)
    
    @staticmethod
    def check_inputs(check_for : 'list[ButtonCursor]|tuple[ButtonCursor, ...]', ev : pygame.event.Event) -> bool:
        """Renvoie si `action()` à été éxecuté au moins une fois."""
        group_checked : list[str] = []
        useless_butt_count : int = 0
        
        callback_execute : bool = False
        for butt in check_for:
            cursor_butt : Curseur = butt._get_cursor()
            if butt._group_name not in group_checked:
                cursor_butt.deplacement_utilisateur(ev)
                group_checked.append(butt._group_name)
                
            if butt._action is None:
                useless_butt_count += 1
                continue
            if utilisateur_valide_menu(ev) and cursor_butt.get_position_dans_position() == butt._cursor_pos:
                butt._action()
                callback_execute = True
                continue
            
            if ev.type == pygame.MOUSEBUTTONDOWN:
                callback_execute |= butt.check_click(ev.pos)
        
        if useless_butt_count == 1:
            logging.warning(f"Un bouton n'a aucune fonction à éxécuter.")
        elif useless_butt_count > 0:
            logging.warning(f"{useless_butt_count} boutons n'ont aucune fonction à éxécuter.")
        return callback_execute
    
    def _get_cursor(self) -> Curseur:
        return ButtonCursor._group_cursors[self._group_name]
    def _get_cursor_color(self) -> color:
        return ButtonCursor._group_colors[self._group_name]
    
    def get_cursor_group_pos_in_pos(self) -> Pos:
        return self._get_cursor().get_position_dans_position()