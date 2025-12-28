"""imports externes et de modules."""

import logging
import pygame
import random
import math
import json

logging.basicConfig(level=logging.INFO)    # Active tous les logs

from typing      import Callable, Optional, Iterable, Sequence, MutableSequence, Mapping, MutableMapping	# les "duck types"
from typing      import TypeAlias, TypeVar, NoReturn, Any, Generator, Literal, overload, override			# les pas "ducks types"
from functools   import partial, total_ordering
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

from tkinter.messagebox import showerror as afficher_erreur
from pygame.math        import Vector2   as Vecteur
v_x = Vecteur(1, 0)    # permet d'alleger certaine définitions de vecteurs
v_y = Vecteur(0, 1)    # 5 * v_y au lieu de Vecteur(0, 5)

pygame.init()