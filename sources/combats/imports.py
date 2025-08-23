# Imports et choses importantes

import pygame
import sys
import time
import random
import logging

logging.basicConfig(level=logging.INFO)    # Active tous les logs

from typing      import TypeAlias, Callable, TypeVar, NoReturn, Any
from enum        import Enum, IntEnum, IntFlag, auto
from copy        import copy, deepcopy
from queue       import PriorityQueue
from dataclasses import dataclass
from functools   import partial
from os          import getcwd
from bisect      import insort
from math        import isnan


from pygame.surface import (
    Surface,
)

from pygame.rect import (
    Rect,
)
pygame.init()