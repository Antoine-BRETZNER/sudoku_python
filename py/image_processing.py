import cv2
import numpy as np

class ImageProcessor:
    @staticmethod
    def adjust_exposure(image, target_brightness=128):
        mean_brightness = ImageProcessor.calculate_mean_brightness(image)
        gamma = ImageProcessor.determine_gamma(mean_brightness, target_brightness)
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        return cv2.LUT(image, table)

    @staticmethod
    def calculate_mean_brightness(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        mean_brightness = np.mean(gray)
        return mean_brightness

    @staticmethod
    def determine_gamma(mean_brightness, target_brightness=128):
        if mean_brightness >= 165:
            return 1.0
        else:
            gamma = target_brightness / mean_brightness
            return gamma
    
    @staticmethod
    def preprocess_image(img, ksize=5):
        """
        Pré-traite une image en appliquant un flou médian, un seuillage adaptatif,
        des transformations morphologiques et une détection des contours.

        :param img: Image à pré-traiter.
        :param ksize: Taille du noyau pour le flou médian (par défaut 5).
        :return: Image avec les contours détectés.
        """
        # Flou médian pour réduire le bruit tout en préservant les bords
        blurred = cv2.medianBlur(img, ksize)
        
        # Convertir en niveaux de gris pour le seuillage
        gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
        
        # Seuillage adaptatif pour gérer les variations d'éclairage
        adaptive_thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        # Transformations morphologiques pour nettoyer l'image
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_OPEN, kernel)
        morph = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        
        # Détection des contours avec l'algorithme de Canny
        edges = cv2.Canny(morph, 50, 100)
        
        return edges


    @staticmethod
    def crop_image(image, crop_percentage=0.11):
        if image is None:
            print("Erreur de chargement de l'image")
            return None

        height, width = image.shape[:2]
        crop_height = int(height * crop_percentage)
        crop_width = int(width * crop_percentage)
        cropped_image = image[crop_height:height - crop_height, crop_width:width - crop_width]
        return cropped_image

    @staticmethod
    def is_mostly_white(image, threshold=88):
        if len(image.shape) != 2:
            raise ValueError("L'image doit être en niveaux de gris")
        total_pixels = image.size
        white_pixels = np.sum(image == 255)
        white_percentage = (white_pixels / total_pixels) * 100
        return white_percentage > threshold

    @staticmethod
    def binary(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        return binary_image

    @staticmethod
    def remove_grid_lines(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        _, binary_image_inv = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        blurred_mask = cv2.GaussianBlur(binary_image_inv, (5, 5), 0)
        mask_edges = cv2.Canny(blurred_mask, 1, 255, apertureSize=3)
        lines = cv2.HoughLines(mask_edges, 1, np.pi / 180, 130)
        filtering_mask = np.zeros_like(binary_image_inv)

        if lines is not None:
            for rho, theta in lines[:, 0]:
                a, b = np.cos(theta), np.sin(theta)
                x0, y0 = a * rho, b * rho
                x1, y1 = int(x0 + 1000 * (-b)), int(y0 + 1000 * (a))
                x2, y2 = int(x0 - 1000 * (-b)), int(y0 - 1000 * (a))
                cv2.line(filtering_mask, (x1, y1), (x2, y2), (255, 255, 255), 2)

        kernel = np.ones((5, 5), np.uint8)
        filtering_mask = cv2.dilate(filtering_mask, kernel, iterations=2)
        final_mask = cv2.subtract(binary_image_inv, filtering_mask)
        final_image = cv2.cvtColor(final_mask, cv2.COLOR_GRAY2BGR)
        return final_image
