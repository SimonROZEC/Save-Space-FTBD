## Présentation

*Save Space FTBD* est un space shooter réalisé en binôme en 2018 dans le cadre d'un cours de Modélisation Mathématique.

Le joueur incarne un pilote de vaisseau spatial devant détruire une menace le plus rapidement possible.

Le jeu se présente sous la forme d'une "course" et inclut un chronomètre ainsi que des indicateurs de segments (temps clé de la run). Si le joueur parvient à détruire le vaisseau ennemi, son temps est enregistré en ligne dans un leaderboard qui s'affiche à la fin de chaque partie.

### Explication de la run
Au début de la partie, le joueur doit commencer par combattre un module de combat du vaisseau ennemi. Lorsque celui-ci est détruit, le joueur doit ensuite traverser un champ d'astéroïdes. Cette phase a une durée définie et ne peut pas être passée, cependant, elle est très importante car elle permet au joueur de récupérer au maximum 3 pièces d'amélioration pour son vaisseau. Chaque pièce procure un bonus qui rendra combat contre le vaisseau ennemi beaucoup plus simple et rapide.


## Développement
Le jeu a dû être réalisé en Python en utilisant la librairie Pygame.

En raison du genre de jeu imposé et du gameplay très simple, notre but a été de rendre notre jeu le plus *juicy* possible en nous concentrant principalement sur les effets visuels et sur la fluidité du gameplay.

Le jeu utilise les packs d'assets suivants :
- [Space Shooter Redux](https://www.kenney.nl/assets/space-shooter-redux)
- [Space Shooter Extension](https://www.kenney.nl/assets/space-shooter-extension)


## Images du jeu

<p float="left">
  <img src="https://github.com/SimonROZEC/Save-Space-FTBD/blob/master/screenshots/intro.png" width="256">
  <img src="https://github.com/SimonROZEC/Save-Space-FTBD/blob/master/screenshots/menu.png" width="256">
</p>

<p float="left">
  <img src="https://github.com/SimonROZEC/Save-Space-FTBD/blob/master/screenshots/preboss-small.gif" width="256">
  <img src="https://github.com/SimonROZEC/Save-Space-FTBD/blob/master/screenshots/asteroids-small.gif" width="256">
  <img src="https://github.com/SimonROZEC/Save-Space-FTBD/blob/master/screenshots/boss-small.gif" width="256">
</p>

<img src="https://github.com/SimonROZEC/Save-Space-FTBD/blob/master/screenshots/leaderboard.png" width="256">


## Installation et exécution:

Le jeu est compatible avec les versions 2 et 3 de python.

Pour commencer, téléchargez ou clonez le dépôt.

Ensuite, les librairies Python à installer pour pouvoir lancer le jeu sont pygame et requests:
```
pip install pygame
pip install requests
```
Pour lancer le jeu, executer le script ./run.sh

