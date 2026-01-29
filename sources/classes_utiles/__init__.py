from .      import EasingConstants as Easing
from .Array import Array
from .Duree import Duree
from .Pos   import Pos, pos_t, pos_t_vers_Pos, pos_t_vers_tuple

from .Animation import (
    SensLecture,
    InterpolationLineaire, MultiInterpolation,
    Gradient             , MultiGradient,
    Deplacement          , MultiDeplacement,
)

from .EasingFunctions import (
    EasingFunction,
    EasingType,
    inversement_ease,
    ecraser_easing,
)
