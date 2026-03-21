"""imports externes."""

import logging
import pygame
import random
import shutil
import math
import json
import sys
import os

logging.basicConfig(level=logging.INFO)    # Active tous les logs

from typing         import TypeAlias, TypeVar, NoReturn, Any, Generator, Literal, overload, override, Generic, ClassVar         # les pas "ducks types"
from typing         import Callable, Optional, Iterable, Sequence, MutableSequence, Mapping, MutableMapping, Iterator, Self     # les "duck types"
from functools      import partial, total_ordering, lru_cache
from abc            import ABC, abstractmethod
from dataclasses    import dataclass, field
from enum           import Enum, Flag, auto
from copy           import copy, deepcopy
from math           import cos, sin, sqrt
from queue          import PriorityQueue
from bisect         import insort
from glob           import glob
from import_tkinter import *

from pygame.surface import Surface
from pygame.rect    import Rect
from pygame.mixer   import Sound
from pygame.font    import Font
from pygame.math    import Vector2 as Vecteur




# https://www.pygame.org/docs/ref/pygame.html#pygame.init
if pygame.init()[1] > 0:
    afficher_erreur(
        "Erreur Pygame",
        "Echec de l'initialisation de certains modules pygame, "
        "veuillez vérifier votre installation."
    )