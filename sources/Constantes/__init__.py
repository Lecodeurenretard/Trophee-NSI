# Ce fichier importe tous les autres fichiers du module (dossier)
# car Python est vraisemblablement incapable de la faire

from . import Chemins    # Why is it like this?
from . import Couleurs   # Python...
from . import Polices
from . import Touches

from .autres import *