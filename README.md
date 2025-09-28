# README

Ce fichier est un [fichier markdown](https://www.markdownguide.org/basic-syntax/) ([guide markdown](https://www.markdownguide.org/getting-started/)) qui explique le fonctionnement du projet, il devrait être automatiquement mis en forme sur Github (sinon il existe pleins d'extentions sur VS code).

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
	+ [save](data/save/): Les données de sauvegarde. Ce n'est pas forcément de la sauvegarde classique, toutes les données de jeu y vont (ex: transférer l'inventaire d'un ficher Python à un autre).
	+ [etc](data/etc/): Les données temporaires qui ne rentrent pas dans les catégories ci-dessus va dans ce fichier.

_note: Certains dossiers peuvent ne pas apparaitre sur Github, c'est parce que Git n'envoie que les dossiers contenant des fichiers. Les répertoires vides ne serons donc pas envoyés._

## Perdu?
Si le certains éléments du code ou de Git vous pertubent, j'ai rédigé des fichiers pouvant vous aider sur [le wiki](https://github.com/Lecodeurenretard/Trophee-NSI/wiki) et si vous ne comprenez toujours pas, n'oubliez pas que Google est votre meilleurs ami.

## Buts
Le fichier est [requirements.txt](requirements.txt).
Voyez ce qui doit être fait à plus court terme dans le [projet Github](https://github.com/users/Lecodeurenretard/projects/5/).

## Les modes d'utilisateurs
Il y a deux modes pour deux types d'utilisateurs:

|               |                     Débug (testeurs/devs)                    | Normal (juste un joueur normal) |
|:--------------|:------------------------------------------------------------:|:-------------------------------:|
| **Affichage** |          Simple (pas de sprites, moins de couleurs)          |      Détaillé, Animations*      |
|  **Actions**  |        Attaquer, pouvoir skip les temps d'attente, choisir si le coup est crit, choisir le monstre, pouvoir choisir le numéro de combat*, obtenir les cheats     |       Attaquer, paramètres basiques        |

\*à faire

Pour activer le mode débug, changez dans le code source le paramètre `mode_debug` dans [Settings.py](sources/Settings.py).

Les touches sont dans le [README](sources/README.md) du répertoire [sources](sources/).