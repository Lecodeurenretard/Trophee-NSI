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
<!--
Nils: J'utilise l'ordre Ajout, Renommage, Déplacement, Modification, Effacement/Destruction, Autre.
-->
_____
## Ajout du capitalisme
+ Changements majeurs
	- Ajout d'un système d'argent (pièces).
		* Ajout attribut `._nombre_pieces` et propriété `.nb_pieces`.
		* Ajout des méthodes `.gagner_pieces()` et `.paiement()`.
	- Les objets ont maintenant un prix.
		* Ajout de l'attribut `prix` aux instances de `Item`.
	- Les monstres ont maintenant une hierarchie;
		* Ajout de la propriété `.classe()` à `TypeMonstre` (pour l'instant ne sert qu'aux nombre de pièces lachées mais obtiendra un rôle dans le spawn).
+ Sur plusieurs fichiers
+ Structure de fichiers
+ READMEs et documentation
	- Les touches ont été mises à jour dans le [README](sources/README.md) de [sources/](sources/).
+ Interactions joueur/testeur
	- Ajout d'une animation pour indiqué que le joueur à gagné des pièces.
	- Le shop à maintenant un cadre montrant les objets et l'argent du joueur.
	- Nouveau paramètre de triche: argent illimité.
+ Correction de bugs
	- `MultiInterpolation.calculer_valeur()` et implémentations ne crashent plus quand `t=1`.
		* Amélioration du message d'erreur si `t > 1`.
	- Les hitbox pour interagir avec les objets dans le shop sont maintenant correctes.
+ [Animation.py](sources/classes_utiles/Animation.py)
	- Les méthodes `.generateur()` finissent maintenant par `t=1`.
	- Ajout de paramètres `easing_funs[]` sur les méthodes `.generateur()`.
	- Renommage des paramètres `easing` en `easing_fun` sur les méthodes `.generateur()`.
+ [EasingConstants.py](sources/classes_utiles/EasingConstants.py)
	- Ajout de variantes `*_IN` et `*_OUT` à toutes les constantes.
+ [Couleurs.py](sources/Constantes/Couleurs.py)
	- Ajout de la constante `JAUNE_PIECE`.
+ [fonctions_main.py](sources/fonctions_main.py)
	- Ajout de l'interruption `animation_argent_gagne()`.
	- Ajout des fonctions `gerer_evenement_shop()` et `dessine_nombre_pieces()` pour éviter de trop encombrer `shop()`.
	- Séparation de `reagir_appui_touche()` en deux: la partie générale (`reagir_appui_touche()`) et celle spécifique à `choix_attaque()` (`reagir_appui_touche_choix_attaque()`).
+ `Jeu`
	- Ajout de `decision_etat_en_cours()`.
	- `reset_etat()` ne modifie plus `precedent_etat`.
+ `Joueur`
	- Ajout de la propriété `.inventaire[]`.