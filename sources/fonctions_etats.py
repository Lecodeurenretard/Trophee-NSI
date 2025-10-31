"""
Ce fichier contient tout le code pour les états de jeu (comme pour une machine à états).
Chaque fonction éponyme à une valeur de `EtatJeu` sera une boucle stournant tant que l'état correspondant est dans `etat`.
"""

from fonctions_main import *
from Item import Item
from Bouton import Button

def attente_prochaine_etape() -> None:
    logging.debug(f"Activation de l'état {Jeu.Etat.ATTENTE_PROCHAINE_ETAPE.name}.")
    
    initialiser_nouveau_combat(Jeu.num_combat)
    ecran_gen : Generator[Surface, None, None] = ecran_nombre_combat()
   
    while True:
        Jeu.commencer_frame()
        if testeur_skip_ou_quitte():
            break
        
        try:
            Jeu.fenetre.blit(next(ecran_gen), (0, 0))
        except StopIteration:
            break
        Jeu.display_flip()
    
    if Jeu.DECISION_SHOP(Jeu.num_combat):
        Jeu.changer_etat(Jeu.Etat.SHOP)
        return
    
    Jeu.changer_etat(Jeu.Etat.CHOIX_ATTAQUE)

def choix_attaque() -> None:
    logging.debug(f"Activation de l'état {Jeu.Etat.CHOIX_ATTAQUE.name}.")
    
    ButtonCursor.enable_drawing("Attaques")
    interruption_gen : Optional[Interruption] = None
    
    finir : bool = False
    while not finir:
        Jeu.commencer_frame()
        if interruption_gen is not None:
            try:
                Jeu.fenetre.blit(next(interruption_gen), (0, 0))
                Jeu.display_flip()
            except StopIteration:
                interruption_gen = None
            continue
        
        for event in pygame.event.get():
            verifier_pour_quitter(event)
            if event.type != pygame.KEYDOWN and event.type != pygame.MOUSEBUTTONDOWN:
                continue
            
            # Si le joueur attaque...
            if ButtonCursor.handle_inputs(boutons_attaques, event):
                monstres_attaquent()
                finir = True
                break
            
            if event.type == pygame.KEYDOWN:
                interruption_gen = reagir_appui_touche(event)
                if Jeu.etat != Jeu.Etat.CHOIX_ATTAQUE:
                    ButtonCursor.disable_drawing("Attaques")
                    return
                continue
        
        rafraichir_ecran()
    
    ButtonCursor.disable_drawing("Attaques")
    Jeu.changer_etat(Jeu.Etat.AFFICHAGE_ATTAQUES)

def affichage_attaques() -> None:
    logging.debug(f"Activation de l'état {Jeu.Etat.AFFICHAGE_ATTAQUES.name}.")
    
    attaque_gen : list[Generator[None, None, None]] = [Attaque.lancer_toutes_les_attaques_gen(Jeu.fenetre)]
    attaque_gen[0].send(None)
    while len(attaque_gen) != 0:
        Jeu.commencer_frame()
        skip : bool = testeur_skip_ou_quitte()
        
        rafraichir_ecran(attaque_gen, to_send_dessin=skip)
    
    # Check pour les monstres morts
    Monstre.tuer_les_monstres_morts()
    if len(Monstre.monstres_en_vie) == 0:
        if not joueur_gagne():
            Jeu.num_combat += 1
            Jeu.changer_etat(Jeu.Etat.ATTENTE_PROCHAINE_ETAPE)
            return
        
        Jeu.a_gagne = True
        Jeu.changer_etat(Jeu.Etat.GAME_OVER)
        return
    
    if joueur.est_mort:
        Jeu.a_gagne = False
        Jeu.changer_etat(Jeu.Etat.GAME_OVER)
        return
    
    Jeu.changer_etat(Jeu.Etat.CHOIX_ATTAQUE)

def ecran_titre() -> None:
    logging.debug(f"Activation de l'état {Jeu.Etat.ECRAN_TITRE.name}.")
    Jeu.set_texte_fenetre("Ecran titre")
    
    LARGEUR_BOUTONS : int = 200
    HAUTEUR_BOUTONS : int = 60
    
    DIMENSIONS_BOUTONS : tuple[tuple[int, int, int, int], ...] = (
        centrer_pos((Jeu.pourcentage_largeur(50), Jeu.pourcentage_hauteur(30), LARGEUR_BOUTONS, HAUTEUR_BOUTONS)),
        centrer_pos((Jeu.pourcentage_largeur(50), Jeu.pourcentage_hauteur(50), LARGEUR_BOUTONS, HAUTEUR_BOUTONS)),
        centrer_pos((Jeu.pourcentage_largeur(50), Jeu.pourcentage_hauteur(70), LARGEUR_BOUTONS, HAUTEUR_BOUTONS)),
    )
    boutons_menu : tuple[ButtonCursor, ...] = (
        ButtonCursor("Jouer"     , DIMENSIONS_BOUTONS[0], line_thickness=0, group_name="Ecran titre", group_color=VERT, action=lambda: Jeu.changer_etat(Jeu.Etat.PREPARATION)),
        ButtonCursor("Paramètres", DIMENSIONS_BOUTONS[1], line_thickness=0, group_name="Ecran titre",                   action=lancer_parametres),
        ButtonCursor("Crédits"   , DIMENSIONS_BOUTONS[2], line_thickness=0, group_name="Ecran titre",                   action=lambda: Jeu.changer_etat(Jeu.Etat.CREDITS)),
    )
    ButtonCursor.enable_drawing("Ecran titre")
    
    
    dessiner_fond_ecran = dessiner_gif(
        Jeu.fenetre,
        f"{Constantes.Chemins.ANIM}/fond/frame *.png",
        Duree(s=.1), Pos(Jeu.centre_fenetre), loop=True, scale=True
    )
    while Jeu.etat == Jeu.Etat.ECRAN_TITRE:
        Jeu.commencer_frame()
        
        potentiellement_fini : bool = False # Vérifie si un bouton à été appuyé
        for event in pygame.event.get():    # si c'est le cas, il se peut que l'on dessine une frame de trop
            verifier_pour_quitter(event)    # donc on revient au début de la boucle
            potentiellement_fini = ButtonCursor.handle_inputs(boutons_menu, event)
        
        if potentiellement_fini:
            continue
        
        next(dessiner_fond_ecran)
        for bouton in boutons_menu:
            bouton.draw(Jeu.fenetre)
        
        ButtonCursor.draw_cursors(Jeu.fenetre)
        Jeu.display_flip()
    
    if Jeu.etat != Jeu.Etat.CREDITS:
        Jeu.changer_etat(Jeu.Etat.PREPARATION)

def credits(duree : Duree = Duree(s=5)) -> None:
    logging.debug(f"Activation de l'état {Jeu.Etat.CREDITS.name}.")
    if duree == Duree():
        return
    
    texte_credits  : Surface = Constantes.Polices.FOURRE_TOUT.render("Développé par Jules et Lucas", True, BLANC)
    texte_credits2 : Surface = pygame.font.Font(None, 30).render("et Nils", True, BLANC)
    
    deplacement : Deplacement = Deplacement(
        Pos(Jeu.pourcentage_largeur(50), Jeu.hauteur),
        Pos(Jeu.pourcentage_largeur(50), -50),  # pour laisser le "et Nils" aller hors écran
    )
    
    debut : Duree = copy(Jeu.duree_execution)
    while not testeur_skip_ou_quitte() and Jeu.duree_execution < debut + duree:
        Jeu.commencer_frame()
        
        pos = deplacement.calculer_valeur((Jeu.duree_execution - debut) / duree)
        
        Jeu.fenetre.fill(NOIR)
        blit_centre(Jeu.fenetre, texte_credits , pos.tuple)
        blit_centre(Jeu.fenetre, texte_credits2, (pos + Vecteur(0, 30)).tuple)
        
        Jeu.display_flip()
    Jeu.changer_etat(Jeu.precedent_etat)

def game_over() -> None:
    logging.debug("")
    logging.debug("")
    logging.debug(f"Activation de l'état {Jeu.Etat.GAME_OVER.name}.")
    
    ecran_gen : Generator[Surface, None, None] = fin_partie(Jeu.a_gagne)
    if Jeu.a_gagne:
        Jeu.set_texte_fenetre("yay!")
    else:
        Jeu.set_texte_fenetre("...")
    
    while not testeur_skip_ou_quitte():
        Jeu.commencer_frame()
        try:
            Jeu.fenetre.blit(next(ecran_gen), (0, 0))
        except StopIteration:
            break
        Jeu.display_flip()
    
    if bool(params.fermer_a_la_fin):
        quit()
    
    joueur.reset_vie()
    Jeu.num_combat = 1
    Jeu.changer_etat(Jeu.Etat.ECRAN_TITRE)

def preparation() -> None:
    logging.debug(f"Activation de l'état {Jeu.Etat.PREPARATION.name}.")
    
    if not bool(params.mode_debug):
        # exception au principe de la boucle principale dans l'état
        # C'est juste plus simple et propre de faire comme ça ici
        Jeu.set_texte_fenetre("Who am I?")
        terminer_interruption(demander_pseudo(Jeu.fenetre))
        
        Jeu.set_texte_fenetre("Chargement...")
        terminer_interruption(faux_chargement(Jeu.fenetre))
    else:
        joueur.pseudo = "Testeur"
    
    Jeu.set_texte_fenetre("Combat!")
    Jeu.changer_etat(Jeu.Etat.ATTENTE_PROCHAINE_ETAPE)

def shop() -> None:
    logging.debug(f"Activation de l'état {Jeu.Etat.SHOP.name}.")
    Jeu.set_texte_fenetre("I like shopping")
    
    sensibilite_scroll : float = 1
    
    # nombre d'éléments -> listes des abscisses
    ABSCISSES_ITEMS : dict[int, tuple[int, ...]] = {
        0: (),
        1: (Jeu.pourcentage_largeur(50),),
        2: (Jeu.pourcentage_largeur(33), Jeu.pourcentage_largeur(66)),
        3: (Jeu.pourcentage_largeur(20), Jeu.pourcentage_largeur(50), Jeu.pourcentage_largeur(80)),
    }
    
    # choisit 2 ou 3 items au hasard
    items : list[Item] = [Item.item_aleatoire() for _ in range(random.randint(2, 3))]
    
    bouton_sortie : Button = Button(
        (20, 20, Jeu.pourcentage_largeur(6), Jeu.pourcentage_largeur(6)),
        img=f"{Constantes.Chemins.IMG}/retour.png",
        action=Jeu.reset_etat,
    )
    
    while Jeu.etat == Jeu.Etat.SHOP:
        for ev in pygame.event.get():
            verifier_pour_quitter(ev)
            
            # Changement d'item en mode débug
            if ev.type == pygame.MOUSEWHEEL and bool(params.mode_debug):
                index = Item.item_survole(items, ABSCISSES_ITEMS[len(items)])
                if index is None: continue
                
                changement : int = round(ev.precise_y * sensibilite_scroll)
                items[index] = Item(items[index].id + changement, permissif=True)
                continue
            
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button in (4, 5): # empèche le scroll de compter pour un click
                    continue
                
                if bouton_sortie.check_click(pygame.mouse.get_pos()):
                    break
                
                index = Item.item_survole(items, ABSCISSES_ITEMS[len(items)])
                if index is None: continue
                
                if joueur.prendre_item(items[index]):
                    items.pop(index)
        
        Jeu.fenetre.fill(BLANC)
        
        bouton_sortie.draw(Jeu.menus_surf)
        for item, abscisse in zip(items, ABSCISSES_ITEMS[len(items)]):
            item.dessiner(Jeu.fenetre, round(abscisse))
        
        Jeu.display_flip()
    
    Jeu.num_combat += 1
    Jeu.changer_etat(Jeu.Etat.ATTENTE_PROCHAINE_ETAPE)

#TODO: continuer le shop:
#    - introduire monnaie
#    - implémenter pour de vrai les items