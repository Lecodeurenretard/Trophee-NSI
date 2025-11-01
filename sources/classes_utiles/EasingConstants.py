from .EasingFunctions import EasingFunction, EasingType

NO_EASING     : EasingFunction = EasingType.ease_in_out(EasingType.NONE)
SQUARE        : EasingFunction = EasingType.ease_in_out(EasingType.POLYNOMIAL, 2)
CUBE          : EasingFunction = EasingType.ease_in_out(EasingType.POLYNOMIAL, 3)
HYPERCUBE     : EasingFunction = EasingType.ease_in_out(EasingType.POLYNOMIAL, 4)
EXPONENTIAL   : EasingFunction = EasingType.ease_in_out(EasingType.EXPONENTIAL, 2.0, 4.0458036896)
CIRCULAR      : EasingFunction = EasingType.ease_in_out(EasingType.CIRCULAR)
TRIGONOMETRIC : EasingFunction = EasingType.ease_in_out(EasingType.TRIGONOMETRIC)

SQUARE_IN        : EasingFunction = EasingType.ease_in(EasingType.POLYNOMIAL, 2)
CUBE_IN          : EasingFunction = EasingType.ease_in(EasingType.POLYNOMIAL, 3)
HYPERCUBE_IN     : EasingFunction = EasingType.ease_in(EasingType.POLYNOMIAL, 4)
EXPONENTIAL_IN   : EasingFunction = EasingType.ease_in(EasingType.EXPONENTIAL, 2.0)
CIRCULAR_IN      : EasingFunction = EasingType.ease_in(EasingType.CIRCULAR)
TRIGONOMETRIC_IN : EasingFunction = EasingType.ease_in(EasingType.TRIGONOMETRIC)

SQUARE_OUT        : EasingFunction = EasingType.ease_out(EasingType.POLYNOMIAL, 2)
CUBE_OUT          : EasingFunction = EasingType.ease_out(EasingType.POLYNOMIAL, 3)
HYPERCUBE_OUT     : EasingFunction = EasingType.ease_out(EasingType.POLYNOMIAL, 4)
EXPONENTIAL_OUT   : EasingFunction = EasingType.ease_out(EasingType.EXPONENTIAL, 2.0)
CIRCULAR_OUT      : EasingFunction = EasingType.ease_out(EasingType.CIRCULAR)
TRIGONOMETRIC_OUT : EasingFunction = EasingType.ease_out(EasingType.TRIGONOMETRIC)

FADE       : EasingFunction = CUBE
EXPONENT_4 : EasingFunction = HYPERCUBE
RADIAL     : EasingFunction = CIRCULAR

FADE_IN       : EasingFunction = CUBE_IN
EXPONENT_4_IN : EasingFunction = HYPERCUBE_IN
RADIAL_IN     : EasingFunction = CIRCULAR_IN

FADE_OUT       : EasingFunction = CUBE_OUT
EXPONENT_4_OUT : EasingFunction = HYPERCUBE_OUT
RADIAL_OUT     : EasingFunction = CIRCULAR_OUT