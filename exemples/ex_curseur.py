import sys
from pathlib import Path
sys.path.insert(0, str(next(Path(__file__).parent.parent.glob('sources/combats/'))))
# La ligne du dessus fais croire à Python que l'on se trouve dans `sources/combats/` au  lieu de `exemple`
# Pourquoi doit-on écrire du spagetti code pour une chose aussi simple qu'importer depuis un autre dossier?

# VSCode bombarde d'erreurs (26 à l'heure du commentaire) mais le script marche
from Curseur import *

lignes   : list[int] = list(range(50, 501, 50))
colonnes : list[int] = list(range(50, 501, 50))
position_interdites : list[Pos] = [
    Pos(100, 100),
    Pos(200, 200),
    Pos(150, 250),
    Pos(200, 250),
    
    # Carré en bas à droite
    Pos(400, 400),
    Pos(450, 400),
    Pos(400, 450),
    Pos(450, 450),
    Pos(500, 450),
    Pos(500, 400),
    Pos(500, 500),
    Pos(450, 500),
    Pos(400, 500),
]
curseur = Curseur(
    colonnes,
    lignes,
    position_interdites
)

clock = clock
fenetre = fenetre

ROUGE = ROUGE
VERT = VERT
NOIR = NOIR

while True:
    clock.tick(60)
    fenetre.fill(NOIR)
    
    for ev in pygame.event.get():
        curseur.deplacement_utilisateur(ev)
        verifier_pour_quitter(ev)
    
    # Desssine les positions disponibles
    for col in colonnes:
        for lne in lignes:
            if Pos(col, lne) not in position_interdites:
                pygame.draw.circle(fenetre, VERT, (col, lne), 5)
            
    curseur.dessiner(fenetre, ROUGE)
    pygame.display.flip()