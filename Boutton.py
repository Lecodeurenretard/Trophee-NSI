from fonctions_bouttons import *

class Boutton:
    def __init__(self, text, x, y, w, h, action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = GRIS
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surf = police.render(self.text, True, BLANC)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            if self.action:
                self.action()

boutons = [
    Boutton("Jouer", 300, 200, 200, 60, jouer),
    Boutton("Paramètres", 300, 300, 200, 60, ouvrir_parametres),
    Boutton("Crédits", 300, 400, 200, 60, afficher_credits),
]