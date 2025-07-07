# L'interface utilisateur
Toutes les classes décrites dans ce fichier sont attendues d'avoir une méthode `.dessiner()` avec la surface surlaquelle dessiner en premier paramètre.

## Les curseurs
Exemple dans [ex_curseur](../exemples/ex_curseur.py).

Un curseur, c'est une icône (pour l'instant un cercle plein) qui ne peut aller qu'à une liste limitée de positions. Les curseurs sont représentés par des instances de la classe [`Curseur`](../sources/combats/Curseur.py).

Chaque objet a des colonnes et des lignes où elle peut aller, on peut aussi faire en sorte qu'une position précise soit interdite (inacessible).
Par exemple, il est possible de vouloir q'un curseur aille à `(5, 10)` mais pas à `(10, 5)`; il suffit d'ajouter `Pos(10, 5)` aux coordonées interdites.  
A l'intérieur de la classe, les colonnes et les lignes sont triées de manière croissante pour que les déplacements de curseurs soient plus faciles. Les positions interdites n'ont par contre pas besoin d'être triées. Dans toutes les listes, les doublons sont automatiquements enlevés.

En principe, les fonctions `.monter()`, `.descendre()`, `.aller_gauche()` et `.aller_droite()` ne devrait pas être appelées autrement que par les méthodes de l'instance car la méthode `.utilisateur_deplace_curseur()` déplace déjà le curseur suivant les inputs de l'utilisateur.

L'attribut `._pos_dans_toutes_pos` peut se montrer mystèrieux, mais il est simple:  
Imaginez un tableau en deux dimensions avec dans une même ligne les positions ayant la même ordonnée et sur une même colonne les positions ayant les positions avec la même absisse.  
Un exemple est plus parlant:
$$
\begin{pmatrix}
(0; 0)   & (50; 0)   & (100; 0) \\
(0; 50)  & (50; 50)  & (100; 50) \\
(0; 100) & (50; 100) & (100; 100) \\
\end{pmatrix}
$$

`._pos_dans_toutes_pos` Représente tous simplement la position de l'attribut `._pos` dans ce tableau. Si `._pos_dans_toutes_pos == Pos(1, 2)`, on prend la position $(1; 2)$ dans le tableau précédent ce qui donne une position $(50; 100)$ du curseur dans la fenêtre. Cet attribut permet à l'objet de se rappeler où il est sans avoir à chercher ce qui ralentirait inutilement le programe.

## Les boutons
Un bouton est un rectangle sur lequel l'utilisateur peut cliquer, s'il clique une fonction sera éxecutée.  
La classe `Button` est la seule à ne pas avoir été trop modifiée pendant les refactorisations ce qui peut laisser quelques inconsistances avec le reste des classes.

La détéction de clics, laisse volontairement à un clic le pouvoir d'activer plusieurs boutons, ce qui permet de simuler un boutons avec plusieurs actions. Faites attentions au placement et à la durée de vie des boutons (quand est-ce que la variable devient innacéssible).

Les fonctions appelées par les boutons sont définies dans [fonctions_boutons](../sources/combats/fonctions_boutons.py).
Contrairement au reste des classes les méthodes des boutons sont en anglais car ¯\\\_(ツ)_/¯.

La classe `ButtonCursor` hérite de `Button` ce qui lui permet d'obtenir tous les membres (statiques ou non) de celle-ci. Les boutons-curseurs sont des boutons auquels un curseur est attaché. Ils sont organisés par groupes, à chaque groupe son curseur; les curseurs sont détruits quand le dernier bouton du groupe est détruit.

La classe fonctionne avec trois dictionnaires statiques:
- `_group_count`: Compte le nombre de boutons dans le groupe.
- `_group_cursors`: Contient les curseurs de groupe.
- `_group_colors`: Contient la couleur du curseur de groupe lors de son affichage.
Pour chacun d'entre eux, il faut utiliser comme clef le nom du groupe.

Une différence avec les les instances de la classe `Button` est dans le moyen de vérifier si l'utilisateur les séléctionne: au lieu d'utiliser `.check_click()` qui ne vérifie que le clic, on utilise la méthode statique `ButtonCursor.check_input()`; comme cette fonction prend une liste, il est plus pratique de garder les boutons d'un même groupe dans une liste.