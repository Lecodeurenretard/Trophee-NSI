from typing import TypeAlias

rgb   : TypeAlias = tuple[int, int, int]
rgba  : TypeAlias = tuple[int, int, int, int]
color : TypeAlias = rgb|rgba


NOIR    : rgb = (0, 0, 0)
BLANC   : rgb = (255, 255, 255)
GRIS    : rgb = (100, 100, 100)
GRIS_CLAIR : rgb = (145, 145, 145)

ROUGE   : rgb = (255, 0, 0)
VERT    : rgb = (0, 255, 0)
BLEU    : rgb = (0, 0, 255)
BLEU_CLAIR : rgb = (50, 50, 255)
CYAN       : rgb = (0, 255, 255)
JAUNE      : rgb = (255, 255, 0)

TRANSPARENT : rgba = (0, 0, 0, 0)



def rgb_to_rgba(couleur : rgb, nouvelle_transparence : int = 255) -> rgba:
    """Convertit une couleur RGB en RGBA. La transparence a donner à la nouvelle couleur est `nouvelle_transparence`."""
    return (*couleur, nouvelle_transparence)

def rgba_to_rgb(couleur : rgba) -> rgb:
    """Convertit une couleur RGBA en RGB en effaçant sa donnée de transparence (Souvent interprété comme si la couleur est opaque)."""
    return (couleur[0], couleur[1], couleur[2])

def color_to_rgba(couleur : color, nouvelle_transparence : int = 255) -> rgba:
    """Cette fonction est pour éviter les longues ternaires et ne pas calmer le vérifieur de types: si necessaire, elle appelle rgb_to_rgba()"""
    if len(couleur) == 3:
        return rgb_to_rgba(couleur, nouvelle_transparence)
    return couleur

def color_to_rgb(couleur : color) -> rgb:
    """Cette fonction est pour éviter les longues ternaires et ne pas calmer le vérifieur de types: si necessaire, elle appelle rgba_to_rgb()"""
    if len(couleur) == 4:
        return rgba_to_rgb(couleur)
    return couleur