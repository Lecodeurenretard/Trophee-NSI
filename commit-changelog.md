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
## Réécriture de `MultiInterpolation` et `MultiDeplacement`.
+ Changements majeurs
	- Les constructeurs des deux classes ne prennent plus en entrée des listes de listes mais des valeurs `rgb`/`rgba` ou des objets `Pos`.
		- Plein de code inutile enlevé.
		- Les méthodes `.generateur()` ne passent plus par t=1
+ Sur plusieurs fichiers
+ Structure de fichier
+ READMEs et documentation
	- Suppression d'une ligne qui n'était plus vraie dans un README.
+ Interactions joueur/testeur
+ Correction de bugs
+ [Couleurs.py](sources/Constantes/Couleurs.py)
	- Les fonctions `iterables_to_*()` ont leurs annotations changées pour prendre un nombre illimité d'éléments (de toute façon, elles élèvent une erreur si le nombre d'élément n'est pas bon.). 
+ `Attaque`
	- Suppression de `_etat_graphique[]`.
+ Entitées
	- Remplacement de `._etat_graphique[]` est remplacé par `.afficher` car `._etat_graphique[]` ne servait à rien de toute façon.