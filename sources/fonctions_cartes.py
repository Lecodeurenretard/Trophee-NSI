"""
Contient toutes les fonctions utilisées par les cartes ainsi que callbacks[] qui contient cesdites fonctions bien emballées.

projet : L'ascension de Esquimot
auteur : Dooheli, Lecodeurenretard, hibou509
"""
from Carte import *


def quitte_ou_double_aplliquer(self : Carte, attr : dict[str, Any]) -> None:
    if random.randint(0, 1) <= 0.5:
        self._attaque.cible.recoit_degats(40, self)
    else:
        self._attaque.lanceur.recoit_degats(40, self)

callbacks : dict[str, CarteInterfaceMethodes]  = {
    "quitte ou double" : CarteInterfaceMethodes(quitte_ou_double_aplliquer)
}