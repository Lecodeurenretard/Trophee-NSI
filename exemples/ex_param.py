import sys
from pathlib import Path
sys.path.insert(0, str(next(Path(__file__).parent.parent.glob('sources/'))))
# La ligne du dessus fais croire à Python que l'on se trouve dans `sources/` au  lieu de `exemple/`


# VSCode ne détecte pas les imports et affiche 2 erreurs
from Parametres import Parametre, TypeParametre, BLANC, pygame
from Jeu import Jeu, Fenetre

def print_nouvelle_valeur(nouveau):
    print(f"Un paramètre à changé de valeur pour avoir: `{nouveau}`.")

params = [
    Parametre(
        "Case à cocher",
        Fenetre.pourcentage_hauteur(20),
        TypeParametre.CASE_A_COCHER,
        False,
        on_change=print_nouvelle_valeur
    ),
]

print("Exemple: Comment se servir des paramètres.")
while True:
    Jeu.commencer_frame()
    Fenetre.surface.fill(BLANC)
    
    for ev in pygame.event.get():
        # Vérifie si l'évènement ne concerne pas les paramètres
        for param in params:
            param.prendre_input(ev)
    
    Parametre.dessiner_groupe(0, params)
    Fenetre.display_flip()