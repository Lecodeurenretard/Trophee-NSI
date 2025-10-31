from Attaque import *

class TypeMonstre(Enum):
    Blob    = auto()
    Sorcier = auto()
    
    @property
    def couleur(self) -> rgb:
        """Renvoie la couleur du type de monstre correspondant."""
        match self:
            case TypeMonstre.Blob:
                return ROUGE
            case TypeMonstre.Sorcier:
                return BLEU
            
            case _:
                raise NotImplementedError("Type de monstre non implémenté.")
    
    @property
    def chemin_sprite(self) -> str:
        """Renvoie le chemin vers le sprite du type de monstre correspondant."""
        match self:
            case TypeMonstre.Blob:
                return f"{Constantes.Chemins.IMG}/blob.png"
            case TypeMonstre.Sorcier:
                return f"{Constantes.Chemins.IMG}/sorcier.png"
            
            case _:
                raise NotImplementedError("Type de monstre non implémenté.")
    
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
                raise NotImplementedError("Type de monstre non implémenté.")
    
    def type_precedent(self) -> 'TypeMonstre':
        if self.value == 1:     # minimum value
            return TypeMonstre(len(TypeMonstre))
        return TypeMonstre(self.value - 1)
    
    def type_suivant(self) -> 'TypeMonstre':
        if self.value == len(TypeMonstre):
            return TypeMonstre(1)
        return TypeMonstre(self.value + 1)


INVICIBLE_ENNEMI : bool = False

class Monstre:
    _STATS_DE_BASE : dict[TypeMonstre, Stat] = {
        TypeMonstre.Blob    : Stat(35, 23, 50, 0 , 17, 30, 2.0, 1.3).reset_vie(),
        TypeMonstre.Sorcier : Stat(40, 10, 30, 15, 40, 60, 1.3, 1.8).reset_vie(),
    }
    POSITION : Pos = Pos(Jeu.pourcentage_largeur(70), Jeu.pourcentage_hauteur(15))
    
    dimensions_sprites : tuple[int, int] = (150, 150)
    
    # La liste de tous les monstres en vie
    # Peut-être des combats vs plusieurs monstres?
    monstres_en_vie : list['Monstre'] = []
    
    # devrait être utilisé le moins possible, préférer nouveau_monstre()
    def __init__(
            self,
            nom           : str,
            stats         : Stat,
            attaques      : tuple[Attaque, ...],
            couleur       : Optional[rgb]         = None,
            chemin_sprite : Optional[str]         = None,
            type_calque   : Optional[TypeMonstre] = None,
        ):
        
        self._nom = nom
        self._stats = stats
        self._moveset = attaques
        self._type = type_calque
        
        assert(couleur is not None or chemin_sprite is not None), "A la fois couleur et chemin_sprite sont None"
        self._couleur : Optional[rgb] = couleur
        
        if chemin_sprite is not None:
            self._sprite  : Optional[Surface] = pygame.transform.scale(pygame.image.load(chemin_sprite), Monstre.dimensions_sprites)
        else:
            self._sprite  : Optional[Surface] = None
        
        Monstre._ajouter_monstre_a_liste(self)
        self.afficher : bool= True
        
        self._id = premier_indice_libre_de_entites_vivantes()
        if self._id >= 0:
            globales.entites_vivantes[self._id] = self
            return
        
        self._id = len(globales.entites_vivantes)
        globales.entites_vivantes.append(self)
    
    def __del__(self):
        # Appelé quand l'objet est détruit (quand nous ne pouvons plus accéder à l'objet)
        if (
            self._id > 0
            and globales.entites_vivantes is not None
            and Monstre.monstres_en_vie is not None
        ):
            self.meurt()
    
    @staticmethod
    def nouveau_monstre(type : TypeMonstre) -> 'Monstre':
        """Crée un nouveau monstre suivant son type"""
        return Monstre(
            type.name,
            copy(Monstre._STATS_DE_BASE[type]),    # Si pas de copie, tous les monstres suivants auront leurs vie à 0
            tuple(type.moveset.values()),
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
            if monstre.est_mort:
                monstre.meurt()
    
    @staticmethod
    def spawn(proba : Optional[dict[TypeMonstre, float]] = None) -> 'Monstre':
        poids : Optional[list[float]] = None
        liste_de_types : list[TypeMonstre] = list(TypeMonstre)
        if proba is not None:
            poids = [-1.0] * len(liste_de_types)    # garantit de trouver une clef
            
            for i, type in enumerate(liste_de_types):
                poids[i] = proba[type]
        
        return Monstre.nouveau_monstre(
            random.choices(liste_de_types, weights=poids)[0]
        )
    
    
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def est_mort(self) -> bool:
        return self._stats.est_mort
    
    @property
    def nom(self) -> str:
        return self._nom
    @property
    def dbg_nom(self) -> str:
        return self.nom
    
    @property
    def stats(self) -> Stat:
        return copy(self._stats)
    
    @property
    def pos_attaque(self) -> Pos:
        return Monstre.POSITION
    
    @property
    def pos_curseur(self) -> Pos:
        return Pos(0, 0)
    
    # même raisonnement que dans Joueur
    def meurt(self) -> None:
        globales.entites_vivantes[self._id] = None
        Monstre._enlever_monstre_a_liste(self)
        self._id = -1
    
    def _vers_type(self, nouveau_type : TypeMonstre) -> None:
        self._nom = nouveau_type.name
        
        ratio_vie = self._stats.vie / self._stats.vie_max
       
        self._stats = copy(Monstre._STATS_DE_BASE[nouveau_type])
        self._stats.vie = round(self._stats.vie_max * ratio_vie)    # Conserve les proportions
        
        self._moveset = tuple(nouveau_type.moveset.values())
        self._couleur = nouveau_type.couleur
        
        self._sprite = pygame.transform.scale(pygame.image.load(nouveau_type.chemin_sprite), Monstre.dimensions_sprites)
        self._type = nouveau_type
    
    def choisir_attaque(self) -> Attaque:
        return random.choice(self._moveset)
    
    def attaquer(self, id_cible : int, attaque : Attaque) -> None:
        """Attaque la cible et retourne si elle a été tuée."""
        assert(globales.entites_vivantes[id_cible] is not None), "La cible est une case vide de globales.entites_vivantes[] dans Monstre.attaquer()."
        assert(attaque in self._moveset), "L'attaque demandée dans Monstre.attaquer() n'est pas dans le moveset du monstre."
        
        attaque.enregister_lancement(self._id, id_cible)
    
    def recoit_degats(self, dommages : int) -> None:
        if bool(params.monstre_invincible) and dommages >= 0:
            return
        
        self._stats.baisser_vie(dommages)
    
    def longueur_barre_de_vie(self) -> int:
        ratio = max(0, self._stats.vie / self._stats.vie_max)
        return round(ratio * Constantes.UI_LONGUEUR_BARRE_DE_VIE)
    
    def dessiner(self, surface : Surface, pos_x : int, pos_y : int) -> None:
        if params.mode_debug.case_cochee and self._couleur is not None:
            boite_de_contours = (pos_x, pos_y, 100, 100)
            pygame.draw.rect(surface, self._couleur, boite_de_contours, 0)
            return
        
        if not params.mode_debug.case_cochee and self._sprite is not None:
            blit_centre(surface, self._sprite, (pos_x, pos_y))
    
    def dessiner_barre_de_vie(self, surface : Surface, pos_x : int, pos_y : int):
        dessiner_barre_de_vie(surface, pos_x, pos_y, self._stats.vie / self._stats.vie_max, self.longueur_barre_de_vie())
       
    def dessine_prochaine_frame(self, surface : Surface) -> None:
        if not self.afficher:
            return
        self.dessiner(surface, Monstre.POSITION.x, Monstre.POSITION.y)
    
    def dessine_prochaine_frame_UI(self, surface : Surface) -> None:
        pass
    
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