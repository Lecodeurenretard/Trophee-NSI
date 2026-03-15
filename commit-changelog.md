Ce fichier contient tous les changements faits dans les commits. Il est rafraichit à _à peu près_ chaque commit (si le commit est assez petit, c'est pas très grave si le fichier n'est pas mis-à-jour).

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
## Les modifications de stats par les attaques périment.
+ Changements majeurs
	- Les modifications de stats apportées par les attaques s'estompent après un ou deux tours ainsi qu'à la fin du combat.
+ Sur plusieurs fichiers
	- Actualisation des exemples.
+ Structure de fichiers
	- Suppression de ex_curseur.py.
+ READMEs et documentation
+ Interactions joueur/testeur
	- Skip n'augmente les défenses que de 2 par utilisation.
	- La fenêtre a toujours le nom du jeu en préfixe.
	- Le pseudo est par défaut à "Esquimot".
	- Ajout d'un système de comparaison des fichiers de paramètres pour empècher un oubli de copie et une erreur pas très parlante.
		* S'il manque des paramètres dans paramètres.txt, une boite de dialogue s'ouvrira et demandera de reset les prarmètres.
+ Correction de bugs
+ `Stat`
	- Ajout de la méthode statique `remplies_de()`pour initialiser un objet plus facilement.
	- Ne cause plus de `RuntimeError` si un un attribut n'est pas bon dans la lecture d'un objet Stat en JSON.