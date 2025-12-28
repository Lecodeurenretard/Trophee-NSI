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
## Actualisation de la doc.
+ Changements majeurs
	- Corrections dans [fight-system.md](doc/fight-system.md), dans [files.md](doc/files.md), dans [Jeu.md](doc/Jeu.md) et dans le [README de doc/](doc/README.md).
+ Sur plusieurs fichiers
	- Renommage de `Entite._CACHER_CARTES` en `Entite._CARTES_DE_DOS` (donc aussi dans les classes filles)
+ Structure de fichiers
+ READMEs et documentation
	- Ajout de la classe `Entite` dans le système de combat.
	- Ajout du système de cartes et du système d'items passifs.
	- Tous les fichiers sont maintenant décrits dans [files.md](doc/files.md).
	- Ajout du shop dans le graphe des états.
	- Corrections dans [Jeu.md](doc/Jeu.md) et dans le README.
	- Suppression du contenu inutile.
+ Interactions joueur/testeur
+ Correction de bugs
	- On peut vraiment jouer cette fois.
	- Si Tkinter n'est pas installé/installable, une issue de secour est prévue dans la console.
+ [Carte.py](sources/Carte.py)
	- Déplacement des infos d'animation dans une nouvelle dataclasse `CarteAnimInfo` (c'est maintenant _un peu_ plus propre).
		- Fusion de `._anim_destination`, `._anim_duree`, `._anim_easing` et `._anim_de_dos` en `._anim_infos`.

_______________
Tout marche correctement sauf le lancer de carte qui lag toujours.