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
    
    @property
    def est_mort(self) -> bool:
        return self.vie <= 0
    
    def reset_vie(self) -> 'Stat':
        self.vie = self.vie_max
        return self
    
    def baisser_vie(self, combien : int) -> None:
        self.vie -= combien
        self.vie = min(self.vie_max, self.vie)  # vie <= vie_max