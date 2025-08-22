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
	- Renommage de `entitees_vivantes` en `entites_vivantes`.
	- Les logs débugs sont cachés si le mode débug est désactivés.
	- Modification des attentes envers les entités:
		+ Ajout de la propriété  `.dbg_nom` qui est le nom en contexte de débug.
		+ Ajout des propriétés `.pos_attaque_x` et `.pos_attaque_y` qui controlent la position du dessin des attaques.
		+ Déplacements des fonctionnalités de `.subir_attaque()` dans `.recoit_degats()` car c'est plus simple dans le nouveau système.
		+ Modification du type de retour de `bool` à `None` pour `.attaquer()`.
		+ `.attaquer()` ne fait plus qu'enregistrer l'attaque dans la file.
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
	- Rennommage de `premier_indice_libre_de_entitees_vivantes()` en `premier_indice_libre_de_entites_vivantes()`.
+ [main](sources/combats/main.py)
	- Déplacement de l'écoute pour les touches spéciales dans `reagir_appui_touche()`.
+ `Stat`
	- Suppression de la définition explicite de `.__copy__()` qui ne faisait que la même chose que la définition implicote mais moins bien.