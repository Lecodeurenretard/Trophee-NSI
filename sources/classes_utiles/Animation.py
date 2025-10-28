from imports import Generator, Optional, logging, copy, deepcopy
from Constantes.Couleurs import rgba, color, color_to_rgba, iterable_to_rgba

from .Pos import Pos
from .EasingFunctions import EasingFunction
from . import EasingConstants as Easing

def valeurs_regulieres_entre_01(nombre_a_produire : int, inclure_0 : bool = True, inclure_1 : bool = False) -> list[float]:
    """
    Renvoie une liste de valeurs "régulières" entre 0 et 1 contenant `nombre_a_produire` éléments (sans toucher aux paramètres optionnels).
    Si ni inclure_0 ni inclure_1 sont True, alors renvoie `nombre_a_produire - 1` éléments. Si un des deux est `True`, renvoie exactement `nombre_a_produire`.  
    """
    debut : int = 0                     if inclure_0 else 1
    fin   : int = nombre_a_produire + 1 if inclure_1 else nombre_a_produire
    
    return [idex / nombre_a_produire for idex in range(debut, fin)]



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
        assert(list(temps_clefs) == sorted(temps_clefs)), "`temps_clefs` n'est pas rangée dans l'ordre croissant."
        # Je doute que `temps_clef` dépasse la dixaine d'éléments, la trier ne demandera pas beaucoup de temps.
        # Aussi, on doit convertir temps_clefs en liste car comparer une liste à une tuple renverra toujours faux (comme quoi, Python est plus sensé que javascript)
        
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

class MultiGradient:
    """Implémentation de MultiInterpolation pour les couleurs."""
    
    def __init__(
                self,
                couleurs_clefs : list[list[int]|tuple[int, ...]],
                temps_clefs    : list[float]|tuple[float, ...] = [],
        ):
        """
        Constructeur de MultiGradient.
        Le paramètre `couleurs_clefs[]` contient les valeurs clefs (la liste passée à MultiInterpolation.calculer_valeurs()) pour dans l'ordre le rouge, vert, bleu et alpha (transparence).
        Le paramètre `temps_clefs[]` contient les temps clefs pour lequels atteindre chaque couleur, si vide se complète de manière à se que les valeurs soient équidistantes.
        
        Exemples d'appel:
        MultiGradient(
            (NOIR, GRIS, BLEU),    # Toutes les valeurs RGB montent (pour aller à gris) puis le bleu augmente au maximum alors que le rouge et le vert décroissent (la transparence reste à 255 tout le long).
            [1/3]                  # On sera gris au tier de l'animation puis la couleur tendra vers le bleu
        )
        
        MultiGradient(
            ([0, 128, 255], [128, 0, 255], [255, 128, 0])
        )
        # reviens à la même chose que
        MultiGradient(
            ([0, 128, 255], [128, 0, 255], [255, 128, 0]),
            [1/2],
        )
        """
        couleurs_clefs = copy(couleurs_clefs)
        temps_clefs    = copy(temps_clefs)
        assert(len(couleurs_clefs) >= 2), "Il doit y avoir au moins 2 couleurs clefs."
        
        # Si les temps clefs sont vides, remplit les avec des valeurs régulières
        if len(temps_clefs) == 0:
            temps_clefs = valeurs_regulieres_entre_01(len(couleurs_clefs) - 1, inclure_0=False)
            # par exemple, si l'utilistateur donne 5 valeurs pour evolution_rgba[]
            # temps_clefs = [1/4, 2/4, 3/4]
            # encore une fois 0/4 et 4/4 sont ajoutés après
        assert(len(temps_clefs) == len(couleurs_clefs) - 2), f"Il doit y avoir exactement 2 éléments de moins dans `temps_clefs[]` que dans `couleurs_clefs[]`, on s'attend à {len(couleurs_clefs) - 2} éléments mais il y en a {len(temps_clefs)}."
        
        self._couleurs_clefs : list[rgba] = [iterable_to_rgba(coul) for coul in couleurs_clefs]
        self._temps_clefs : tuple[float, ...] = tuple(temps_clefs)
    
    def __repr__(self):
        return f"MultiGradient({self._couleurs_clefs=}, {self._temps_clefs=})"
    
    def calculer_valeur(
            self,
            t : float,
            easing_fun : EasingFunction = Easing.NO_EASING, easing_funs : list[EasingFunction]|tuple[EasingFunction, ...] = []
        ) -> rgba:
        """
        Même chose que sa version dans Gradient mais sur un nombre de couleurs indéterminées.
        Si `easing_funs[]` n'est pas vide alors utilise ses valeurs (doit avoir une valeur de moins que `self._couleurs_clefs[]`) sinon utilise `easing_fun`.
        """
        
        # La compréhension de liste en bas sert à extraire les couleurs en canaux
        # par exemple: ([255, 128, 0, 200], [128, 0, 200, 255], [0, 200, 255, 128])
        # -----------> ([255, 128, 0], [128, 0, 200], [0, 200, 255], [200, 255, 128])
        
        # Rien à voir mais maintenant que j'y pense, c'est une rotation de matrice:
        # (                                  (
        #  [255, 128, 0  , 200],              [255, 128, 0  ],
        #  [128, 0  , 200, 255],   ------>    [128, 0  , 200],
        #  [0  , 200, 255, 128]               [0  , 200, 255],
        # )                                   [200, 255, 128]
        #                                    )
        return iterable_to_rgba([
            round(
                MultiInterpolation.calculer_valeur(
                    [couleur[canal] for couleur in self._couleurs_clefs],
                    self._temps_clefs,
                    t,
                    easing_fun=easing_fun, easing_funs=easing_funs
                )
            )   for canal in range(4)
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
            
            for i in range(nb_iterations):
                yield self.calculer_valeur(i / (nb_iterations), easing_fun=easing)


class MultiDeplacement:
    """Implémentation de MultiInterpolation pour les positions."""
    
    def __init__(
                self,
                pos_clefs : list[Pos]|tuple[Pos, ...],
                temps_clefs : list[float]|tuple[float] = [],
        ) -> None:
        """
        Constructeur de MultiDeplacement.
        Le paramètre `pos_clefs[]` contient les positions clefs aux déplacement, un peu comme des keyframes.
        Le paramètre `temps_clefs[]` contients les temps clefs, soit pour temps_clef[i], le `t` pour lequel pos_clef[i-1] serait atteint (le premier (t=0) et dernier (t=1) sont implicites et ne doivent pas être présent).
                                    Si vide, est remplit de valeurs réglières.
        Exemples d'appel:
        MultiDeplacement(
            (Pos(0, 500), Pos(250, 250), Pos(500, 0))   # Les abcisses croissent  et les ordonnées décroissent.
            [.5]                                        # C'est comprit comme étant [0, 1/2, 1]
        )
        
        MultiDeplacement(
            (Pos(50, 200), Pos(50, 0), Pos(200, 200), Pos(200, 0))
            # si aucun autre argument n'est donné, chaque position sera atteinte avec un interval égal
            # dans ce cas là, c'est  comme si on avait passé
            # [1/3, 2/3]
        )
        """
        pos_clefs   = deepcopy(pos_clefs)
        temps_clefs = deepcopy(temps_clefs)
        assert(len(pos_clefs) >= 2), "Il doit y avoir au moins 2 positions clefs."
        
        # Si les temps clefs sont vides, remplit les avec des valeurs régulières
        if len(temps_clefs) == 0:
            temps_clefs = valeurs_regulieres_entre_01(len(pos_clefs) - 1, inclure_0=False)
        
        assert(len(temps_clefs) == len(pos_clefs) - 2), f"Il doit y avoir exactement 2 éléments de moins dans `temps_clefs[]` que dans `pos_clefs[]`, on s'attend à {len(pos_clefs) - 2} éléments mais il y en a {len(temps_clefs)}."
        
        self._positions_clefs : tuple[Pos, ...]   = tuple(pos_clefs)
        self._temps_clefs     : tuple[float, ...] = tuple(temps_clefs)
    
    def __repr__(self):
        return f"MultiDeplacement({self._positions_clefs=}, {self._temps_clefs=})"
    
    def calculer_valeur(
            self,
            t : float,
            easing_fun : EasingFunction = Easing.NO_EASING, easing_funs : list[EasingFunction]|tuple[EasingFunction, ...] = []
        ) -> Pos:
        """
        Même chose que sa version dans Deplacement mais sur un nombre de couleurs indéterminées.
        Si `easing_funs[]` n'est pas vide alors utilise ses valeurs (doit avoir une valeur de moins que `self._couleurs_clefs[]`) sinon utilise `easing_fun`.
        """
        
        # La compréhension de liste en bas sert à extraire les directions.
        # c'est la même chose que dans la classe `MultiGradent`,
        # allez voir la méthode coresspondante pour plus d'infos
        return Pos([
            round(
                MultiInterpolation.calculer_valeur(
                    [pos.tuple[direction] for pos in self._positions_clefs],
                    self._temps_clefs,
                    t,
                    easing_fun=easing_fun, easing_funs=easing_funs
                )
            )   for direction in range(2)
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