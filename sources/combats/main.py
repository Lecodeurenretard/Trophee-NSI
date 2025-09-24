from fonctions_boutons import *
import etats_jeu as GameState
from etats_jeu import (
    EtatJeu,
    changer_etat,
    attente_nouveau_combat, choix_attaque, ecran_titre,
)


def jeu() -> None:
    global etat_du_jeu
    
    joueur.reset_vie()
    reset_monstre()
    
    anim_gen : list[Generator] = []
    while True:
        rafraichir_ecran(generateurs_dessin=anim_gen)
        commencer_frame()
        
        for event in pygame.event.get():
            verifier_pour_quitter(event)
            if (event.type != pygame.KEYDOWN and event.type != pygame.MOUSEBUTTONDOWN) or not globales.tour_joueur:
                continue
            
            # Si le joueur attaque...
            if ButtonCursor.handle_inputs(boutons_attaques, event):
                globales.tour_joueur = False
                continue
            
            if event.type == pygame.KEYDOWN:
                reagir_appui_touche(event)
                continue
        
        match GameState.etat_du_jeu:
            case EtatJeu.ATTENTE_NOUVEAU_COMBAT:
                attente_nouveau_combat()
            case EtatJeu.CHOIX_ATTAQUE:
                choix_attaque()
            case _:
                raise NotImplementedError(f"Etat `{GameState.etat_du_jeu.name}` non implémenté dans jeu().")
        
        
        iter += 1
        Monstre.tuer_les_monstres_morts()
        if len(Monstre.monstres_en_vie) == 0:
            if fin_combat():
                return
            continue
        
        if not globales.tour_joueur:
            monstres_attaquent()
            anim_gen.append(
                Attaque.lancer_toutes_les_attaques_gen(fenetre)
            )
            
            globales.tour_joueur = True
        
        if joueur.est_mort:
            fin_partie(gagne=False)
            return

def __main__() -> None:
    changer_etat(EtatJeu.ECRAN_TITRE)
    
    reset_monstre()
    while True:
        ecran_titre()
        jeu()

# N'éxecute le programme que si on le lance depuis ce fichier
if __name__ == "__main__":
    __main__()