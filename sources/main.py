from fonctions_boutons import *
from fonctions_etats import (
    Jeu,
    attente_nouveau_combat, choix_attaque, ecran_titre,
)


def jeu() -> None:
    joueur.reset_vie()
    reset_monstre()
    
    anim_gen : list[Generator] = []
    while True:
        Jeu.commencer_frame()
        
        match Jeu.etat:
            case Jeu.Etat.ECRAN_TITRE:
                ecran_titre()
            case Jeu.Etat.ATTENTE_NOUVEAU_COMBAT:
                Jeu.num_combat += 1
                attente_nouveau_combat()
            case Jeu.Etat.CHOIX_ATTAQUE:
                choix_attaque()
            case _:
                raise NotImplementedError(f"Etat `{Jeu.etat.name}` non implémenté dans jeu().")
        continue
        
        
        # Je laisse tout ça ici pour pouvoir facilement les copier dans les états.
        Monstre.tuer_les_monstres_morts()
        if len(Monstre.monstres_en_vie) == 0:
            if fin_combat():
                return
            continue
        
        if not Jeu.tour_joueur:
            monstres_attaquent()
            anim_gen.append(
                Attaque.lancer_toutes_les_attaques_gen(fenetre)
            )
            
            Jeu.tour_joueur = True
        
        if joueur.est_mort:
            fin_partie(gagne=False)
            return

def __main__() -> None:
    Jeu.changer_etat(Jeu.Etat.ECRAN_TITRE)
    while True:
        ecran_titre()
        jeu()

# N'éxecute le programme que si on le lance depuis ce fichier
if __name__ == "__main__":
    __main__()