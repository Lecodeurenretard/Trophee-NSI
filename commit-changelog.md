Ce fichier contient tous les changements faits dans les commits.
Un bon moyen de savoir si le changement devrait être écrit ici, c'est de se demander si il changera la façcon d'interagir sur la fonction/classe.

<!--format:--
> **[message du commit]**
+ Changements majeurs
	- [Changements à la base du but du commit?]
+ Sur plusieurs fichiers:
	- [Autres changements?]
+ Structure de fichier
	- [changements sur la structure de ficher?]
+ READMEs et documentation
	- [changements dans la doc?]
+ [fichier/classe]
	- [changements...]
+ [...]


--template:--
> **[]**
+ 
	- 
-->
<!--
Nils: J'utilise l'ordre Ajout, Renommage, Déplacement, Modification, Effacement/Destruction, Autre.
-->
_____
> **Ajout de changelog et petits Changements**
+ Structure de fichier
	- Création de ce fichier.
	- Déplacement des constantes de [variables_globales.py](sources/combats/variables_globales.py) dans [variables_globales.py](sources/combats/variables_globales.py)
+ READMEs et documentation
	- Changements de liens dans le README de [combats](sources/combats/).
+ [Attaque.py](sources/combats/Attaque.py)
	- Ajout de la propriété non publique `._couleur` dans `Attaque`.
	- Déplacement de la décision de la couleur de l'attaque est maintenant faite dans la propriété `.couleur` de `TypeAttaque`.
	- La définition de `ATTAQUE_DISPONIBLES` est maintenant plus belle à lire.
+ `BoutonCursor`
	- Ajout des propriétés (non statiques) `._group_count`, `._group_cursor` et `._group_color`.
		* La propriété `.cursor` devient un getter pour `._group_cursor`.
	- Ajout de `._do_group_cursor_select_button()`.
	- Renommage des propriétés statiques `_group_count`, `_group_cursor` et `_group_color` pour avoir le préfixe `_static`.
	- Renommage de `check_inputs()` en `handle_inputs()` avec son premier paramètre.
	- Déplacement des créations de groupe et l'ajout des objets à ceux-ci dans leurs méthodes statiques respective: `_create_group()`, `_add_to_group()`.
	- Destruction de la propriété `.cursor_color`.
+ `Curseur`
	- Renommage de `._ligne_dispo` en `._lne_dispo`.
	- Renommage de `.coordonee_globale_vers_coordonee_curseur()` en `.coordonees_globales_vers_coordonees_curseur()`.
	- Renommage de `.position_dans_position` en `.position_dans_positions`.
+ [fonctions_boutons.py](sources/combats/fonctions_boutons.py).
	- Renommage de `jouer()` en `lancer_jeu()`.
+ [fonctions_vrac.py](sources/combats/fonctions_vrac.py).
	- Effacement de la fonction `find()`.
		* Effacement de ses tests.
		* Effacement des types génériques `T` et `Err`.
+ `Joueur`
	- L'attribut `dimensions_sprite` est maintenant une constante.
		* Renommage en `DIMENSION_SPRITE`.


> **Implémentation de la vitesse**
+ Changements majeurs
	- Ajout de `Attaque.attaques_du_tour[]` regroupant toutes les attaques lancées.
	- Modification de la pipeline des attaques pour la centraliser dans `Attaque.lancer_toutes_les_attaques()`.
+ Sur plusieurs fichiers
	- Renommage de `entitees_vivantes` en `globales.entites_vivantes`.
	- Les logs débugs sont cachés si le mode débug est désactivés.
	- Modification des attentes envers les entités:
		* Ajout de la propriété  `.dbg_nom` qui est le nom en contexte de débug.
		* Ajout des propriétés `.pos_attaque_x` et `.pos_attaque_y` qui controlent la position du dessin des attaques.
		* Déplacements des fonctionnalités de `.subir_attaque()` dans `.recoit_degats()` car c'est plus simple dans le nouveau système.
		* Modification du type de retour de `bool` à `None` pour `.attaquer()`.
		* `.attaquer()` ne fait plus qu'enregistrer l'attaque dans la file.
		* Suppression de `.dessiner_attaque()` car la responsabilité du dessin revient à l'attaque elle-même.
	- 
+ Structure de fichier
	- [guide](guides/) à son propre dossier [img](guides/imgs/) maintenant.
+ READMEs et documentation
	- Update des guides
		* Correction d'erreur sur la copie d'objets, `copy()` n'a pas besoin de `.__copy__()`.
		* Nouvel exemple.
		* Ajout de la section sur les files et les piles.
+ ce fichier
	- Ajout des sections sur plusieurs fichier et majeurs.
+ [Attaque](sources/combats/Attaque.py)
	* Dans `Attaque`
		- Ajout de l'attribut `._vitesse`.
			+ Ajout de `vitesse` dans le constructeur
			+ Ajout du getter `.vitesse`.
		- Ajout de l'attribut `._ajustement_degats()`.
			+ Ajout de `dernier_changements` dans le constructeur
		- Ajout des attributs `._lanceur_id` et `._cible_id`.
			+ Ajout des propriétés `._lanceur` et `._cible` pour accéder plus facilements aux objets.
			+ Modification de `.calculer_degats()` et `.dessiner()` pour ne prendre qu'un seul argument.
		- Ajout de l'attribut `._crit`.
			+ Modification de la pipeline des attaques pour ne plus avoir à passer si l'aataque est un crit.
		- Ajout de la méthode statique `lancer_toutes_les_attaques()` se chargeant d'appliquer les effets des attaques et de les dessiner.
		- Ajout de la méthode `Attaque.appliquer()` qui applique les effets de l'attaque.
		- Ajout de la méthode `.enregister_lancement()` qui insère l'attaque dans la file.
		- Déplacement de la convertion en string dans la méthode `.dbg_str()`.
	* Ajout de `AttaquePriorisee` faisant office d'enveloppe pour les attaques dans la file.
+ [constantes_globales](sources/combats/constantes_globales.py)
	- Ajout de `VITESSE_MAXIMUM` et `MAXIMUM_ENTITES_SIMULTANEES`.
+ `Joueur`
	- Ajout des propriétés `.dbg_nom`, `.stats`, `.pos_attaque_x` et `.pos_attaque_y`.
	- Suppression de `.subir_attaque()` qui est devenu inutile.
	- Suppression de `.dessiner_attaque()` vu qu'elle se fait dans `Attaque.lancer_toutes_les_attaques()`.
+ [fonction_vrac](sources/combats/fonctions_vrac.py)
	- Renommage de `premier_indice_libre_de_entitees_vivantes()` en `premier_indice_libre_de_entites_vivantes()`.
+ [main](sources/combats/main.py)
	- Déplacement de l'écoute pour les touches spéciales dans `reagir_appui_touche()`.
+ `Stat`
	- Suppression de la définition explicite de `.__copy__()` qui ne faisait que la même chose que la définition implicote mais moins bien.


> **Les "structures" sont désormais des dataclasses.**
+ Structure de fichier
	- Ajout de fichiers:
		* [fonctions_main](sources/combats/fonctions_main.py) pour les fonctions seulement utilisées dans [main](sources/combats/main.py)
		* [settings](sources/combats/settings.py) pour l'implémentation des settings.
		* [settings](sources/combats/settings.py) pour l'implémentation des settings.
	- Renommage de Stat.py en [Stats.py](sources/combats/Stats.py).
	- Suppression du main.py de [source](sources/).
+ Sur plusieurs fichiers
+ `Attaque`
	- Ajout de test dans `.appliquer()` pour voir si l'attaque peut attaquer sa cible.
+ [constantes_globales](sources/combats/constantes_globales.py)
	- Le logging de débogage est maintenant bien affiché.
+ [fonctions_boutons](sources/combats/fonctions_boutons.py)
	- Ajout d'une vérification de d'évènement pour pouvoir quitter dans les crédits.
+ [fonctions_vrac](sources/combats/fonctions_vrac.py)
	- Réimplémentation de la fonction qui n'écoute les évènements seulement pour quitter le programme sous le nom `verifier_pour_quitter()`.
+ `Stats`
	- Maintenant une dataclass.
	- Suppression de `.est_initialise` car inutile.
	- Suppression de `.__init__()`, `.__str__()`, `.__eq__()` car générées automatiquement (`__str__()` l'est par `__repr__()`).
	- Suppression de la méthode `.set()` car inutile.
	<!--On est passé de 118 à 24 ligne-->
+ `Pos`
	- Maintenant une dataclass.
	- Déplacement des fonctions de `.__str__()` dans `.__repr__()`.
	- Suppression de `.__init__()`, `.__eq__()` car générées automatiquement.
	- Suppression de la méthode `.set()` car inutile.

> **Retour et update de la documentation dans le repo.**
+ Changements majeurs
	- Déplacement des documentations dans le dossier [doc](doc/).
		* Création de [global-vars](doc/global-vars.md) pour la liste des variables globales.
		* Création de [fight-system](doc/fight-system.md) pour le système de combat (fichier principal).
	- Déplacement des guides dans le wiki.
		* Suppression de Git.md
		* Suppression de Python.md
+ READMEs et documentation
	- Ajout de [files.md](doc/files.md)
		+ Correction des liens cassés.
		+ Corrections des descriptions et ajouts de fichiers manquant.
	- [fight-system](doc/fight-system.md)
		+ Modification des liens pour pointer en local.
		+ Correction des liens cassés.
		+ Modification des dans la doc des suppositions faites aux entités.
			* Modifications du commit _Implémentation de la vitesse_.
			* Ajout de `.dbg_nom`, `.pos_attaque_*`.
		+ Correction d'erreurs.
		+ Ajout d'une section _"Un tour expliqué sous différents points de vue"_.
	- [GUI](doc/GUI.md)
		+ Réparation des liens.
		+ Le /shrug est mort
	- Les liens des READMEs ont étés corrigés.
+ Sur plusieurs fichiers
	- Renommage de `UI_autoriser_affichage_fps` en `UI_affichage_fps_autorise`.
	- Déplacement `UI_affichage_fps_autorise` de [constantes_globales](sources/combats/constantes_globales.py) vers [variables_globales](sources/combats/variables_globales.py).
+ `Attaque`
	- `.dbg_str` devient `.__repr__()`
	- Renommage de `.type_attaque` et `.type`.
	- Suppression de `._nom_surf`, ses fonctions ont été déplacé dans `.nom_surface`.
+ `Joueur` et `Monstre`
	- La propriété `.stats` renvoie maintenant une copie de `._stats` au lieu d'une reférence.

> **Ajout des settings de catégorie "case à cocher".**
+ Changements majeurs
	- Grand développemment la classe `Setting`.
	- Ajout de paramètres
	- Implémentation de la fonction `ouvrir_parametres()`.
+ Sur plusieurs fichiers:
	- `MODE_DEBUG` est maintenant un `Parametre` (non accéssible à l'utilisateur).
		* Renommage en `mode_debug`.
+ Structure de fichier
	- Ajout de [import_local](sources/combats/import_local.py) pour les imports des classes de ce projet.
	- Renommage de settings.py en [Settings.py](sources/combats/Settings.py).
+ READMEs et documentation
	- La documentation sera ajoutée dans le prochain commit.
+ `Attaque`
	- Ajout de la vitesse dans `.__repr__()`.
	- Remplacement des `time.sleep()` par `attendre()` dans `lancer_toutes_les_attaques()`.
+ `Button`
	- Ajout de la méthode `.in_butt_hit()`.
+ [constantes_globales](sources/combats/constantes_globales.py)
	- Ajout de `CENTRE_FENETRE`.
	- Ajout des alias `rgb` et `rgba`
		* Ajout de fonctions de convertions dans [fonction_vrac](sources/combats/fonctions_vrac.py): `rgb_to_rgba()`, `rgba_to_rgb()`, `color_to_rgba()` et `color_to_rgb()`.
		* `color` n'est plus que l'union des deux.
	- Ajout des couleurs `GRIS_CLAIR` et `TRANSPARENT`.
	- Ajout de `UI_TOUCHES_INFOS` et de `UI_TOUCHE_SETTINGS`.
	- `POLICE_TITRE` est maintenant souslignée.
+ `Curseur`
	- Mise en public de `._interdir_col_sauf()` et de `._interdir_lne_sauf()`
		- Renommés en `.interdir_col_sauf()` et `.interdir_lne_sauf()`
+ [dessin.py](sources/combats/dessin.py)
	- Ajout de `dessiner_rect()` qui permet de centrer des rectangles.
+ [fonctions_boutons](sources/combats/fonctions_boutons.py)
	- Renommage de `ouvrir_parametres()` en `menu_parametres()`.
+ [fonctions_main](sources/combats/fonctions_main.py)
	- Ajout d'une touche pour des settings dans `reagir_appui_touche()`.
	- Ajout d'une séparation débug/non débug dans `reagir_appui_touche()`.
	- Modification valeur de retour de `fin_combat()`. `None` -> S'il faut retournen au menu.
	- Modification de `nouveau_combat()`.
		* Nouveau paramètre: `reset_joueur` permet de reset la vie du joueur.
		* Le paramètre `numero_combat` n'est plus automatiquement encadré entre $[1; \text{MAX\_COMBAT}]$, si sa valeur est en dehors de ces limites, la fonction élèvera une `ValueError`. Si jamais le testeur essaye d'aller en dehors de ses limites avec Z et S, l'exception est attrapée et le jeu ne réagit.
+ [fonction_vrac](sources/combats/fonctions_vrac.py)
	- Ajout de `blit_centre()` qui reproduit `Surface.blit()` mais la position indiquée sera le milieu de la surface.
+ `Pos`
	- Ajout d'opérateurs `+` et `-` pour les `Pos`s et `Vecteur`s (`pygame.math.Vector2`).
	- Renommage de `a_partir_de_liste()` en `a_partir_de_collection()`.
+ [settings_var](sources/combats/settings_vars.py):
	- ReCreéation du fichier. (c'est comme si le fichier avait été créé dans ce commit).
	- Ajout d'un générateur pour décider des positions des fichiers.
	- Ajout et implémentation des paramètres
		* `fermer_a_la_fin`,
		* `joueur_invincible`,
		* `monstre_invicible`,
	- Ajout des listes `PARAMETRES_NORMAUX[]` et `PARAMETRES_TRICHE[]` pour pouvoir classer les paramètres à afficher.
+ [Settings.py](sources/combats/Settings.py)
	- `TypeParametre`
		* Ajout propriétés `.hauteur`, `.largeur` et `.dimensions`.
		* Ajout de `.type_correspondant` pour pouvoir facilement vérifier si `Parametre._valeur` est correct.
		* Ajout de la méthode statique `dessiner()` (statique pour faciliter la récursivité).
		* Renommage de `CHOIX_UN_SEUL` en `RADIO` (comme en HTML).
		* Renommage de `CHOIX_PLUSIEURS` en `CHECKBOXES` (aussi comme en HTML).
		* Séparation de `SLIDER` en `SLIDERI` et `SLIDERF`.
	- `Parametre`
		* Ajout attributs statiques `_ECART_NOM_VALEUR` et `_POLICE`.
		* Ajout de convertions vers `bool`, `int`, `float` et `str` pour récupérer la valeur plus facilement.
		* Ajout des propriétés `._possibilites_finies`, `._hitbox`, `._hitbox_globale`, `.valeurs_autorisees` (getter + setter) ainsi que `.case_cochee`.
		* Ajout de `dessiner_groupe()` et `.dessiner()`.
		* Ajout des méthodes `._convertion_vers_type()`, `.reset_val()` et `.prendre_input()`.
		* Suppression du status de dataclass.
			+ Ajout d'un constructeur.