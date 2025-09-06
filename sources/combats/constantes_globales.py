from imports import *

DBG_TOUCHES_SKIP : tuple[int, ...] = (
    pygame.K_SPACE,
)

DBG_TOUCHE_CRIT     : int = pygame.K_c

DBG_TOUCHE_PRECEDENT_COMBAT : int = pygame.K_s
DBG_TOUCHE_PROCHAIN_COMBAT  : int = pygame.K_z

DBG_TOUCHE_PREDECENT_MONSTRE: int = pygame.K_q
DBG_TOUCHE_PROCHAIN_MONSTRE : int = pygame.K_d

LARGEUR : int = 800 ;   HAUTEUR : int = 600
CENTRE_FENETRE : tuple[int, int] = (LARGEUR // 2, HAUTEUR // 2)

rgb : TypeAlias = tuple[int, int, int]
NOIR    : rgb = (0, 0, 0)
BLANC   : rgb = (255, 255, 255)
GRIS    : rgb = (100, 100, 100)
GRIS_CLAIR : rgb = (145, 145, 145)

ROUGE   : rgb = (255, 0, 0)
VERT    : rgb = (0, 255, 0)
BLEU    : rgb = (0, 0, 255)
BLEU_CLAIR : rgb = (50, 50, 255)
JAUNE   : rgb = (255, 255, 0)

rgba : TypeAlias = tuple[int, int, int, int]
TRANSPARENT : rgba = (0, 0, 0, 0)

color : TypeAlias = rgb|rgba

MAX_COMBAT : int = 5

INVICIBLE_ENNEMI : bool = False

VITESSE_MAXIMUM : int = 10**9
MAXIMUM_ENTITES_SIMULTANEES : int = 10

UI_LONGUEUR_BARRE_DE_VIE : int = 200
UI_HAUTEUR_BARRE_DE_VIE : int = 10

POLICE_TITRE : pygame.font.Font = pygame.font.Font(None, 36)    # police par défaut de pygame
POLICE_TEXTE : pygame.font.Font = pygame.font.Font(None, 25)
POLICE_FOURRE_TOUT : pygame.font.Font = pygame.font.SysFont(None, 50)

POLICE_TITRE.set_underline(True)

TEXTE_INFO_UTILISER : pygame.Surface = POLICE_TEXTE.render("SPACE : utiliser", True, BLANC)
TEXTE_INFO_INFO     : pygame.Surface = POLICE_TEXTE.render("I : info"        , True, BLANC)

# v. doc pour son usage
NaN : TypeAlias = float
NAN : NaN = float("nan")

UI_TOUCHES_VALIDER : tuple[int, ...] = (
    pygame.K_SPACE,
    pygame.K_RETURN,    # entrée (return pour carriage return ou retour chariot sur les machines à écrire)
    pygame.K_KP_ENTER,  # entrée du pavé numérique
)

UI_TOUCHES_INFOS        : int = pygame.K_i
UI_TOUCHE_AFFICHAGE_FPS : int = pygame.K_LSHIFT
UI_TOUCHE_SETTINGS      : int = pygame.K_TAB

TOUCHE_QUITTER          : int = pygame.K_ESCAPE


# Le chemin du fichier vers le dossier racine
# Quand on lance de VSCode, on lance le projet depuis racine
# Quand on lance du terminal, on le lance du dossier "combats"
CHEMIN_RACINE : str = ''
if getcwd().endswith("combats"):    # rudimentaire mais fonctionnel
    CHEMIN_RACINE = "../../"
elif getcwd().endswith("sources"):
    CHEMIN_RACINE = "../"
else:
    logging.warning("Le dossier n'est pas reconnu, on suppose que l'on est à la racine.")

CHEMIN_DOSSIER_IMG  : str = f"{CHEMIN_RACINE}data/img"
CHEMIN_DOSSIER_SAVE : str = f"{CHEMIN_RACINE}data/save"
CHEMIN_DOSSIER_ETC  : str = f"{CHEMIN_RACINE}data/etc"