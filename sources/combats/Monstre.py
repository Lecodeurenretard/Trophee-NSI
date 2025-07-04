from dessin import *
from fonctions_vrac import *
from Attaque import *
from Joueur import joueur

class TypeMonstre(Enum):
    Blob    = auto()
    Sorcier = auto()
    
    def couleur(self) -> color:
        """Renvoie la couleur du type de monstre correspondant."""
        match self:
            case TypeMonstre.Blob:
                return ROUGE
            case TypeMonstre.Sorcier:
                return BLEU
            
            case _:
                raise NotImplementedError("Type de monstre non implémenté dans Monstre.Type.couleur().")
    
    def sprite(self) -> str:
        """Renvoie le chemin vers le sprite du type de monstre correspondant."""
        match self:
            case TypeMonstre.Blob:
                return f"{CHEMIN_DOSSIER_IMG}/blob_placeholder.webp"
            case TypeMonstre.Sorcier:
                return f"{CHEMIN_DOSSIER_IMG}/sorcier_placeholder.png"
            
            case _:
                raise NotImplementedError("Type de monstre non implémenté dans Monstre.Type.sprite().")
    
    def attaques_du_type(self) -> tuple[Attaque]:
        match self:
            case TypeMonstre.Blob:
                return (
                    ATTAQUES_DISPONIBLES["physique"],
                    # d'autres attaques?
                )
            
            case TypeMonstre.Sorcier:
                return (
                    ATTAQUES_DISPONIBLES["magie"],
                    # d'autres attaques?
                )
            
            case _:
                raise NotImplementedError("Type de monstre non implémenté dans Monstre.Type.attaques_du_type().")

class Monstre:
    sont_invincibles : bool = False
    
    _STATS_DE_BASE : dict[TypeMonstre, Stat] = {
        TypeMonstre.Blob	: Stat(40+5, 30-7, 45, 0 , 25+5, 30, 2.0, 1.3),
        TypeMonstre.Sorcier	: Stat(30+5, 10  , 30, 15, 80+5, 60, 1.3, 1.8),
    }

    dimensions_sprites : tuple[int, int] = (150, 150)
    
    # La liste de tous les monstres en vie
    # Peut-être des combats vs plusieurs monstres?
    monstres_en_vie : list['Monstre'] = []
    
    # devrait être utilisé le moins possible, préférer nouveau_monstre()
    def __init__(self, nom : str, stats : Stat, attaques : tuple[Attaque], couleur : color|None = None, chemin_sprite : str|None = None):
        assert(stats.est_initialise), "stats n'est pas initialisé dans le constructeur de Monstre."

        self._nom = nom
        self._stats = stats
        self._attaques_disponibles = attaques
        
        assert(couleur is not None or chemin_sprite is not None), "A la fois couleur et chemin_sprite sont None"
        self._couleur : color|None = couleur
        
        if chemin_sprite is not None:
            self._sprite  : Surface|None = pygame.transform.scale(pygame.image.load(chemin_sprite), Monstre.dimensions_sprites)
        else:
            self._sprite : Surface|None = None
        
        Monstre._ajouter_monstre_a_liste(self)
        
        self._id = premier_indice_libre_de_entitees_vivantes()
        if self._id >= 0:
            entitees_vivantes[self._id] = self
            return
        
        self._id = len(entitees_vivantes)
        entitees_vivantes.append(self)
    
    def __del__(self):
        # Appelé quand l'objet est détruit (plus utilisé ou détruit avec del())
        if (
            self._id > 0
            and entitees_vivantes is not None
            and Monstre.monstres_en_vie is not None
        ):
            self.meurt()
    
    @staticmethod
    def nouveau_monstre(type : TypeMonstre) -> 'Monstre':
        """Crée un nouveau monstre suivant son type"""
        return Monstre(
            type.name,
            copy(Monstre._STATS_DE_BASE[type]),    # Si pas de copie, tous les monstres suivants auront leurs vie à 0
            type.attaques_du_type(),
            couleur=type.couleur(),
            chemin_sprite=type.sprite()
        )
    
    @staticmethod
    def _ajouter_monstre_a_liste(monstre : 'Monstre') -> None:
        Monstre.monstres_en_vie.append(monstre)
    
    @staticmethod
    def _enlever_monstre_a_liste(monstre : 'Monstre') -> None:
        for i in range(len(Monstre.monstres_en_vie)):
            m = Monstre.monstres_en_vie[i]
            if monstre._id == m._id:
                Monstre.monstres_en_vie.pop(i)
                return
        print("Warning: La fonction Monstre._enlever_monstre_a_liste() à été appellée sur un monstre pas dans la liste dans Monstre.monstres_en_vie[].")
    
    @staticmethod
    def tuer_les_monstres_morts() -> None:
        for monstre in Monstre.monstres_en_vie:
            if monstre.est_mort():
                monstre.meurt()
    
    def get_id(self) -> int:
        return self._id
    def get_nom(self) -> str:
        return self._nom
    
    def meurt(self) -> None:
        entitees_vivantes[self._id] = None
        Monstre._enlever_monstre_a_liste(self)
        self._id = -1
    
    def choisir_attaque(self) -> Attaque:
        return random.choice(self._attaques_disponibles)
    
    def attaquer(self, id_cible : int, attaque : Attaque) -> bool:
        """Attaque la cible et retourne si elle a été tuée."""
        assert(entitees_vivantes[id_cible] is not None), "La cible est une case vide de entitees_vivantes[] dans Monstre.attaquer()."
        assert(attaque in self._attaques_disponibles), "L'attaque demandée dans Monstre.attaquer() n'est pas dans le moveset du monstre."
        
        if attaque.get_friendly_fire():
            return self.subir_attaque(attaque, self._stats)
        if attaque.get_ennemy_fire():
            return entitees_vivantes[id_cible].subir_attaque(attaque, self._stats)
        return False
    
    def subir_attaque(self, attaque : Attaque, stats_attaquant : Stat) -> bool:
        degats, crit = attaque.calculer_degats(stats_attaquant, self._stats)
        
        self.recoit_dommages(degats)
        return crit
    
    def recoit_dommages(self, dommages : int) -> bool:
        if Monstre.sont_invincibles and dommages >= 0:
            return False
        
        self._stats.baisser_vie(dommages)
        return self.est_mort()
    
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
    
    def dessiner_attaque(self, surface : Surface, attaque : Attaque, crit : bool) -> None:
        attaque.dessiner(surface, 400, 300, crit)
        
        pygame.display.flip()
        attendre(1)
        
    def est_mort(self) -> bool:
        return self._stats.est_mort()