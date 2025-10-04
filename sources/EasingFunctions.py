from imports import TypeAlias, Callable, math, cos, sqrt, Enum, auto

# Ces fonctions sont définies dans [0; 1] et ont leurs images dans [0; 1]
EasingFunction : TypeAlias = Callable[[float], float]
def inversement_ease(easing_fun : EasingFunction) -> EasingFunction:
        """Les fonctions ease-in deviennent ease-out et inversement."""
        return lambda x: 1 - easing_fun(1 - x)


class EasingType(Enum):
    NONE = 0
    POLYNOMIAL    = auto()
    EXPONENTIAL   = auto()
    CIRCULAR      = auto()
    TRIGONOMETRIC = auto()
    
    # Tout le commentaire est un essai d'overload pour ease_in(), ease_out() et ease_in_out(). C'est impossible à faire.
    # Par contre, j'ai trouvé une libraire externe pour ça, je ne sais pas si ça vaut le coup de l'intaller encore
    # https://github.com/t2y/extenum
    ## Voilà pourquoi les headers sont importants
    ## @classmethod
    ## @overload(NONE)
    ## def ease_in(cls, type) -> EasingFunction:
    ##     """Renvoie la fonction d'easing n'ayant aucun effet. La fonction retounée admet que son argument est entre 0 et 1 (inclus)."""
    ## @classmethod
    ## @overload
    ## def ease_in(cls, type : Literal[1], n_a : int) -> EasingFunction:
    ##     """Renvoie la fonction ease-in correspondant pour les x^n_a. La fonction retounée admet que son argument est entre 0 et 1 (inclus)."""
    ## @classmethod
    ## @overload
    ## def ease_in(cls, type : Literal[2], n_a : float) -> EasingFunction:
    ##     """Renvoie la fonction ease-in correspondant pour les n_a^x. La fonction retounée admet que son argument est entre 0 et 1 (inclus)."""
    ## @classmethod
    ## @overload
    ## def ease_in(cls, type : Literal[3]) -> EasingFunction:
    ##     """Renvoie la fonction ease-in radiale. La fonction retounée admet que son argument est entre 0 et 1 (inclus)."""
    ## @classmethod
    ## @overload
    ## def ease_in(cls, type : Literal[4]) -> EasingFunction:
    ##     """Renvoie la fonction ease-in trigonometrique. La fonction retounée admet que son argument est entre 0 et 1 (inclus)."""
    ## 
    ## @classmethod
    ## @overload
    ## def ease_out(cls, type : Literal[0]) -> EasingFunction:
    ##     """Renvoie la fonction d'easing n'ayant aucun effet. La fonction retounée admet que son argument est entre 0 et 1 (inclus)."""
    ## @classmethod
    ## @overload
    ## def ease_out(cls, type : Literal[1], n_a : int) -> EasingFunction:
    ##     """Renvoie la fonction ease-out correspondant pour les x^n_a. La fonction retounée admet que son argument est entre 0 et 1 (inclus)."""
    ## @classmethod
    ## @overload
    ## def ease_out(cls, type : Literal[2], n_a : float) -> EasingFunction:
    ##     """Renvoie la fonction ease-out correspondant pour les n_a^x. La fonction retounée admet que son argument est entre 0 et 1 (inclus)."""
    ## @classmethod
    ## @overload
    ## def ease_out(cls, type : Literal[3]) -> EasingFunction:
    ##     """Renvoie la fonction ease-out radiale. La fonction retounée admet que son argument est entre 0 et 1 (inclus)."""
    ## @classmethod
    ## @overload
    ## def ease_out(cls, type : Literal[4]) -> EasingFunction:
    ##     """Renvoie la fonction ease-out trigonometrique. La fonction retounée admet que son argument est entre 0 et 1 (inclus)."""
    ## 
    ## @classmethod
    ## @overload
    ## def ease_in_out(cls, type : Literal[0]) -> EasingFunction:
    ##     """Renvoie la fonction d'easing n'ayant aucun effet. La fonction retounée admet que son argument est entre 0 et 1 (inclus)."""
    ## @classmethod
    ## @overload
    ## def ease_in_out(cls, type : Literal[1], n_a : int) -> EasingFunction:
    ##     """Renvoie la fonction ease-in-out correspondant pour les x^n_a. La fonction retounée admet que son argument est entre 0 et 1 (inclus)."""
    ## @classmethod
    ## @overload
    ## def ease_in_out(cls, type : Literal[2], n_a : float = 2, b : float = 4.04) -> EasingFunction:
    ##     """Renvoie la fonction ease-in-out correspondant pour les n_a^x. La fonction retounée admet que son argument est entre 0 et 1 (inclus)."""
    ## @classmethod
    ## @overload
    ## def ease_in_out(cls, type : Literal[3]) -> EasingFunction:
    ##     """Renvoie la fonction ease-in-out radiale. La fonction retounée admet que son argument est entre 0 et 1 (inclus)."""
    ## @classmethod
    ## @overload
    ## def ease_in_out(cls, type : Literal[4]) -> EasingFunction:
    ##    """Renvoie la fonction ease-in-out trigonometrique. La fonction retounée admet que son argument est entre 0 et 1 (inclus)."""
    
    @classmethod
    def ease_in(cls, type_fun : 'EasingType', n_a : int|float|None = None) -> EasingFunction:
        # Ne me demandez pas pourquoi tel formule est comme ça, j'ai demandé à Claude
        # et ses réponses semblaient correctes sur Desmos du coup je les aient mises ici.
        match type_fun:
            case cls.NONE:
                return lambda x: x
            
            case cls.POLYNOMIAL:
                assert(type(n_a) is int and n_a > 0), "On ne considère que les exponents strictements postifs et entiers."
                return lambda x: x ** n_a
            
            case cls.EXPONENTIAL:
                assert(type(n_a) is float and n_a >= 2), "On accepte que les n_a supérieurs ou égaux à 2."
                return lambda x: n_a**(10*x - 10)
            
            case cls.CIRCULAR:
                return lambda x: 1 - sqrt(1 -  x**2)
            
            case cls.TRIGONOMETRIC:
                return lambda x: 1 - cos(x * math.pi / 2)
            
            case _:
                raise NotImplementedError("Cas non prévu.")
    
    
    @classmethod
    def ease_out(cls, type_fun : 'EasingType', n_a : int|float|None = None) -> EasingFunction: # pyright: ignore[reportInconsistentOverload]
        if type_fun == cls.NONE:
            return lambda x: x
        return lambda y: 1 - cls.ease_in(type_fun, n_a)(1 - y)
    
    @classmethod
    def ease_in_out(cls, type_fun : 'EasingType', n_a : int|float|None = None, b : float = 4.04) -> EasingFunction:
        # calque prend 2 arguments, le premier sera (x) si x < .5 sinon (1 - x), le second sera toujours égal à x.
        calque : EasingFunction = lambda x: 0
        
        match type_fun:
            case cls.NONE:
                return lambda x: x
            
            case cls.POLYNOMIAL:
                assert(type(n_a) is int and n_a > 0), "On ne considère que les exponents strictements postifs et entiers."
                calque = lambda x, n=n_a: 2**(n - 1) * x**n
            
            case cls.EXPONENTIAL:
                assert(type(n_a) is float and n_a >= 2 and b >= 4.04), "On accepte que les n_a supérieurs ou égaux à 2, b doit donc être supérieur ou égal à 4.04."
                calque = lambda x, n_a=n_a, b=b: n_a**(10 * (x - 1) + b) - n_a**(b - 10)
            
            case cls.CIRCULAR:
                calque = lambda x: .5 - sqrt(abs(.25 -  x**2))
            
            case cls.TRIGONOMETRIC:
                # Celle-ci marche pour tout 0 <= x <=1 pour je ne sais qu'elle raison.
                return lambda x: .5 - cos(math.pi * x) / 2
            
            case _:
                raise NotImplementedError("Cas non prévu.")
        
        # En principe, les deux doivent être égales à 0.5 dans les cas codés (sauf les exponentielles qui doivent être environ égales)
        assert(math.isclose(calque(.5), inversement_ease(calque)(.5))), f"Erreur de formule: {calque(.5)} != {inversement_ease(calque)(.5)}"
        
        return lambda x: calque(x) if x < .5 else inversement_ease(calque)(x)

def ecraser_easing(easing : EasingFunction, intervalle : tuple[float, float]) -> EasingFunction:
    """
    Fait en sorte que la fonction `easing` (on admet qu'elle ne soit pas déjà écrasée) ne varie seulement que dans l'intervalle donné.
    Avant la fonction renvoie `easing(0)`, après l'intervalle elle renvoie `easing(1)`.
    Visualitation Desmos (dossier après la définition de p): https://www.desmos.com/calculator/rrinotdfez
    """
    assert(0 <= intervalle[0] < intervalle[1] <= 1), "Les valeurs de l'intervalle doivent être entre 0 et 1, et la première strictement inférieure à la seconde."
    return lambda x, a=intervalle[0], b=min(intervalle[1], 1-intervalle[0]): easing(max(min((x - a) / b, 1), 0))

NO_EASING     : EasingFunction = EasingType.ease_in_out(EasingType.NONE)
SQUARE        : EasingFunction = EasingType.ease_in_out(EasingType.POLYNOMIAL, 2)
CUBE          : EasingFunction = EasingType.ease_in_out(EasingType.POLYNOMIAL, 3)
HYPERCUBE     : EasingFunction = EasingType.ease_in_out(EasingType.POLYNOMIAL, 4)
EXPONENTIAL   : EasingFunction = EasingType.ease_in_out(EasingType.EXPONENTIAL, 2.0, 4.0458036896)
CIRCULAR      : EasingFunction = EasingType.ease_in_out(EasingType.CIRCULAR)
TRIGONOMETRIC : EasingFunction = EasingType.ease_in_out(EasingType.TRIGONOMETRIC)

FADE       : EasingFunction = CUBE
EXPONENT_4 : EasingFunction = HYPERCUBE
RADIAL     : EasingFunction = CIRCULAR