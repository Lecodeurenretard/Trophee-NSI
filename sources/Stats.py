from imports import *

@dataclass
class Stat:
    vie_max         : int
    force           : int
    defense         : int
    magie           : int
    defense_magique : int
    crit_puissance  : float
    crit_resitance  : float
    vie             : int = -0xFFFF

    @staticmethod
    def depuis_dictionnaire_json(json_dict : dict, valeur_par_defaut : int = -1000) -> 'Stat':
        """
        Après avoir décodé un fichier JSON, passez le dictionnaire correspondant à l'objet pour initialiser un objet Stat.
        Si une valeur n'est pas présente, `valeur_par_defaut` est utilisé.
        """
        resultat : Stat = Stat(*([valeur_par_defaut] * 7))   # Initialise l'objet Stat avec tous les attributs à -100 sauf .VITESSE_MAX
        for clef, valeur in json_dict.items():
            match clef:
                case "vie_max"        : resultat.vie_max         = valeur
                case "force"          : resultat.force           = valeur
                case "defense"        : resultat.defense         = valeur
                case "magie"          : resultat.magie           = valeur
                case "defense_magique": resultat.defense_magique = valeur
                case "crit_puissance" : resultat.crit_puissance  = valeur
                case "crit_resitance" : resultat.crit_resitance  = valeur
                case "vie"            : resultat.vie             = valeur
                case _                : raise RuntimeError(f"Mauvaise clef \"{clef}\" dans le JSON d'un objet Stat.")
        return resultat
    
    def additionner(self, delta : 'Stat', ajouter_vie : bool = False) -> None:
        """Ajoute les attributs deux à deux. Si `ajouter_vie` est active, ajoute aussi les vies."""
        self.vie_max         += delta.vie_max
        self.force           += delta.force
        self.defense         += delta.defense
        self.magie           += delta.magie
        self.defense_magique += delta.defense_magique
        self.crit_puissance  += delta.crit_puissance
        self.crit_resitance  += delta.crit_resitance
        if ajouter_vie:
            self.vie += delta.vie
    def soustraire(self, delta : 'Stat', ajouter_vie : bool = False) -> None:
        """Soustraire les attributs deux à deux. Si `ajouter_vie` est active, ajoute aussi les vies."""
        self.vie_max         -= delta.vie_max
        self.force           -= delta.force
        self.defense         -= delta.defense
        self.magie           -= delta.magie
        self.defense_magique -= delta.defense_magique
        self.crit_puissance  -= delta.crit_puissance
        self.crit_resitance  -= delta.crit_resitance
        if ajouter_vie:
            self.vie -= delta.vie
    
    @property
    def est_mort(self) -> bool:
        return self.vie <= 0
    
    def reset_vie(self) -> 'Stat':
        self.vie = self.vie_max
        return self
    
    def baisser_vie(self, combien : int) -> None:
        self.vie -= combien
        self.vie = min(self.vie_max, self.vie)  # vie <= vie_max