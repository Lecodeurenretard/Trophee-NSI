from imports import *

# Ces types pourrons potentiellements être ajoutés plus tard
# en fonction des paramètres qui serons implémentés plus tard
class TypeParametre(Enum):       # types de l'attribut valeur:
    CASE_A_COCHER    = auto()    # bool
    CHOIX_UN_SEUL    = auto()    # Enum
    CHOIX_PLUSIEURS  = auto()    # Flag
    SLIDER           = auto()    # float/int
    TEXTE            = auto()    # str
    INT              = auto()    # int
    FLOAT            = auto()    # float

type_valeur_parametre : TypeAlias = None #|bool|int|float|str|Enum|Flag
@dataclass
class Parametre:
    type : TypeParametre
    valeur_par_defaut : type_valeur_parametre
    valeur            : type_valeur_parametre = None
    pass