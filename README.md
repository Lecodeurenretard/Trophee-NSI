# README

Ce fichier est un [fichier markdown](https://www.markdownguide.org/basic-syntax/) ([guide markdown](https://www.markdownguide.org/getting-started/)) qui explique le fonctionnement du projet, il devrait être automatiquement mis en forme sur Github (sinon il existe pleins d'extentions sur VS code).

## Rester ordonné
L'architecture du projet suit celui qu'il faut faire pour les trophées de NSI ([source](https://trophees-nsi.fr/participation)):
- [sources](sources/): Tout le code Python qui sera éxécuté.
- [docs](docs/): Les documentations du projets.
- [data](data/): Toutes les données qui seront lues ou écrites par le projets.
	+ [img](data/img/): Les images dans le jeu.
	+ [save](data/save/): Les données de sauvegarde. Ce n'est pas forcément de la suvegarde classique, même les données temporaires y vont.
	+ [etc](data/etc/): Les données temporaires qui ne rentre pas dans les catégories ci-dessus va dans ce fichier.

## Utiliser Github
J'ai rédigé [un fichier](Git.md) pour ça.

## Des notions de Python
Des notions Python que l'on a pas vu en NSI: [Python.md](Python.md)

## Buts
Le fichier est [requirements.txt](requirements.txt).
Voyez ce qui doit être fait à plus court terme dans le projet Github.