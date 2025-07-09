# Apprendre Git

## Git c'est quoi?  
C'est un outil pour pouvoir archiver un projet; de cet outil ont évolué Github et Gitlab qui font la même chose mais en ligne ce qui permet à tout le monde d'avoir une vesion à jour du projet.

## Les différents git
En informatique, on a souvent la distinction entre GUI et CLI: le premier veut dire _Graphical User Interface_, le deuxième veut dire _Command Line Interface_, leurs noms parlent pour eux-même.  
Pour Git on peut utiliser 4 options:
+ Git CLI: Le git de base, celui qui sera utilisé par la suite
+ Git GUI: Une interface graphique de git, je ne l'ai pas beaucoup utilisé mais c'est plus confus que git CLI d'après moi.
+ Github GUI: Une interface graphique faite par les devs de Github (Microsoft), si vous voulez une bonne interface graphique c'est ici qu'il faut aller.
+ Git sur VS code (nécessite Git CLI): Il existe des extentions à VS code qui permettent de faire des commandes basique d'un clic. Pour une extention dédié téléchargez aussi GitLens.

## Installer Git (CLI)
Pour installer git, il faut aller prendre l'installeur sur le [site officiel](https://git-scm.com/downloads), vous téléchargez la version compatible avec votre système d'exploitation et éxécutez l'installeur. Plusieurs questions seront posées mais vous pourrez toujours changer les choix après intallation. Assurez vous de séléctionner sur l'option demandant d'afficher "open git CLI here".

Ensuite il faut configurer git avec ces commandes:
```bash
git config --global user.name "<votre nom>"		# sert pour l'authentification
git config --global user.email "<votre mail>"	# sert aussi pour l'authentification
git config --global pull.rebase false	# sert pour les merge conflicts
```

## Utiliser Git
### Le terminal
#### Le principe de la commande
C'est le truc que les hackers utilisent pour hacker dans les films. Vous pouvez ouvrir le votre en appuyant sur windows puis tapez cmd. Souvent on utilise deux mot pour le désigner: _terminal_ et _console_, c'est deux choses différentes mais nous allons utiliser les deux pour désigner le logiciel dans lequel on tape les commandes.

Une commandes est composée de 2 éléments:
- Le nom de la commande (parfois appelé _verbe_);
- Les arguments/paramètres de la commande, peuvent être composés:
	+ du nom du paramètre (commence par un ou deux tiret `-`)
	+ de la valeur de l'argument

exemples:
```bash
echo "Bonjour"		# écrit "Bonjour" à l'écran
ls -a mon-fichier	# Teste si "mon-fichier" existe
rm -r mon-dossier	# Supprime définitivement "mon-dossier" et son contenu
gcc --help		# affiche l'aide de gcc
```
Ces commandes ne devraient pas marcher sur la console Windows car ils aiment être spéciaux et ne pas faire comme Linux et MacOS.

#### Ouvrir le terminal git
Comme souligné précedemment, Windows n'aime pas avoir les même commandes que tous le monde, il faut donc faire une étape suppémentaire pour utiliser git. Il y a deux choix: soit vous utilisez WSL (compliqué pour un débutant), soit vous utilisez le terminal git; pour cela dans l'explorateur de fichier faites click droit et _"open git CLI here"_.

#### Commandes du terminal git
La console git prend ses commandes de Linux si jamais vous voulez une liste.

Les chemins de fichiers fonctionnent de la même façon que sur Python.

- **`cd <dossier>`**: Se déplace jusqu'au dossier.
- **`ls`**: Affiche les fichiers à l'emplacement de la console (équivalent à `ls .`).
- **`ls <dossier>`**: Affiche les fichiers à contenus dans le dossier.
- **`rm <fichier>`**: Efface définitivement (pas de corbeille) un fichier.
- **`rm -r <dossier>`**: Efface définitivement (pas de corbeille) le contenu d'un dossier.


### Termes semi-techniques
Quand on utilise git, il y a certains termes qui sont compliqués:
+ **l'index**: Une sauvegarde temporaire et locale des fichiers
+ **un commit**: Une sauvegarde permanente des fichiers.
+ **un repo(_sitory_)**: Une sauvegarde en ligne dont tous le monde à accès (sur Github).

### Commandes principales
Sur à chaque nouveau repo github, il y a ce guide pour pouvoir commencer tranquillement:
> push an existing repository from the command line
> 
> ```bash
> git remote add origin https://github.com/Lecodeurenretard/Trophee-NSI.git
> git branch -M master
> git push -u origin master
> ```

J'aivais aussi posté une liste des commandes usuelles de git sur l'ancien serveur discord:
```bash
git add .   # ajoute tous les fichiers à l'index
git add "<fichier>" # ajoute un fichier spécifique à l'index 
git status # affiche l'état de l'index

git commit -m "<message>" # commit (enregistre les fichiers de l'index et les y enlèvent)
git push <nom> # Envoie les commits sur le repo
git remote add origin "<url>" # ajoute le repo github avec comme nom "origin"
```
(notez que les guillemets sont facultatifs s'il n'y a pas d'espace)

### Gitignore
Des fois on a pas envie d'inclure des fichiers dans le commit, c'est exactement le but du fichier [.gitignore](../.gitignore) qui inclue tous les fichiers qu'il ne faut pas inclure dans le commit (ils n'apparaitrons même pas comme "untracked" avec `git status`).

### Exemples
Commit toutes les modifications depuis le dernier commit:
```bash
git add .	
# git add * peut aussi marcher mais exclus les fichers cachés

git status	# On s'assure que tous les fichiers y sont
# Sinon on réutilise git add sur le fichier

git commit -m "J'ai modifié X"
```

Se remettre à jour sur github:
```bash
git pull
```