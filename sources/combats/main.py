from Monstre import *
from fonctions_boutons import *
from fonction_combat import *

def quit(exit_code : int = 0) -> NoReturn:
    pygame.quit()
    sys.exit(exit_code)

def menu() -> None:
    boutons_menu : tuple[ButtonCursor, ...] = (
        ButtonCursor("Jouer"     , (300, 200, 200, 60), line_thickness=0, group_name="Ecran titre", group_color=VERT, callback=jouer),
        ButtonCursor("Paramètres", (300, 300, 200, 60), line_thickness=0, group_name="Ecran titre",                   callback=ouvrir_parametres),
        ButtonCursor("Crédits"   , (300, 400, 200, 60), line_thickness=0, group_name="Ecran titre",                   callback=afficher_credits),
    )
    while variables_globales.menu_running:
        fenetre.fill(BLEU_CLAIR)
        for bouton in boutons_menu:
            bouton.draw(fenetre)
        ButtonCursor.draw_cursors(fenetre)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            quitter_si_necessaire(event)
            ButtonCursor.check_inputs(boutons_menu, event)

def partie_fin(gagne : bool) -> NoReturn:
    couleur_fond : color
    texte_fin : Surface
    if gagne:
        couleur_fond = VERT
        texte_fin = TEXTE_VICTOIRE
        print("Vous avez gagné !")
    else:
        couleur_fond = BLEU_CLAIR
        texte_fin = TEXTE_DEFAITE
        print("Vous avez perdu...")
    
    fenetre.fill(couleur_fond)
    fenetre.blit(texte_fin, (LARGEUR // 2 - 120, HAUTEUR // 2 - 20))
    pygame.display.flip()
    
    attendre(2)
    quit()

def reset_monstre() -> None:
    Monstre.nouveau_monstre(
        random.choice(list(TypeMonstre))    # choisit au hasard un type de monstre
    )

def __main__() -> None:
    reset_monstre()
    menu()
    
    while True:
        rafraichir_ecran()
        clock.tick(60)
        
        for event in pygame.event.get():
            quitter_si_necessaire(event)
            if (event.type != pygame.KEYDOWN and event.type != pygame.MOUSEBUTTONDOWN) or not variables_globales.tour_joueur:
                continue
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                afficher_info()
                continue        # Un event ne peut être qu'une seule touche à la fois
            
            if ButtonCursor.check_inputs(boutons_attaques, event):
                variables_globales.tour_joueur = False
                rafraichir_ecran()
                attendre(1)
                continue
        
        Monstre.tuer_les_monstres_morts()
        if len(Monstre.monstres_en_vie) == 0:
            # La vie du joueur est délibérément pas reset.
            
            variables_globales.nbr_combat += 1
            
            variables_globales.tour_joueur = True
            
            if variables_globales.nbr_combat > MAX_COMBAT:
                partie_fin(gagne=True)
            
            # else implicite
            afficher_nombre_combat(variables_globales.nbr_combat)
            
            reset_monstre()
        
        if not variables_globales.tour_joueur:
            monstres_attaquent()
            variables_globales.tour_joueur = True
        
        if joueur.est_mort():
            partie_fin(gagne=False)

# N'éxecute le programme que si on le lance depuis ce fichier
if __name__ == "__main__":
    __main__()