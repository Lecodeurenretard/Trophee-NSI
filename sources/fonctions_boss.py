from Monstre import *

@dataclass
class BossInterfaceMethodes:
    nouveau_tour : None|Callable[[Monstre, dict[str, Any]]              , None] = None
    choisir_atk  : None|Callable[[Monstre, dict[str, Any]]              , int]  = None
    subir_dmg    : None|Callable[[Monstre, int, Attaque, dict[str, Any]], None] = None
    
    # default_factory est appelé et sa valeur de retour va initialiser l'attribut
    attributs_supplementaires : dict[str, Any] = field(default_factory=lambda: {})

callbacks : dict[str, BossInterfaceMethodes] = {
    "Roi Blob": BossInterfaceMethodes(),
}