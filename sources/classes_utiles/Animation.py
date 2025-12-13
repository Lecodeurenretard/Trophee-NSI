from imports import Generator, Optional, logging, Any, TypeVar, Enum, auto
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


# dans l'idéal, _generer_generateur() devrait être un décorateur
# mais l'intellisense ne marche pour les classes avec un décorateur custom

T = TypeVar('T')
#template<typename T>
def _generer_generateur(
        debut : T,
        fin   : T,
        nb_iterations : int,
        cls : type,
        easing : Optional[EasingFunction] = Easing.NO_EASING,
        boucle : bool = False,
        *postionnels, **noms_seulment   #d'autres arguments à passer
    ) -> Generator[T, None, None]:
    """
    Utilisé pour contenir la logique des méthodes generateur_s().
    cls` représente la classe accueillant la méthode.
    """
    if nb_iterations == 0:
        return
    
    premiere_iteration = True
    while boucle or premiere_iteration:
        premiere_iteration = False
        
        for i in range(nb_iterations-1):
            yield cls.calculer_valeur_s(debut, fin, i / (nb_iterations-1), easing_fun=easing, *postionnels, **noms_seulment)
        yield cls.calculer_valeur_s(debut, fin, 1, easing_fun=easing, *postionnels, **noms_seulment)

def _generer_generateur_multi(
        valeurs_clefs : list[T]|tuple[T, ...],
        temps_clefs   : list[float]|tuple[float, ...],
        nb_iterations : int,
        cls : type,
        easing_fun  : Optional[EasingFunction] = Easing.NO_EASING,
        easing_funs : list[EasingFunction]|tuple[EasingFunction, ...] = (),
        loop : bool = False,
        *postionnels, **noms_seulment   # d'autres arguments à passer
    ) -> Generator[T, None, None]:
    """_generer_generateur() mais pour les classes Multi..."""
    return _generer_generateur(valeurs_clefs, temps_clefs, nb_iterations, cls, easing=easing_fun, easing_funs=easing_funs, boucle=loop, *postionnels, **noms_seulment)  # type: ignore # erreur de template

# Certains logiciels d'animations et de montage proposent ces fonctionnalités (par exemple Blender et DaVinci)
# Les easing functions (j'ai pas le nom français) permettent d'avoir une animation plus fluide
# en accélerant au début et en ralentissant à la fin.
# Démo Desmos: https://www.desmos.com/calculator/rrinotdfez

# ici seules les fonctions ease-in-out sont mise car ce sont les plus naturelles.

# On pourrait le remplacer par un booléen
# mais il faudrait créer un alias de type de toute façon.
class SensLecture(Enum):
    AVANT   = auto()
    ARRIERE = auto()

class InterpolationLineaire:
    """
    L'interpolation linéaire, va d'une valeur A à une valeur B sans jamais changer de vitesse (on pourrait dire que sa dérivée est constante)
    https://fr.wikipedia.org/wiki/Interpolation_lin%C3%A9aire
    """
    
    def __init__(self, debut : float, fin : float, sens_lecture : SensLecture = SensLecture.AVANT):
        self._debut = debut
        self._fin  = fin
        self._sens = sens_lecture
    
    def __repr__(self):
        return f"InterpolationLineaire(debut={self._debut}; fin={self._fin}; sens_lecture={self._sens.name})"
    
    @staticmethod
    def calculer_valeur_s(debut : float, fin : float, t : float, easing_fun : EasingFunction = Easing.NO_EASING, sens_lecture : SensLecture = SensLecture.AVANT) -> float:
        """
        Calcule la valeur qu'a une valeur variant de `debut` à `fin` avec la fonction d'easing `easing_fun`.
        En d'autre mots, calcule l'ordonnée  de la courbe correspondante sur la fonction Desmos: https://www.desmos.com/calculator/rrinotdfez.
        """
        if sens_lecture == SensLecture.ARRIERE:
            t = 1 - t
        return debut + easing_fun(t) * (fin - debut)
    
    @staticmethod
    def generateur_s(
            debut : float,
            fin : float,
            nb_iterations : int,
            easing : EasingFunction = Easing.NO_EASING,
            loop : bool = False,
        ) -> Generator[float, None, None]:
        return _generer_generateur(debut, fin, nb_iterations, InterpolationLineaire, easing=easing, boucle=loop)
    
    def calculer_valeur(self, t : float, easing_fun : EasingFunction) -> float:
        return InterpolationLineaire.calculer_valeur_s(self._debut, self._fin, t, easing_fun=easing_fun, sens_lecture=self._sens)
    
    def generateur(
            self,
            nb_iterations : int,
            easing : EasingFunction = Easing.NO_EASING,
            loop : bool = False
        ) -> Generator[float, None, None]:
        return InterpolationLineaire.generateur_s(self._debut, self._fin, nb_iterations, easing=easing, loop=loop)


class Gradient:
    """Implémentation de InterpolationLineaire pour les couleurs."""
    def __init__(self, couleur_debut : color, couleur_fin : color, sens : SensLecture = SensLecture.AVANT):
        self._debut : rgba = color_to_rgba(couleur_debut)
        self._fin   : rgba = color_to_rgba(couleur_fin)
        self._sens  : SensLecture = sens
    
    def __repr__(self):
        return f"Gradient(debut={self._debut}, fin={self._fin}; sens_lecture={self._sens.name})"
    
    @staticmethod
    def calculer_valeur_s(
            debut : color,
            fin : color,
            t : float,
            easing_fun : Optional[EasingFunction] = None,
            sens_lecture : SensLecture = SensLecture.AVANT, *,
            r : EasingFunction = Easing.NO_EASING, g : EasingFunction = Easing.NO_EASING,
            b : EasingFunction = Easing.NO_EASING, a : EasingFunction = Easing.NO_EASING, 
        ) -> rgba:
        """
        Même chose que sa version dans InterpolationLineaire mais le fait sur 4 valeurs.
        Si l'argument `easing_fun` est fourni alors l'utilise pour toutes les couleurs, sinon utilise les arguments `r`, `g`, `b` et `a` pour les valeurs correspodantes.
        """
        if easing_fun is not None:
            return Gradient.calculer_valeur_s(debut, fin, t, sens_lecture=sens_lecture, r=easing_fun, g=easing_fun, b=easing_fun, a=easing_fun)
        
        debut = color_to_rgba(debut)
        fin = color_to_rgba(fin)
        return (
            round(InterpolationLineaire.calculer_valeur_s(debut[0], fin[0], t, easing_fun=r, sens_lecture=sens_lecture)),
            round(InterpolationLineaire.calculer_valeur_s(debut[1], fin[1], t, easing_fun=g, sens_lecture=sens_lecture)),
            round(InterpolationLineaire.calculer_valeur_s(debut[2], fin[2], t, easing_fun=b, sens_lecture=sens_lecture)),
            round(InterpolationLineaire.calculer_valeur_s(debut[3], fin[3], t, easing_fun=a, sens_lecture=sens_lecture)),
        )
    
    @staticmethod
    def generateur_s(
            debut : color,
            fin : color,
            nb_iterations : int,
            easing : Optional[EasingFunction] = None, *,
            r : EasingFunction = Easing.NO_EASING, g : EasingFunction = Easing.NO_EASING,
            b : EasingFunction = Easing.NO_EASING, a : EasingFunction = Easing.NO_EASING,
            loop : bool = True,
        ) -> Generator[rgba, None, None]:
                debut = color_to_rgba(debut)
                fin   = color_to_rgba(fin)
                return _generer_generateur(debut, fin, nb_iterations, Gradient, easing=easing, boucle=loop, r=r, g=g, b=b, a=a)
    
    @property
    def debut(self) -> rgba:
        return self._debut
   
    @property
    def fin(self) -> rgba:
        return self._fin
    
    def calculer_valeur(self, t : float, easing_fun : EasingFunction) -> rgba:
        return Gradient.calculer_valeur_s(self._debut, self._fin, t, easing_fun=easing_fun, sens_lecture=self._sens)
    
    def generateur(
            self,
            nb_iterations : int,
            easing : EasingFunction = Easing.NO_EASING,
            loop : bool = False
        ) -> Generator[rgba, None, None]:
        return Gradient.generateur_s(self._debut, self._fin, nb_iterations, easing=easing, loop=loop)


class Deplacement:
    """Implémentation de InterpolationLineaire pour les positions."""
    def __init__(self, position_debut : Pos, position_fin : Pos, sens_lecture : SensLecture = SensLecture.AVANT):
        self._debut : Pos = position_debut
        self._fin   : Pos = position_fin
        self._sens  : SensLecture = sens_lecture
    
    def __repr__(self):
        return f"Deplacement(debut={self._debut}, fin={self._fin}; sens_lecture={self._sens.name})"
    
    @staticmethod
    def calculer_valeur_s(
            debut : Pos,
            fin : Pos,
            t : float,
            sens_lecture : SensLecture = SensLecture.AVANT,
            *, easing_fun : Optional[EasingFunction] = None,
            x : EasingFunction = Easing.NO_EASING, y : EasingFunction = Easing.NO_EASING,
        ) -> Pos:
        """
        Même chose que sa version dans InterpolationLineaire mais le fait sur 2 valeurs.
        Si l'argument `easing_fun` est fourni alors l'utilise pour toutes les couleurs, sinon utilise les arguments `x` et `y` pour les valeurs correspodantes.
        """
        if easing_fun is not None:
            return Deplacement.calculer_valeur_s(debut, fin, t, sens_lecture=sens_lecture, x=easing_fun, y=easing_fun)
        return Pos(
            round(InterpolationLineaire.calculer_valeur_s(debut.x, fin.x, t, easing_fun=x, sens_lecture=sens_lecture)),
            round(InterpolationLineaire.calculer_valeur_s(debut.y, fin.y, t, easing_fun=y, sens_lecture=sens_lecture)),
        )
    
    @staticmethod
    def generateur_s(
            debut : Pos,
            fin : Pos,
            nb_iterations : int,
            easing_fun : Optional[EasingFunction] = None, *,
            x : EasingFunction = Easing.NO_EASING, y : EasingFunction = Easing.NO_EASING,
            loop : bool = False,
        ) -> Generator[Pos, None, None]:
        return _generer_generateur(debut, fin, nb_iterations, Deplacement, easing=easing_fun, boucle=loop, x=x, y=y)
    
    @property
    def debut(self) -> Pos:
        return self._debut
   
    @property
    def fin(self) -> Pos:
        return self._fin
    
    def calculer_valeur(
            self,
            t : float,
            easing_fun : Optional[EasingFunction] = None, *,
            x : EasingFunction = Easing.NO_EASING, y : EasingFunction = Easing.NO_EASING,
        ) -> Pos:
        return Deplacement.calculer_valeur_s(self._debut, self._fin, t, easing_fun=easing_fun, x=x, y=y, sens_lecture=self._sens)
    
    def generateur(
            self,
            nb_iterations : int,
            easing_fun : EasingFunction = Easing.NO_EASING,
            loop : bool = False
        ) -> Generator[Pos, None, None]:
        return Deplacement.generateur_s(self._debut, self._fin, nb_iterations, easing_fun=easing_fun, loop=loop)


# TODO: Métaclasses?

class MultiInterpolation:
    """
    Interpole une valeur avec plus de deux valeurs sans de magie de polynômes.
    """
    
    def __init__(
            self,
            valeurs_clefs : list[float]|tuple[float, ...],
            temps_clefs   : list[float]|tuple[float, ...] = (),
            sens_lecture  : SensLecture = SensLecture.AVANT,
        ) -> None:
        if len(temps_clefs) == 0:
            temps_clefs = valeurs_regulieres_entre_01(len(valeurs_clefs) - 1, inclure_0=False)
        MultiInterpolation.verifications_parametres(valeurs_clefs, temps_clefs)
        
        self._val_clefs   = valeurs_clefs
        self._temps_clefs = temps_clefs
        self._sens        = sens_lecture
    
    def __repr__(self):
        return f"MultiInterpolation(val_clefs={self._val_clefs}; temps_clefs={self._temps_clefs}; sens_lecture={self._sens.name})"
    
    # L'avantage de na pas approximer avec des polynômes, c'est que l'on peut
    # facilement changer les fonctions d'easing.
    @staticmethod
    def _adaptation_pour_2_points(valeurs, temps_clefs, t, easing_fun, easing_funs, sens_lecture : SensLecture) -> tuple[int, int, int, EasingFunction]:
        """
        Adapte les arguments de `.calculer_valeur()` pour les passer à la méthode de `InterpolationLinéaire`.
        Renvoie une tuple contenant dans l'ordre: le début et la fin du lerp, le t correspondant au nouvel interval ainsi que la fonction d'easing choisie.
        """
        # On garde t entre 0 et 1
        t = max(0, min(1, t))
        if sens_lecture == SensLecture.ARRIERE:
            t = 1 - t
        
        index_fin : int = 0
        for i, temps_clef in enumerate(temps_clefs):
            if t < temps_clef :
                index_fin = i
                break
        else:   # C'est bien indenté, Python authorise les for... else
            if t == 1: index_fin = len(temps_clefs) - 1
            else: raise ValueError(f"{t=} est strictement supérieur à 1.")
        
        # vérifie si on a besoin de changer `easing_fun`
        if len(easing_funs) != 0:
            if easing_fun != Easing.NO_EASING:
                logging.warning("Le paramètre `easing_fun` est ignoré car `easing_funs` a été passé.")
            
            easing_fun = easing_funs[index_fin-1] if index_fin != 0 else easing_funs[0]
        
        a = temps_clefs[index_fin - 1]; b = temps_clefs[index_fin]
        assert(0 <= a < b <= 1), f"Mauvais ordre, on devrait avoir 0 <= temps_clef[{index_fin-1}] (={a}) < temps_clef[{index_fin}] (={b}) <= 1"
        
        t_entre_ab = (t - a) / (b - a)
        
        return (valeurs[index_fin - 1], valeurs[index_fin], t_entre_ab, easing_fun)
    
    @staticmethod
    def verifications_parametres(
            valeurs_clefs : list[Any]|tuple[Any, ...],          # Le type des éléments de `valeurs_clefs[]` change suivant les classes
            temps_clefs   : list[float]|tuple[float, ...],
            easing_funs   : list[EasingFunction]|tuple[EasingFunction, ...] =  (),
        ) -> None:
        """Vérifie les valeurs passées en paramètre pour `MultiInterpolation` et classes dérivées."""
        if len(valeurs_clefs) < 2:
            raise ValueError(f"Pour faire une interpolation, il faut au moins 2 valeurs (seulemeent {len(valeurs_clefs)} ont été passées).")
        
        if len(temps_clefs) != len(valeurs_clefs) - 2:
            raise ValueError(
                "Il doit y avoir exactement deux valeurs de moins dans `temps_clefs`"           # C'est une syntaxe héritée du C
                " que dans valeurs (t=0 et t=1 sont implicites), seulement "                    # Le signe '+' est implicite entre les string litérales
                f"temps_clef contient {len(temps_clefs)} éléments contre {len(valeurs_clefs)}." # "bon" + "jour" == "bon" "jour" == "bonjour"
            )
        
        # Je doute que `temps_clef` dépasse la dixaine d'éléments, la trier ne demandera pas beaucoup de temps.
        # Aussi, on doit convertir temps_clefs en liste car comparer une liste à une tuple renverra toujours faux
        # (comme quoi, Python est plus sensé que javascript)
        if list(temps_clefs) != sorted(temps_clefs):
            raise ValueError("`temps_clefs[]` n'est pas rangée dans l'ordre croissant.")
        
        
        if len(easing_funs) != 0 and len(easing_funs) != len(valeurs_clefs):
            raise ValueError(
                f"Le nombre d'éléments dans `easing_funs[]` ({len(easing_funs)}) doit être le même"
                f" que le nombre d'éléments de `valeurs_clefs` ({len(valeurs_clefs)})."
            )
    
    @staticmethod
    def calculer_valeur_s(
            valeurs_clefs : list[float]|tuple[float, ...],
            temps_clefs   : list[float]|tuple[float, ...],
            t : float,
            easing_fun : EasingFunction = Easing.NO_EASING,
            easing_funs : list[EasingFunction]|tuple[EasingFunction, ...] = (),
            sens_lecture : SensLecture = SensLecture.AVANT,
        ) -> float:
        """
        Même chose que la version de `InterpolationLineaire` mais agit sur un "chemin" de valeurs `valeurs_clefs[]` au lieu d'un début et d'une fin.
        `temps_clefs[i]` est la valeur de `t` pour laquelle `valeur_clef[i]` sera atteinte.
        Si `easing_funs[]` est fournie, sa valeur écrasera celle de `easing_fun`.

        La version mathématique si ça interesse quelqu'un:
        Soit un plan quelconque, on ne s'interesse qu'aux points dont l'abcisse est entre 0 et 1 inclus.
        On y place des points qui ont pour coordonées (temps_clefs[i]; valeurs[i+1]) avec 0 < i <= n, n = len(valeurs) - 2 = len(temps_clefs).
        On place aussi (0; valeurs[0]) et (n+1; valeurs[n+1]).
        Nous relions ensuite les points entre eux en respectant les fonctions d'easing repectives pour obtenir une courbe C.
        La fonction renvoie donc l'ordonnée du point de C ayant pour abcisse `t`.
        """
        MultiInterpolation.verifications_parametres(valeurs_clefs, temps_clefs)
        temps_clefs = [0, *temps_clefs, 1]  # 0 et 1 sont implicites pour l'utilisateur, on les met ici
        
        debut, fin, nouveau_t, easing_fun = MultiInterpolation._adaptation_pour_2_points(
            valeurs_clefs, temps_clefs,
            t,
            easing_fun, easing_funs,
            sens_lecture=sens_lecture
        )
        return InterpolationLineaire.calculer_valeur_s(debut, fin, nouveau_t, easing_fun=easing_fun, sens_lecture=sens_lecture)
    
    @staticmethod
    def generateur_s(
            valeurs_clefs : list[float]|tuple[float, ...],
            temps_clefs   : list[float]|tuple[float, ...],
            nb_iterations : int,
            easing_fun    : EasingFunction = Easing.NO_EASING,
            easing_funs   : list[EasingFunction]|tuple[EasingFunction, ...] = (),
            loop          : bool = False,
        ) -> Generator[float, None, None]:
        return _generer_generateur_multi(valeurs_clefs, temps_clefs, nb_iterations, MultiInterpolation, easing_fun=easing_fun, easing_funs=easing_funs, loop=loop)
    
    def calculer_valeur(
            self,
            t : float,
            easing_fun : EasingFunction,
            easing_funs   : list[EasingFunction]|tuple[EasingFunction, ...] = (),
        ) -> float:
        return MultiInterpolation.calculer_valeur_s(self._val_clefs, self._temps_clefs, t, easing_fun=easing_fun, easing_funs=easing_funs, sens_lecture=self._sens)
    
    def generateur(
            self,
            nb_iterations : int,
            easing_fun    : EasingFunction = Easing.NO_EASING,
            easing_funs   : list[EasingFunction]|tuple[EasingFunction, ...] = (),
            loop          : bool = False,
        ) -> Generator[float, None, None]:
        return MultiInterpolation.generateur_s(self._val_clefs, self._temps_clefs, nb_iterations, easing_fun=easing_fun, easing_funs=easing_funs, loop=loop)

class MultiGradient:
    """Implémentation de MultiInterpolation pour les couleurs."""
    
    def __init__(
            self,
            couleurs_clefs : list[color]|tuple[color, ...],
            temps_clefs    : list[float]|tuple[float, ...] = (),
            sens_lecture : SensLecture = SensLecture.AVANT,
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
        
        # Si les temps clefs sont vides, remplit les avec des valeurs régulières
        if len(temps_clefs) == 0:
            temps_clefs = valeurs_regulieres_entre_01(len(couleurs_clefs) - 1, inclure_0=False)
            # par exemple, si l'utilistateur donne 5 valeurs pour evolution_rgba[]
            # temps_clefs = [1/4, 2/4, 3/4]
            # encore une fois 0/4 et 4/4 sont ajoutés après
        MultiInterpolation.verifications_parametres(couleurs_clefs, temps_clefs)
        
        self._couleurs_clefs : list[rgba]        = [color_to_rgba(coul) for coul in couleurs_clefs]
        self._temps_clefs    : tuple[float, ...] = tuple(temps_clefs)
        self._sens           : SensLecture       = sens_lecture
    
    def __repr__(self):
        return f"MultiGradient({self._couleurs_clefs=}, {self._temps_clefs=}, {self._sens.name=})"
    
    @staticmethod
    def calculer_valeur_s(
            couleurs_clefs : list[color]|tuple[color, ...],
            temps_clefs    : list[float]|tuple[float, ...],
            t : float,
            easing_fun : EasingFunction = Easing.NO_EASING,
            easing_funs : list[EasingFunction]|tuple[EasingFunction, ...] = [],
            sens_lecture : SensLecture = SensLecture.AVANT,
        ) -> rgba:
        """
        Même chose que sa version dans Gradient mais sur un nombre de couleurs indéterminées.
        Si `easing_funs[]` n'est pas vide alors utilise ses valeurs (doit avoir une valeur de moins que `self._couleurs_clefs[]`) sinon utilise `easing_fun`.
        """
        
        # La compréhension de liste en bas sert à extraire les couleurs en canaux
        # par exemple: ([255, 128, 0, 200], [128, 0, 200, 255], [0, 200, 255, 128])
        # -----------> ([255, 128, 0], [128, 0, 200], [0, 200, 255], [200, 255, 128])
        
        # Rien à voir mais maintenant que j'y pense, c'est (presque) une rotation de matrice:
        # (                                  (
        #  [255, 128, 0  , 200],              [255, 128, 0  ],
        #  [128, 0  , 200, 255],   ------>    [128, 0  , 200],
        #  [0  , 200, 255, 128]               [0  , 200, 255],
        # )                                   [200, 255, 128]
        #                                    )
        return iterable_to_rgba([
            round(
                MultiInterpolation.calculer_valeur_s(
                    [couleur[canal] for couleur in couleurs_clefs],
                    temps_clefs,
                    t,
                    easing_fun=easing_fun, easing_funs=easing_funs,
                    sens_lecture=sens_lecture
                )
            )   for canal in range(4)
        ])
    
    @staticmethod
    def generateur_s(
            couleurs_clefs : list[color]|tuple[color, ...],
            temps_clefs    : list[float]|tuple[float, ...],
            nb_iterations : int,
            easing_fun : EasingFunction = Easing.NO_EASING,
            easing_funs   : list[EasingFunction]|tuple[EasingFunction, ...] = (),
            loop : bool = False,
        ) -> Generator[rgba, None, None]:
        couleurs_clefs = [color_to_rgba(col) for col in couleurs_clefs]
        return _generer_generateur_multi(couleurs_clefs, temps_clefs, nb_iterations, MultiGradient, easing_fun=easing_fun, easing_funs=easing_funs, loop=loop)  #type:ignore # on est sûr que le type est rgba
    
    def calculer_valeur(
            self,
            t : float,
            easing_fun : EasingFunction = Easing.NO_EASING,
            easing_funs : list[EasingFunction]|tuple[EasingFunction, ...] = [],
        ):
        return MultiGradient.calculer_valeur_s(
            self._couleurs_clefs,        # type: ignore # même problème que dans .generateur()
            self._temps_clefs,
            t,
            easing_fun=easing_fun,
            easing_funs=easing_funs,
            sens_lecture=self._sens
        )
    
    def generateur(
            self,
            nb_iterations : int,
            easing_fun    : EasingFunction = Easing.NO_EASING,
            easing_funs   : list[EasingFunction]|tuple[EasingFunction, ...] = (),
            loop : bool = False,
        ):
        return MultiGradient.generateur_s(
            self._couleurs_clefs,       # type: ignore  # apparament "list[rgba]" to "list[color]|tuple[color, ...]" n'est pas une bonne convertion.
            self._temps_clefs,
            nb_iterations, loop=loop,
            easing_fun=easing_fun, easing_funs=easing_funs
        )


class MultiDeplacement:
    """Implémentation de MultiInterpolation pour les positions."""
    
    def __init__(
                self,
                pos_clefs   : list[Pos]|tuple[Pos, ...],
                temps_clefs : list[float]|tuple[float, ...] = [],
                sens_lecture : SensLecture = SensLecture.AVANT,
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
        # Si les temps clefs sont vides, remplit les avec des valeurs régulières
        if len(temps_clefs) == 0:
            temps_clefs = valeurs_regulieres_entre_01(len(pos_clefs) - 1, inclure_0=False)
        MultiInterpolation.verifications_parametres(pos_clefs, temps_clefs)
        
        self._positions_clefs : tuple[Pos, ...]   = tuple(pos_clefs)
        self._temps_clefs     : tuple[float, ...] = tuple(temps_clefs)
        self._sens            : SensLecture       = sens_lecture
    
    def __repr__(self):
        return (
            "MultiDeplacement("
            f"positions_clefs={self._positions_clefs}"
            f", temps_clefs={self._temps_clefs}"
            f", sens_lecture={self._sens.name}"
            ")"
        )
    
    @staticmethod
    def calculer_valeur_s(
            positions_clefs : list[Pos]|tuple[Pos, ...],
            temps_clefs     : list[float]|tuple[float, ...],
            t : float,
            easing_fun : EasingFunction = Easing.NO_EASING,
            easing_funs : list[EasingFunction]|tuple[EasingFunction, ...] = [],
            sens_lecture : SensLecture = SensLecture.AVANT,
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
                MultiInterpolation.calculer_valeur_s(
                    [pos.tuple[direction] for pos in positions_clefs],
                    temps_clefs,
                    t,
                    easing_fun=easing_fun,
                    easing_funs=easing_funs,
                    sens_lecture=sens_lecture,
                )
            )   for direction in range(2)
        ])
    
    @staticmethod
    def generateur_s(
            positions_clefs : list[Pos]|tuple[Pos, ...],
            temps_clefs     : list[float]|tuple[float, ...],
            nb_iterations : int,
            easing_fun        : EasingFunction = Easing.NO_EASING,
            easing_funs   : list[EasingFunction]|tuple[EasingFunction, ...] = (),
            loop : bool = False,
        ) -> Generator[Pos, None, None]:
        return _generer_generateur_multi(positions_clefs, temps_clefs, nb_iterations, MultiDeplacement, easing_fun=easing_fun, easing_funs=easing_funs, loop=loop)
    
    def calculer_valeur(
            self,
            t : float,
            easing_fun : EasingFunction = Easing.NO_EASING,
            easing_funs : list[EasingFunction]|tuple[EasingFunction, ...] = [],
        ) -> Pos:
        return MultiDeplacement.calculer_valeur_s(
            self._positions_clefs,
            self._temps_clefs,
            t,
            easing_fun=easing_fun,
            easing_funs=easing_funs,
            sens_lecture=self._sens
        )
    
    def generateur(
            self,
            nb_iterations : int,
            easing_fun : EasingFunction = Easing.NO_EASING,
            easing_funs   : list[EasingFunction]|tuple[EasingFunction, ...] = (),
            loop : bool = False,
        ) -> Generator[Pos, None, None]:
        return MultiDeplacement.generateur_s(self._positions_clefs, self._temps_clefs, nb_iterations, easing_fun=easing_fun, easing_funs=easing_funs, loop=loop)