# Imports et choses importantes

import pygame
import sys
import time
import random
import logging
logging.basicConfig(level=logging.DEBUG)    # Active tous les logs

from os import getcwd
from math import isnan
from typing import TypeAlias, Callable, TypeVar, NoReturn, Any
from copy import copy, deepcopy
from functools import partial
from enum import Enum, IntEnum, IntFlag, auto


from pygame.surface import (
    Surface,
)

from pygame.rect import (
    Rect,
)

MODE_DEBUG : bool = True