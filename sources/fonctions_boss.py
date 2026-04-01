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

def _charger_sprite(nom_fichier : str) -> Surface:
    return pygame.image.load(f"{Chemins.IMG}boss/{nom_fichier}").convert_alpha()

def roi_blob_nouveau_tour(self : Monstre, attributs : dict[str, Any]) -> None:
    DUREE_TYPE : int = 2        # la durée du type (att ou magie)  en nombre de tours
    if Jeu.nb_tours_combat % DUREE_TYPE != 0:
        return
    
    if "sprite physique" not in attributs.keys():
        sprite_physique = _charger_sprite("Roi blob ph.png")
        sprite_magie    = _charger_sprite("Roi blob mg.png")
        
        facteur = 6
        w, h = sprite_physique.get_size()
        attributs["sprite physique"] = pygame.transform.scale(sprite_physique, (int(w * facteur), int(h * facteur)))
        
        w, h = sprite_magie.get_size()
        attributs["sprite magie"] = pygame.transform.scale(sprite_magie, (int(w * facteur), int(h * facteur)))
    
    # intervertit les stats du boss de sorte à ce que
    # ses stats les plus fortes soient du bon type
    min_att, max_att = sorted((self._stats.magie, self._stats.force))
    min_def, max_def = sorted((self._stats.defense_magique, self._stats.defense))
    if Jeu.nb_tours_combat % (DUREE_TYPE * 2) == 0:
        # Si DUREE_TYPE == 1, s'active pour les tours 0, 2, 4, ...
        self._stats.magie           = min_att
        self._stats.defense_magique = min_def
        self._stats.force   = max_att
        self._stats.defense = max_def
        self._sprite = attributs["sprite physique"]
    else:
        # Si DUREE_TYPE == 1, s'active pour les tours 1, 3, 5, ...
        self._stats.magie           = max_att
        self._stats.defense_magique = max_def
        self._stats.force   = min_att
        self._stats.defense = min_def
        self._sprite = attributs["sprite magie"]


def demon_nouveau_tour(self : Monstre, attributs : dict[str, Any]) -> None:
    if "sprite physique" not in attributs.keys():
        sprite_demon = pygame.image.load(f"{Chemins.IMG}boss/demon.png").convert_alpha()
        sprite_pretre = pygame.image.load(f"{Chemins.IMG}boss/pretre.png").convert_alpha()
        
        w, h = sprite_demon.get_size()
        facteur = 6
        attributs["sprite physique"] = pygame.transform.scale(sprite_demon, (int(w * facteur), int(h * facteur)))
        
        w, h = sprite_pretre.get_size()
        attributs["sprite magie"] = pygame.transform.scale(sprite_pretre, (int(w * facteur), int(h * facteur)))
    
    if Jeu.nb_tours_combat % 3 == 0:
        self._stats.defense_magique = 40
        self._stats.defense = 70
        self._stats.magie = 25
        self._stats.force = 90
        self._sprite = attributs["sprite physique"]
    else :
        self._stats.defense_magique = 80
        self._stats.defense = 70
        self._stats.magie = 50
        self._stats.force = 15
        self._sprite = attributs["sprite magie"]

def monstre_statique_thermofluide_nouveau_tour(self : Monstre, attributs : dict[str, Any]) -> None:
    ...


callbacks : dict[str, BossInterfaceMethodes] = {
    "Roi Blob": BossInterfaceMethodes(
        nouveau_tour=roi_blob_nouveau_tour,
    ),
    "Démon": BossInterfaceMethodes(
        nouveau_tour=demon_nouveau_tour,
    ),
    "Monstre statique thermofluide": BossInterfaceMethodes(
        nouveau_tour=monstre_statique_thermofluide_nouveau_tour,
    ),
}