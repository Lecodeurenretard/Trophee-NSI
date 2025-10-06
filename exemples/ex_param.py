import sys
from pathlib import Path
sys.path.insert(0, str(next(Path(__file__).parent.parent.glob('sources/'))))
# La ligne du dessus fais croire à Python que l'on se trouve dans `sources/combats/` au  lieu de `exemple/`


# VSCode ne détecte pas les imports et affiche 8 erreurs
from Parametres import *
from Jeu import verifier_pour_quitter, Jeu

def print_nouvelle_valeur(nouveau):
    print(f"Un paramètre à changé de valeur pour avoir: `{nouveau}`.")

params = [
    Parametre(
        "Case à cocher",
        Jeu.pourcentage_hauteur(20),
        TypeParametre.CASE_A_COCHER,
        False,
        on_change=print_nouvelle_valeur
    ),
]


while True:
    Jeu.fenetre.fill(BLANC)
    
    for ev in pygame.event.get():
        verifier_pour_quitter(ev)
        
        for param in params:
            param.prendre_input(ev)
    
    Parametre.dessiner_groupe(Jeu.fenetre, params)
    pygame.display.flip()
    Jeu.clock.tick(60)