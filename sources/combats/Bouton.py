from fonctions_boutons import *

class Bouton:
    def __init__(self, text : str, x : int, y : int, w : int, h : int, action : Callable[[], None] | None = None):
        self.rect : Rect = Rect(x, y, w, h)
        self.text : str = text
        self.color : color = GRIS
        self.action : Callable[[], None] | None = action

    def draw(self, surface : Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)
        
        text_surf : Surface = variables_globales.police.render(self.text, True, BLANC)
        text_rect : Rect = text_surf.get_rect(center=self.rect.center)
        
        surface.blit(text_surf, text_rect)

    def check_click(self, pos_click : Pos):
        if self.rect.collidepoint(tuple(pos_click)) and self.action:
            self.action()

boutons_menu : list[Bouton] = [
    Bouton("Jouer"     , 300, 200, 200, 60, jouer),
    Bouton("Paramètres", 300, 300, 200, 60, ouvrir_parametres),
    Bouton("Crédits"   , 300, 400, 200, 60, afficher_credits),
]

def check_all_clicks(pos_click : Pos):
    for butt in boutons_menu:
        butt.check_click(pos_click)