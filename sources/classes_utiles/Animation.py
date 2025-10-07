from imports import Generator, Optional
from Constantes.Couleurs import rgba, color, color_to_rgba, TypeAlias

from .Pos import Pos
from .EasingFunctions import EasingFunction
from . import EasingConstants as Easing

# Certains logiciels d'animations et de montage proposent ces fonctionnalités (par exemple Blender et DaVinci)
# Les easing functions (j'ai pas le nom français) permettent d'avoir une animation plus fluide
# en accélerant au début et en ralentissant à la fin.
# Démo Desmos: https://www.desmos.com/calculator/rrinotdfez

# ici seules les fonctions ease-in-out sont mise car ce sont les plus naturelles.

class InterpolationLineaire:
    """
    L'interpolation linéaire, va d'une valeur A à une valeur B sans jamais changer de vitesse (on pourrait dire que sa dérivée est constante)
    https://fr.wikipedia.org/wiki/Interpolation_lin%C3%A9aire
    """
    @staticmethod
    def calculer_valeur(debut : float, fin : float, t : float, easing_fun : EasingFunction = Easing.NO_EASING) -> float:
        """
        Calcule la valeur qu'a une valeur variant de `debut` à `fin` avec la fonction d'easing `easing_fun`.
        En d'autre mots, calcule l'ordonnée  de la courbe correspondante sur la fonction Desmos: https://www.desmos.com/calculator/rrinotdfez.
        """
        return debut + easing_fun(t) * (fin - debut)

    @staticmethod
    def generateur(debut : float, fin : float, nb_iterations : int, easing : EasingFunction = Easing.NO_EASING) -> Generator[float, None, None]:
        for i in range(nb_iterations):
            yield InterpolationLineaire.calculer_valeur(debut, fin, i / nb_iterations, easing_fun=easing)


class Gradient:
    """Implémentation de InterpolationLineaire pour les couleurs."""
    def __init__(self, couleur_debut : color, couleur_fin : color):
        self._debut : rgba = color_to_rgba(couleur_debut)
        self._fin   : rgba = color_to_rgba(couleur_fin)
    
    def __repr__(self):
        return f"Gradient(debut={self._debut}; fin={self._fin})"
    
    def calculer_valeur(
            self,
            t : float,
            easing_fun : Optional[EasingFunction] = None, *,
            r : EasingFunction = Easing.NO_EASING, g : EasingFunction = Easing.NO_EASING,
            b : EasingFunction = Easing.NO_EASING, a : EasingFunction = Easing.NO_EASING, 
        ) -> rgba:
        """
        Même chose que sa version dans InterpolationLineaire mais le fait sur 4 valeurs.
        Si l'argument `easing_fun` est fourni alors l'utilise pour toutes les couleurs, sinon utilise les arguments `r`, `g`, `b` et `a` pour les valeurs correspodantes.
        """
        if easing_fun is not None:
            return self.calculer_valeur(t, r=easing_fun, g=easing_fun, b=easing_fun, a=easing_fun)
        return (
            round(InterpolationLineaire.calculer_valeur(self._debut[0], self._fin[0], t, easing_fun=r)),
            round(InterpolationLineaire.calculer_valeur(self._debut[1], self._fin[1], t, easing_fun=g)),
            round(InterpolationLineaire.calculer_valeur(self._debut[2], self._fin[2], t, easing_fun=b)),
            round(InterpolationLineaire.calculer_valeur(self._debut[3], self._fin[3], t, easing_fun=a)),
        )
    
    def generateur(
            self,
            nb_iterations : int,
            easing : Optional[EasingFunction] = None, *,
            r : EasingFunction = Easing.NO_EASING, g : EasingFunction = Easing.NO_EASING,
            b : EasingFunction = Easing.NO_EASING, a : EasingFunction = Easing.NO_EASING,
        ) -> Generator[rgba, None, None]:
        for i in range(nb_iterations):
            yield self.calculer_valeur(i / nb_iterations, easing_fun=easing, r=r, g=g, b=b, a=a)


class Deplacement:
    """Implémentation de InterpolationLineaire pour les positions."""
    def __init__(self, position_debut : Pos, position_fin : Pos):
        self._debut : Pos = position_debut
        self._fin   : Pos = position_fin
    
    def __repr__(self):
        return f"Deplacement(debut={self._debut}; fin={self._fin})"
    
    def calculer_valeur(
            self,
            t : float,
            easing_fun : Optional[EasingFunction] = None, *,
            x : EasingFunction = Easing.NO_EASING, y : EasingFunction = Easing.NO_EASING,
        ) -> Pos:
        """
        Même chose que sa version dans InterpolationLineaire mais le fait sur 2 valeurs.
        Si l'argument `easing_fun` est fourni alors l'utilise pour toutes les couleurs, sinon utilise les arguments `x` et `y` pour les valeurs correspodantes.
        """
        if easing_fun is not None:
            return self.calculer_valeur(t, x=easing_fun, y=easing_fun)
        return Pos(
            round(InterpolationLineaire.calculer_valeur(self._debut.x, self._fin.x, t, easing_fun=x)),
            round(InterpolationLineaire.calculer_valeur(self._debut.y, self._fin.y, t, easing_fun=y)),
        )
    
    def generateur(
            self,
            nb_iterations : int,
            easing : Optional[EasingFunction] = None, *,
            x : EasingFunction = Easing.NO_EASING, y : EasingFunction = Easing.NO_EASING,
        ) -> Generator[Pos, None, None]:
        for i in range(nb_iterations):
            yield self.calculer_valeur(i / nb_iterations, easing_fun=easing, x=x, y=y)