"""imports externes et de modules."""

import logging
import pygame
import random
import math
import json

logging.basicConfig(level=logging.INFO)    # Active tous les logs

from typing      import TypeAlias, TypeVar, NoReturn, Any, Generator, Literal, overload, override, Generic         # les pas "ducks types"
from typing      import Callable, Optional, Iterable, Sequence, MutableSequence, Mapping, MutableMapping, Iterator # les "duck types"
from functools   import partial, total_ordering, lru_cache
from abc         import ABC, abstractmethod
from dataclasses import dataclass, field
from enum        import Enum, Flag, auto
from copy        import copy, deepcopy
from math        import cos, sin, sqrt
from queue       import PriorityQueue
from bisect      import insort
from glob        import glob
from sys         import exit

from pygame.surface import Surface
from pygame.rect    import Rect
from pygame.mixer   import Sound
from pygame.font    import Font

try:
    from tkinter.messagebox import showerror as afficher_erreur # pyright: ignore[reportAssignmentType]
except ModuleNotFoundError:
    logging.error("Impossible d'importer tkinter.")
    # Si on ne peut pas importer tKinter (aka on est sur mon PC)
    # On crée une fonction de remplacement
    def afficher_erreur(
            title: str | None = None,
            message: str | None = None,
            *,
            icon: Literal['error', 'info', 'question', 'warning'] = 'error',
        ):
        logging.error(f"{title}: {message}")
from pygame.math        import Vector2   as Vecteur
v_x = Vecteur(1, 0)    # permet d'alleger certaine définitions de vecteurs
v_y = Vecteur(0, 1)    # 5 * v_y au lieu de Vecteur(0, 5)

pygame.init()