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
## Implémentation primitive des boss et bugfix!
+ Changements majeurs
	- Ajout d'un système de boss (v. le tiret sur `Boss`)
+ Sur plusieurs fichiers
+ Structure de fichiers
+ READMEs et documentation
+ Interactions joueur/testeur
	- La pioche se fait maintenant en début de tour.
	- Ajout d'un boss pour les étapes 10 et 20.
+ Correction de bugs
+ `Array`
	- nouvelle fonction `.at()`.
+ `Boss`
	- Fonctionne un peu comme `Monstre` (hérite aussi de cette classe).
	- Pour l'instant les boss sont juste de gros ennemis.
+ `Carte`
	- L'arret de l'animation fait en sorte que la carre soit cachée.
+ `Entite` (donc filles)
	- Ajout de `.piocher_si_main_vide()` car écrire un if, c'est énervant.
+ `Monstre`
	- `.vivants()` garantit le retour de type monstre.

____________
Enfin!  
Sinon pour le système de boss, je pense faire un système de callback qui modifie l'objet `Boss` sans prendre en compte l'encapsulation. Comme un dico qui à le nom de boss en clef et le callback en valeur.