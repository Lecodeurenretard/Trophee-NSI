Ce fichier contient tous les changements faits dans les commits.
Un bon moyen de savoir si le changement devrait être écrit ici, c'est de se demander si il changera la façcon d'interagir sur la fonction/classe.

<!--format:--
> **[message du commit]**
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