# Ce fichier pré-importe les variables globales

import variables_globales
from variables_globales import (
    pygame,
    sys,
    time,
    random,
    clock,
    
    # fenetre est une variable "mutable" => peut être changée entre les fichiers
    # une variable immutable (ex: tuple ou int) ne peut pas être changée entre les fichiers
    # => on ne les importe pas directement, on les modifies avec le nom de modules
    fenetre,
    texte_gagner,
    texte_perdu,
    texte_magique,
    texte_soin,
    texte_torgnole,
    texte_input_ligne1,
    texte_input_ligne2,
    police,
    police_ecriture,
    police_ecriture2,
    
    # ces variables sont, certes, immutables mais elles ne doivent pas être changées
    # on peut donc les importer librement
    BLANC,
    NOIR,
    GRIS,
    BLEU,
    BLEU_CLAIR,
    ROUGE,
    VERT,
    LARGEUR,
    HAUTEUR,
	MAX_COMBAT,
	INVICIBLE_PLAYER,
	INVICIBLE_ENNEMI,
	UI_LONGUEUR_BARRE_DE_VIE,
)