from fonctions_boutons import *
from etats_jeu import (
    changer_etat,
    attente_nouveau_combat, choix_attaque, ecran_titre,
)


def jeu() -> None:
    joueur.reset_vie()
    reset_monstre()
    
    anim_gen : list[Generator] = []
    while True:
        commencer_frame()
        
        match globales.etat_jeu:
            case EtatJeu.ECRAN_TITRE:
                ecran_titre()
            case EtatJeu.ATTENTE_NOUVEAU_COMBAT:
                globales.nbr_combat += 1
                attente_nouveau_combat()
            case EtatJeu.CHOIX_ATTAQUE:
                choix_attaque()
            case _:
                raise NotImplementedError(f"Etat `{globales.etat_jeu.name}` non implémenté dans jeu().")
        continue
        
        
        # Je laisse tout ça ici pour pouvoir facilement les copier dans les états.
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
    while True:
        ecran_titre()
        jeu()

# N'éxecute le programme que si on le lance depuis ce fichier
if __name__ == "__main__":
    __main__()