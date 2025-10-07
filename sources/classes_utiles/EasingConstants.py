from .EasingFunctions import EasingFunction, EasingType

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