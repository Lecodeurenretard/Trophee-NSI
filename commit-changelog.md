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
## Continuation de la refactoriasation du jeu, commencement implémentation machine à états
+ Changements majeurs
	- Avancement vers le but 1 seule boucle while True par états.
		* La fonction `attendre()` à été beaucoup modifiée.
			* Renommage en `pause()`.
			* Changement complet de logique <!--ne vous inquiétez pas, j'ai résolu le bateau de Thésée-->, la fonction ne bloque plus le programme mais pose une heure où le programme pourra reprendre et retourne `False` jusqu'à que l'horloge interne l'atteigne.
	- Ajout d'une notion d'interruption qui monopolisent la boucle de l'état courant. C'est pour éviter de créer trop d'états.
		* Ajout d'une interruption: l'écran d'informations pour les attaques.
		* Le menu des paramètres à été changé en interruption.
	- Import du décorateur `@overload` de `typing` pour mieux séparer les fonctions de mêmes noms.
		- Ajout d'overloads pour `verifier_pour_quitter()`
		- Ajout d'overloads pour le constructeur de `Pos`.
+ Sur plusieurs fichiers
	- Renommage de `etat_du_jeu` et `precedent_etat_du_jeu` en `etat_jeu` et `precedent_etat_jeu`.
	- Déplacement de `EtatJeu`, `etat_jeu` et `precedent_etat_jeu` de [etats_jeu](sources/combats/etats_jeu.py) à [variables_globales](sources/combats/variables_globales.py).
	- Déplacement de `changer_etat()` dans [fonctions_vrac](sources/combats/fonctions_vrac.py).
+ Structure de fichier
+ READMEs et documentation
+ Interactions utilisateur
	- Le joueur peut maintenant accéder aux états ``
	- Les noms de touches sont en français.
	- Le testeur peut skip l'écran avant le combat.
	- Tweak des positions des boutons sur l'écran titre.
		* Ils sont maintent relatifs à la taille de l'écran.
	- Le texte dans les infos du joueur sont maintenant correctement centrés.
	- Les textes indiquant les touches sont maintenant à un endroit correct.
+ `Attaque`
	- La méthode statique `lancer_toutes_les_attaques_gen()` n'élève plus une `StopIteration` quand le lanceur de l'attaque meurt mais `return` à la place.
+ `ButtonCursor`
	- Ajout d'un attribut de groupe: `_is_drawn` pour cacher les curseurs des groupes déclarés mais pas explicitements affichés.
		* Ajout des méthodes `.enable_drawing()` et `.disable_drawing()` pour afficher/cacher le curseur.
+ [variables_globales](sources/combats/variables_globales.py)
	- Ajout d'un alias `Interruption` pou les générateurs venant interompre l'état courant.
+ [etats_jeu](sources/combats/etats_jeu.py)
	- Ajout d'une docstring.
	- Vraie implémentation de `choix_attaque()`, on ne peut par contre pas encore lancer d'attaques.
	- `attente_nouveau_combat()` n'incrémente plus `nbr_combat` pour les touches du mode débug.
+ [fonctions_boutons](sources/combats/fonctions_boutons.py)
	- `menu_parametres()` est maintenant une interruption.
+ [fonctions_main](sources/combats/fonctions_main.py)
	- La fonction `reagir_appui_touche()` renvoie maintenant une interruption si necéssaire (pour l'instant seule source d'interruptions).
+ [fonctions_vrac](sources/combats/fonctions_vrac.py)
	- Ajout de `testeur_skip_ou_quitte()` (2 overloads) qui fusionne `testeur_skip()` et `verifier_pour_quitter()`.
	- Ajout d'un paramètre `a_envoyer` à `terminer_generateur()`.
	- Ajout s'une variante à `terminer_generateur()`: `terminer_interruption()` qui s'exécute jusqu'à que l'interuption soit terminée.
	- Ajout de `centrer_pos_tuple()` (2 overloads) qui centre une position (sous forme de tuple) comme si c'était un rectangle.
+ `Pos`
	- Suppression de `a_partir_de_collection()` car inutile avec le nouveau constructeur..
+ [UI.py](sources/combats/UI.py)
	- Renommage de `chargement()` en `faux_chargement()`, et son argument est maintenant une durée.