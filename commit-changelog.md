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
## Les attaques peuvent se jouer plusieurs fois.
+ Changements majeurs
	- La pile d'attaque est remplacée par une liste `attaques_jouees[]`.
	- `Attaque.lancer_toutes_les_attaques_gen()` est remplacée par la méthode non statique `Attaque.lancer()`
	- Ajout de `Jeu.ATTAQUES_PAR_TOUR` et `Jeu.attaques_restantes_joueur[]`.
+ Sur plusieurs fichiers
+ Structure de fichiers
+ READMEs et documentation
+ Interactions joueur/testeur
	- Le son de victoire/défaite est toujours au max maintenant.
	- Un décompte des attaques restantes est affiché en bas à droite.
+ Correction de bugs
+ `Attaque`
	- Ajout de `._jouer_animation()`.
	- L'attribut `.effet` est maintenant mit à `NotImplemented`.
	- Renommage de `._animation` en `._autoriser_animation`
+ [dessin.py](sources/dessin.py)
	- `dessiner_rect()` peut maintenant dessiner des bords ronds.
+ [Jeu.py](sources/Jeu.py)
	- Ajout de `Jeu.pourcentages_coordonees()`.
	- Suppression de `@staticclass` car inutilisé (bien qu'utile).