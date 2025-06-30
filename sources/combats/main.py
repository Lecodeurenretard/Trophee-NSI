from Monstre import *
from Bouton import *
from fonction_combat import *

def quit(exit_code : int = 0) -> NoReturn:
    pygame.quit()
    sys.exit(exit_code)

def menu() -> None:
    curseur_menu : Curseur = Curseur(
        (270,),
        (230, 330, 430)
    )
    while variables_globales.menu_running:
        fenetre.fill(BLEU_CLAIR)
        for bouton in boutons_menu:
            bouton.draw(fenetre)
        
        curseur_menu.dessiner(fenetre, VERT, 20)
        pygame.display.flip()
        
        for event in pygame.event.get():
            quitter_si_necessaire(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                check_all_clicks(event.pos)
                continue
            
            if event.type == pygame.KEYDOWN and event.key in UI_TOUCHES_VALIDER:
                position_curseur : int = curseur_menu.get_position_dans_position()[1]   # Ce menu n'est que sur une ligne
                match position_curseur:
                    case 0:
                        jouer()
                        return
                    case 1:
                        ouvrir_parametres()
                        break
                    case 2:
                        afficher_credits()
                        break
                    case _:
                        raise NotImplementedError("Boutton non implémenté.")

            curseur_menu.changer_pos_curseur(event)

def partie_fin(gagne : bool) -> NoReturn:
    couleur_fond : color
    texte_fin : pygame.Surface
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
    
    time.sleep(2)
    quit()

def reset_monstre() -> None:
    Monstre.nouveau_monstre(
        random.choice(list(TypeMonstre))    # choisit au hasard un type de monstre
    )

def __main__() -> None:
    reset_monstre()
    while True:
        rafraichir_ecran()
        clock.tick(60)
        
        # Le menu qu'il y a avant le jeu
        menu()
        
        rafraichir_ecran()
        for event in pygame.event.get():
            quitter_si_necessaire(event)
            if event.type != pygame.KEYDOWN or not variables_globales.tour_joueur:
                continue
            
            if event.key == pygame.K_i:
                afficher_info()
                continue        # Un event ne peut être qu'une seule touche à la fois
            
            if event.key == pygame.K_SPACE:
                joueur_selectionne_attaque()
                variables_globales.tour_joueur = False
                continue
            
            if variables_globales.tour_joueur:
                curseur_menu_combat.changer_pos_curseur(event)
        
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
            monstre_attaque()
            variables_globales.tour_joueur = True
        
        if joueur.est_mort():
            partie_fin(gagne=False)

# N'éxecute le programme que si on le lance de ce fichier
if __name__ == "__main__":
    __main__()