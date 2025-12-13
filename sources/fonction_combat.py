from Monstre import Monstre
from Joueur import joueur

def monstres_attaquent() -> None:
    for monstre in Monstre.monstres_en_vie:
        monstre.attaquer(joueur.id, monstre.choisir_carte().nom)