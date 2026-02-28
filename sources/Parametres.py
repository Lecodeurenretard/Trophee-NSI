from import_var import *
from dessin import dessiner_rect
from fonctions_vrac import blit_centre

# les catégories que peut prendre Parametre.valeur
categorie_valeur_parametre : TypeAlias = None|bool#|int|float|str|list[str]

# Ces catégories pourrons potentiellements être ajoutés plus tard
# en fonction des paramètres qui serons implémentés plus tard
class TypeParametre(Enum):
    CASE_A_COCHER    = auto()
    RADIO            = auto()
    CHECKBOXES       = auto()
    SLIDERF          = auto()
    SLIDERI          = auto()
    TEXTE            = auto()
    INT              = auto()
    FLOAT            = auto()
    
    @staticmethod
    def dessiner(num_couche : int, categ : 'TypeParametre', position : Pos, dimensions : tuple[int, int]|list[int], valeur : categorie_valeur_parametre) -> None:
        match(categ):
            case TypeParametre.CASE_A_COCHER:
                dessiner_rect(
                    num_couche,
                    position, dimensions,
                    BLEU if valeur else BLANC,
                    epaisseur_trait=2, couleur_bords=GRIS
                )
            case TypeParametre.RADIO:
                pass
            case TypeParametre.CHECKBOXES:
                pass
            case TypeParametre.SLIDERF:
                pass
            case TypeParametre.SLIDERI:
                pass
            case TypeParametre.TEXTE:
                pass
            case TypeParametre.INT:
                pass
            case TypeParametre.FLOAT:
                pass
            
            case _:
                raise NotImplementedError(f"Catégorie '{categ.name}' non implémenté dans `ParametreCategorie.dessiner()`.")
    
    @property
    def hauteur(self) -> int:
        return Jeu.pourcentage_hauteur(2.5)
    
    @property
    def largeur(self) -> int:
        match(self):
            case TypeParametre.CASE_A_COCHER:
                return self.hauteur # carré
            
            case TypeParametre.RADIO:
                return self.hauteur
            
            case TypeParametre.CHECKBOXES:
                return self.hauteur
            
            case TypeParametre.SLIDERF:
                return self.hauteur * 10
            
            case TypeParametre.SLIDERI:
                return self.hauteur * 10
            
            case TypeParametre.TEXTE:
                return self.hauteur * 10
            
            case TypeParametre.INT:
                return self.hauteur * 10
            
            case TypeParametre.FLOAT:
                return self.hauteur * 10
            
            case _:
                raise NotImplementedError(f"Catégorie '{self.name}' non implémenté dans `ParaetreCategorie.largeur`.")
    
    @property
    def dimensions(self) -> tuple[int, int]:
        return (self.largeur, self.hauteur)
    
    @property
    def type_correspondant(self) -> type:
        match(self):
            case TypeParametre.CASE_A_COCHER:
                return bool
            case TypeParametre.RADIO:
                return str
            case TypeParametre.CHECKBOXES:
                return list[str]
            case TypeParametre.SLIDERF:
                return float
            case TypeParametre.SLIDERI:
                return int
            case TypeParametre.TEXTE:
                return str
            case TypeParametre.INT:
                return int
            case TypeParametre.FLOAT:
                return float
            
            case _:
                raise NotImplementedError(f"Catégorie '{self.name}' non implémenté dans `ParametreCategorie.categorie_correspondante`.")



class Parametre:
    _ECART_NOM_VALEUR : int = 50
    _POLICE : pygame.font.Font = pygame.font.SysFont(None, 40)
    
    def __init__(
            self,
            nom_affichage : str,
            hauteur : int,
            categ : TypeParametre, valeur_par_defaut : categorie_valeur_parametre,
            on_change : Callable[[categorie_valeur_parametre], None]|None = None,
        ):
        self._nom_affichage = nom_affichage
        self._position : Pos = Pos(Jeu.pourcentage_largeur(50) + Parametre._ECART_NOM_VALEUR // 2, hauteur)
        
        self._categorie = categ
        self._valeur_par_defaut = valeur_par_defaut
        self._valeur            = self._valeur_par_defaut
        
        self._changement_utilisateur = on_change
        
        self._valeurs_autorisees : Optional[list[str]] = None
        if self._possibilites_finies:
            self._valeurs_autorisees = []
    
    def __bool__(self):
        return self._convertion_vers_type(bool)
    def __int__(self):
        return self._convertion_vers_type(int)
    def __float__(self):
        return self._convertion_vers_type(float)
    def __str__(self) -> str:   # annotation sinon le type chcker se plaint
        return self._convertion_vers_type(str)  # type: ignore
    #def __iter__(self):
    #    if self._categorie == ParametreCategorie.CHECKBOXES:
    #        return (val for val in self._valeur)
    #    
    #    raise TypeError(f"On ne peut itérer à travers un paramètre de catégorie {self._categorie}.")
    
    @staticmethod
    def dessiner_groupe(num_couche : int, groupe_a_dessiner : 'list[Parametre]|tuple[Parametre]') -> int:
        y_maximum : int = -1
        
        for param in groupe_a_dessiner:
            param.dessiner(num_couche)
            
            if param._hitbox_globale.bottom > y_maximum:
                y_maximum = param._hitbox_globale.bottom
        
        return y_maximum
    
    @property
    def _possibilites_finies(self) -> bool:
        return self._categorie in (TypeParametre.RADIO, TypeParametre.CHECKBOXES)
    
    @property
    def _hitbox(self) -> Rect:
        """La hitbox d'un seul élément du paramètre, s'il ne contient qu'un seul paramètre, est équivalent à `._hitbox_globale`."""
        match(self._categorie):
            case TypeParametre.CASE_A_COCHER:
                ...
            case TypeParametre.RADIO:
                pass
            case TypeParametre.CHECKBOXES:
                pass
            case TypeParametre.SLIDERF:
                pass
            case TypeParametre.SLIDERI:
                pass
            case TypeParametre.TEXTE:
                pass
            case TypeParametre.INT:
                pass
            case TypeParametre.FLOAT:
                pass
            case _:
                raise NotImplementedError(f"Catégorie '{self._type.name}' non implémenté dans `Setting._hitbox`.")
        
        # implémentation pour les paramètres avec une seule hitbox, les cas avec des points de suspensions l'implémentent
        # (pour rappel, pass indique que le cas n'est pas implémenté)
        return self._hitbox_globale
    
    @property
    def _hitbox_globale(self) -> Rect:
        """La hitbox de tous les éléments du paramètres."""
        match(self._categorie):
            case TypeParametre.CASE_A_COCHER:
                ...
            case TypeParametre.RADIO:
                pass
            case TypeParametre.CHECKBOXES:
                pass
            case TypeParametre.SLIDERF:
                pass
            case TypeParametre.SLIDERI:
                pass
            case TypeParametre.TEXTE:
                pass
            case TypeParametre.INT:
                pass
            case TypeParametre.FLOAT:
                pass
            case _:
                raise NotImplementedError(f"Catégorie '{self._type.name}' non implémenté dans `Setting._hitbox_globale`.")
        
        # implémentation par défaut, les cas avec des points de suspensions l'implémentent
        position : Pos = self._position - Vecteur(*self._categorie.dimensions) // 2
        position.x += Parametre._ECART_NOM_VALEUR // 2
        
        return Rect(position.tuple, self._categorie.dimensions)
    
    @property
    def valeurs_autorisees(self) -> list[str]:
        assert(self._possibilites_finies), f"Le paramètre de catégorie {self._categorie} ne peut pas contenir plusieurs valeurs."
        assert(self._valeurs_autorisees is not None), "._valeurs_autorisees est None alors que ._peut_contenir_plusieurs_valeurs est True."
        
        return self._valeurs_autorisees
    
    # _valeur à plusieurs getters pour être sûr de ce qui est renvoyé
    @property
    def case_cochee(self) -> bool:
        if self._categorie != TypeParametre.CASE_A_COCHER:
            raise TypeError(f"Une case ne peut être cochée que si c'est une CASE_A_COCHER, au lieu de cela c'est un.e {self._categorie}.")
        
        return self._valeur # type: ignore
    
    @valeurs_autorisees.setter
    def valeurs_autorisees(self, val : list[str]) -> None:
        assert(self._possibilites_finies), f"Le paramètre de catégorie {self._categorie} peut prendre un nombre trop grand de valeurs pour les avoir stockées dans une liste."
        
        self._valeurs_autorisees = val
    
    # Les types génériques n'ont pas l'air de trop marcher avec cette fonction
    def _convertion_vers_type(self, type_cible : type): # -> type_cible
        if self._categorie.type_correspondant is type_cible:
            return self._valeur
        
        raise TypeError(f"Convertion illégale d'un objet Paramètre de catégorie {self._categorie.name} en {type_cible.__name__}.")
    
    def reset_val(self) -> None:
        self._valeur = self._valeur_par_defaut
    
    def dessiner(self, num_couche : int) -> None:
        DECALAGE : Vecteur = Vecteur(Parametre._ECART_NOM_VALEUR // 2, 0)
        nom_rendered : Surface = Parametre._POLICE.render(self._nom_affichage, True, NOIR)
        
        blit_centre(
            num_couche,
            nom_rendered,
            (self._position - Vecteur(nom_rendered.get_width(), 0) - DECALAGE).tuple,
            centre_en_x=False
        )
        
        self._categorie.dessiner(
            num_couche,
            self._categorie,
            Pos(self._hitbox_globale.topleft),
            self._categorie.dimensions,
            self._valeur,
        )
    
    def prendre_input(self, ev : pygame.event.Event) -> None:
        match(self._categorie):
            case TypeParametre.CASE_A_COCHER:
                if ev.type == pygame.MOUSEBUTTONDOWN and self._hitbox_globale.collidepoint(ev.pos):
                    if ev.button in (4, 5): # empèche le scroll de compter pour un click
                        return
                    self._valeur = not self._valeur
                    
                    if self._changement_utilisateur is not None:
                        self._changement_utilisateur(self._valeur)
            
            case TypeParametre.RADIO:
                pass
            case TypeParametre.CHECKBOXES:
                pass
            case TypeParametre.SLIDERF:
                pass
            case TypeParametre.SLIDERI:
                pass
            case TypeParametre.TEXTE:
                pass
            case TypeParametre.INT:
                pass
            case TypeParametre.FLOAT:
                pass
            
            case _:
                raise NotImplementedError(f"catégorie '{self._categorie.name}' non implémenté dans `Setting.prendre_input()`.")
        self._categorie