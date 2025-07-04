from imports import import_from_filepath
curse = import_from_filepath("sources/combats/Curseur.py")

import pygame

lignes   : tuple[int, ...] = tuple(range(50, 501, 50))
colonnes : tuple[int, ...] = tuple(range(50, 501, 50))
position_interdites : tuple['Pos', ...] = ( # type: ignore  # Pos est défini dans curse
    curse.Pos(100, 100),
    curse.Pos(200, 200),
    curse.Pos(150, 250),
    curse.Pos(200, 250),
    
    #Carré en bas à droite
    curse.Pos(400, 400),
    curse.Pos(450, 400),
    curse.Pos(400, 450),
    curse.Pos(450, 450),
    curse.Pos(500, 450),
    curse.Pos(500, 400),
    curse.Pos(500, 500),
    curse.Pos(450, 500),
    curse.Pos(400, 500),
)
curseur = curse.Curseur(
	lignes,
	colonnes,
    position_interdites
)

clock = curse.clock
fenetre = curse.fenetre

ROUGE = curse.ROUGE
VERT = curse.VERT
NOIR = curse.NOIR

while True:
    clock.tick(60)
    fenetre.fill(NOIR)
    
    for ev in pygame.event.get():
        curseur.utilisateur_deplace_curseur(ev)
        if ev.type == pygame.QUIT:
            quit()
    
    # Desssine les positions disponibles
    for col in colonnes:
        for lne in lignes:
            if curse.Pos(col, lne) not in position_interdites:
                pygame.draw.circle(fenetre, VERT, (col, lne), 5)
            
    curseur.dessiner(fenetre, ROUGE)
    pygame.display.flip()