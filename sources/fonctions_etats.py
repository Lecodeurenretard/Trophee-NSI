"""
Ce fichier contient tout le code pour les états de jeu (comme pour une machine à états).
Chaque fonction éponyme à une valeur de `EtatJeu` sera une boucle stournant tant que l'état correspondant est dans `etat`.
"""

from fonctions_boutons import *

def attente_nouveau_combat() -> None:
    ecran_gen : Generator[Surface, None, None] = nouveau_combat(Jeu.num_combat)
    while True:
        Jeu.commencer_frame()
        
        if testeur_skip_ou_quitte():
            break
        
        try:
            Jeu.fenetre.blit(next(ecran_gen), (0, 0))
        except StopIteration:
            break
        pygame.display.flip()
    
    Jeu.changer_etat(Jeu.Etat.CHOIX_ATTAQUE)

def choix_attaque() -> None:
    boutons_attaques[0].enable_drawing()
    interruption_gen : Optional[Interruption] = None
    
    while True:
        Jeu.commencer_frame()
        if interruption_gen is not None:
            try:
                Jeu.fenetre.blit(next(interruption_gen), (0, 0))
                pygame.display.flip()
            except StopIteration:
                interruption_gen = None
            continue
        
        for event in pygame.event.get():
            verifier_pour_quitter(event)
            if (event.type != pygame.KEYDOWN and event.type != pygame.MOUSEBUTTONDOWN) or not Jeu.tour_joueur:
                continue
            
            # Si le joueur attaque...
            if ButtonCursor.handle_inputs(boutons_attaques, event):
                Jeu.tour_joueur = False
                continue
            
            if event.type == pygame.KEYDOWN:
                interruption_gen = reagir_appui_touche(event)
                continue
        
        
        rafraichir_ecran()
    # inutile maintenant, le sera un jour
    boutons_attaques[0].disable_drawing()
    changer_etat(EtatJeu.AFFICHAGE_ATTAQUES)

def ecran_titre() -> None:
    LARGEUR_BOUTONS : int = 200
    HAUTEUR_BOUTONS : int = 60
    
    DIMENSIONS_BOUTONS : tuple[tuple[int, int, int, int], ...] = (
        centrer_pos_tuple((pourcentage_largeur(50), pourcentage_hauteur(30), LARGEUR_BOUTONS, HAUTEUR_BOUTONS)),
        centrer_pos_tuple((pourcentage_largeur(50), pourcentage_hauteur(50), LARGEUR_BOUTONS, HAUTEUR_BOUTONS)),
        centrer_pos_tuple((pourcentage_largeur(50), pourcentage_hauteur(70), LARGEUR_BOUTONS, HAUTEUR_BOUTONS)),
    )
    boutons_menu : tuple[ButtonCursor, ...] = (
        ButtonCursor("Jouer"     , DIMENSIONS_BOUTONS[0], line_thickness=0, group_name="Ecran titre", group_color=VERT, action=lancer_jeu),
        ButtonCursor("Paramètres", DIMENSIONS_BOUTONS[1], line_thickness=0, group_name="Ecran titre",                   action=lancer_parametres),
        ButtonCursor("Crédits"   , DIMENSIONS_BOUTONS[2], line_thickness=0, group_name="Ecran titre",                   action=afficher_credits),
    )
    boutons_menu[0].enable_drawing()
    
    
    while Jeu.ecran_titre_running:
        Jeu.commencer_frame()
        for event in pygame.event.get():
            verifier_pour_quitter(event)
            ButtonCursor.handle_inputs(boutons_menu, event)
        
        Jeu.fenetre.fill(BLEU_CLAIR)
        for bouton in boutons_menu:
            bouton.draw(Jeu.fenetre)
        
        ButtonCursor.draw_cursors(Jeu.fenetre)
        pygame.display.flip()
    Jeu.changer_etat(Jeu.Etat.ATTENTE_NOUVEAU_COMBAT)