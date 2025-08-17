# Ce fichier pré-importe les variables globales

# En Python, il y a deux types de données: les variables mutables et immuables.
# Une variable immuable (ex de types: int, tuple, str) ne peut être changée, on doit la remplacer (x = 4; x += 1 -> on remplace la valeur de x par x + 1);
# une variable mutable peut être remplacée mais on peut aussi la changer partiellement (penser à la méthode list.append()).
# 
# Python n'aime pas quand on remplace la valeur des variables entre les fichiers (la modification est ignorée entre les fichiers);
# pour contourner ce problème, il faut changer la variable directement dans le module (d'où la notation variables_globales.var).
# Le deuxième import donne une liste de variables que l'on peut utiliser sans la notation variables_globales.var.
# On pourrait y mettre les variables mutables mais le risque est de les remplacer, ce qui ne serait pas prit en compte dans les autres fichiers.

from imports import *
from constantes_globales import *

import variables_globales as globales
from variables_globales import (
    # types
    color,
    NaN,
    Stat,
    Pos,
    
    # Fonctions
    copy,
    deepcopy,
    auto,
    
    # ça ne fait pas sens de remplacer ces variables pendant le programme
    # on peut donc se permettre le raccourcit
    fenetre,
    clock,
    entitees_vivantes
)