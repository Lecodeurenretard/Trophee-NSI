"""Fonctions seulements utilisées dans fonctions_etat.py."""
from fonctions_boutons import *
from Item import Item
from Carte import Carte
from Monstre import Monstre

def quit(exit_code : int = 0) -> NoReturn:
    pygame.quit()
    sys.exit(exit_code)

def fin_partie(num_couche : int, gagne : bool) -> Interruption:
    couleur_fond : rgb
    texte_fin : str
    if gagne:
        couleur_fond = VERT
        texte_fin = "Vous avez gagné !"
    else:
        couleur_fond = BLEU_CLAIR
        texte_fin = "Vous avez perdu !"
    
    logging.info(texte_fin)
    texte_fin_render = Jeu.construire_police(Polices.TEXTE, 20).render(texte_fin, True, NOIR)
    
    image : Surface = Surface((Jeu.largeur, Jeu.hauteur))
    image.fill(couleur_fond)
    blit_centre(image, texte_fin_render, Jeu.centre_fenetre)
    
    return blit_generateur(num_couche, image, Duree(s=2), gerer_evenements=True)



def victoire_joueur() -> bool:
    return Jeu.num_etape >= Jeu.COMBAT_MAX

def initialiser_nouveau_combat(numero_combat : int, reset_joueur : bool = False) -> None:
    if not (1 <= numero_combat <= Jeu.COMBAT_MAX):
        raise ValueError(f"`numero_combat` ({numero_combat}) doit être compris dans [1; {Jeu.COMBAT_MAX}].")
    Jeu.num_etape = numero_combat
    
    Jeu.nb_tours_combat = 0
    Jeu.attaques_restantes_joueur = Jeu.ATTAQUES_PAR_TOUR
    
    Carte.derniere_enregistree = None
    Attaque.attaques_jouees.clear()
    
    Monstre.massacre()
    Monstre.spawn()
    
    if reset_joueur:
        joueur.reset()
    Carte.vider_cartes_affichees()

def reagir_appui_touche(ev : pygame.event.Event) -> Optional[Interruption]:
    if ev.type != pygame.KEYDOWN:
        return
    
    match ev.key:
        case Touches.PARAMETRES:
            return menu_parametres()
    
    if not params.mode_debug.case_cochee:
        return
    match ev.key:
        case Touches.DBG_CRIT:
            Attaque.toujours_crits = not Attaque.toujours_crits
            return
        
        case Touches.DBG_PRECEDENT_COMBAT:
            Jeu.num_etape -= 1
            if Jeu.num_etape < 1: 
                Jeu.num_etape = Jeu.COMBAT_MAX
            
            Jeu.changer_etat(Jeu.Etat.ATTENTE_PROCHAINE_ETAPE)
            return
        
        case Touches.DBG_PROCHAIN_COMBAT:
            Jeu.num_etape += 1
            if Jeu.num_etape > Jeu.COMBAT_MAX: 
                Jeu.num_etape = 1
            
            Jeu.changer_etat(Jeu.Etat.ATTENTE_PROCHAINE_ETAPE)
        
        case Touches.DBG_SHOP:
            for i in range(Jeu.num_etape, Jeu.COMBAT_MAX):
                if Jeu.decision_shop(i):
                    Jeu.num_etape = i
                    Jeu.changer_etat(Jeu.Etat.ATTENTE_PROCHAINE_ETAPE)
                    break
            else:   # boucle for... else, le msg n'est affiché que si on ne break pas
                logging.error("Le dernier shop a été dépassé.")
                return
                
        case Touches.DBG_BOSS:
            for i in range(Jeu.num_etape, Jeu.COMBAT_MAX):
                if Jeu.decision_boss(i):
                    Jeu.num_etape = i
                    Jeu.changer_etat(Jeu.Etat.ATTENTE_PROCHAINE_ETAPE)
                    break
            else:
                logging.error("Le dernier boss a été dépassé.")
                return
            return

def reagir_appui_touche_choix_attaque(ev : pygame.event.Event) -> Optional[Interruption]:
    if ev.type != pygame.KEYDOWN:
        return
    
    interruption_potentielle = reagir_appui_touche(ev)
    if interruption_potentielle is not None:
        return interruption_potentielle
    
    match ev.key:
        # Il ne se passe rien sans le mode débug
        case _:
            ...
    
    if not params.mode_debug.case_cochee:
        return
    match ev.key:
        case Touches.DBG_REROLL:
            joueur.repiocher_tout()
        
        case Touches.DBG_PREDECENT_MONSTRE:
            Monstre.vivants()[0].vers_type_precedent()
            return
       
        case Touches.DBG_PROCHAIN_MONSTRE:
            Monstre.vivants()[0].vers_type_suivant()
            return
            
            
            logging.info(f"Skip jusqu'au combat {Jeu.num_etape}.")
            Jeu.changer_etat(Jeu.Etat.SHOP)
            return

def reagir_appui_touche_shop(ev : pygame.event.Event, lst_items : list['Item'],  min_max_items : tuple[int, int]) -> Optional[Interruption|bool]:
    """
    S'occupe des évènements d'appuie de touche.
    Renvoie None si l'évènement n'est pas un appui de touche ou si l'appui n'a plus d'effet après la fonction,
    renvoie une Interruption si `reagir_appui_touche()` en renvoie une,
    renvoie True s'il faut reroll les items du shop.
    """
    if ev.type != pygame.KEYDOWN:
        return
    
    interruption_potentielle = reagir_appui_touche(ev)
    if interruption_potentielle is not None:
        return interruption_potentielle
    
    # Les cas sans le debug sont traités dans reagir_appui_touche()
    ...
    
    if not bool(params.mode_debug):
        return None
    
    if ev.key in Touches.DBG_SHOP_AJOUT_ITEM and len(lst_items) < min_max_items[1]:
        lst_items.append(Item.item_aleatoire())
    
    elif ev.key in Touches.DBG_SHOP_SUPPRESSION_ITEM and len(lst_items) > min_max_items[0]:
        lst_items.pop()
    
    elif ev.key == Touches.DBG_REROLL:
        return True

def animation_argent_gagne(montant : int, num_couche : int = 0, duree : Duree = Duree(s=1)) -> Interruption:
    TEXTE_AFFICHE : str  = f"{montant:+} pieces"
    POLICE        : Font = Jeu.construire_police(Polices.FOURRE_TOUT, 10)
    POLICE.set_italic(True)
    
    espacement_bord : int = POLICE.size(TEXTE_AFFICHE)[0] + Jeu.pourcentage_largeur(1)
    
    nb_frames : int = round(Jeu.framerate * duree.secondes)
    
    deplacement = Deplacement.generateur_s(
        Pos(Jeu.largeur - espacement_bord, Jeu.pourcentage_hauteur(10)),
        Pos(Jeu.largeur - espacement_bord, Jeu.pourcentage_hauteur(0)),
        nb_frames,
        easing_fun=Easing.NO_EASING,
    )
    
    # La courbe de la transparence ressemblera
    # à une courbe en cloche aplatie
    transparence = MultiInterpolation.generateur_s(
        [0, 220, 220, 0],
        [.3, .7],
        nb_frames,
        easing_funs=[Easing.FADE_IN, Easing.FADE, Easing.FADE_OUT,],
    )
    
    # Animation
    fond = copy(Jeu.fenetre)
    for pos, alpha in zip(deplacement, transparence):
        if testeur_skip():
            break
        
        a_dessiner = POLICE.render(TEXTE_AFFICHE, True, JAUNE_PIECE)
        a_dessiner.set_alpha(round(alpha))
        
        Jeu.blit_couche(num_couche, fond)
        Jeu.blit_couche(num_couche, a_dessiner, pos.tuple)
        
        try:
            yield
        except GeneratorExit:
            break

def dbg_shop_scroll(ev : pygame.event.Event, items : list[Item], abcisses : tuple[int, ...]) -> None:
    """Fonction à appeler quand le testeur scroll dans le shop."""
    sensibilite_scroll : float = 1
    
    index = Item.item_survole(items, abcisses)
    if index is None:
        return
    
    changement : int = round(ev.precise_y * sensibilite_scroll)
    items[index] = Item(items[index].id + changement, permissif=True)

def shop_click(ev : pygame.event.Event, items : list[Item], bouton_sortie : Bouton, abcisses : tuple[int, ...]):
    """Fonction à appeler quand le joueur/testeur clique dans le shop."""
    if ev.button in (4, 5): # empèche le scroll de compter pour un click
        return
    
    if bouton_sortie.check_click(pygame.mouse.get_pos()):
        return
    
    index = Item.item_survole(items, abcisses)
    if index is None:
        return
    
    if joueur.paiement(items[index].prix, payer_max=False) > 0:
        pass    # Ajouter animation
        return
    
    son_paiment = Sound(f"{Chemins.SFX}/argent2.wav")
    son_paiment.play()
    
    joueur.prendre_item(items[index])
    items.pop(index)

def tour_des_monstres() -> Generator[None, None, None]:
    joueur.main_jouer_sortir()
    for monstre in Monstre.vivants():
        monstre.main_jouer_entrer()
    
    # laisse le temps au cartes d'entrer
    # (encore un fois, on considère qu'ils arrivent tous au même moment)
    while not Monstre.vivants()[0].cartes_main_sont_a_pos_defaut:
        Jeu.commencer_frame()
        verifier_pour_quitter()
        
        rafraichir_ecran_combat()
        Jeu.display_flip()
        yield
    
    # fait attaquer les monstres
    for monstre in Monstre.vivants():
        monstre.attaquer(joueur.id, monstre.choisir_index_carte_main())
    
    Jeu.reset_etat()
    Jeu.attaques_restantes_joueur -= 1