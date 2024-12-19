import cv2
import numpy as np
from image_processing import ImageProcessor

class SudokuDetector:
    @staticmethod
    def find_largest_contour(edges):
        # Trouver tous les contours dans l'image des arêtes
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Sélectionner le plus grand contour basé sur l'aire
        largest_contour = max(contours, key=cv2.contourArea)
        return largest_contour

    @staticmethod
    def warp_perspective(img, contour):
        # Approximé le contour pour obtenir un quadrilatère
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # Si le contour approximé a 4 points, procéder à la transformation de perspective
        if len(approx) == 4:
            points = approx.reshape(4, 2)
            rect = np.zeros((4, 2), dtype="float32")

            # Ordre des points : (top-left, top-right, bottom-right, bottom-left)
            s = points.sum(axis=1)
            rect[0] = points[np.argmin(s)]
            rect[2] = points[np.argmax(s)]
            diff = np.diff(points, axis=1)
            rect[1] = points[np.argmin(diff)]
            rect[3] = points[np.argmax(diff)]
            (tl, tr, br, bl) = rect

            # Calculer la largeur et la hauteur de l'image transformée
            width = max(np.linalg.norm(br - bl), np.linalg.norm(tr - tl))
            height = max(np.linalg.norm(tr - br), np.linalg.norm(tl - bl))

            # Créer une matrice pour la transformation de perspective
            dst = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype="float32")
            M = cv2.getPerspectiveTransform(rect, dst)

            # Appliquer la transformation de perspective
            warped = cv2.warpPerspective(img, M, (int(width), int(height)))
            return warped
        else:
            raise Exception("La grille n'a pas été détectée correctement.")

    @staticmethod
    def extract_cells(warped, grid_size=9):
        cells = []

        # Calculer la hauteur et la largeur de chaque cellule
        cell_height, cell_width = warped.shape[0] // grid_size, warped.shape[1] // grid_size

        # Parcourir chaque cellule dans la grille
        for i in range(grid_size):
            row = []
            for j in range(grid_size):
                cell = warped[i * cell_height:(i + 1) * cell_height, j * cell_width:(j + 1) * cell_width]
                row.append(cell)
            cells.append(row)
        
        return cells
