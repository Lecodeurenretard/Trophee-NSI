"""
Ce fichier contient tout le code pour les états de jeu (comme pour une machine à états).
Chaque fonction éponyme à une valeur de `EtatJeu` sera une boucle stournant tant que l'état correspondant est dans `etat`.
"""

from fonctions_main import *
from Item import Item
from Bouton import Button

def attente_prochaine_etape() -> None:
    logging.debug(f"Activation de l'état {Jeu.Etat.ATTENTE_PROCHAINE_ETAPE.name}.")
    
    initialiser_nouveau_combat(Jeu.num_etape)
    ecran_gen : Generator[Surface, None, None] = ecran_nombre_combat()
   
    while True:
        Jeu.commencer_frame()
        if testeur_skip_ou_quitte():
            break
        
        try:
            Jeu.fenetre.blit(next(ecran_gen), (0, 0))
        except StopIteration:
            break
        
        dessiner_infos()
        Jeu.display_flip()
    
    if Jeu.DECISION_SHOP(Jeu.num_etape):
        Jeu.changer_etat(Jeu.Etat.SHOP)
        return
    
    Jeu.changer_etat(Jeu.Etat.CHOIX_ATTAQUE)

def choix_attaque() -> None:
    logging.debug(f"Activation de l'état {Jeu.Etat.CHOIX_ATTAQUE.name}.")
    
    ButtonCursor.enable_drawing("Attaques")
    interruption : Optional[Interruption] = None
    
    while Jeu.etat == Jeu.Etat.CHOIX_ATTAQUE:
        Jeu.commencer_frame()
        if interruption is not None:
            terminer_interruption(interruption)
        
        for event in pygame.event.get():
            verifier_pour_quitter(event)
            interruption = reagir_appui_touche_choix_attaque(event)
            if interruption is not None: break
            
            if event.type != pygame.KEYDOWN and event.type != pygame.MOUSEBUTTONDOWN:
                continue
            
            # Si le joueur attaque...
            if ButtonCursor.handle_inputs(boutons_attaques, event):
                monstres_attaquent()
                Jeu.reset_etat()
                break
        
        rafraichir_ecran()
    
    ButtonCursor.disable_drawing("Attaques")
    if Jeu.decision_etat_en_cours():
        Jeu.changer_etat(Jeu.Etat.AFFICHAGE_ATTAQUES)

def affichage_attaques() -> None:
    logging.debug(f"Activation de l'état {Jeu.Etat.AFFICHAGE_ATTAQUES.name}.")
    
    attaque_gen : list[Generator[None, None, None]] = [Attaque.lancer_toutes_les_attaques_gen(Jeu.fenetre)]
    attaque_gen[0].send(None)
    while len(attaque_gen) != 0:
        Jeu.commencer_frame()
        skip : bool = testeur_skip_ou_quitte()
        
        rafraichir_ecran(attaque_gen, to_send_dessin=skip)
    rafraichir_ecran(attaque_gen)
    
    if joueur.est_mort:
        Jeu.a_gagne = False
        Jeu.changer_etat(Jeu.Etat.GAME_OVER)
        return
    
    pieces_gagnees : int = 0
    for monstre in Monstre.tuer_les_monstres_morts():
        assert(monstre.rang is not None), "Le monstre n'avait aucun type."
        pieces_gagnees += 2**monstre.rang + random.randint(1, 4)  # Dites non au décalage de bit et exponentiez
    
    if pieces_gagnees != 0:
        joueur.gagner_pieces(pieces_gagnees)
        terminer_interruption(animation_argent_gagne(pieces_gagnees))
    
    if len(Monstre.monstres_en_vie) == 0:
        if not victoire_joueur():
            Jeu.num_etape += 1
            Jeu.changer_etat(Jeu.Etat.ATTENTE_PROCHAINE_ETAPE)
            return
        
        Jeu.a_gagne = True
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
        pygame.mixer.music.load(f"{Constantes.Chemins.SFX}/victoire.wav")
    else:
        Jeu.set_texte_fenetre("...")
        pygame.mixer.music.load(f"{Constantes.Chemins.SFX}/defaite.wav")
    
    pygame.mixer.music.play()
    while not testeur_skip_ou_quitte():
        Jeu.commencer_frame()
        try:
            Jeu.fenetre.blit(next(ecran_gen), (0, 0))
        except StopIteration:
            break
        Jeu.display_flip()
    
    if bool(params.fermer_a_la_fin):
        quit()
    
    joueur.reset()
    Jeu.num_etape = 1
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
    
    INVENTAIRE_EPAISSEUR_TRAIT : int = 2
    INVENTAIRE_LARGEUR : int = 100 + INVENTAIRE_EPAISSEUR_TRAIT
    INVENTAIRE_BOITE : Rect = Rect(
        Jeu.largeur - INVENTAIRE_LARGEUR + INVENTAIRE_EPAISSEUR_TRAIT,
        -INVENTAIRE_EPAISSEUR_TRAIT,
        INVENTAIRE_LARGEUR,
        Jeu.hauteur + INVENTAIRE_EPAISSEUR_TRAIT * 2
    )
    
    # nombre d'éléments -> listes des abscisses (pour une fenêtre de dimension 100x100)
    ABSCISSES_RELATIVE_ITEMS : tuple[tuple[float, ...], ...] = (
        (),
        (50,),
        (30, 70),
        (18, 50, 82),
    )
    # nombre d'éléments -> listes des abscisses (avec les dimensions de la fenêtre)
    ABSCISSES_ITEMS : tuple[tuple[int, ...], ...] = tuple([
        tuple([
            round(pc_abcisse * (Jeu.largeur - INVENTAIRE_BOITE.width) / 100)  # Convertit les pourcentages en vraies valeurs
            for pc_abcisse in liste_abscisses   # pc pour pourcentage
        ])
        for liste_abscisses in ABSCISSES_RELATIVE_ITEMS
    ])
    
    # choisit 2 ou 3 items au hasard
    items : list[Item] = [Item.item_aleatoire() for _ in range(random.randint(2, 3))]
    
    bouton_sortie : Button = Button(
        (20, 20, Jeu.pourcentage_largeur(6), Jeu.pourcentage_largeur(6)),
        img=f"{Constantes.Chemins.IMG}/retour.png",
        action=Jeu.reset_etat,
    )
    
    premiere_frame : bool = True
    interruption : Optional[Interruption] = None
    
    while Jeu.etat == Jeu.Etat.SHOP:
        Jeu.commencer_frame()
        if interruption is not None:
            terminer_interruption(interruption)
        
        for ev in pygame.event.get():
            verifier_pour_quitter(ev)
            
            interruption = reagir_appui_touche(ev)
            if interruption is not None:
                break
            
            if ev.type == pygame.MOUSEWHEEL and bool(params.mode_debug):
                dbg_shop_scroll(ev, items, ABSCISSES_ITEMS[len(items)])
            
            if ev.type == pygame.MOUSEBUTTONDOWN:
                shop_click(ev, items, bouton_sortie, ABSCISSES_ITEMS[len(items)])
            
            if ev.type == pygame.KEYDOWN and bool(params.mode_debug):
                if ev.key in Constantes.Touches.DBG_SHOP_AJOUT_ITEM and len(items) < len(ABSCISSES_ITEMS) - 1:
                    items.append(Item.item_aleatoire())
                elif ev.key in Constantes.Touches.DBG_SHOP_SUPPRESSION_ITEM and len(items) > 0:
                    items.pop()
        
        
        Jeu.fenetre.fill(BLANC)
        
        # Dessine l'inventaire du joueur
        dessiner_rect(
            Jeu.fenetre,
            INVENTAIRE_BOITE.topleft, INVENTAIRE_BOITE.size,
            couleur_remplissage=GRIS, couleur_bords=NOIR,
            epaisseur_trait=INVENTAIRE_EPAISSEUR_TRAIT
        )
        
        dessiner_nombre_pieces(INVENTAIRE_BOITE)
        dessiner_inventaire(Jeu.fenetre, INVENTAIRE_BOITE)
        
        dessiner_infos()
        
        bouton_sortie.draw(Jeu.menus_surf)
        for item, pourcentage_abscisse in zip(items, ABSCISSES_ITEMS[len(items)]):
            item.dessiner(Jeu.fenetre, pourcentage_abscisse, afficher_avertissements=premiere_frame)
        
        Jeu.display_flip()
        premiere_frame = False
    
    Jeu.num_etape += 1
    if Jeu.decision_etat_en_cours():
        Jeu.changer_etat(Jeu.Etat.ATTENTE_PROCHAINE_ETAPE)