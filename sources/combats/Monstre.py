from dessin import *
from fonctions_vrac import *
from Attaque import *
from Joueur import joueur

class TypeMonstre(IntEnum):
    Blob    = auto()
    Sorcier = auto()
    
    @property
    def couleur(self) -> color:
        """Renvoie la couleur du type de monstre correspondant."""
        match self:
            case TypeMonstre.Blob:
                return ROUGE
            case TypeMonstre.Sorcier:
                return BLEU
            
            case _:
                raise NotImplementedError("Type de monstre non implémenté dans Monstre.Type.couleur().")
    
    @property
    def chemin_sprite(self) -> str:
        """Renvoie le chemin vers le sprite du type de monstre correspondant."""
        match self:
            case TypeMonstre.Blob:
                return f"{CHEMIN_DOSSIER_IMG}/blob_placeholder.webp"
            case TypeMonstre.Sorcier:
                return f"{CHEMIN_DOSSIER_IMG}/sorcier_placeholder.png"
            
            case _:
                raise NotImplementedError("Type de monstre non implémenté dans Monstre.Type.sprite().")
    
    @property
    def moveset(self) -> dict[str, Attaque]:
        match self:
            case TypeMonstre.Blob:
                return {
                    "base": ATTAQUES_DISPONIBLES["physique"],
                    # d'autres attaques?
                }
            
            case TypeMonstre.Sorcier:
                return {
                    "base": ATTAQUES_DISPONIBLES["magie"],
                    # d'autres attaques?
                }
            
            case _:
                raise NotImplementedError("Type de monstre non implémenté dans Monstre.Type.attaques_du_type().")
    
    def type_precedent(self) -> 'TypeMonstre':
        if self.value == 1:     # minimum value
            return TypeMonstre(len(TypeMonstre))
        return TypeMonstre(self.value - 1)
    
    def type_suivant(self) -> 'TypeMonstre':
        if self.value == TypeMonstre(len(TypeMonstre)):
            return TypeMonstre(1)
        return TypeMonstre(self.value + 1)


class Monstre:
    sont_invincibles : bool = False
    
    _STATS_DE_BASE : dict[TypeMonstre, Stat] = {
        TypeMonstre.Blob : Stat(
            35,         # vie
            23, 50,     # att/def physique
            0, 17,      # att/def magique
            40,         # vitesse
            2.0, 1.3    # att/def crits
        ),
        TypeMonstre.Sorcier	: Stat(
            40,
            10, 30,
            15, 40,
            60,
            1.3, 1.8
        ),
    }

    dimensions_sprites : tuple[int, int] = (150, 150)
    
    # La liste de tous les monstres en vie
    # Peut-être des combats vs plusieurs monstres?
    monstres_en_vie : list['Monstre'] = []
    
    # devrait être utilisé le moins possible, préférer nouveau_monstre()
    def __init__(
            self,
            nom : str,
            stats : Stat,
            attaques : dict[str, Attaque],
            couleur       :       color|None = None,
            chemin_sprite :         str|None = None,
            type_calque   : TypeMonstre|None = None
        ):
        assert(stats.est_initialise), "stats n'est pas initialisé dans le constructeur de Monstre."
        
        self._nom = nom
        self._stats = stats
        self._attaques_disponibles = copy(attaques)
        self._type = type_calque
        
        assert(couleur is not None or chemin_sprite is not None), "A la fois couleur et chemin_sprite sont None"
        self._couleur : color|None = couleur
        
        if chemin_sprite is not None:
            self._sprite  : Surface|None = pygame.transform.scale(pygame.image.load(chemin_sprite), Monstre.dimensions_sprites)
        else:
            self._sprite : Surface|None = None
        
        Monstre._ajouter_monstre_a_liste(self)
        
        self._id = premier_indice_libre_de_entites_vivantes()
        if self._id >= 0:
            entites_vivantes[self._id] = self
            return
        
        self._id = len(entites_vivantes)
        entites_vivantes.append(self)
    
    def __del__(self):
        # Appelé quand l'objet est détruit (quand nous ne pouvons plus accéder à l'objet)
        if (
            self._id > 0
            and entites_vivantes is not None
            and Monstre.monstres_en_vie is not None
        ):
            self.meurt()
    
    # même raisonnement que dans Joueur
    def meurt(self) -> None:
        entites_vivantes[self._id] = None
        Monstre._enlever_monstre_a_liste(self)
        self._id = -1
    
    @staticmethod
    def nouveau_monstre(type : TypeMonstre) -> 'Monstre':
        """Crée un nouveau monstre suivant son type"""
        return Monstre(
            type.name,
            copy(Monstre._STATS_DE_BASE[type]),    # Si pas de copie, tous les monstres suivants auront leurs vie à 0
            type.moveset,
            couleur=type.couleur,
            chemin_sprite=type.chemin_sprite,
            type_calque=type
        )
    
    @staticmethod
    def _ajouter_monstre_a_liste(monstre : 'Monstre') -> None:
        Monstre.monstres_en_vie.append(monstre)
    
    @staticmethod
    def _enlever_monstre_a_liste(monstre : 'Monstre') -> None:
        for i, m in enumerate(Monstre.monstres_en_vie):
            if monstre._id == m._id:
                Monstre.monstres_en_vie.pop(i)
                return
        logging.warning("La fonction Monstre._enlever_monstre_a_liste() à été appellée sur un monstre pas dans la liste dans Monstre.monstres_en_vie[].")
    
    @staticmethod
    def tuer_les_monstres_morts() -> None:
        for monstre in Monstre.monstres_en_vie:
            if monstre.est_mort():
                monstre.meurt()
    
    @property
    def _moveset_clefs(self) -> tuple[str, ...]:
        return tuple(self._attaques_disponibles.keys())

    @property
    def id(self) -> int:
        return self._id
    
    @property
    def nom(self) -> str:
        return self._nom
    
    @property
    def stats(self) -> Stat:
        return self._stats
    
    def _recoit_dommages(self, dommages : int) -> bool:
        if Monstre.sont_invincibles and dommages >= 0:
            return False
        
        self._stats.baisser_vie(dommages)
        return self.est_mort()
    
    def choisir_attaque(self) -> Attaque:
        return random.choice(tuple(self._attaques_disponibles.values()))
    
    def attaquer(self, id_cible : int, attaque : Attaque) -> None:
        """Attaque la cible et retourne si elle a été tuée."""
        assert(entites_vivantes[id_cible] is not None), "La cible est une case vide de entites_vivantes[] dans Monstre.attaquer()."
        assert(attaque in self._attaques_disponibles.values()), "L'attaque demandée dans Monstre.attaquer() n'est pas dans le moveset du monstre."
        assert()

        if attaque.friendly_fire:
            attaque.inserer_dans_liste_attaque(self._id)
            return
        if attaque.enemy_fire:
            attaque.inserer_dans_liste_attaque(id_cible)
            return
    
    def subir_attaque(self, attaque : Attaque, stats_attaquant : Stat) -> None:
        assert(attaque.cible_id == -1 or attaque.cible_id == self._id), f"L'attaque n'est pas dirigée vers l'entité id {self.id} mais vers celle id {attaque.cible_id}."
        attaque.cible_id = self.id

        degats = attaque.calculer_degats(stats_attaquant)
        
        self._recoit_dommages(degats)
    
    def longueur_barre_de_vie(self) -> int:
        ratio = max(0, self._stats.vie / self._stats.vie_max)
        return round(ratio * UI_LONGUEUR_BARRE_DE_VIE)
    
    def dessiner(self, surface : Surface, pos_x : int, pos_y : int) -> None:
        if MODE_DEBUG and self._couleur is not None:
            boite_de_contours = (pos_x, pos_y, 100, 100)
            pygame.draw.rect(surface, self._couleur, boite_de_contours, 0)
            return
        
        if not MODE_DEBUG and self._sprite is not None:
            surface.blit(self._sprite, (pos_x, pos_y))
    
    def dessiner_barre_de_vie(self, surface : Surface, pos_x : int, pos_y : int):
        dessine_barre_de_vie(surface, pos_x, pos_y, self._stats.vie / self._stats.vie_max, self.longueur_barre_de_vie())
    
    def dessiner_attaque(self, surface : Surface, attaque : Attaque|str) -> None:
        if type(attaque) is str:
            assert(attaque in self._moveset_clefs), f"L'argument `attaque` de Monstre.dessiner_attaque() n'est pas une clef du moveset de l'entitée d'ID {self._id}."
            attaque = self._attaques_disponibles[attaque]
        elif type(attaque) is Attaque:
            assert(attaque in self._attaques_disponibles.values()), f"L'argument `attaque` de Monstre.dessiner_attaque() n'est pas dans le moveset de l'entitée d'ID {self._id}."
        else:
            raise TypeError(f"L'argument `attaque` de doit être de type str ou Attaque mais est de type {type(attaque)}.")
        
        attaque.dessiner(surface, 400, 300)
        pygame.display.flip()
        attendre(1)
        
    def est_mort(self) -> bool:
        return self._stats.est_mort()
    
    def _vers_type(self, nouveau_type : TypeMonstre) -> None:
        self._nom = nouveau_type.name
        
        ratio_vie = self._stats.vie / self._stats.vie_max
       
        self._stats = copy(Monstre._STATS_DE_BASE[nouveau_type])
        self._stats.vie = round(self._stats.vie_max * ratio_vie)    # Conserve les proportions
        
        self._attaques_disponibles = nouveau_type.moveset
        self._couleur = nouveau_type.couleur
        
        self._sprite = pygame.transform.scale(pygame.image.load(nouveau_type.chemin_sprite), Monstre.dimensions_sprites)
        self._type = nouveau_type
    
    def vers_type_precedent(self) -> bool:
        """Si le monstre à un type, change le type du monstre vers le précédent et renvoie True, sinon renvoie False et ne fait rien."""
        if self._type is None:
            return False
        
        self._vers_type(self._type.type_precedent())
        return True
    
    def vers_type_suivant(self) -> bool:
        """Si le monstre à un type, change le type du monstre vers le suivant et renvoie True, sinon renvoie False et ne fait rien."""
        if self._type is None:
            return False
        
        self._vers_type(self._type.type_suivant())
        return True