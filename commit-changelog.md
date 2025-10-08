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
+ Structure de fichier
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
## Implémentation des crédits et fin du remaniement de la logique du jeu.
+ Changements majeurs
	- Création fonction `credits()`.
+ Sur plusieurs fichiers
+ Structure de fichier
+ READMEs et documentation
+ Interactions joueur/testeur
	- Les logs sont mieux espacés.
	- L'attaque "Skip" ne glisse plus.
+ Correction de bug
	- `nouveau_combat()` n'est appelée qu'une seule fois avant le premier combat.
	- Les touches débugs marchent.
+ [Ce fichier](commit-changelog.md)
	- Modification nom catégorie "Interaction utilisateur" --> "Interaction joueur/testeur".
+ `Pos`
	- Ajout de la propriété ``
	- Remplacement de la méthode `.__iter__()` par la propriété `.tuple` pour aider le _type checker_.
+ `Attaque`
	- La fin de `lancer_toutes_les_attaques_gen()` est maintenant toujours exécutée.
+ [Bouton.py](sources/Bouton.py)
	- `Button.check_click()` peut prendre une tuple en argument.
	- `ButtonCursor.enable_drawing()` et `ButtonCursor.disable_drawing()` sont maintenant des fonctions statiques prenant le nom du groupe en argument.
+ [fonctions_main.py](sources/fonctions_main.py)
	- Ajout de `joueur_gagne()`.
	- Suppression de `fin_combat()`.
		* Le rôle est déplacé dans l'état `AFFICHAGE_ATTAQUES`.
+ [fonctions_vrac.py](sources/fonctions_vrac.py)
	- Ajout overload pour que `centrer_pos_tuple()` accepte les objets `Pos`.
		* Renommage de la fonction en `centrer_pos()`.
+ [main.py](sources/main.py)
	- `jeu()` ne modifie plus le numéro de combat.
	- Suppression de la fonction `__main__()`.
		* On passe directement par `jeu()`.

_________________________________
note: Les docs serons dans le prochain commit