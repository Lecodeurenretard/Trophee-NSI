<!--
Voir celui des autres projets:
The Graphics Engine: https://forge.apps.education.fr/laureats_2025/prix-meilleur-projet-terminale/-/blob/main/docs/presentation.pdf?ref_type=heads

HeatCore: https://forge.apps.education.fr/laureats_2025/prix-coup-de-coeur-terminale/-/blob/main/docs/presentation.pdf?ref_type=heads

et le reglement: https://trophees-nsi.fr/media/pages/ressources/cf8c835af4-1771927618/trophees-nsi_reglement_2026.pdf
-->

# Présentation du projet
## Présentation globale

## Organisation du travail
+ **Nils Adekambi** a.k.a. **[@LeRetardatN](https://github.com/Lecodeurenretard)**: Le code et la documentation.
+ **Jules Penas** a.k.a.**[@Dooheli](https://github.com/Dooheli)**: Les graphismes et le code des boss.
+ **Lucas Deland'huy** a.k.a. **[@hibou509](https://github.com/hibou509)**: Béta-test et équilibrage.


Le projet est commencé en mai 2025 par [@Dooheli](https://github.com/Dooheli) et [@hibou509](https://github.com/hibou509). [@LeRetardatN](https://github.com/Lecodeurenretard) est arrivé à la création du Github le 13 juin 2025.

## Etapes du projet
### Avant l'arrivée de @LeRetardatN
### La refactorisation
De ce moment, jusqu'à la rentrée en septembre. J'était seul sur le développement du fait à des erreurs de communications et du fait que ni @Dooheli ni @hibou509 connaissaient Git.

Quand je reçus le code, il était concentré qu'en un seul fichier d'un peu moins de 400 lignes. Le code était répétitif et dispersé à travers les fonctions. Ainsi la première semaine fut consacrée séparer le code en fonctions puis en modules. Les tout débuts du développement ont aussi données naissance à des guides sur le style et la manière d'utiliser Git/Github.  
Assez rapidement, les classes principales comme `Joueur`, `Stat`, `Attaque`, etc... sont impémentées.

La structure du code est toujours instable et jusqu'à l'arborescence de fichiers change toujours beaucoup.

### Les pas vers la forme finale
Ces pas commencent avec l'implémentation de la machine à états qui ancre le code dans une logique plus stricte. Elle a aussi permis de rendre le code beaucoup plus lisible en délimitant les différentes régions du jeu.  
Rapidement après, le shop puis le système d'objets pouvant modifier les statistiques d'une entité sont ajoutés.

Début novembre, les attaques et les monstres obtiennent leurs fichiers JSON respectifs ce qui sépare les données du code.

Comme les cours ont repris nous avons pu nous concerter en présentiel ce qui permet d'enfin pouvoir concrétiser le gameplay.

Après les changements de gameplay, la plupart des modifications visaient à améliorer le code ou était des ajouts mineurs. La seule exception étant l'ajout de l'interface Boss milieu février qui permet une plus grande diversité dans ceci.

## Etat du projet
Le jeu est presque terminé, il lui manque quelques éléments:
- la réparation des bugs,
- l'implémentation d'une interface similaire à celle des boss pour les cartes et les items,
- L'ajout de nouvelles cartes et de nouveaux items (les [discussions Github](https://github.com/Lecodeurenretard/Trophee-NSI/discussions) contiennent quleques idées),
- L'ajout d'un tutoriel et d'une histoire.

### approches mises en œuvre pour vérifier l’absence de bugs
Beaucoups de playtests.

### difficultés rencontrées et solutions apportées.
La codebase est tellement grande qu'il a fallu utiliser des IA (Claude) pour le débug.

## Ouverture
### idées d'amélioration du projet
Elements pour casser la routine du RPG car le jeu est ennuyeux si l'on regarde au delà du coté technique.

### analyse critique

### compétences personnelles développées.
#### Pour Nils
Avant les trophées, je n'avais jamais eu de projet en Python, ce projet m'a permis d'apprendre Python au dela de la syntaxe que l'on apprend (utilisation des dataclasses, des générateurs, plusieurs moyens de tirer des choses au hasard, gestions des modules).  
J'ai aussi vu des concepts propre au jeux vidéos (horloge interne (je n'avais jusqu'ici utilisé que le delta timing), courbes d'animations).

### démarche d'inclusion.
