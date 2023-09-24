from src.menus import MainMenu


if __name__ == "__main__":
    menu = MainMenu()
    menu.show()


# RythmoSphere/
# ├── main.py                     | Fichier principal du jeu
# ├── config.py                   | Fichier de configuration global
# ├── menus/
# │   ├── __init__.py             | Fichier d'initialisation du répertoire
# │   ├── accueil.py              | Menu d'accueil
# │   ├── paramètres.py           | Menu des paramètres
# │   ├── selection_niveaux.py    | Menu de sélection des niveaux
# ├── src/
# │   ├── __init__.py             | Fichier d'initialisation du répertoire
# │   ├── load_map.py             | Gestionnaire de chargement de cartes
# │   ├── trail.py                | Classe pour les traînées
# │   ├── particle.py             | Classe pour les particules
# ├── game/
# │   ├── __init__.py             | Fichier d'initialisation du répertoire
# │   ├── game.py                 | Classe principale du jeu
# │   ├── ui.py                   | Gestion de l'interface utilisateur
# │   ├── circle.py               | Classe représentant un cercle dans le jeu
# ├── beat_maps/
# │   ├── beat_map_1/
# │   │   ├── map.csv             | Données de la carte
# │   │   ├── config.json         | Fichier de configuration de la carte
# │   │   ├── music.mp3           | Fichier de musique du niveau
# │   ├── beat_map_2/
# │   │   ├── map.csv             | Données de la carte
# │   │   ├── config.json         | Fichier de configuration de la carte
# │   │   ├── music.mp3           | Fichier de musique du niveau
# ├── assets/
# │   ├── images/
# │   │   ├── circles/
# │   │   │   ├── image1.png
# │   │   │   ├── image2.png
# │   │   ├── cursors/
# │   │   │   ├── image1.png
# │   │   │   ├── image2.png
# │   │   ├── trails/
# │   │   │   ├── image1.png
# │   │   │   ├── image2.png
# │   │   ├── buttons/
# │   │   │   ├── image1.png
# │   │   │   ├── image2.png
# │   ├── fonts/
# │   │   ├── font1.ttf
# │   │   ├── font2.ttf
# │   ├── sounds/
# │   │   ├── effects/
# │   │   │   ├── sound1.wav
# │   │   │   ├── sound2.wav
# │   │   ├── musics/
# │   │   │   ├── sound1.wav
# │   │   │   ├── sound2.wav
