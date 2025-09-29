# Imports et choses importantes

import pygame
import random
import logging
import math

logging.basicConfig(level=logging.INFO)    # Active tous les logs

from typing      import TypeAlias, Callable, TypeVar, NoReturn, Any, Generator, Optional, overload
from enum        import Enum, IntEnum, IntFlag, auto
from functools   import partial, total_ordering
from math        import isnan, cos, sin, sqrt
from copy        import copy, deepcopy
from queue       import PriorityQueue
from dataclasses import dataclass
from os          import getcwd
from bisect      import insort
from sys         import exit


from pygame.surface import Surface
from pygame.rect    import Rect

from pygame.math import Vector2 as Vecteur

pygame.init()