# Imports et choses importantes

import pygame
import sys
import time
import random
import logging

logging.basicConfig(level=logging.INFO)    # Active tous les logs

from typing      import TypeAlias, Callable, TypeVar, NoReturn, Any, Generator
from enum        import Enum, IntEnum, IntFlag, auto
from math        import isnan, cos, sin, pi, sqrt
from functools   import partial, total_ordering
from copy        import copy, deepcopy
from queue       import PriorityQueue
from dataclasses import dataclass
from os          import getcwd
from bisect      import insort


from pygame.math import Vector2 as Vecteur

from pygame.surface import (
    Surface,
)

from pygame.rect import (
    Rect,
)
pygame.init()