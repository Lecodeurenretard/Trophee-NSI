from Settings import *

_HAUTEUR_PREMIER_PARAMETRE : int = pourcentage_hauteur(11)
_ECART_ENTRE_PARAMETRES : int = 10
_ECART_ENTRE_SECTIONS   : int = 40

def _generer_menu_pos() -> Generator[int, int, NoReturn]:
    h = _HAUTEUR_PREMIER_PARAMETRE
    while True:
        h += _ECART_ENTRE_PARAMETRES + (yield h)
        # La ligne du dessus ajoute la position envoyée par l'utilisateur avec la position interne
        # pour plus de détails recherchez l'utilisation des générateurs en Python et l'utilisation de .send()
menu_h = _generer_menu_pos()
menu_h.send(None)    #type: ignore # https://stackoverflow.com/questions/19892204/send-method-using-generator-still-trying-to-understand-the-send-method-and-quir

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
    -1,
    TypeParametre.CASE_A_COCHER,
    False,
    on_change=_on_mode_debug_change # type: ignore # on est certain que la valeur pasée est un booléen
)


# paramètres de triche
menu_h.send(_ECART_ENTRE_SECTIONS)

joueur_invincible = Parametre(
    "joueur invicible",
    menu_h.send(TypeParametre.CASE_A_COCHER.hauteur),
    TypeParametre.CASE_A_COCHER,
    False
)
monstre_invincible = Parametre(
    "monstre invicible",
    menu_h.send(TypeParametre.CASE_A_COCHER.hauteur),
    TypeParametre.CASE_A_COCHER,
    False
)




PARAMETRES_NORMAUX : list[Parametre] = [
    fermer_a_la_fin,
]

PARAMETRES_TRICHE : list[Parametre] = [
    joueur_invincible,
    monstre_invincible,
]