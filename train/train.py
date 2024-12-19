import os
from ultralytics import YOLO

# Variables configurables
data_yaml = os.path.join(os.path.dirname(__file__), 'model.yaml')
model_config = 'yolov8n.pt'  # Configuration du modèle
model_name = 'my_trained_model'  # Nom du modèle entraîné

# Charger le modèle
model = YOLO(model_config)

# Entraîner le modèle
model.train(data=data_yaml, epochs=0, batch=16, imgsz=640)

# Chemin pour sauvegarder le modèle entraîné
save_dir = os.path.join(os.path.dirname(__file__), '../models')
os.makedirs(save_dir, exist_ok=True)

# Sauvegarder le modèle entraîné avec un nom spécifique
model.save(os.path.join(save_dir, model_name + '.pt'))
