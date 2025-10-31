from imports import *

@dataclass
class Stat:
    vie_max         : int
    force           : int
    defense         : int
    magie           : int
    defense_magique : int
    vitesse         : int
    crit_puissance  : float
    crit_resitance  : float
    vie             : int = -0xFFFF
    VITESSE_MAX : int = 10**9
    
    @staticmethod
    def depuis_dictionnaire_json(json_dict : dict, valeur_par_defaut : int = -1000) -> 'Stat':
        """
        Après avoir décodé un fichier JSON, passez le dictionnaire correspondant à l'objet pour initialiser un objet Stat.
        Si une valeur n'est pas présente, `valeur_par_defaut` est utilisé.
        """
        attributs_decode : dict[str, bool] = {
            "vie_max"       : False,
            "force"         : False,
            "defense"       : False,
            "magie"         : False,
            "vitesse"       : False,
            "crit_puissance": False,
            "crit_resitance": False,
            "vie"           : False,
        }
        
        resultat : Stat = Stat(*([valeur_par_defaut] * 9))   # Initialise l'objet Stat avec tous les attributs à -100 sauf .VITESSE_MAX
        for clef, valeur in json_dict.items():
            if clef in attributs_decode.keys():
                attributs_decode[clef] = True
                match clef:
                    case "vie_max"        : resultat.vie_max         = valeur
                    case "force"          : resultat.force           = valeur
                    case "defense"        : resultat.defense         = valeur
                    case "magie"          : resultat.magie           = valeur
                    case "defense_magique": resultat.defense_magique = valeur
                    case "vitesse"        : resultat.vitesse         = valeur
                    case "crit_puissance" : resultat.crit_puissance  = valeur
                    case "crit_resitance" : resultat.crit_resitance  = valeur
                    case "vie"            : resultat.vie             = valeur
        return resultat
    
    
    @property
    def est_mort(self) -> bool:
        return self.vie <= 0
    
    def reset_vie(self) -> 'Stat':
        self.vie = self.vie_max
        return self
    
    def baisser_vie(self, combien : int) -> None:
        self.vie -= combien
        self.vie = min(self.vie_max, self.vie)  # vie <= vie_max
    
    def corriger_vitesse(self) -> None:
        self.vitesse = min(self.VITESSE_MAX, max(self.vitesse, -1))