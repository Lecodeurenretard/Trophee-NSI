from fonctions_boutons import *

def menu() -> None:
    boutons_menu : tuple[ButtonCursor, ...] = (
        ButtonCursor("Jouer"     , (300, 200, 200, 60), line_thickness=0, group_name="Ecran titre", group_color=VERT, action=lancer_jeu),
        ButtonCursor("Paramètres", (300, 300, 200, 60), line_thickness=0, group_name="Ecran titre",                   action=menu_parametres),
        ButtonCursor("Crédits"   , (300, 400, 200, 60), line_thickness=0, group_name="Ecran titre",                   action=afficher_credits),
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

def jeu() -> None:
    joueur.reset_vie()
    reset_monstre()
    
    while True:
        rafraichir_ecran()
        globales.delta = clock.tick(60) / 1000      # convertion en secondes
        
        for event in pygame.event.get():
            verifier_pour_quitter(event)
            if (event.type != pygame.KEYDOWN and event.type != pygame.MOUSEBUTTONDOWN) or not globales.tour_joueur:
                continue
            
            # Si le joueur attaque...
            if ButtonCursor.handle_inputs(boutons_attaques, event):
                globales.tour_joueur = False
                continue
            
            if event.type == pygame.KEYDOWN:
                reagir_appui_touche(event)
                continue
        
        Monstre.tuer_les_monstres_morts()
        if len(Monstre.monstres_en_vie) == 0:
            if fin_combat():
                return
            continue
        
        if not globales.tour_joueur:
            monstres_attaquent()
            Attaque.lancer_toutes_les_attaques(rafraichir_ecran)
            
            globales.tour_joueur = True
        
        if joueur.est_mort():
            fin_partie(gagne=False)
            return

def __main__() -> None:
    reset_monstre()
    
    while True:
        menu()
        jeu()

# N'éxecute le programme que si on le lance depuis ce fichier
if __name__ == "__main__":
    __main__()