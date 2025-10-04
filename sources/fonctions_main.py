"""Fonctions seulements utilisées dans main.py."""
from UI import *

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
    
    image : Surface = Surface((Jeu.LARGEUR, Jeu.HAUTEUR))
    image.fill(couleur_fond)
    blit_centre(image, texte_fin, Jeu.CENTRE_FENETRE)
    
    return image_vers_generateur(image, Duree(s=2), gerer_evenements=True)


def reset_monstre() -> None:
    for monstre in Monstre.monstres_en_vie:
        monstre.meurt()
        # monstre sera détruit par le garbage collector
    Monstre.spawn()

def fin_combat() -> bool:
    if Jeu.num_combat >= Jeu.MAX_COMBAT:
        fin_partie(gagne=True)
        return True
    
    nouveau_combat(Jeu.num_combat + 1)
    return False

def nouveau_combat(numero_combat : int, reset_joueur : bool = False) -> Generator[Surface, None, None]:
    if not (1 <= numero_combat <= Jeu.MAX_COMBAT):
        raise ValueError(f"`numero_combat` ({numero_combat}) doit être compris dans [1; {Jeu.MAX_COMBAT}].")
    Jeu.num_combat = numero_combat
    
    reset_monstre()
    if reset_joueur:
        joueur.reset_vie()
    
    return ecran_nombre_combat()

def reagir_appui_touche(ev) -> Optional[Interruption]:
    from fonctions_boutons import menu_parametres
    import Constantes as c
    
    assert(ev.type == pygame.KEYDOWN), "L'évènement passé à reagir_appui_touche() n'est pas un appui de bouton."
    match ev.key:        # Un event ne peut être qu'une seule touche à la fois
        case c.Touches.INFOS:
            return afficher_info()
        
        case c.Touches.SETTINGS:
            return menu_parametres()
    
    if not param.mode_debug.case_cochee:
        return
    match ev.key:
        case c.Touches.DBG_CRIT:    # encore un moment où python ne fait sens: https://stackoverflow.com/questions/77164443/why-does-my-match-case-statement-not-work-for-class-members
            Attaque.toujours_crits = not Attaque.toujours_crits
            return
        
        case c.Touches.DBG_PREDECENT_MONSTRE:
            if not Monstre.monstres_en_vie[0].vers_type_precedent():
                logging.warning("Le monstre n'a pas de type!")
            return
       
        case c.Touches.DBG_PROCHAIN_MONSTRE:
            if not Monstre.monstres_en_vie[0].vers_type_suivant():
                logging.warning("Le monstre n'a pas de type!")
            return
        
        case c.Touches.DBG_PRECEDENT_COMBAT:
            Jeu.num_combat -= 1
            Jeu.changer_etat(Jeu.Etat.ATTENTE_NOUVEAU_COMBAT)
            return
        
        case c.Touches.DBG_PROCHAIN_COMBAT:
            Jeu.num_combat += 1
            Jeu.changer_etat(Jeu.Etat.ATTENTE_NOUVEAU_COMBAT)
            return