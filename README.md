# README

Ce fichier est un [fichier markdown](https://www.markdownguide.org/basic-syntax/) ([guide markdown](https://www.markdownguide.org/getting-started/)) qui explique le fonctionnement du projet, il devrait être automatiquement mis en forme sur Github (sinon il existe pleins d'extentions sur VS code).

## Configuration minimum
+ [Python 3.10](https://www.python.org/downloads/release/python-31018/) ou plus récent
+ [pygame 2.6](https://www.pygame.org/news) ou plus récent

Pas de configuration minimum pour les composants du PC à moins que ce soit littéralement une patate.

## Télécharger la dernière version du jeu
Dans la section Code, en haut à droite des fichier, vous pouvez télécharger le .zip.  
Pour avoir un projet (repo) Git de configuré exécutez la commande suivante dans la console Git.
```bash
git clone "https://github.com/Lecodeurenretard/Trophee-NSI.git"
```

## Rester ordonné
L'architecture du projet suit celui qu'il faut faire pour les trophées de NSI ([page des trophées](https://trophees-nsi.fr/participation)):
- [sources](sources/): Tout le code Python qui sera éxécuté. [Description ficher par fichier](doc/files.md)
- [docs](docs/): Les documentations dans le dossier [doc](doc/).
- [data](data/): Toutes les données qui seront lues ou écrites par le projets.
	+ [img](data/img/): Les images dans le jeu.
	+ [save](data/save/): Les données de sauvegarde.
	+ [etc](data/etc/): Les données temporaires qui ne rentrent pas dans les catégories ci-dessus va dans ce fichier.

_note: Certains dossiers peuvent ne pas apparaitre sur Github, c'est parce que Git n'envoie que les dossiers contenant des fichiers. Les répertoires vides ne serons donc pas envoyés._

## Perdu?
Si le certains éléments du code ou de Git vous pertubent, j'ai rédigé des fichiers pouvant vous aider sur [le wiki](https://github.com/Lecodeurenretard/Trophee-NSI/wiki) et si vous ne comprenez toujours pas, n'oubliez pas que Google est votre meilleurs ami.

## Buts
Le fichier est [requirements.txt](requirements.txt).
Voyez ce qui doit être fait à plus court terme dans le [projet Github](https://github.com/users/Lecodeurenretard/projects/5/).

## Les modes d'utilisateurs
Il y a deux modes pour deux types d'utilisateurs: le mode normal (par défaut) et le mode débug. Le mode débug est comme le mode normal mais à accès aux paramètres de triche.

Les touches sont dans le [README](sources/README.md) du répertoire [sources](sources/).