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
## [buggy] Changements divers
+ Changements majeurs
+ Sur plusieurs fichiers
+ Structure de fichiers
+ READMEs et documentation
+ Interactions joueur/testeur
	- Changement de couleur pour les barres de vies à 100%.
	- Le joueur peut maintenant utiliser les touches de base (celles gérées dans `reagir_appui_touche()`) dans l'état `AFFICHAGE_ATTAQUE`.
	- Les appuis ne sont plus gardés entre les états.
+ Correction de bugs
	- [Entite.py](sources/Entite.py) est enlevé du [.gitignore](.gitignore).
	- Les deux bugs du commits précédents ont été réparés.
+ `Array`
	- `.pop()` vérifie l'index passé en argument.
+ [Carte.py](sources/Carte.py)
	- Les animations sont représentées par une enum `CarteAnimEtat`.
	- Ajout de `.dans_hitbox()`.
	- Renommage de `.anim_nom` en `.anim_etat`.
	- Suppression de `.souris_survole`.
+ `Entite`
	- Renommage de `._inserer_carte_main()` en `._ajouter_carte_main()` et ajout du paramètre `faire_revenir`.
	- Ajout de `._vider_main()`.
+ `Jeu`
	- Ajout de `decision_boss()` (inutile pour l'instant).
	- `DECISION_SHOP()` est maintenant une vraie fonction est est renommée `decision_shop()`.
+ `Joueur`
	- Remplacement de `.verifier_pour_attaquer()` par `.carte_du_dessus()`.


____________
Je laisse un bug dont je n'arrive oas à trouver l'origine et donc à fix.  
Si on spam le clic après l'animation de la carte, elle va en animation `JOUER` pour instantanément revenir  en `IDLE`.
Le joueur verra la carte de dos pendant 1 frame et après le jeu plante.