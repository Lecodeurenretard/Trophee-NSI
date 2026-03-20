from Monstre import *

@dataclass
class BossInterfaceMethodes:
    nouveau_tour : None|Callable[[Monstre, dict[str, Any]]              , None] = None
    choisir_atk  : None|Callable[[Monstre, dict[str, Any]]              , int]  = None
    subir_dmg    : None|Callable[[Monstre, int, Attaque, dict[str, Any]], None] = None
    
    # default_factory est appelé et sa valeur de retour va initialiser l'attribut
    attributs_supplementaires : dict[str, Any] = field(default_factory=lambda: {})


def roi_blob_nouveau_tour(monstre: Monstre, attributs: dict[str, Any]) -> None:
    if "sprite physique" not in attributs.keys():
        sprite_physique = pygame.image.load("data/img/boss/Roi blob ph.png").convert_alpha()
        sprite_magie = pygame.image.load("data/img/boss/Roi blob mg.png").convert_alpha()

        w, h = sprite_physique.get_size()
        facteur = 6
        attributs["sprite physique"] = pygame.transform.scale(sprite_physique, (int(w * facteur), int(h * facteur)))

        w, h = sprite_magie.get_size()
        attributs["sprite magie"] = pygame.transform.scale(sprite_magie, (int(w * facteur), int(h * facteur)))
    
    if Jeu.nb_tours_combat % 3 == 0:
        monstre._stats.defense_magique = 50
        monstre._stats.defense = 25
        monstre._stats.magie = 30
        monstre._stats.force = 50
        monstre._sprite = attributs["sprite physique"]
    else :
        monstre._stats.defense_magique = 25
        monstre._stats.defense = 50
        monstre._stats.magie = 50
        monstre._stats.force = 30
        monstre._sprite = attributs["sprite magie"]


callbacks : dict[str, BossInterfaceMethodes] = {
    "Roi Blob": BossInterfaceMethodes(roi_blob_nouveau_tour),
}