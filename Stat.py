from enum import Enum, auto

class Stat:
    """
    Représente les stats de quelque chose.

    Attributs:
    - vie
    - vie_max
    - force
    - defense
    - magie
    - defense_magique
    - vitesse
    - est_initialise: Si l'objet est initialisé.
    
    Si l'objet n'est pas initialisé aucun de ces attributs autre que `est_initialise` est fiable à lire.
    """
    # Cette classe n'en n'est pas une à proprement parler
    # C'est un aggrégat de données (un dictionnaire à entrées limitées quoi)
    # L'encapsulation ne s'applique donc pas ici
    
    def __init__(
            self,
            vie_max     : int,
            force   : int,
            defense : int,
            magie   : int,
            defense_m : int,
            vitesse : int,
            unset   : bool = False,
            vie_initiale : int = -1
        ) -> None:
        if unset:
            self.est_initialise = False
            return
        
        
        if vie_initiale >= 0:
            self.vie : int = vie_initiale
        else:
            self.vie : int = vie_max
        
        self.vie_max    : int = vie_max
        self.force      : int = force
        self.defense    : int = defense
        self.magie      : int = magie
        self.defense_magique : int = defense_m
        self.vitesse    : int = vitesse
        self.est_initialise = True

    def __eq__(self, stats: 'Stat') -> bool:
        # Défini le comportement de l'opérateur `==` si comparé à un autre objet
        return (
            (not self.est_initialise and not stats.est_initialise)
            or (
                self.vie            == stats.vie
                and self.force      == stats.force
                and self.defense    == stats.defense
                and self.magie      == stats.magie
                and self.defense_magique == stats.defense_magique
                and self.vitesse    == stats.vitesse
            )
        )
    
    def __ne__(self, stats: 'Stat') -> bool:
        # Défini le comportement de l'opérateur `!=` si comparé à un autre objet
        return not self == stats
    
    def __str__(self) -> str:
        # Défini ce que l'objet doit retourner pour une string "jolie"
        return (
            "Stat{"
            + f"vie: {self.vie}; "
            + f"force: {self.force}; "
            + f"defense: {self.defense}; "
            + f"magie: {self.magie}; "
            + f"defense_magique: {self.defense_magique}; "
            + f"vie: {self.vie}; "
            + f"vitesse: {self.vitesse}; "
            + f"est_initialise: {self.est_initialise}"
            +"}"
        )
    
    def __copy__(self):
        # définir __deepcopy__() est futile vu qu'aucun attribut n'est passé par référence
        return Stat(
            self.vie,
            self.force,
            self.defense,
            self.magie,
            self.defense_magique,
            self.vitesse,
            not self.est_initialise,
        )
    
    def set(
        self,
        vie     : int,
        force   : int,
        defense : int,
        magie   : int,
        defense_m : int,
        vitesse : int,
    ) -> None:
        self.vie        = vie
        self.force      = force
        self.defense    = defense
        self.magie      = magie
        self.defense_magique = defense_m
        self.vitesse    = vitesse
        self.est_initialise  = True
    
    def baisser_vie(self, combien : int) -> None:
        assert(self.est_initialise), "Objet Stat non initatialisé éssaye de baisser sa vie."
        self.vie -= combien
        self.vie = min(self.vie_max, max(0, self.vie))  # 0 <= vie <= vie_max
    
    def est_mort(self) -> bool:
        return self.vie <= 0