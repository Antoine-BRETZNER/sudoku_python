import cv2
import numpy as np
from ultralytics import YOLO
from sudoku import affiche
import os

# Chemin vers le fichier de configuration et le dossier de données
config_path = 'sudoku_config.yaml'

# Initialiser le modèle YOLO
model = YOLO(config_path).load("yolov8n.pt")

data_path = 'dataset/'

# Entraîner le modèle
model.train(data=data_path, epochs=50, batch=16, imgsz=640)

# Sauvegarder le modèle entraîné s'il n'existe pas déjà
if not os.path.exists('yolov8n_trained.pt'):
    model.save('yolov8n_trained.pt')
else :
    # Charger le modèle entraîné
    model = YOLO('yolov8n_trained.pt')

# Charger l'image du Sudoku
image = cv2.imread('sudoku1.png')

# Effectuer la détection des chiffres dans l'image
results = model.predict(image)

# Extraire les positions et les valeurs des chiffres
chiffres = []
for result in results:
    boxes = result.boxes.xyxy.cpu().numpy()  # Coordonnées des boîtes englobantes
    scores = result.boxes.conf.cpu().numpy()  # Scores de confiance des détections
    classes = result.boxes.cls.cpu().numpy()  # Classes des objets détectés

    for box, score, cls in zip(boxes, scores, classes):
        if score > 0.5:  # Seulement les chiffres avec une probabilité > 0.5
            x1, y1, x2, y2 = box  # Coordonnées de la boîte englobante
            valeur = int(cls)  # Classe détectée (chiffre)
            # Convertir les coordonnées en indices de grille
            row = int(y1 // (image.shape[0] / 9))
            col = int(x1 // (image.shape[1] / 9))
            chiffres.append((row, col, valeur))

# Créer la grille de Sudoku
grille = [[0 for _ in range(9)] for _ in range(9)]
for row, col, valeur in chiffres:
    grille[row][col] = valeur

# Afficher la grille de Sudoku détectée
print("Grille détectée :")
affiche(grille)


# Résoudre la grille de Sudoku
# if genere(grille):
#     print("La grille résolue est :")
#     affiche(grille)
# else:
#     print("Cette grille n'est pas résolvable !")
