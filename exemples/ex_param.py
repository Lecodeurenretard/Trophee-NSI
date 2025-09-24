import sys
from pathlib import Path
sys.path.insert(0, str(next(Path(__file__).parent.parent.glob('sources/combats/'))))
# La ligne du dessus fais croire à Python que l'on se trouve dans `sources/combats/` au  lieu de `exemple/`


# VSCode ne détecte pas les imports et affiche 12 erreurs
from Settings import *
from fonctions_vrac import verifier_pour_quitter

def print_nouvelle_valeur(nouveau):
    print(f"Un paramètre à changé de valeur pour avoir: `{nouveau}`.")

params = [
    Parametre(
        "Case à cocher",
        pourcentage_hauteur(20),
        TypeParametre.CASE_A_COCHER,
        False,
        on_change=print_nouvelle_valeur
    ),
]


while True:
    fenetre.fill(BLANC)
    
    for ev in pygame.event.get():
        verifier_pour_quitter(ev)
        
        for param in params:
            param.prendre_input(ev)
    
    Parametre.dessiner_groupe(fenetre, params)
    pygame.display.flip()
    clock.tick(60)