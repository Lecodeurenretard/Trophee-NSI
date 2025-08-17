# Des boutons à utiliser dans le jeu principal

from Bouton import *
from fonction_combat import *
from fonctions_vrac import attendre

dimensions_boutons : tuple[tuple[int, int, int, int], ...]= (
    (70 , (13 * HAUTEUR // 16) - 25, 200, 50),
    (70 , (13 * HAUTEUR // 16) + 45, 200, 50),
    (375, (13 * HAUTEUR // 16) - 25, 200, 50),
    (375, (13 * HAUTEUR // 16) + 45, 200, 50),
)

def joueur_attaque_comment(index_attaque : int) -> None:
    joueur_attaque(joueur.moveset_clefs[index_attaque], Monstre.monstres_en_vie[0])

boutons_attaques : list[ButtonCursor] = [   # honnêtement, c'est vraiment moche
    ButtonCursor(
        joueur.moveset_clefs[i], dimensions_boutons[i], group_name="Attaques",
        action=partial(lambda idex: joueur_attaque_comment(idex), i),     # pourquoi partial? v. cette merveilleuse réponse: https://stackoverflow.com/questions/6076270/lambda-function-in-list-comprehensions
        line_thickness=5, line_color=BLANC, bg_color=NOIR, group_color=BLEU # La partie intéressante commence un peu avant son edit de du 30/08/2019
    )
    for i in range(len(joueur.moveset_clefs))
]
del dimensions_boutons  # ne sert plus à rien