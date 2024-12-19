import cv2
import numpy as np

class ImageProcessor:
    @staticmethod
    def adjust_exposure(image, target_brightness=128):
        # Calculer la luminosité moyenne actuelle de l'image
        mean_brightness = ImageProcessor.calculate_mean_brightness(image)
        
        # Déterminer la valeur gamma pour ajuster l'exposition
        gamma = ImageProcessor.determine_gamma(mean_brightness, target_brightness)
        inv_gamma = 1.0 / gamma
        
        # Créer une table de correspondance pour ajuster la luminosité
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        return cv2.LUT(image, table)

    @staticmethod
    def calculate_mean_brightness(image):
        # Convertir l'image en niveaux de gris pour calculer la luminosité moyenne
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        mean_brightness = np.mean(gray)
        return mean_brightness

    @staticmethod
    def determine_gamma(mean_brightness, target_brightness=128):
        # Si la luminosité moyenne est élevée, ne pas ajuster (gamma = 1.0)
        if mean_brightness >= 165:
            return 1.0
        else:
            # Calculer le gamma pour atteindre la luminosité cible
            gamma = target_brightness / mean_brightness
            return gamma
    
    @staticmethod
    def preprocess_image(img, ksize=5):
        # Appliquer un flou médian pour réduire le bruit
        blurred = cv2.medianBlur(img, ksize)
        
        # Convertir l'image floutée en niveaux de gris
        gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
        
        # Appliquer un seuillage adaptatif pour obtenir une image binaire
        adaptive_thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        # Utiliser des transformations morphologiques pour nettoyer l'image binaire
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_OPEN, kernel)
        morph = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        
        # Détecter les contours avec l'algorithme de Canny
        edges = cv2.Canny(morph, 50, 100)
        
        return edges

    @staticmethod
    def crop_image(image, crop_percentage=0.11):
        # Calculer les dimensions pour rognage
        height, width = image.shape[:2]
        crop_height = int(height * crop_percentage)
        crop_width = int(width * crop_percentage)
        
        # Rogner l'image en fonction des pourcentages calculés
        cropped_image = image[crop_height:height - crop_height, crop_width:width - crop_width]
        return cropped_image

    @staticmethod
    def is_mostly_white(image, threshold=88):
        # Vérifier que l'image est en niveaux de gris
        if len(image.shape) != 2:
            raise ValueError("L'image doit être en niveaux de gris")
        
        # Calculer le pourcentage de pixels blancs
        total_pixels = image.size
        white_pixels = np.sum(image == 255)
        white_percentage = (white_pixels / total_pixels) * 100
        
        # Déterminer si l'image est majoritairement blanche
        return white_percentage > threshold

    @staticmethod
    def binary(image):
        # Convertir l'image en niveaux de gris
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Appliquer un seuillage pour obtenir une image binaire
        _, binary_image = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        return binary_image