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
JAUNE      : rgb = (255, 255, 0)

TRANSPARENT : rgba = (0, 0, 0, 0)