Ce fichier contient tous les changements faits dans les commits. Il est rafraichit à chaque commits.
Un bon moyen de savoir si le changement devrait être écrit ici, c'est de se demander si il changera la façcon d'interagir sur la fonction/classe.

<!--
format:
## [message du commit]
+ Changements majeurs
	- [Changements à la base du but du commit?]
+ Sur plusieurs fichiers
	- [Autres changements?]
+ Structure de fichier
	- [changements sur la structure de ficher?]
+ READMEs et documentation
	- [changements dans la doc?]
+ Interaction joueur/testeur
	- [Changement touches/dialogue/...]
+ [fichier/classe]
	- [changements...]
+ [...]


--template:--
## 
+ Changements majeurs
+ Sur plusieurs fichiers
+ Structure de fichier
+ READMEs et documentation
+ Interactions utilisateur
+ 
	- 
-->
<!--
Nils: J'utilise l'ordre Ajout, Renommage, Déplacement, Modification, Effacement/Destruction, Autre.
-->
_____
## Réorganisation rapide des fichiers
+ Changements majeurs
+ Sur plusieurs fichiers
+ Structure de fichier
	- Renommage de
		* constantes_globales.py en [globales_constantes.py](sources/globales_constantes.py),
		* variables_globales.py en [globales_variables.py](sources/globales_variables.py),
		* etat_jeu.py en [fonctions_etats.py](sources/fonctions_etats.py),
		* settings_var.py en [parametres_var.py](sources/parametres_vars.py)
		* Settings.py en [Parametres.py](sources/Parametres.py)
	- Suppression du répertoire combat et tout son contenu a été déplacé directement dans [sources](sources/),
	- Supression du repertoire overworld.
+ READMEs et documentation
+ Interactions utilisateur