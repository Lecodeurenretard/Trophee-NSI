# Les variables globales
Une variable est globale si elle est déclarée dans [variables_globales](../variables_globales.py).

## Alias de types
> `color`

Une tuple contenant trois valeurs de couleurs RGB.


> `NaN`

Un alias à `float`, utilisé pour indiquer que le nombre est érroné. Sa seule valeure accéptée est `NAN`.


## Constantes
Les constantes sont importées directement dans [import_var](../import_var.py) ce qui permet de ne pas avoir à écrire `globales.` devant.
> `MODE_DEBUG : bool`

Si le mode débug est actif, pour la liste des fonctionnalités du mode allez voir le [README](../sources/README.md) du répertoire [sources](../sources/).  
Toutes les variables avec le préfixe `DBG_` ne doivent avoir aucun effet si le mode débug est inactif.



> `LARGEUR : int` et `HAUTEUR : int`

Les dimensions de l'écran en pixel.


> `NOIR`, `BLANC`, `GRIS`, `ROUGE`, `VERT`, `BLEU`, `BLEU_CLAIR` et `JAUNE` de type `color`

Des couleurs RGB.


> `MAX_COMBAT : int`

Le numéro de combat maximum (inclus).


> `INVICIBLE_ENNEMI : bool`

Si l'ennemi ne peut pas prendre de dégat.


> `UI_LONGUEUR_BARRE_DE_VIE` et `UI_HAUTEUR_BARRE_DE_VIE` de type `int`

Les dimensions des barres de vie à l'écran en pixel.

> `POLICE_TITRE` et `POLICE_TEXTE` de type `Font`

Les polices à utiliser pour le titre et les textes normaux.


> `POLICE_FOURRE_TOUT : Font`

Une police utilisée pour le texte des boutons de l'écran titre et pour les crédits, comme elle était sobrement nommée `police`, je l'ai renommé en `POLICE_FOURRE_TOUT` ne sachant ce qu'elle faisait de particulier.


> `TEXTE_INFO_UTILISER` et `TEXTE_INFO_INFO` de type `Surface`

Les textes à afficher sur le côté de l'écran pré-rendus.


> `NAN : NaN`

Représente un nombre indéterminé, il a le même rôle que None mais est réservé aux nombres.  
Il n'est égal à aucun nombre, même pas lui-même (`NAN != NAN`);
pour vérifier si un nombre est nan, utilisez `math.isnan()`.





> Les variables avec en deuxième préfixe `TOUCHE_` ou `TOUCHES_` (types `int` ou `tuple[int, ...]`)

Des touches pour que l'utilisateur puisse interagir avec l'application avec les codes de pygame. (ex: `pygame.UP`)


> `CHEMIN_RACINE : str`
 
Un chemin vers [la racine](../) du projet, change suivant d'où le projet est éxécuté.


> `CHEMIN_DOSSIER_IMG`, `CHEMIN_DOSSIER_SAVE` et `CHEMIN_DOSSIER_ETC` de type `str`

Les chemins vers les sous-dossiers de [data](../data/), changent en fonction de `CHEMIN_RACINE`.

## Autres variables
> `clock : Clock`

La `Clock` se chargeant de plafonner le framerate à 60fps.


> `fenetre : Surface`

Une surface représentant la fenêtre.

> `nbr_combat : int`

Le numéro de combat.


> `tour_joueur : bool`

Si c'est au joueur d'attaquer.


> `menu_running : bool`

Si le l'ecran titre doit être affiché, devrait être enlevé.


> `entitees_vivantes : list[Monstre|Joueur|None]`

La liste de toutes les entitées vivante, plus d'info dans le document [fight-sys.md](../doc/fight-system.md).