"""Fonctions seulements utilisées dans main.py."""
from Monstre import *
from fonctions_boutons import *
from fonction_combat import *

def quit(exit_code : int = 0) -> NoReturn:
    pygame.quit()
    sys.exit(exit_code)

def fin_partie(gagne : bool) -> None:
    couleur_fond : color
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
    fenetre.blit(texte_fin, (LARGEUR // 2 - 120, HAUTEUR // 2 - 20))
    pygame.display.flip()
    
    attendre(2)
    globales.menu_running = True
    #quit()

def reset_monstre() -> None:
    for monstre in Monstre.monstres_en_vie:
        monstre.meurt()
        # monstre sera détruit par le garbage collector
        # donc pas de mem leak
    Monstre.spawn()

def fin_combat() -> None:
    if globales.nbr_combat >= MAX_COMBAT:
        fin_partie(gagne=True)
    
    nouveau_combat(globales.nbr_combat + 1)

def nouveau_combat(numero_combat : int) -> None:
    globales.nbr_combat = numero_combat % MAX_COMBAT # combat maximum == MAX_COMBAT
    if globales.nbr_combat <= 0:
        globales.nbr_combat += MAX_COMBAT   # On les ramène sur ]0; 5]
    assert(globales.nbr_combat > 0), "Réviser le calcul du numéro de combat dans `nouveau_combat()`."

    globales.tour_joueur = True
    
    reset_monstre()
    afficher_nombre_combat(globales.nbr_combat)

def reagir_appui_touche(ev):
    assert(ev.type == pygame.KEYDOWN), "L'évènement passé à reagir_appui_touche() n'est pas un appui de bouton."
    match ev.key:        # Un event ne peut être qu'une seule touche à la fois
        case pygame.K_i:
            afficher_info()
            return
        
        case globales.UI_TOUCHE_AFFICHAGE_FPS:
            globales.UI_autoriser_affichage_fps = not globales.UI_autoriser_affichage_fps       # v. pavé dans import_var
            return
        
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
            nouveau_combat(globales.nbr_combat-1)
            return
        
        case globales.DBG_TOUCHE_PROCHAIN_COMBAT:
            nouveau_combat(globales.nbr_combat+1)
            return
        
        case _:
            ...