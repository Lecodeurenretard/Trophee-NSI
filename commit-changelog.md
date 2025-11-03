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
## Implémentation des stats pour les items (sauf régénération).
+ Changements majeurs
+ Sur plusieurs fichiers
+ Structure de fichiers
+ READMEs et documentation
+ Interactions joueur/testeur
	- Ajout de touches pour changer le nombre d'items dans le shop.
		* Ajout constantes `DBG_SHOP_AJOUT_ITEM` et `DBG_SHOP_SUPPRESSION_ITEM`.
	- Plus d'antialiasing pour les textes: ils deviennent plus faciles à lire.
	- Changement du texte d'effets pour la peluche d'Hornet.
	- Corrections dans le message de Teto maigre.
	- Changement dans les positions et tailles des items du shop.
+ Correction de bugs
+ [fonctions_main.py](sources/fonctions_main.py)
	- Ajout fonction `dessiner_inventaire()`.
	- La fonction `gerer_evenement_shop()` a été scindée en deux fonctions plus petites: `dbg_shop_scroll()` et `shop_click()`.
+ `Item`
	- `.dessiner()` lance des avertissements quand du texte n'est pas affiché.
+ `Jeu`
	- Ajout de `infos_surf` pour que les textes d'informations soient dessinés en dernier.
+ `Joueur`
	- Renommage `.reset_vie()` en `.reset()`, la fonction reset aussi les stats maintenant.
	- `.prendre_item()` et `.lacher_item()` modifient les stats.
+ `Stat`
	- Ajout des méthodes `.additionner()` et `.soustraire()`.