from fonctions_boutons import *

# Graphe des états: http://graphonline.top/fr/?graph=ZCaEuQwPStCefLfb
class EtatJeu(Enum):
    DECISION_ETAT          = auto()
    CHOIX_ATTAQUE      = auto()
    AFFICHAGE_ATTAQUES     = auto()
    ATTENTE_NOUVEAU_COMBAT = auto()
    FIN_DU_JEU             = auto()
    
    ECRAN_TITRE            = auto()
    MENU_PARAMETRES_JEU    = auto() # paramètred quand on est dans le jeu
    MENU_PARAMETRES_TITRE  = auto() # paramètres quand on vient de l'écran titre
    CREDITS                = auto()

etat_du_jeu           : EtatJeu = EtatJeu.DECISION_ETAT
precedent_etat_du_jeu : EtatJeu = EtatJeu.DECISION_ETAT
def changer_etat(nouveau_etat : EtatJeu) -> None:
    global etat_du_jeu, precedent_etat_du_jeu
    
    precedent_etat_du_jeu = etat_du_jeu
    etat_du_jeu = nouveau_etat



def attente_nouveau_combat() -> None:
    ecran_gen : Generator[Surface, None, None] = nouveau_combat(globales.nbr_combat + 1)
    while True:
        commencer_frame()
        verifier_pour_quitter()
        try:
            fenetre.blit(next(ecran_gen), (0, 0))
        except StopIteration:
            changer_etat(EtatJeu.CHOIX_ATTAQUE)
            return
        pygame.display.flip()

def choix_attaque() -> None:
    while True:
        commencer_frame()
        verifier_pour_quitter()
        
        rafraichir_ecran()
    # inutile maintenant, le sera un jour
    changer_etat(EtatJeu.AFFICHAGE_ATTAQUES)

def ecran_titre() -> None:
    boutons_menu : tuple[ButtonCursor, ...] = (
        ButtonCursor("Jouer"     , (pourcentage_largeur(50), 200, 200, 60), line_thickness=0, group_name="Ecran titre", group_color=VERT, action=lancer_jeu),
        ButtonCursor("Paramètres", (pourcentage_largeur(50), 300, 200, 60), line_thickness=0, group_name="Ecran titre",                   action=menu_parametres),
        ButtonCursor("Crédits"   , (pourcentage_largeur(50), 400, 200, 60), line_thickness=0, group_name="Ecran titre",                   action=afficher_credits),
    )
    while globales.menu_running:
        fenetre.fill(BLEU_CLAIR)
        for bouton in boutons_menu:
            bouton.draw(fenetre)
        
        ButtonCursor.draw_cursors(fenetre)
        pygame.display.flip()
        
        for event in pygame.event.get():
            verifier_pour_quitter(event)
            ButtonCursor.handle_inputs(boutons_menu, event)
    changer_etat(EtatJeu.ATTENTE_NOUVEAU_COMBAT)