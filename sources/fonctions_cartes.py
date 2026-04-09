"""
Contient toutes les fonctions utilisées par les cartes ainsi que callbacks[] qui contient cesdites fonctions bien emballées.

projet : L'ascension de Esquimot
auteur : Dooheli, Lecodeurenretard, hibou509
"""
from Carte import *


def quitte_ou_double_jouee(self : Carte, attr : dict[str, Any]) -> None:
    if random.random() <= 0.4:
        self._attaque._cible_id = self._attaque._lanceur_id
    self._attaque.cible.recoit_degats(self._attaque.calculer_degats(), self._attaque)


callbacks : dict[str, CarteInterfaceMethodes]  = {
    "quitte ou double" : CarteInterfaceMethodes(jouee=quitte_ou_double_jouee)
}