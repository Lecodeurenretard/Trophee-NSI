Ce fichier contient tous les changements faits dans les commits. Il est rafraichit à chaque commits.
Un bon moyen de savoir si le changement devrait être écrit ici, c'est de se demander si il changera la façcon d'interagir sur la fonction/classe.

<!--
format:
## [message du commit]
+ Changements majeurs
	- [Changements à la base du but du commit]
+ Sur plusieurs fichiers
	- [Autres changements?]
+ Structure de fichier
	- [Changements sur la structure de ficher]
+ READMEs et documentation
	- [Changements dans la doc?]
+ Interaction joueur/testeur
	- [Changement touches/dialogue/...]
+ Correction de bug
	- [Interaction joueur/testeur mais pour les corrections de bugs]
+ [fichier/classe]
	- [...]

--------------template--------------
## 
+ Changements majeurs
+ Sur plusieurs fichiers
+ Structure de fichiers
+ READMEs et documentation
+ Interactions joueur/testeur
+ Correction de bugs
+ []()
	- 
------------------------------------
-->
_____
## Implémentation (incomplète) des cartes.
+ Changements majeurs
	- Des cartes sont jetées à la place des rectangles de couleur.
	- Ajout des sprites de cartes.
	- Beaucoup de changements dans le fichier [Attaque.py](sources/Attaque.py) (v. puce dédiée).
	- Ajout de la classe `Carte` (donc du fichier [Carte.py](sources/Carte.py)).
	- Réorganisation de [attaques.json](data/cartes.json) avec un objet "attaque" qui contiendra toutes les infos passées aux objets `Attaque` (le reste l'étant aux instances de `Carte`).
+ Sur plusieurs fichiers
+ Structure de fichiers
	- Renommage de /data/attaques.json en [/data/cartes.json](data/cartes.json).
+ READMEs et documentation
+ Interactions joueur/testeur
	- Le bouton de sortie du shop est maintenant carré.
	- Ajustement du point de départ/d'arrivée des cartes.
	- La stat de "vitesse" n'existe plus.
+ Correction de bugs
	- Le texte de fenêtre se remet à "Combat!" après être partit du shop.
	- Le curseur n'apparait plus pendant une frame entre les attaques.
	- Les pseudos vides ne sont plus acceptés.
+ [Attaque.py](sources/Attaque.py)
	- Le fichier est plus court de 150 lignes.
	- Ajout des constantes `Attaque._DEFAUT_PROB_CRIT`, `Attaque._DEFAUT_FLAGS` et `Attaque._DEFAUT_AJUSTEMENT`.
	- Ajout des propriétés `Attaque.id`.
	- Ajout de la méthode `Attaque.decider_crit()`.
	- Déplacement des membres suivants (de `Attaque`) vers `Carte`:
		* `_DUREE_ANIMATION`,
		* `_DUREE_ENTRE_ATTAQUES`,
		* `SON_COUP`,
		* `SON_HEAL`,
		* `SON_CRIT`,
		* `._desc`,
		* `._autoriser_animation`,
		* `._deplacement`,
		* `._dessiner()`,
		* `._jouer_animation()`,
		* `pos_anim_attaque()`,
		* `.lancer()` (renommé en `.jouer()`),
		* `.enregister_lancement()`,
		* `.jouer_sfx()`,
	- Renommage de `_ajustements` en `_ajustements_t` pour mieux le différencier avec la constante.
	- Renommage et changement de type de `Attaque.LISTE` en  `Attaque._liste`. <!--Bateau de Thésée?-->
	- Réécriture du constructeur de `Attaque` pour qu'il aille chercher ses données directment dans `Attaque._liste` au lien de devoir passer par une fonction intermédiaire.
		* Suprression de `Attaque._depuis_json_dict().`
	- Remplacement de `Attaque.actualiser_liste()` par `Attaque.set_liste()`.
	- Les propriétés `Attaque.lanceur` et `Attaque.cible` sont maintenant publiques.
	- Suppression de `Attaque._vitesse`.
		* Suppression de `Attaque.vitesse`.
	- Suppression de `TypeAttaque.couleur`.
		- Suppression de `Attaque._couleur`.
+ [fonctions_vrac.py](sources/fonctions_vrac.py)
	* Ajout d'une variable de type générique `T`.
	* Ajout de la fonction `valeur_par_defaut()`.
+ `Joueur`
	- Renommage de `.noms_attaques` en `.noms_cartes`.
	- Suppression de `.get_attaque_surface()`, `.attaque_peut_toucher_lanceur()` et de `.attaque_peut_toucher_ennemis()`
+ `Monstre`
	- Renommage de `.choisir_attaque()`en `.choisir_carte()`.
+ [UI.py](sources/UI.py)
	- `trouve_attaque_a_partir_du_curseur()` renvoie maintenant une carte et est renommé `trouve_carte_a_partir_du_curseur()`.