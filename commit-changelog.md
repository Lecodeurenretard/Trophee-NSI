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
+ Interaction utilisateur
+ 
	- 
-->
<!--
Nils: J'utilise l'ordre Ajout, Renommage, Déplacement, Modification, Effacement/Destruction, Autre.
-->
_____
## Changements mineurs en vue d'un changement de comportement des curseurs
+ Changements majeurs
+ Sur plusieurs fichiers
	- Suppression de la fonctionnalité du compteur FPS car impréci et inutile
		* Enlèvement de la constante `UI_TOUCHE_AFFICHAGE_FPS`.
		* Suppression des variables globales `UI_affichage_fps_autorise` et `delta`.
		* Ajustement des documentations.
+ Structure de fichier
+ READMEs et documentation
+ Interaction utilisateur
+ `ButtonCursor`
	- Renommage et changement en propriété: `._do_group_cursor_select_button()` -> `._do_cursor_select_button`.
+ `Curseur`
	- Ajout de `._aller_premier_emplacement_autorise()` pour éviter que le curseur spawn à une position interdite.
	- Ajout de la méthode (non finie) `._bouger()` qui généralisera le rôle de `.monter()`, `.aller_gauche()`, ....
	- Renommage de `._ajouter_a_pdp_y` en `._ajouter_a_pdtp_y`.
	- Modification du message d'erreur si jamais les coordonnées sont incorrecte dans `.coordonees_globales_vers_coordonees_curseur()`.
+ entités
	- Ajout de propriétés (pas encore ajoustées ni utilisées) `.pos_curseur_x` et `.pos_curseur_y`.