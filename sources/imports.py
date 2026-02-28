"""imports externes et de modules."""

import logging
import pygame
import random
import shutil
import math
import json
import sys
import os

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

from pygame.surface import Surface
from pygame.rect    import Rect
from pygame.mixer   import Sound
from pygame.font    import Font
from pygame.math    import Vector2 as Vecteur

try:
    # le message d'erreur dit que le afficher_erreur() importé n'a pas la même signature
    # que le afficher_erreur() défini en bas (ce sont des paramètre non utilisés, c'est pas grave)
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
        logging.error(f"{title} ({icon}): {message}")



# https://www.pygame.org/docs/ref/pygame.html#pygame.init
if pygame.init()[1] > 0:
    afficher_erreur(
        "Erreur Pygame",
        "Echec de l'initialisation de certains modules pygame, "
        "veuillez vérifier votre installation."
    )