"""
Contient toutes les fonctions utilisées par les boss ainsi que callbacks[] qui contient cesdites fonctions bien emballées.
projet : L'ascension de Esquimot
auteur : Dooheli, Lecodeurenretard, hibou509
"""
from Monstre import *

# La documententation pour L'interface de Boss se trouve dans doc/boss.md
# ouvrez dans le navigateur:
# https://github.com/Lecodeurenretard/Trophee-NSI/blob/master/doc/boss.md#linterface
@dataclass
class BossInterfaceMethodes:
    nouveau_tour : None|Callable[[Monstre, dict[str, Any]]              , None] = None
    choisir_atk  : None|Callable[[Monstre, dict[str, Any]]              , int]  = None
    subir_dmg    : None|Callable[[Monstre, int, Attaque, dict[str, Any]], None] = None
    
    attributs_supplementaires : dict[str, Any] = field(default_factory=dict)


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

def demon_nouveau_tour(monstre: Monstre, attributs: dict[str, Any]) -> None:
    if "sprite physique" not in attributs.keys():
        sprite_demon = pygame.image.load("data/img/boss/demon.png").convert_alpha()
        sprite_pretre = pygame.image.load("data/img/boss/pretre.png").convert_alpha()

        w, h = sprite_demon.get_size()
        facteur = 6
        attributs["sprite physique"] = pygame.transform.scale(sprite_demon, (int(w * facteur), int(h * facteur)))

        w, h = sprite_pretre.get_size()
        attributs["sprite magie"] = pygame.transform.scale(sprite_pretre, (int(w * facteur), int(h * facteur)))
    
    if Jeu.nb_tours_combat % 3 == 0:
        monstre._stats.defense_magique = 40
        monstre._stats.defense = 70
        monstre._stats.magie = 25
        monstre._stats.force = 90
        monstre._sprite = attributs["sprite demon"]
    else :
        monstre._stats.defense_magique = 80
        monstre._stats.defense = 70
        monstre._stats.magie = 50
        monstre._stats.force = 15
        monstre._sprite = attributs["sprite pretre"]


callbacks : dict[str, BossInterfaceMethodes] = {
    "demon": BossInterfaceMethodes(roi_blob_nouveau_tour),
}