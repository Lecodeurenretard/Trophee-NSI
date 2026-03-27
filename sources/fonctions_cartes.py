"""
Contient toutes les fonctions utilisées par les cartes ainsi que callbacks[] qui contient cesdites fonctions bien emballées.

projet : L'ascension de Esquimot
auteur : Dooheli, Lecodeurenretard, hibou509
"""
from Attaque import *

#reprend le principe de BossInterfaceMethodes mais pour les cartes.

@dataclass
class CarteInterfaceMethodes:
    appliquer : None|Callable[[Attaque, dict[str, Any]], None] = None
    
    attributs_supplementaires : dict[str, Any] = field(default_factory=dict)

def quitte_ou_double_aplliquer(attaque : Attaque, attributs : dict[str, Any]) -> None:
    if random.randint(0, 1) <= 0.5:
        attaque.cible.recoit_degats(40, attaque)
    else:
        attaque.lanceur.recoit_degats(40, attaque)

callbacks : dict[str, CarteInterfaceMethodes]  = {
    "quitte ou double" : CarteInterfaceMethodes(quitte_ou_double_aplliquer)
}