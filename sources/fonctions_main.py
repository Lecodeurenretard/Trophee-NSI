"""Fonctions seulements utilisées dans main.py."""
from UI import *

def quit(exit_code : int = 0) -> NoReturn:
    pygame.quit()
    sys.exit(exit_code)

def fin_partie(gagne : bool) -> None:
    couleur_fond : rgb
    texte_fin : Surface
    if gagne:
        couleur_fond = VERT
        texte_fin = POLICE_TITRE.render("Vous avez gagné !", True, NOIR)
        logging.info("Vous avez gagné !")
    else:
        couleur_fond = BLEU_CLAIR
        texte_fin = POLICE_TITRE.render("Vous avez perdu !", True, NOIR)
        logging.info("Vous avez perdu...")
    
    fenetre.fill(couleur_fond)
    blit_centre(fenetre, texte_fin, CENTRE_FENETRE)
    pygame.display.flip()
    
    attendre = pause(Duree(s=2))
    while not next(attendre):
        commencer_frame()
    
    if param.fermer_a_la_fin.case_cochee:
        quit()
    
    globales.menu_running = True


def reset_monstre() -> None:
    for monstre in Monstre.monstres_en_vie:
        monstre.meurt()
        # monstre sera détruit par le garbage collector
    Monstre.spawn()

def fin_combat() -> bool:
    if globales.nbr_combat >= MAX_COMBAT:
        fin_partie(gagne=True)
        return True
    
    nouveau_combat(globales.nbr_combat + 1)
    return False

def nouveau_combat(numero_combat : int, reset_joueur : bool = False) -> Generator[Surface, None, None]:
    if not (1 <= numero_combat <= MAX_COMBAT):
        raise ValueError(f"`numero_combat` ({numero_combat}) doit être compris dans [1; {MAX_COMBAT}].")
    globales.nbr_combat = numero_combat
    
    globales.tour_joueur = True
    
    reset_monstre()
    if reset_joueur:
        joueur.reset_vie()
    
    return ecran_nombre_combat()

def reagir_appui_touche(ev) -> Optional[Interruption]:
    from fonctions_boutons import menu_parametres
    
    assert(ev.type == pygame.KEYDOWN), "L'évènement passé à reagir_appui_touche() n'est pas un appui de bouton."
    match ev.key:        # Un event ne peut être qu'une seule touche à la fois
        case globales.UI_TOUCHES_INFOS:
            return afficher_info()
        
        case globales.UI_TOUCHE_SETTINGS:
            return menu_parametres()
    
    if not param.mode_debug.case_cochee:
        return
    match ev.key:
        case globales.DBG_TOUCHE_CRIT:    # encore un moment où python ne fait sens: https://stackoverflow.com/questions/77164443/why-does-my-match-case-statement-not-work-for-class-members
            Attaque.toujours_crits = not Attaque.toujours_crits
            return
        
        case globales.DBG_TOUCHE_PREDECENT_MONSTRE:
            if not Monstre.monstres_en_vie[0].vers_type_precedent():
                logging.warning("Le monstre n'a pas de type!")
            return
       
        case globales.DBG_TOUCHE_PROCHAIN_MONSTRE:
            if not Monstre.monstres_en_vie[0].vers_type_suivant():
                logging.warning("Le monstre n'a pas de type!")
            return
        
        case globales.DBG_TOUCHE_PRECEDENT_COMBAT:
            globales.nbr_combat -= 1
            changer_etat(EtatJeu.ATTENTE_NOUVEAU_COMBAT)
            return
        
        case globales.DBG_TOUCHE_PROCHAIN_COMBAT:
            globales.nbr_combat += 1
            changer_etat(EtatJeu.ATTENTE_NOUVEAU_COMBAT)
            return