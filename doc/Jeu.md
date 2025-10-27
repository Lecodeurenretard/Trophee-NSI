# Comment marche le jeu?

Depuis le commit ["Implémentation des crédits et fin du remaniement de la logique du jeu." (aa692b3)](https://github.com/Lecodeurenretard/Trophee-NSI/commit/aa692b3e8b5f55c6ee741e53cb5120b431b88c55), le _control flow_ du programme à drastiquement changé. Ce fichier décrit donc comment le jeu fonctionne dans son ensemble.

## 1. Le système d'états
### Une machine à état?
Un état est une subdivision du programme qui ne s'occupe de ne faire qu'une seule tâche. Par exemple, on peut découper la journée d'un écolier en états avec l'écolier ne pouvant être que dans un état à a fois, il vivra donc les états suivants:
1. se lever
2. se préparer à aller en cours
3. être en cours
4. activités diverses
5. se coucher

Pour pouvoir plus facilement voir quel état va déclencher le suivant, on les représentes dans un graphe:
<!--Lien pour le modifier: http://graphonline.top/fr/?graph=LWzxFmwOqxFHmRQC -->
![Graphe correspondant](graphe_écolier.png)

Pour notre jeu, c'est la même chose mais un état peut mener à plusieurs suivant des conditions externes.

### La machine du jeu
Voici le graphe:  
![Le graphe listant les états de `Jeu.Etat`](graphe_etat.svg)  
_<sub>potentiellement pas à jour, [la version à jour](http://graphonline.top/fr/?graph=OMlRPwRCzhQxYjcl)</sub>_

Un comportement typique serait:
1. Commencement à l'écran-titre
	1. Si le joueur choisit de regarder les crédits, il les regarde puis est renvoyé à l'écran d'accueil.
	2. Sinon il peut aussi choisir de commencer le jeu.
2. Avant de commencer le jeu, il faut que le joueur entre son nom et qu'il regarde le faux chargement (skip en mode débug).
3. L'écran de nouveau combat apparait pour quelques secondes.
4. Le joueur combat le premier monstre
	1. Le joueur choisit son attaque.
	2. Les attaques sont affichées et appliquées suivant leurs vitesses.
		- Si le monstre meurt et que ce n'est pas le dernier combat, on déclenche un nouveau combat.
		- Si le joueur meurt ou qu'il a vaincu le dernier monstre, on affiche l'écran de game over.
4. Un deuxième combat...
4. ...
5. L'écran de game over apparait.
	- Ici "Game Over" veut juste dire que le joueur doit commencer une nouvelle partie pour jouer plus (comme sur les bornes d'arcades), ainsi quand il gagne, il est en game over.
	- Si le joueur a coché le paramètre `fermeture_automatique`, le jeu se ferme sinon il est redirigé sur l'écran titre.

### Et dans le code, ça donne quoi?
La liste des états se trouve dans l'énumération [`Jeu.Etat`](../sources/Jeu.py), les variables globales `Jeu.etat` et `Jeu.precedent_etat` permettent d'accéder à l'état actuel du jeu; par contre pour le changer, il faut utiliser `Jeu.changer_etat()`.  
Chaque état possède une fonction correspondante (définies dans le fichier [fonctions_etats.py](../sources/fonctions_etats.py)).

Mis à part les états `GAME_OVER`, `CREDITS` et `PREPARATION`, toutes les fonctions respectent le principe que j'appelle celui de _la boucle d'état_ (je ne sais pas s'il a un nom). Dans une application, il existe ce que l'on appelle une _boucle principale_, la nôtre se trouve dans [main.py](../sources/main.py) et se contente de lancer la fonction correspondante à l'état actuel; la boucle d'état est une boucle principale pour un état.

La boucle d'état ne doit pas être interrompue, c'est-à-dire qu'elle ne doit pas appeler une fonction qui empèche le retour à la boucle d'état pour une période longue; la seule exeption est `Jeu.commencer_frame()` qui attend assez de temps pour que le jeu ne tourne pas au-dessus de 60fps.

### Les interruptions
Les interruptions sont en quelques sortes des mini-états, ils doivent gèrer leurs évènements et dessiner ce qu'ils doivent afficher sur une surface qu'ils renvoierons.

Comme le nom ne l'indique pas, les interuptions ne cassent pas la règle décrite précédement car ce sont en fait des générateurs, ils empèchent juste la boucle d'exécuter autre chose qu'eux.

Pour distinguer les interruptions, il faut utiliser l'alias `Interruption` en type de retour.

## 2. Les animations
On distingue deux types d'animations: celles qui sont préfaites et qui proviennent d'un fichier GIF ou vidéo et celles qui doivent être générées par le jeu. Par exemple, <!--...-->