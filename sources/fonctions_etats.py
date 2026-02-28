"""
Ce fichier contient tout le code pour les états de jeu (comme pour une machine à états).
Chaque fonction éponyme à une valeur de `EtatJeu` sera une boucle stournant tant que l'état correspondant est dans `etat`.
"""

from fonctions_main import *
from Item           import Item
from Bouton         import Bouton
from Carte          import Carte, CarteAnimEtat
from Joueur         import Entite, joueur
from Boss           import Monstre, Boss

def attente_prochaine_etape() -> None:
    logging.debug(f"Activation de l'état {Jeu.Etat.ATTENTE_PROCHAINE_ETAPE.name}.")
    
    initialiser_nouveau_combat(Jeu.num_etape)
    ecran_gen : Generator[None, None, None] = ecran_nombre_combat(0)
   
    while True:
        Jeu.commencer_frame()
        if testeur_skip():
            break
        
        try:
            next(ecran_gen)
        except StopIteration:
            break
        
        dessiner_infos()
        Jeu.display_flip()
    
    if Jeu.etape_est_shop():
        Jeu.changer_etat(Jeu.Etat.SHOP)
        return
    
    if Jeu.etape_est_boss():
        Monstre.massacre()
        Boss.spawn_boss()
    
    joueur.repiocher_tout()
    Jeu.set_texte_fenetre("Combat!")
    Jeu.changer_etat(Jeu.Etat.CHOIX_ATTAQUE)

def choix_attaque() -> None:
    logging.debug(f"Activation de l'état {Jeu.Etat.CHOIX_ATTAQUE.name}.")
    
    # Si nouveau tour (commencement tour joueur)
    if Jeu.attaques_restantes_joueur == Jeu.ATTAQUES_PAR_TOUR:
        Jeu.nb_tours_combat += 1
        joueur.piocher()
        for boss in Boss.vivants_boss():
            boss.nouveau_tour()
    
    joueur.piocher_si_main_vide()
    for m in Monstre.vivants():
       m.piocher_si_main_vide()
    
    if Jeu.attaques_restantes_joueur > 0:
        logging.debug('')
        joueur.main_jouer_entrer()
        for m in Monstre.vivants():
            m.main_jouer_sortir()
    
    interruption : Optional[Interruption] = None
    while Jeu.etat == Jeu.Etat.CHOIX_ATTAQUE:
        Jeu.commencer_frame()
        if interruption is not None:
            terminer_interruption(interruption)
        
        # Si le joueur ne peut pas jouer
        if Jeu.attaques_restantes_joueur <= 0:
            terminer_generateur(tour_des_monstres())
            if Jeu.attaques_restantes_joueur <= -Jeu.ATTAQUES_PAR_TOUR:
                Jeu.attaques_restantes_joueur = Jeu.ATTAQUES_PAR_TOUR
            continue
        
        joueur.gerer_dessin_infos_cartes()
        for event in pygame.event.get():
            interruption = reagir_appui_touche_choix_attaque(event)
            if interruption is not None:
                break
            
            if event.type == pygame.MOUSEMOTION:
                joueur.lever_carte_du_dessus(event.pos)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                index_carte : Optional[int] = joueur.index_carte_du_dessus(event.pos)
                if index_carte is None:
                    continue
                
                joueur.attaquer(Monstre.vivants()[0].id, index_carte)        # TODO: Ew.
                
                Jeu.attaques_restantes_joueur -= 1
                logging.debug(f"Il reste {Jeu.attaques_restantes_joueur} attaques au joueur.")
                Jeu.reset_etat()
                break
        
        rafraichir_ecran_combat()
    
    if Jeu.decision_etat_en_cours():
        Jeu.changer_etat(Jeu.Etat.AFFICHAGE_ATTAQUE)

def affichage_attaque() -> None:
    logging.debug(f"Activation de l'état {Jeu.Etat.AFFICHAGE_ATTAQUE.name}.")
    
    if Carte.derniere_enregistree is None:
        raise RuntimeError("Il n'y a aucune dernière attaque alors que l'état AFFICHAGE_ATTAQUE est actif.")
    # joue l'animation de l'attaque
    interruption : Optional[Interruption] = None
    while Carte.derniere_enregistree.est_affiche:
        Jeu.commencer_frame()
        if interruption is not None:
            terminer_interruption(interruption)
        
        # Ce n'est pas sûr que les cartes soient dans cet état apparament
        Carte.derniere_enregistree.anim_etat = CarteAnimEtat.JOUER
        
        skip : bool = False
        for ev in pygame.event.get():
            if testeur_skip(ev):
                skip = True
                continue
            
            if ev.type == pygame.MOUSEMOTION:
                joueur.lever_carte_du_dessus(ev.pos)
                continue
            
            interruption = reagir_appui_touche(ev)
        
        if skip:
            Carte.derniere_enregistree.skip_animation()
        
        rafraichir_ecran_combat()
    rafraichir_ecran_combat()   # comme ça on a pas de dernière frame moche
    
    # Vérifie si c'est la fin du combat
    if not joueur.en_vie:
        Jeu.a_gagne = False
        Jeu.changer_etat(Jeu.Etat.GAME_OVER)
        return
    
    # Si c'est la fin
    # fait gagner les pieces
    pieces_gagnees : int = 0
    for monstre in Entite.tuer_les_entites_mortes():
        if type(monstre) is Monstre:
            pieces_gagnees += 2**monstre.rang + random.randint(1, 4)  # Dites non au décalage de bit et exponentiez
        elif type(monstre) is Boss:
            pieces_gagnees += 10**monstre.rang + random.randint(5, 10)
        else:
            raise TypeError(f"On veut exécuter les monstres/boss morts mais il y a un innocent parmis eux de type {type(monstre)}: {monstre}.")
    
    # Animation pièces
    if pieces_gagnees != 0:
        joueur.gagner_pieces(pieces_gagnees)
        terminer_interruption(animation_argent_gagne(pieces_gagnees))
    
    # Passage au prochain combat
    if len(Monstre.vivants()) == 0:
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
    
    LARGEUR_BOUTONS : int = 400
    HAUTEUR_BOUTONS : int = 120
    
    DIMENSIONS_BOUTONS : tuple[tuple[int, int, int, int], ...] = (
        centrer_pos((Jeu.pourcentage_largeur(50), Jeu.pourcentage_hauteur(30), LARGEUR_BOUTONS, HAUTEUR_BOUTONS)),
        centrer_pos((Jeu.pourcentage_largeur(50), Jeu.pourcentage_hauteur(50), LARGEUR_BOUTONS, HAUTEUR_BOUTONS)),
        centrer_pos((Jeu.pourcentage_largeur(50), Jeu.pourcentage_hauteur(70), LARGEUR_BOUTONS, HAUTEUR_BOUTONS)),
    )
    boutons_menu : tuple[Bouton, ...] = (
        Bouton(DIMENSIONS_BOUTONS[0], "Jouer"     , epaisseur_ligne=0, action=lambda: Jeu.changer_etat(Jeu.Etat.PREPARATION)),#group_name="Ecran titre", group_color=VERT,
        Bouton(DIMENSIONS_BOUTONS[1], "Paramètres", epaisseur_ligne=0, action=lancer_parametres),                             #group_name="Ecran titre",
        Bouton(DIMENSIONS_BOUTONS[2], "Crédits"   , epaisseur_ligne=0, action=lambda: Jeu.changer_etat(Jeu.Etat.CREDITS)),    #group_name="Ecran titre",
    )
    #ButtonCursor.enable_drawing("Ecran titre")
    
    
    dessiner_fond_ecran = dessiner_gif(
        0,
        f"{Chemins.ANIM}fond/frame *.png",
        Duree(s=.1),
        pos=(0, 0),
        en_boucle=True,
        etendre=True
    )
    while Jeu.etat == Jeu.Etat.ECRAN_TITRE:
        Jeu.commencer_frame()
        
        for event in pygame.event.get():
            if event.type != pygame.MOUSEBUTTONDOWN:
                continue
            for butt in boutons_menu:
                butt.check_click(event.pos)
        
        next(dessiner_fond_ecran)
        for bouton in boutons_menu:
            bouton.dessiner(0, point_size=90)
        
        Jeu.display_flip()
    
    if Jeu.etat != Jeu.Etat.CREDITS:
        Jeu.changer_etat(Jeu.Etat.PREPARATION)

def credits(duree : Duree = Duree(s=5)) -> None:
    logging.debug(f"Activation de l'état {Jeu.Etat.CREDITS.name}.")
    if duree == Duree(s=0):
        return
    
    texte_credits  : Surface = Jeu.construire_police(Polices.TEXTE, 10).render("Développé par Jules, Lucas", True, BLANC)
    texte_credits2 : Surface = Jeu.construire_police(Polices.TEXTE, 6).render("et Nils", True, BLANC)
    
    deplacement : Deplacement = Deplacement(
        Pos(Jeu.pourcentage_largeur(50), Jeu.hauteur),
        Pos(Jeu.pourcentage_largeur(50), - texte_credits2.height - 20),  # pour laisser le "et Nils" aller hors écran
    )
    
    debut : Duree = copy(Jeu.duree_execution)
    while not testeur_skip() and Jeu.duree_execution < debut + duree:
        Jeu.commencer_frame()
        
        pos = deplacement.calculer_valeur((Jeu.duree_execution - debut) / duree)
        
        Jeu.fenetre.fill(NOIR)
        blit_centre(Jeu.fenetre, texte_credits , pos.tuple)
        blit_centre(Jeu.fenetre, texte_credits2, (pos + Vecteur(0, texte_credits2.height + 10)).tuple)
        
        Jeu.display_flip()
    Jeu.changer_etat(Jeu.precedent_etat)

def game_over() -> None:
    logging.debug("")
    logging.debug("")
    logging.debug(f"Activation de l'état {Jeu.Etat.GAME_OVER.name}.")
    
    ecran_gen : Interruption = fin_partie(0, Jeu.a_gagne)
    if Jeu.a_gagne:
        Jeu.set_texte_fenetre("yay!")
        pygame.mixer.music.load(f"{Chemins.SFX}/victoire.wav")
    else:
        Jeu.set_texte_fenetre("...")
        pygame.mixer.music.load(f"{Chemins.SFX}/defaite.wav")
    
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play()
    while not testeur_skip():
        Jeu.commencer_frame()
        try:
            next(ecran_gen)
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
    
    if bool(params.mode_debug):
        joueur.nom = "Testeur"
    else:
        # exception au principe de la boucle principale dans l'état
        # C'est juste plus simple et propre de faire comme ça ici
        Jeu.set_texte_fenetre("Who am I?")
        terminer_interruption(demander_pseudo())
        
        Jeu.set_texte_fenetre("Chargement...")
        terminer_interruption(faux_chargement())
    
    Jeu.changer_etat(Jeu.Etat.ATTENTE_PROCHAINE_ETAPE)

def shop() -> None:
    logging.debug(f"Activation de l'état {Jeu.Etat.SHOP.name}.")
    Jeu.set_texte_fenetre("I like shopping")
    
    INVENTAIRE_EPAISSEUR_TRAIT : int = 2
    INVENTAIRE_LARGEUR         : int = Jeu.pourcentage_largeur(10) + INVENTAIRE_EPAISSEUR_TRAIT
    INVENTAIRE_BOITE           : Rect = Rect(
        Jeu.largeur - INVENTAIRE_LARGEUR + INVENTAIRE_EPAISSEUR_TRAIT,
        -INVENTAIRE_EPAISSEUR_TRAIT,
        INVENTAIRE_LARGEUR,
        Jeu.hauteur + INVENTAIRE_EPAISSEUR_TRAIT * 2
    )
    
    # nombre d'éléments -> listes des abscisses (en pourcentage de largeur)
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
    def nouv_items() -> list[Item]:
        gen_item = Item.generateur_items(consecutifs_differents=True)
        return [next(gen_item) for _ in range(random.randint(2, 3))]
    items : list[Item] = nouv_items()
    
    bouton_sortie : Bouton = Bouton(
        (
            *Jeu.pourcentages_coordonnees(2, 2, ret_pos=False),
            Jeu.pourcentage_largeur(4), Jeu.pourcentage_largeur(4),
        ),
        img=f"{Chemins.IMG}retour.png",
        action=Jeu.reset_etat,
    )
    
    premiere_frame : bool = True
    interruption : Optional[bool|Interruption] = None
    
    radio = gerer_radio()
    while Jeu.etat == Jeu.Etat.SHOP:
        Jeu.commencer_frame()
        
        for ev in pygame.event.get():
            interruption = reagir_appui_touche_shop(ev, items, (0, len(ABSCISSES_ITEMS) - 1))
            if interruption is not None:
                items = nouv_items()
            
            if ev.type == pygame.MOUSEWHEEL and bool(params.mode_debug):
                dbg_shop_scroll(ev, items, ABSCISSES_ITEMS[len(items)])
            
            if ev.type == pygame.MOUSEBUTTONDOWN:
                shop_click(ev, items, bouton_sortie, ABSCISSES_ITEMS[len(items)])
        
        
        # Si il n'y a plus de musique, en charge une aléatoire.
        next(radio)
        rafraichir_ecran_shop(
            items,
            ABSCISSES_ITEMS[len(items)],
            INVENTAIRE_BOITE,
            INVENTAIRE_EPAISSEUR_TRAIT,
            bouton_sortie,
            afficher_avertissements=premiere_frame,
        )
        premiere_frame = False
    
    if Jeu.decision_etat_en_cours():
        Jeu.num_etape += 1
        Jeu.changer_etat(Jeu.Etat.ATTENTE_PROCHAINE_ETAPE)
    
    Jeu.interrompre_musique()