import pygame

DBG_SHOP_AJOUT_ITEM : tuple[int, ...] = (
    pygame.K_PLUS,
    pygame.K_KP_PLUS,
)
DBG_SHOP_SUPPRESSION_ITEM : tuple[int, ...] = (
    pygame.K_MINUS,
    pygame.K_KP_MINUS,
)
DBG_SKIP : tuple[int, ...] = (
    pygame.K_SPACE,
)
VALIDER : tuple[int, ...] = (
    pygame.K_SPACE,
    pygame.K_RETURN,    # entrée (return pour carriage return ou retour chariot sur les machines à écrire)
    pygame.K_KP_ENTER,  # entrée du pavé numérique
)

DBG_CRIT              : int = pygame.K_c
DBG_PRECEDENT_COMBAT  : int = pygame.K_s
DBG_PROCHAIN_COMBAT   : int = pygame.K_z

DBG_PREDECENT_MONSTRE : int = pygame.K_q
DBG_PROCHAIN_MONSTRE  : int = pygame.K_d

DBG_SHOP              : int = pygame.K_p
DBG_INFOS_ENTITES     : int = pygame.K_F9

INFOS                 : int = pygame.K_i
SETTINGS              : int = pygame.K_TAB
DIFFS                 : int = pygame.K_F10

QUITTER               : int = pygame.K_ESCAPE


@staticmethod
def utilisateur_valide_menu(ev : pygame.event.Event) -> bool:
    """Vérifie si l'utilisateur valide dans un menu."""
    return ev.type == pygame.KEYDOWN and ev.key in VALIDER

@staticmethod
def testeur_skip(ev : pygame.event.Event) -> bool:
    """Si en mode débug, le testeur veut skip."""
    from parametres_vars import mode_debug
    
    return mode_debug.case_cochee and ev.type == pygame.KEYDOWN and ev.key in DBG_SKIP