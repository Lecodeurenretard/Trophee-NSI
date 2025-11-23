"""Fonctions seulements utilisées dans fonctions_etat.py."""
from fonctions_boutons import *
from Item import Item
from Carte import Carte

def quit(exit_code : int = 0) -> NoReturn:
    pygame.quit()
    exit(exit_code)

def fin_partie(gagne : bool) -> Interruption:
    couleur_fond : rgb
    texte_fin : Surface
    if gagne:
        couleur_fond = VERT
        texte_fin = Constantes.Polices.TITRE.render("Vous avez gagné !", True, NOIR)
        logging.info("Vous avez gagné !")
    else:
        couleur_fond = BLEU_CLAIR
        texte_fin = Constantes.Polices.TITRE.render("Vous avez perdu !", True, NOIR)
        logging.info("Vous avez perdu...")
    
    image : Surface = Surface((Jeu.largeur, Jeu.hauteur))
    image.fill(couleur_fond)
    blit_centre(image, texte_fin, Jeu.centre_fenetre)
    
    return image_vers_generateur(image, Duree(s=2), gerer_evenements=True)


def reset_monstre() -> None:
    for monstre in Monstre.monstres_en_vie:
        monstre.meurt()
        # monstre sera détruit par le garbage collector
    Monstre.spawn()

def victoire_joueur() -> bool:
    return Jeu.num_etape >= Jeu.MAX_COMBAT

def initialiser_nouveau_combat(numero_combat : int, reset_joueur : bool = False) -> None:
    if not (1 <= numero_combat <= Jeu.MAX_COMBAT):
        raise ValueError(f"`numero_combat` ({numero_combat}) doit être compris dans [1; {Jeu.MAX_COMBAT}].")
    Jeu.num_etape = numero_combat
    
    Jeu.attaques_restantes_joueur = Jeu.ATTAQUES_PAR_TOUR
    
    Carte.derniere_enregistree = None
    Attaque.attaques_jouees.clear()
    
    reset_monstre()
    if reset_joueur:
        joueur.reset()

def reagir_appui_touche(ev : pygame.event.Event) -> Optional[Interruption]:
    if ev.type != pygame.KEYDOWN:
        return
    
    match ev.key:
        case Constantes.Touches.SETTINGS:
            return menu_parametres()
    
    if not params.mode_debug.case_cochee:
        return
    match ev.key:
        case Constantes.Touches.DBG_CRIT:
            Attaque.toujours_crits = not Attaque.toujours_crits
            return
        
        case Constantes.Touches.DBG_PRECEDENT_COMBAT:
            Jeu.num_etape -= 1
            if Jeu.num_etape < 1: 
                Jeu.num_etape = Jeu.MAX_COMBAT
            
            Jeu.changer_etat(Jeu.Etat.ATTENTE_PROCHAINE_ETAPE)
            return
        
        case Constantes.Touches.DBG_PROCHAIN_COMBAT:
            Jeu.num_etape += 1
            if Jeu.num_etape > Jeu.MAX_COMBAT: 
                Jeu.num_etape = 1
            
            Jeu.changer_etat(Jeu.Etat.ATTENTE_PROCHAINE_ETAPE)
            return

def reagir_appui_touche_choix_attaque(ev : pygame.event.Event) -> Optional[Interruption]:
    if ev.type != pygame.KEYDOWN:
        return
    
    potentielle_interruption = reagir_appui_touche(ev)
    if potentielle_interruption is not None:
        return potentielle_interruption
    
    match ev.key:        # Un event ne peut être qu'une seule touche à la fois
        case Constantes.Touches.INFOS:
            return afficher_infos()
    
    if not params.mode_debug.case_cochee:
        return
    match ev.key:
        case Constantes.Touches.DBG_PREDECENT_MONSTRE:
            if not Monstre.monstres_en_vie[0].vers_type_precedent():
                logging.warning("Le monstre n'a pas de type!")
            return
       
        case Constantes.Touches.DBG_PROCHAIN_MONSTRE:
            if not Monstre.monstres_en_vie[0].vers_type_suivant():
                logging.warning("Le monstre n'a pas de type!")
            return
        
        case Constantes.Touches.DBG_SHOP:
            for i in range(Jeu.num_etape, Jeu.MAX_COMBAT):
                if Jeu.DECISION_SHOP(i):
                    Jeu.num_etape = i
                    break
            else:   # for... else, si jamis le break n'est jamais atteint
                logging.error("Le dernier shop a été dépassé.")
                return
            
            
            logging.info(f"Skip jusqu'au combat {Jeu.num_etape}.")
            Jeu.changer_etat(Jeu.Etat.SHOP)
            return

def animation_argent_gagne(montant : int, arriere_plan : Surface = Jeu.fenetre, duree : Duree = Duree(s=1)) -> Interruption:
    arriere_plan = copy(arriere_plan)
    TEXTE_AFFICHE : str = f"+{montant} pieces"
    
    # il y a plus efficace mais "the only thing better than good is good enough"
    espacement_bord : int = Constantes.Polices.FOURRE_TOUT.render(TEXTE_AFFICHE, True, JAUNE).get_rect().width + 50    # et c'est "good enough"
    
    nb_frames : int = round(Jeu.framerate * duree.secondes)
    
    deplacement = Deplacement.generateur_s(
        Pos(Jeu.largeur - espacement_bord, Jeu.pourcentage_hauteur(10)),
        Pos(Jeu.largeur - espacement_bord, Jeu.pourcentage_hauteur(0)),
        nb_frames,
        easing_fun=Easing.NO_EASING,
    )
    
    transparence = MultiInterpolation.generateur_s(
        [0, 220, 220, 0],
        [.3, .7],
        nb_frames,
        easing_funs=[Easing.FADE_IN, Easing.FADE, Easing.FADE_OUT,],
    )
    
    # Animation
    for pos, alpha in zip(deplacement, transparence):
        Jeu.commencer_frame()
        if testeur_skip_ou_quitte():
            break
        
        a_dessiner = Constantes.Polices.FOURRE_TOUT.render(TEXTE_AFFICHE, True, JAUNE_PIECE)
        a_dessiner.set_alpha(round(alpha))
        
        image = copy(arriere_plan)
        image.blit(a_dessiner, pos.tuple)
        
        try:
            yield image
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

def shop_click(ev : pygame.event.Event, items : list[Item], bouton_sortie : Button, abcisses : tuple[int, ...]):
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
    
    son_paiment = Sound(f"{Constantes.Chemins.SFX}/argent2.wav")
    son_paiment.play()
    
    joueur.prendre_item(items[index])
    items.pop(index)

def dessiner_nombre_pieces(boite_inventaire : Rect, ordonnees : int = Jeu.pourcentage_hauteur(5)) -> None:
    if params.argent_infini.case_cochee:
        dessiner_texte(
            Jeu.menus_surf,
            "genre, beaucoup de p",
            JAUNE_PIECE,
            (
                boite_inventaire.left + 10, ordonnees,
                boite_inventaire.width, ordonnees + Jeu.pourcentage_hauteur(5)
            ),
            Constantes.Polices.TEXTE,
            True,
        )
    else:
        TEXTE_PIECES = Constantes.Polices.TEXTE.render(
            f"{joueur.nb_pieces}p",
            True, JAUNE_PIECE,
        )
        Jeu.menus_surf.blit(TEXTE_PIECES, (
            boite_inventaire.left + boite_inventaire.width // 2,
            ordonnees,
        ))

def dessiner_inventaire(surface : Surface, boite_inventaire : Rect) -> None:
    y : int = Jeu.pourcentage_hauteur(5) + 55
    for item in joueur.inventaire:
        icone : Surface = pygame.transform.scale_by(
            item.sprite,
            (boite_inventaire.width - 20) / item.sprite.get_rect().width
        )
        
        surface.blit(
            icone,
            (boite_inventaire.left, y)
        )
        y += icone.get_bounding_rect().height + 10