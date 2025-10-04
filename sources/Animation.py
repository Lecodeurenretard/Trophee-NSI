from imports import dataclass, Generator, Callable, TypeAlias, cos, sqrt, math

# Certains logiciels d'animations et de montage proposent ces fonctionnalités (par exemple Blender et DaVinci)
# Les easing functions (j'ai pas le nom français) permettent d'avoir une animation plus fluide
# en accélerant au début et en ralentissant à la fin.
# Démo Desmos: https://www.desmos.com/calculator/rrinotdfez

# ici seules les fonctions ease-in-out sont mise car ce sont les plus naturelles.
EasingFunction : TypeAlias = Callable[[float], float]

no_easing          : EasingFunction = lambda x: x
easing_square      : EasingFunction = lambda x: (2 * x**2) if x < .5 else (1 - 2 * (1 - x)**2)
easing_cube        : EasingFunction = lambda x: (4 * x**3) if x < .5 else (1 - 4 * (1 - x)**3)
easing_hypercube   : EasingFunction = lambda x: (8 * x**4) if x < .5 else (1 - 8 * (1 - x)**4)
easing_circular    : EasingFunction = lambda x: (.5 - sqrt(.25 - x**2))             if x < .5 else (.5 + sqrt(.25 - (x - 1)**2))
easing_exponential : EasingFunction = lambda x: (2**(10 * x - 10 + 4.04) - 2**5.96) if x < .5 else (1 - 2**(-10 * x + 4.04) + 2**5.96)
easing_trig        : EasingFunction = lambda x: (.5 - cos(math.pi * x) / 2)

easing_fade       : EasingFunction = easing_cube
easing_exponent_4 : EasingFunction = easing_hypercube
easing_radial     : EasingFunction = easing_circular

@dataclass(init=False)  # Comment dréer une interface en Python /s
class InterpolationLineaire:
    """
    L'interpolation linéaire, va d'une valeur A à une valeur B sans jamais changer de vitesse (on pourrait dire que sa dérivée est constante)
    https://fr.wikipedia.org/wiki/Interpolation_lin%C3%A9aire
    """
    @staticmethod
    def calculer_valeur(debut, fin, t, easing_fun : EasingFunction = no_easing):
        return debut + easing_fun(t) * (fin - debut)

    @staticmethod
    def generateur(debut : float, fin : float, easing : EasingFunction = no_easing) -> Generator[float, None, None]:
        valeur : float = debut
        while valeur < fin:
            valeur = InterpolationLineaire.calculer_valeur(debut, fin, valeur, easing)
            yield valeur