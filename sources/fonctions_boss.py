from Monstre import *

@dataclass
class BossMethodeWrapper:
    nouveau_tour : None|Callable[[Monstre]              , None] = None
    choisir_atk  : None|Callable[[Monstre]              , int]  = None       # renvoie l'index de la carte dans la main
    subir_dmg    : None|Callable[[Monstre, int, Attaque], None] = None
    
    # default_factory est appelé et sa valeur de retour va initialiser l'attribut
    attributs_supplementaires : dict[str, Any] = field(default_factory=lambda: {})

callbacks : dict[str, BossMethodeWrapper] = {
    "Roi Blob": BossMethodeWrapper(),
}