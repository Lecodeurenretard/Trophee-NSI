from dessin import *
from fonctions_vrac import *

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
    
    _stats_base : dict[TypeMonstre, Stat] = {
        TypeMonstre.Blob	: Stat(40+5, 30, 45, 0 , 25+5, 30),
        TypeMonstre.Sorcier	: Stat(30+5, 10, 30, 15, 80+5, 60),
    }
    
    # La liste de tous les monstres en vie
    # Peut-être des combats vs plusieurs monstres?
    monstres_en_vie : list['Monstre'] = []
    
    # devrait être utilisé le moins possible, préférer nouveau_monstre()
    def __init__(self, nom : str, stats : Stat, couleur : color, attaques : tuple[Attaque]):
        assert(stats.est_initialise), "stats n'est pas initialisé dans le constructeur de Monstre."

        self._nom = nom
        self._stats = stats
        self._couleur = couleur
        self._attaques_disponibles = attaques
        
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
            copy(Monstre._stats_base[type]),
            type.couleur(),
            type.attaques_du_type()
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
        return self.recoit_dommages(
            attaque.calculer_degats(stats_attaquant, self._stats)
        )
    
    def recoit_dommages(self, dommages : int) -> bool:
        if Monstre.sont_invincibles and dommages >= 0:
            return False
        
        self._stats.baisser_vie(dommages)
        return self.est_mort()
    
    def longueur_barre_de_vie(self) -> int:
        ratio = max(0, self._stats.vie / self._stats.vie_max)
        return round(ratio * UI_LONGUEUR_BARRE_DE_VIE)
    
    def dessiner(self, surface : pygame.Surface, pos_x : int, pos_y : int) -> None:
        boite_de_contours = (pos_x, pos_y, 100, 100)
        pygame.draw.rect(surface, self._couleur, boite_de_contours, 0)
    
    def dessine_barre_de_vie(self, pos_x, pos_y):
        dessine_barre_de_vie(pos_x, pos_y, self._stats.vie / self._stats.vie_max, self.longueur_barre_de_vie())
    
    def dessine_attaque(self, surface : pygame.Surface, attaque : Attaque) -> None:
        attaque.dessiner(surface, 400, 300)
        
        pygame.display.flip()
        time.sleep(1)
        
    def est_mort(self) -> bool:
        return self._stats.est_mort()