from fonctions_boutons import *
from fonctions_etats import (
    attente_nouveau_combat, choix_attaque, ecran_titre, fin_jeu, affichage_attaques
)


def jeu() -> None:
    joueur.reset_vie()
    reset_monstre()
    
    while True:
        match Jeu.etat:
            case Jeu.Etat.ECRAN_TITRE:
                ecran_titre()
            case Jeu.Etat.ATTENTE_NOUVEAU_COMBAT:
                Jeu.num_combat += 1
                attente_nouveau_combat()
            case Jeu.Etat.CHOIX_ATTAQUE:
                choix_attaque()
            case Jeu.Etat.AFFICHAGE_ATTAQUES:
                affichage_attaques()
            case Jeu.Etat.FIN_JEU:
                fin_jeu()
            case _:
                raise NotImplementedError(f"Etat `{Jeu.etat.name}` non implémenté dans jeu().")
        continue
        
        
        # Je laisse tout ça ici pour pouvoir facilement les copier dans les états.
        Monstre.tuer_les_monstres_morts()
        if len(Monstre.monstres_en_vie) == 0:
            if fin_combat():
                return
            continue
        
        if joueur.est_mort:
            fin_partie(gagne=False)
            return

def __main__() -> None:
    while True:
        Jeu.changer_etat(Jeu.Etat.ECRAN_TITRE)
        jeu()

# N'éxecute le programme que si on le lance depuis ce fichier
if __name__ == "__main__":
    __main__()