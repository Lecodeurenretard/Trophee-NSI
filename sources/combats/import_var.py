# Ce fichier pré-importe les variables globales

# En python, il y a deux types de données: les variables muables (mutables?) et immuables.
# Une variable immuable (ex de types: int, tuple, str) ne peut être changée, on doit la remplacer (x = 4; x += 1 -> on remplace la valeur de x par x + 1);
# une variable muable peut être remplacée mais on peut aussi la changer partiellement (penser à la méthode list.append()).
# 
# Tous ceci pour dire que python n'aime pas quand on remplace la valeur des variables entre les fichiers (la modification est ignorée entre les fichiers);
# pour contourner ce problème, il faut changer la variable directement dans le module (d'où la notation variables_globales.var).
# Le deuxième import donne une liste de variables que l'on peut utiliser sans la notation variables_globales.var (la _dot notation_).
# On pourrait y mettre les variables muables mais le risque est de les remplacer, ce qui ne serait pas prit en compte dans tous les fichiers.

import variables_globales as globales
from variables_globales import (
	# Différentes librairies
    pygame,
    sys,
    time,
    random,
    isnan,
    
    # types
    color,
    NaN,
    Callable,
    TypeVar,
    NoReturn,
    Any,
    Stat,
    Pos,
    partial,
    Enum,
    IntEnum,
    
    # Fonctions
    copy,
    deepcopy,
    auto,
    
    # ça ne fait pas sens de remplacer ces variables pendant le programme
    # on peut donc se permettre le raccourcit
    fenetre,
    clock,
    entitees_vivantes,
    CHEMIN_RACINE,
    CHEMIN_DOSSIER_IMG,
    CHEMIN_DOSSIER_SAVE,
    CHEMIN_DOSSIER_ETC,
    
    # ces variables sont, certes, immuables mais elles ne doivent pas être changées
    # on peut donc les importer librement
    BLANC,
    NOIR,
    GRIS,
    BLEU,
    BLEU_CLAIR,
    ROUGE,
    VERT,
    JAUNE,
    
    LARGEUR,
    HAUTEUR,
    
    MAX_COMBAT,
    UI_LONGUEUR_BARRE_DE_VIE,
    UI_HAUTEUR_BARRE_DE_VIE,
    
    POLICE_TITRE,
    POLICE_TEXTE,
    
    TEXTE_INFO_UTILISER,
    TEXTE_INFO_INFO,
    NAN,
    UI_TOUCHES_VALIDER,
    
    MODE_DEBUG,
    DBG_TOUCHES_SKIP,
    
    DBG_TOUCHE_CRIT,
    DBG_TOUCHE_PRECEDENT_COMBAT,
    DBG_TOUCHE_PROCHAIN_COMBAT,
    DBG_TOUCHE_PREDECENT_MONSTRE,
    DBG_TOUCHE_PROCHAIN_MONSTRE,
)

from pygame.surface import (
    Surface,
)

from pygame.rect import (
    Rect,
)