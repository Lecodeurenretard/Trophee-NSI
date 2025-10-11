"""
Ce fichier contient tout le code pour les états de jeu (comme pour une machine à états).
Chaque fonction éponyme à une valeur de `EtatJeu` sera une boucle stournant tant que l'état correspondant est dans `etat`.
"""

from fonctions_boutons import *
from Jeu import *

def attente_nouveau_combat() -> None:
    logging.debug(f"Activation de l'état {Jeu.Etat.ATTENTE_NOUVEAU_COMBAT.name}.")
    
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
    logging.debug(f"Activation de l'état {Jeu.Etat.CHOIX_ATTAQUE.name}.")
    
    ButtonCursor.enable_drawing("Attaques")
    interruption_gen : Optional[Interruption] = None
    
    finir : bool = False
    while not finir:
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
            Jeu.changer_etat(Jeu.Etat.ATTENTE_NOUVEAU_COMBAT)
            return
        
        Jeu.a_gagne = True
        Jeu.changer_etat(Jeu.Etat.FIN_JEU)
        return
    
    if joueur.est_mort:
        Jeu.a_gagne = False
        Jeu.changer_etat(Jeu.Etat.FIN_JEU)
        return
    
    Jeu.changer_etat(Jeu.Etat.CHOIX_ATTAQUE)

def ecran_titre() -> None:
    logging.debug(f"Activation de l'état {Jeu.Etat.ECRAN_TITRE.name}.")
    
    LARGEUR_BOUTONS : int = 200
    HAUTEUR_BOUTONS : int = 60
    
    DIMENSIONS_BOUTONS : tuple[tuple[int, int, int, int], ...] = (
        centrer_pos((Jeu.pourcentage_largeur(50), Jeu.pourcentage_hauteur(30), LARGEUR_BOUTONS, HAUTEUR_BOUTONS)),
        centrer_pos((Jeu.pourcentage_largeur(50), Jeu.pourcentage_hauteur(50), LARGEUR_BOUTONS, HAUTEUR_BOUTONS)),
        centrer_pos((Jeu.pourcentage_largeur(50), Jeu.pourcentage_hauteur(70), LARGEUR_BOUTONS, HAUTEUR_BOUTONS)),
    )
    boutons_menu : tuple[ButtonCursor, ...] = (
        ButtonCursor("Jouer"     , DIMENSIONS_BOUTONS[0], line_thickness=0, group_name="Ecran titre", group_color=VERT, action=lancer_jeu),
        ButtonCursor("Paramètres", DIMENSIONS_BOUTONS[1], line_thickness=0, group_name="Ecran titre",                   action=lancer_parametres),
        ButtonCursor("Crédits"   , DIMENSIONS_BOUTONS[2], line_thickness=0, group_name="Ecran titre",                   action=lambda: Jeu.changer_etat(Jeu.Etat.CREDITS)),
    )
    ButtonCursor.enable_drawing("Ecran titre")
    
    
    dessiner_fond_ecran = dessiner_gif(
        Jeu.fenetre,
        f"{Constantes.Chemins.DOSSIER_ANIM}/fond/frame *.png",
        Duree(s=.1), Pos(Jeu.CENTRE_FENETRE), loop=True, scale=True
    )
    while Jeu.etat == Jeu.Etat.ECRAN_TITRE:
        Jeu.commencer_frame()
        for event in pygame.event.get():
            verifier_pour_quitter(event)
            ButtonCursor.handle_inputs(boutons_menu, event)
        
        next(dessiner_fond_ecran)
        for bouton in boutons_menu:
            bouton.draw(Jeu.fenetre)
        
        ButtonCursor.draw_cursors(Jeu.fenetre)
        pygame.display.flip()
    
    if Jeu.etat != Jeu.Etat.CREDITS:
        Jeu.changer_etat(Jeu.Etat.ATTENTE_NOUVEAU_COMBAT)

def credits(duree : Duree = Duree(s=5)) -> None:
    logging.debug(f"Activation de l'état {Jeu.Etat.CREDITS.name}.")
    if duree == Duree():
        return
    
    texte_credits  : Surface = Constantes.Polices.FOURRE_TOUT.render("Développé par Jules et Lucas", True, BLANC)
    texte_credits2 : Surface = pygame.font.Font(None, 30).render("et Nils", True, BLANC)
    
    deplacement : Deplacement = Deplacement(
        Pos(Jeu.pourcentage_largeur(50), Jeu.HAUTEUR),
        Pos(Jeu.pourcentage_largeur(50), -50),  # pour laisser le "et Nils" aller hors écran
    )
    
    debut : Duree = copy(Jeu.duree_execution)
    while not testeur_skip_ou_quitte() and Jeu.duree_execution < debut + duree:
        Jeu.commencer_frame()
        
        pos = deplacement.calculer_valeur((Jeu.duree_execution - debut) / duree)
        
        Jeu.fenetre.fill(NOIR)
        blit_centre(Jeu.fenetre, texte_credits , pos.tuple)
        blit_centre(Jeu.fenetre, texte_credits2, (pos + Vecteur(0, 30)).tuple)
        
        pygame.display.flip()
    Jeu.changer_etat(Jeu.precedent_etat)

def fin_jeu() -> None:
    logging.debug("")
    logging.debug("")
    logging.debug(f"Activation de l'état {Jeu.Etat.FIN_JEU.name}.")
    
    ecran_gen : Generator[Surface, None, None] = fin_partie(Jeu.a_gagne)
    while not testeur_skip_ou_quitte():
        Jeu.commencer_frame()
        try:
            Jeu.fenetre.blit(next(ecran_gen), (0, 0))
        except StopIteration:
            break
        pygame.display.flip()
    
    if param.fermer_a_la_fin.case_cochee:
        quit()
    
    Jeu.changer_etat(Jeu.Etat.ECRAN_TITRE)