# L'interface utilisateur
Toutes les classes décrites dans ce fichier sont attendues d'avoir une méthode `.dessiner()` avec la surface surlaquelle dessiner en premier paramètre.

## Les curseurs
Exemple dans [ex_curseur](../exemples/ex_curseur.py).

Un curseur, c'est une icône (pour l'instant un cercle plein) qui ne peut aller qu'à une liste limitée de positions. Les curseurs sont représentés par des instances de la classe [`Curseur`](../sources/combats/Curseur.py).

Chaque objet a colonnes et des lignes où elle peut aller, on peut aussi faire en sorte qu'une position précise soit interdite (innacessible).  
Par exemple, il est possible de vouloir q'un curseur aille à `(5, 10)` mais pas à `(10, 5)`; il suffit d'ajouter `Pos(10, 5)` aux coordonées interdites.

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
La classe boutons est la seule à ne pas avoir été trop modifiée pendant les refactorisations.  
Un bouton est un rectangle sur lequel l'utilisateur peut cliquer, s'il clique une fonction sera éxecutée.

Les fonctions appelées par les boutons sont définies dans [fonctions_boutons](../sources/combats/fonctions_boutons.py).  
Contrairement au reste des classes les méthodes des boutons sont en anglais car ¯\\\_(ツ)_/¯.