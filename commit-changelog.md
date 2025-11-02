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
## Ajout de boutons pour voir les stats
+ Changements majeurs
	- Ajout de constantes `Constantes.Touches.DIFFS` et `Constantes.Touches.DBG_INFOS_ENTITES`.
	- Ajout méthodes `ecran_nombre_combat()` et `dessiner_descriptions_entites()`.
+ Sur plusieurs fichiers
+ Structure de fichiers
+ READMEs et documentation
+ Interactions joueur/testeur
+ Correction de bugs
+ entités:
	- Ajout de la méthode `.decrire()`.
+ [fonctions_vrac.py](sources/fonctions_vrac.py)
	- `dessiner_texte()` prend maintenant en compte les sauts de lignes.
+ `Attaque`
	- Ajout de la propriété `.nom`.
_____
Ce commit n'a pas eu beaucoup de temps pour être testé, il y a sûrment quelques bugs.