# Des boutons à utiliser dans le jeu principal

from Bouton import *
from fonction_combat import *

dimensions_boutons : tuple[tuple[int, int, int, int], ...] = (
    (70 , Jeu.pourcentage_hauteur(81.25) - 25, 200, 50),
    (70 , Jeu.pourcentage_hauteur(81.25) + 45, 200, 50),
    (375, Jeu.pourcentage_hauteur(81.25) - 25, 200, 50),
    (375, Jeu.pourcentage_hauteur(81.25) + 45, 200, 50),
)

# On initialise les 4 boutons pour attaquer (je sais )
boutons_attaques : list[ButtonCursor] = [   # honnêtement, c'est vraiment moche
    ButtonCursor(
        joueur.noms_cartes[i],
        dimensions_boutons[i],
        group_name="Attaques",
        action=partial(lambda nom: joueur_attaque(nom, Monstre.monstres_en_vie[0]), nom_att),   # pourquoi partial? https://stackoverflow.com/questions/6076270/lambda-function-in-list-comprehensions
        line_thickness=5, line_color=BLANC,                                                     # La partie intéressante commence un peu avant son edit de du 30/08/2019
        bg_color=NOIR, group_color=BLEU,
    )
    for i, nom_att in enumerate(joueur.noms_cartes)
]
del dimensions_boutons  # ne sert plus à rien