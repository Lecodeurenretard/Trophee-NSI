from fonctions_bouttons import *

class Boutton:
    def __init__(self, text : str, x : int, y : int, w : int, h : int, action : Callable[[], None] | None = None):
        self.rect : pygame.Rect = pygame.Rect(x, y, w, h)
        self.text : str = text
        self.color : color = GRIS
        self.action : Callable[[], None] | None = action

    def draw(self, surface : pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)
        
        text_surf : pygame.Surface = variables_globales.police.render(self.text, True, BLANC)
        text_rect : pygame.Rect = text_surf.get_rect(center=self.rect.center)
        
        surface.blit(text_surf, text_rect)

    def check_click(self, pos_click : pos):
        if self.rect.collidepoint(pos_click) and self.action:
            self.action()

bouttons : list[Boutton] = [
    Boutton("Jouer"     , 300, 200, 200, 60, jouer),
    Boutton("Paramètres", 300, 300, 200, 60, ouvrir_parametres),
    Boutton("Crédits"   , 300, 400, 200, 60, afficher_credits),
]

def check_all_clicks(pos_click : pos):
    for butt in bouttons:
        butt.check_click(pos_click)