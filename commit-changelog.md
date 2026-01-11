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
## [buggy] Les cartes disparaissent et réapparaissent + Nouveau conteneur `Array`.
+ Changements majeurs
	- Ajout de la classe `Array` pour remplacer les dicos qui étaient utilisés avant.
		- Suppression de `premier_indice_libre()` car c'est juste un cas spécifique de `Array.search()`.
+ Sur plusieurs fichiers
+ Structure de fichiers
+ READMEs et documentation
+ Interactions joueur/testeur
+ Correction de bugs
	- Il n'y a plus de frame où les cartes disparaissent entre les animations.
+ `Duree`
	- Le constructeur à maintenant 2 overloads qui l'empèche d'être appelé sans et avec 2 arguments (du moins virtuellement).
	- Les opérateurs de comparaisons ne marchent plus avec les `int`s.
+ `Attaque`
	- `.avec_nom()` élève une meilleure erreur s'il n'y a pas d'attaque avec le nom en argument.
+ `Carte`
	- Ajout de la propriété `.est_a_pos_defaut`.
	- Si l'animation passée à `._anim_nom` n'existe pas, on se reporte à `idle`.
	- Suppression de `._anim_sens`.
+ `Entite`
	- Ajout de la propriété `.cartes_main_sont_a_pos_defaut`.
	- Ajout des méthodes `.main_jouer_entrer()` et `.main_jouer_sortir()`.
+ [fonctions_main.py](sources/fonctions_main.py)
	- Ajout de `tour_des_monstres()` pour accueillir le code pour faire jouer les monstres.
+ [fonctions_vrac.py](sources/fonctions_vrac.py)
	- `avancer_generateurs()` et `terminer_generateur()` sont maintenant des génériques.



____________
Les bugs sont beaucoup moins fréquents en mode débug pour une certaine raison.  
J'en ai distingué 2:
- Le jeu plante quand l'ennemi joue (1/4 sans le mode débug assez rare avec)
- Les cartes réapparaissent dans le mauvais ordre et les nouvelles ne sont piochées q'après en avoir joué une.