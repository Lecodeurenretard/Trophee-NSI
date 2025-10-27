from imports import Generator, Optional, logging, copy, deepcopy
from Constantes.Couleurs import rgba, color, color_to_rgba, iterable_to_rgba

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
    def generateur(
        debut : float,
        fin : float,
        nb_iterations : int,
        easing : EasingFunction = Easing.NO_EASING,
        loop : bool = False,
    ) -> Generator[float, None, None]:
        premiere_iteration = True
        while loop or premiere_iteration:
            premiere_iteration = False
            
            for i in range(nb_iterations):
                yield InterpolationLineaire.calculer_valeur(debut, fin, i / nb_iterations, easing_fun=easing)


class Gradient:
    """Implémentation de InterpolationLineaire pour les couleurs."""
    def __init__(self, couleur_debut : color, couleur_fin : color):
        self._debut : rgba = color_to_rgba(couleur_debut)
        self._fin   : rgba = color_to_rgba(couleur_fin)
    
    def __repr__(self):
        return f"Gradient(debut={self._debut}, fin={self._fin})"
    
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
            loop : bool = True,
        ) -> Generator[rgba, None, None]:
        premiere_iteration = True
        while loop or premiere_iteration:
            premiere_iteration = False
            
            for i in range(nb_iterations):
                yield self.calculer_valeur(i / nb_iterations, easing_fun=easing, r=r, g=g, b=b, a=a)


class Deplacement:
    """Implémentation de InterpolationLineaire pour les positions."""
    def __init__(self, position_debut : Pos, position_fin : Pos):
        self._debut : Pos = position_debut
        self._fin   : Pos = position_fin
    
    def __repr__(self):
        return f"Deplacement(debut={self._debut}, fin={self._fin})"
    
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
            loop : bool = False,
        ) -> Generator[Pos, None, None]:
        premiere_iteration = True
        while loop or premiere_iteration:
            premiere_iteration = False
            
            for i in range(nb_iterations):
                yield self.calculer_valeur(i / nb_iterations, easing_fun=easing, x=x, y=y)


# TODO: Métaclasses?

class MultiInterpolation:
    """
    Interpole une valeur avec plus de deux valeurs sans de magie de polynômes.
    """
    # L'avantage de na pas approximer avec des polynômes, c'est que l'on peut
    # facilement changer les fonctions d'easing.
    
    @staticmethod
    def _adaptation_pour_2_points(valeurs, temps_clefs, t, easing_fun, easing_funs) -> tuple[int, int, int, EasingFunction]:
        """
        Adapte les arguments de `.calculer_valeur()` pour les passer à la méthode de `InterpolationLinéaire`.
        Renvoie une tuple contenant dans l'ordre: le début et la fin du lerp, le t correspondant au nouvel interval ainsi que la fonction d'easing choisie.
        """
        # On garde t entre 0 et 1
        t = max(0, min(1, t))
        
        index_fin : int = 0
        for i, temps_clef in enumerate(temps_clefs):
            if t < temps_clef :
                index_fin = i
                break
        else:   # C'est bien indenté, Python authorise les for... else
            index_fin = len(temps_clefs)
        
        # vérifie si on a besoin de changer `easing_fun`
        if len(easing_funs) != 0:
            assert(len(easing_funs) == len(valeurs)), "Le nombre de fonctions d'easing doit être le même que le nombre de valeurs fournies."
            if easing_fun != Easing.NO_EASING:
                logging.warning("Le paramètre `easing_fun` est ignoré car `easing_funs` a été passé.")
            
            easing_fun = easing_funs[index_fin]
        
        a = temps_clefs[index_fin - 1]; b = temps_clefs[index_fin]
        assert(0 <= a <= b <= 1), f"Mauvais ordre, on devrait avoir 0 <= {temps_clefs[index_fin - 1]=} <= {temps_clefs[index_fin]=} <= 1"
        
        t_entre_ab = (t - a) / (b - a)
        
        return (valeurs[index_fin - 1], valeurs[index_fin], t_entre_ab, easing_fun)
        
    @staticmethod
    def calculer_valeur(
            valeurs_clefs : list[float]|tuple[float, ...],
            temps_clefs   : list[float]|tuple[float, ...], 
            t : float,
            easing_fun : EasingFunction = Easing.NO_EASING, easing_funs : list[EasingFunction]|tuple[EasingFunction, ...] = []
        ) -> float:
        """
        Soit un plan, on ne s'interesse qu'aux valeurs dont l'abcisse est entre 0 et 1 inclus.
        On y place des points qui ont pour coordonées (temps_clefs[i]; valeurs[i+1]) avec 0 < i < n, n = len(valeurs) - 2 = len(temps_clefs) -1. On place aussi (temps_clefs[0]; valeurs[0]) et (temps_clefs[n-1]; valeurs[n+1]).
        Nous relions ensuite les points entre eux en respectant les fonctions d'easing repectives pour obtenir une courbe.
        La fonction renvoie donc l'ordonnée du point ayant pour abcisse `t`.
        """
        if len(valeurs_clefs) < 2:
            raise ValueError(f"Pour faire une interpolation, il faut au moins 2 valeurs (seulemeent {len(valeurs_clefs)} ont été passées).")
        assert(len(temps_clefs) == len(valeurs_clefs) - 2), f"Il doit y avoir exactement deux valeurs de moins dans `temps_clefs` que dans valeurs (t=0 et t=1 sont implicites), seulement {len(temps_clefs)} temps_clefs ont été passées contre {len(valeurs_clefs)}." # plus de 3 fois les recomandations de la PEP 8, pas mal.
        assert(temps_clefs == sorted(temps_clefs)), "`temps_clefs` n'est pas rangée dans l'ordre croissant."  # Je doute que `temps_clef` dépasse la dixaine d'éléments, la trier ne demandera pas beacoup de temps
        
        temps_clefs = [0, *temps_clefs, 1]  # 0 et 1 sont implicites pour l'utilisateur, on les met ici
        
        debut, fin, nouveau_t, easing_fun = MultiInterpolation._adaptation_pour_2_points(valeurs_clefs, temps_clefs, t, easing_fun, easing_funs)
        return InterpolationLineaire.calculer_valeur(debut, fin, nouveau_t, easing_fun=easing_fun)
    
    @staticmethod
    def generateur(
            valeurs     : list[float]|tuple[float, ...],
            temps_clefs : list[float]|tuple[float, ...],
            nb_iterations : int,
            easing : EasingFunction = Easing.NO_EASING,
            loop : bool = False,
        ) -> Generator[float, None, None]:
        premiere_iteration = True
        while loop or premiere_iteration:
            premiere_iteration = False
            
            yield MultiInterpolation.calculer_valeur(valeurs, temps_clefs, 0, easing_fun=easing)
            for i in range(1, nb_iterations):
                yield MultiInterpolation.calculer_valeur(valeurs, temps_clefs, i / (nb_iterations-1), easing_fun=easing)


def valeurs_regulieres_entre_01(nombre_a_produire : int, inclure_0 : bool = True, inclure_1 : bool = False) -> list[float]:
    """
    Renvoie une liste de valeurs "régulières" entre 0 et 1 contenant `nombre_a_produire` éléments (sans toucher aux paramètres optionnels).
    Si ni inclure_0 ni inclure_1 sont True, alors renvoie `nombre_a_produire - 1` éléments. Si un des deux est `True`, renvoie exactement `nombre_a_produire`.  
    """
    debut : int = 0                     if inclure_0 else 1
    fin   : int = nombre_a_produire + 1 if inclure_1 else nombre_a_produire
    
    return [idex / nombre_a_produire for idex in range(debut, fin)]

class MultiGradient:
    """Implémentation de MultiInterpolation pour les couleurs."""
    
    def __init__(self, evolution_rgba : list[list[int]|tuple[int, ...]], liste_temps_clefs : list[list[float]|tuple[float, ...]] = []):
        """
        Constructeur de MultiGradient.
        Le paramètre `evolution_rgba[]` contient les valeurs clefs (la liste passée à MultiInterpolation.calculer_valeurs()) pour dans l'ordre le rouge, vert, bleu et alpha (transparence).
        Le paramètre `liste_temps_clefs[]` contients les temps clefs de la même manière que `evolution_rgba[]`, si vide se complète de manière à se que les valeurs soient équidistantes.
        
        Exemples d'appel:
        MultiGradient(
            ([0, 128, 255], [128, 0, 255], [255, 128, 0]),   # Le rouge croit, le bleu décroit et le vert décroit puis croit (la transparence reste à 255).
            ([.5], [.33], [.5])                              # La "valeur du milieu" sera atteinte à la moitié du temps pour le rouge et bleu alors qu'elle sera atteite qu'au tier por le vert (la transaprence est constante).
        )
        
        MultiGradient(
            ([0, 128, 255], [128, 0, 255], [255, 128, 0])
        )
        """
        evolution_rgba     = deepcopy(evolution_rgba)
        liste_temps_clefs =     copy(liste_temps_clefs)
        
        # Si evolution_rgba n'a que 3 valeurs, ajoute en une à la fin de `evolution_rgba[]`
        if len(evolution_rgba) == 3:
            evolution_rgba.append([])
        assert(len(evolution_rgba) == 4), "Il doit y avoir 3 ou 4 éléments dans `evolution_rgba[]`."
        
        # Si la liste des temps clefs sont vides, remplit la avec des listes vides
        if len(liste_temps_clefs) == 0:
            liste_temps_clefs = [[], [], [], []]
        
        # Si les temps clefs sont vides, remplit les avec des valeurs régulières
        for i, temps_clefs in enumerate(liste_temps_clefs):
            if len(temps_clefs) == 0:
                liste_temps_clefs[i] = valeurs_regulieres_entre_01(len(evolution_rgba[0]))
                # par exemple, si l'utilistateur donne 5 valeurs
                # liste_temps_clefs = [1/5, 2/5, 3/5, 4/5] * 4
        
        # S'il manque une valeur à la liste des temps clefs, ajoute une liste vide
        if len(liste_temps_clefs) == 3:
            liste_temps_clefs.append([])
        assert(len(liste_temps_clefs) == 4), "Il doit y avoir aucun, 3 ou 4 éléments dans `liste_temps_clefs[]`."
        
        for valeur_clef, temps_clefs in zip(evolution_rgba, liste_temps_clefs):
            assert(len(temps_clefs) == len(valeur_clef) - 2), f"Il devrait avoir {len(valeur_clef) - 2} éléments dans chaque éléments de `liste_temps_clefs[]` car le début et la fin sont implicites, au lieu de ça il y a {len(temps_clefs)=}."
        
        self._couleurs_clefs = evolution_rgba
        
        self._liste_temps_clefs = liste_temps_clefs
    
    def __repr__(self):
        return f"MultiGradient({self._couleurs_clefs=}, {self._liste_temps_clefs=})"
    
    def calculer_valeur(
            self,
            t : float,
            easing_fun : EasingFunction = Easing.NO_EASING, easing_funs : list[EasingFunction]|tuple[EasingFunction, ...] = []
        ) -> rgba:
        """
        Même chose que sa version dans Gradient mais sur un nombre de couleurs indéterminées.
        Si `easing_funs[]` n'est pas vide alors utilise ses valeurs (doit avoir une valeur de moins que `self._couleurs_clefs[]`) sinon utilise `easing_fun`.
        """
        
        # Le truc en bas est un peut compliqué à lire donc voilà ce qu'il fait:
        # Il calcule la valeur des lerp pour r, v, b et a puis met tout ça dans une liste
        # la liste est ensuite "convertie" en couleur rgba.
        return iterable_to_rgba([
            MultiInterpolation.calculer_valeur(
                self._couleurs_clefs[i],        # type: ignore  # il n'accèpte pas la convertion list[int]|tuple[int, ...] --> list[float]|tuple[float, ...]
                self._liste_temps_clefs[i],
                t,
                easing_fun=easing_fun, easing_funs=easing_funs
            )
            for i in range(4)
        ])
    
    def generateur(
            self,
            nb_iterations : int,
            easing : EasingFunction = Easing.NO_EASING,
            loop : bool = False,
        ) -> Generator[rgba, None, None]:
        premiere_iteration = True
        while loop or premiere_iteration:
            premiere_iteration = False
            
            yield self.calculer_valeur(0, easing_fun=easing)
            for i in range(1, nb_iterations):
                yield self.calculer_valeur(i / (nb_iterations-1), easing_fun=easing)


class MultiDeplacement:
    """Implémentation de MultiInterpolation pour les positions."""
    
    def __init__(self, evolution_pos : list[list[int]|tuple[int, ...]]|tuple[list[int]|tuple[int, ...], list[int]|tuple[int, ...]], liste_temps_clefs : list[list[float]|tuple[float, ...]]):
        """
        Constructeur de MultiDeplacement.
        Le paramètre `evolution_pos[]` contient les valeurs clefs (la liste passée à MultiInterpolation.calculer_valeurs()) pour dans l'ordre les abcisses et les ordonées.
        Le paramètre `liste_temps_clefs[]` contients les temps clefs de la même manière que `evolution_pos[]`.
        
        Exemple d'appel:
        MultiDeplacement(
            ([0, 250, 500], [500, 250, 0]),   # Les abcisses croissent  et les ordonnées décroissent.
            ([.5], [.5])                      # La "valeur du milieu" sera atteinte à la moitié du temps pour à la fois les abcisses et les ordonnées.
        )
        """
        assert(len(evolution_pos) == 2)    , "Il doit y avoir exactement 2 éléments dans `evolution_pos[]`."
        assert(len(liste_temps_clefs) == 2), "Il doit y avoir exactement 2 éléments dans `liste_temps_clefs[]`."
        
        evolution_pos     = deepcopy(evolution_pos)
        liste_temps_clefs =     copy(liste_temps_clefs)
        
        for valeurs_clef, temps_clefs in zip(evolution_pos, liste_temps_clefs):
            assert(len(temps_clefs) == len(valeurs_clef) - 2), f"Il devrait avoir {len(valeurs_clef) - 2} éléments dans chaque éléments de `liste_temps_clefs[]` car le début et la fin sont implicites, au lieu de ça il y a {len(temps_clefs)=}."
        
        self._positions_clefs = evolution_pos
        self._liste_temps_clefs = liste_temps_clefs
    
    def __repr__(self):
        return f"MultiDeplacement({self._positions_clefs=}, {self._liste_temps_clefs=})"
    
    def calculer_valeur(
            self,
            t : float,
            easing_fun : EasingFunction = Easing.NO_EASING, easing_funs : list[EasingFunction]|tuple[EasingFunction, ...] = []
        ) -> Pos:
        """
        Même chose que sa version dans Deplacement mais sur un nombre de couleurs indéterminées.
        Si `easing_funs[]` n'est pas vide alors utilise ses valeurs (doit avoir une valeur de moins que `self._couleurs_clefs[]`) sinon utilise `easing_fun`.
        """
        
        # Le truc en bas est un peut compliqué à lire donc voilà ce qu'il fait:
        # Il calcule la valeur des lerp pour r, v, b et a puis met tout ça dans une liste
        # la liste est ensuite "convertie" en couleur rgba.
        return Pos([
            MultiInterpolation.calculer_valeur(
                self._positions_clefs[i],         #type: ignore # pyright: ignore[reportArgumentType] # il n'accèpte pas la convertion list[int]|tuple[int, ...] --> list[float]|tuple[float, ...] 
                self._liste_temps_clefs[i],
                t,
                easing_fun=easing_fun, easing_funs=easing_funs
            )
            for i in range(2)
        ])
    
    def generateur(
            self,
            nb_iterations : int,
            easing : EasingFunction = Easing.NO_EASING,
            loop : bool = False,
        ) -> Generator[Pos, None, None]:
        premiere_iteration = True
        while loop or premiere_iteration:
            premiere_iteration = False
            for i in range(nb_iterations):
                yield self.calculer_valeur(i / nb_iterations, easing_fun=easing)