# 🔢 Sudoku Solver

Ce projet propose une solution complète pour la détection et la résolution des grilles de Sudoku à partir d'images. Il est structuré en deux versions : 
- Une version classique (`sudoku.py`) qui fonctionne via le terminal.
- Une version interactive avec une interface graphique (`canva.py`) utilisant Tkinter.

## Fonctionnalités

### Version Classique (`sudoku.py`)

- **Lecture d'images de Sudoku** : Charge une image contenant une grille de Sudoku.
- **Extraction de la grille** : Utilise la vision par ordinateur pour détecter et extraire la grille de Sudoku de l'image.
- **Résolution de la grille** : Résout automatiquement la grille de Sudoku détectée.
- **Affichage dans le terminal** : Affiche la grille originale et la grille résolue directement dans le terminal.
- **Sauvegarde de la grille résolue** (optionnelle) : Permet de sauvegarder la grille résolue dans un fichier CSV.

### Version Interactive (`canva.py`)

- **Interface graphique avec Tkinter** : Propose une interface utilisateur interactive pour charger, résoudre et sauvegarder les grilles de Sudoku.
- **Boutons d'action** : Comprend trois boutons :
  - **Load Sudoku** : Pour charger une image de Sudoku depuis le répertoire.
  - **Solve Sudoku** : Pour résoudre la grille de Sudoku et afficher la solution.
  - **Save Sudoku** : Pour sauvegarder la grille résolue dans un fichier CSV.
- **Affichage amélioré** : Grille de Sudoku avec lignes séparatrices épaisses pour les sous-grilles 3x3 et différenciation des chiffres d'origine et des chiffres résolus par couleur.

## Prérequis

- Python 3.x
- OpenCV
- Matplotlib
- Tkinter
- PIL (Python Imaging Library)
- YOLO (You Only Look Once) pour la détection de chiffres

## Utilisation

### Version Classique (`sudoku.py`)

#### Commande de base :

```sh
python3 sudoku.py path_to_sudoku_image.jpg
```

#### Commande avec sauvegarde :

```sh
python3 sudoku.py path_to_sudoku_image.jpg -g path_to_sudoku_csv.csv
```

### Version Interactive (`canva.py`)

Lancez l'interface graphique avec la commande :

```sh
python3 canva.py
```

### Fonctionnement

1. **Chargement de l'image** :
   - `sudoku.py` : Charge l'image de Sudoku depuis le chemin spécifié.
   - `canva.py` : Utilisez le bouton "Load Sudoku" pour sélectionner et charger une image de Sudoku.

2. **Détection et extraction de la grille** :
   - Utilisation de OpenCV pour détecter les contours et extraire la grille de Sudoku.
   - Utilisation de YOLO pour détecter les chiffres dans chaque cellule de la grille.

3. **Résolution de la grille** :
   - `sudoku.py` : Résolution automatique de la grille et affichage dans le terminal.
   - `canva.py` : Cliquez sur le bouton "Solve Sudoku" pour afficher la grille résolue dans l'interface graphique.

4. **Sauvegarde de la grille résolue** :
   - `sudoku.py` : Utilisez l'option `-g` pour sauvegarder la grille résolue dans un fichier CSV.
   - `canva.py` : Cliquez sur le bouton "Save Sudoku" pour sauvegarder la grille résolue.

## Notes

- Assurez-vous que l'image de Sudoku est bien éclairée et clairement visible pour des résultats optimaux.
- Le modèle YOLO utilisé pour la détection des chiffres doit être entraîné pour reconnaître les chiffres de Sudoku.

## Problèmes rencontées dans cette version du code (16/12/24 21h54) :

- 8 : un 8 en trop
- 13 : deux 1 en moins
- 14 : un 1 en moins
- 16 : six 1 en trop
- 18 : il y a rien qui va
- 19 : mieux qu'avant mais plein de problèmes
- 21 : un 3 devenu un 9 et un 4 en trop

## Sources des Données

### Dataset

Les données utilisées pour entraîner le modèle YOLO pour la détection des chiffres de Sudoku proviennent de plusieurs sources :

- https://github.com/rg1990/cv-sudoku-solver/tree/main/data/digit_images

### Images de `sudoku_images`

Les images contenues dans le dossier `sudoku_images` proviennent des sources suivantes :

- https://github.com/rg1990/cv-sudoku-solver/tree/main/data/sudoku_images