from Parametres import *

_HAUTEUR_PREMIER_PARAMETRE : int = Jeu.pourcentage_hauteur(11)
_ECART_ENTRE_PARAMETRES : int = Jeu.pourcentage_hauteur(1)
_ECART_ENTRE_SECTIONS   : int = Jeu.pourcentage_hauteur(7)

def _generer_menu_pos() -> Generator[int, int, NoReturn]:
    h = _HAUTEUR_PREMIER_PARAMETRE
    while True:
        h += _ECART_ENTRE_PARAMETRES + (yield h)
        # La ligne du dessus ajoute la position envoyée par l'utilisateur avec la position interne
        # pour plus de détails recherchez l'utilisation des générateurs en Python et l'utilisation de .send()
menu_h = _generer_menu_pos()
next(menu_h)    # https://stackoverflow.com/questions/19892204/send-method-using-generator-still-trying-to-understand-the-send-method-and-quir

# paramètres normaux
fermer_a_la_fin : Parametre = Parametre(
    "Fermeture automatique",
    menu_h.send(TypeParametre.CASE_A_COCHER.hauteur),
    TypeParametre.CASE_A_COCHER,
    False,
)

def _on_mode_debug_change(nouvelle_valeur : bool) -> None:
    if nouvelle_valeur:
        logging.basicConfig(level=logging.DEBUG, force=True)
    else:
        logging.basicConfig(level=logging.INFO, force=True)

mode_debug : Parametre = Parametre(
    "Mode développeur",
    menu_h.send(TypeParametre.CASE_A_COCHER.hauteur),
    TypeParametre.CASE_A_COCHER,
    False,
    on_change=_on_mode_debug_change, # type: ignore # on est certain que la valeur passée est un booléen
)
_on_mode_debug_change(bool(mode_debug))


# paramètres de triche
menu_h.send(_ECART_ENTRE_SECTIONS)

joueur_invincible = Parametre(
    "joueur invicible",
    menu_h.send(TypeParametre.CASE_A_COCHER.hauteur),
    TypeParametre.CASE_A_COCHER,
    False,
)

argent_infini = Parametre(
    "Argent illimité",
    menu_h.send(TypeParametre.CASE_A_COCHER.hauteur),
    TypeParametre.CASE_A_COCHER,
    False,
)




PARAMETRES_NORMAUX : list[Parametre] = [
    fermer_a_la_fin,
    mode_debug,
]

PARAMETRES_TRICHE : list[Parametre] = [
    joueur_invincible,
    argent_infini,
]
