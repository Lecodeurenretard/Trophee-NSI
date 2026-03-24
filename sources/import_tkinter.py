"""
Essaye d'importer Tkinter, s'il n'est pas trouvé, crée les fonctions nécessaires.
projet : L'ascension de Esquimot
auteur : Dooheli, Lecodeurenretard, hibou509
"""
import logging
from typing import Literal

try:
    # le message d'erreur dit que le afficher_erreur() importé n'a pas la même signature
    # que le afficher_erreur() défini en bas (ce sont des paramètre non utilisés, c'est pas grave)
    from tkinter.messagebox import showerror as afficher_erreur # pyright: ignore[reportAssignmentType]
    from tkinter.messagebox import askyesno as demander_ouinon # pyright: ignore[reportAssignmentType]

except ModuleNotFoundError:
    logging.error("Impossible d'importer tkinter.")
    # Si on ne peut pas importer tKinter (aka on est sur mon PC)
    # On crée une fonction de remplacement
    def afficher_erreur(
            title   : str | None = None,
            message : str  = '',
            *,
            icon: Literal['error', 'info', 'question', 'warning'] = 'error',
        ):
        fonction_affichage = logging.info
        if icon == "error":
            fonction_affichage = logging.error
        if icon == "info":
            fonction_affichage = logging.info
        if title is None:
            title = ''
        fonction_affichage(f"{title} ({icon}): {message}")
    
    def demander_ouinon(
        title   : str|None = None,
        message : str      = '',
        *,
        detail  : str|None = None,
    ) -> bool:
        while True:
            if title is not None:
                logging.info(title)
            
            choix_accord = ("oui", 'o')
            choix_refus = ("non", 'n')
            
            reponse : str = ''
            while reponse not in choix_accord and reponse not in choix_refus:
                reponse = input(f"{message}: ")
            return reponse in choix_accord