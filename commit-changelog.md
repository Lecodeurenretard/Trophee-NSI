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
## Ajout de radio + pop up quand le programme s'arrête dû à une erreur
+ Changements majeurs
	- Le shop boucle sur des musiques random.
	- Le jeu ouvre une fenêtre Tkinter avec le message d'erreur qi le joueur n'est pas dans le mode débug.
+ Sur plusieurs fichiers
+ Structure de fichiers
	- Ajout des musiques dans [data/musique/radio/](data/musique/radio/).
		* Ajout des constantes `MUSIQUE` et `RADIO` dans [Chemins.py](sources/Constantes/Chemins.py).
+ READMEs et documentation
+ Interactions joueur/testeur
+ Correction de bugs
+ `Jeu`
	- Ajout de la variable `volume_musique`.
	- Ajout des méthodes `jouer_musique()` et `interrompre_musique()`.

_______
Musiques qûrement copyright, il faudra les changer.