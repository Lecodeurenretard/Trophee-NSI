import parametres_vars as params
from imports import afficher_erreur, NoReturn
from Jeu import Jeu
import pygame

from fonctions_etats import (
    ecran_titre,
    credits,
    preparation,
    attente_prochaine_etape,
    choix_attaque,
    affichage_attaque,
    game_over,
    shop,
)


def jeu() -> NoReturn:
    Jeu.changer_etat(Jeu.Etat.ECRAN_TITRE)
    Jeu.lire_parametres()
    
    while True:
        pygame.event.clear()    # il ne faut pas que les évènements transitent entre les états
        match Jeu.etat:
            case Jeu.Etat.ECRAN_TITRE:
                ecran_titre()
            
            case Jeu.Etat.CREDITS:
                credits()
            
            case Jeu.Etat.PREPARATION:
                preparation()
            
            case Jeu.Etat.ATTENTE_PROCHAINE_ETAPE:
                attente_prochaine_etape()
            
            case Jeu.Etat.SHOP:
                shop()
            
            case Jeu.Etat.CHOIX_ATTAQUE:
                choix_attaque()
            
            case Jeu.Etat.AFFICHAGE_ATTAQUE:
                affichage_attaque()
            
            case Jeu.Etat.GAME_OVER:
                game_over()
            
            case _:
                raise NotImplementedError(f"Etat `{Jeu.etat.name}` non implémenté dans jeu().")

# N'exécute le programme que si on le lance depuis ce fichier
if __name__ == "__main__":
    try:
        jeu()
    
    except (ValueError, NotImplementedError, RuntimeError, AssertionError) as err:
        # Erreurs susceptibles d'être élevées par les développeurs.
        if not bool(params.mode_debug):
            afficher_erreur("Une erreur est survenue.", f"{type(err).__name__}: {err.args[0]}")
        raise err
    
    except Exception as err:
        # Erreurs susceptibles d'être élevées par Python directement.
        if not bool(params.mode_debug):
            afficher_erreur("oups", "Le jeu est cassé, contactez un développeur.\nSi vous en êtes un, regardez la console.")
        raise err   # Comme ça la console à toutes les infos