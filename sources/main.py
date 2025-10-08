from fonctions_boutons import *
from fonctions_etats import (
    ecran_titre,
    credits,
    attente_nouveau_combat,
    choix_attaque,
    affichage_attaques,
    fin_jeu,
)


def jeu() -> None:
    Jeu.changer_etat(Jeu.Etat.ECRAN_TITRE)
    
    joueur.reset_vie()
    reset_monstre()
    
    while True:
        match Jeu.etat:
            case Jeu.Etat.ECRAN_TITRE:
                ecran_titre()
            
            case Jeu.Etat.CREDITS:
                credits()
            
            case Jeu.Etat.ATTENTE_NOUVEAU_COMBAT:
                attente_nouveau_combat()
            
            case Jeu.Etat.CHOIX_ATTAQUE:
                choix_attaque()
            
            case Jeu.Etat.AFFICHAGE_ATTAQUES:
                affichage_attaques()
            
            case Jeu.Etat.FIN_JEU:
                fin_jeu()
            
            case _:
                raise NotImplementedError(f"Etat `{Jeu.etat.name}` non implémenté dans jeu().")

# N'éxecute le programme que si on le lance depuis ce fichier
if __name__ == "__main__":
    jeu()