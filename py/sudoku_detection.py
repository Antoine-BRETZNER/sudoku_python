import cv2
import numpy as np
from image_processing import ImageProcessor

class SudokuDetector:
    @staticmethod
    def find_largest_contour(edges):
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        largest_contour = max(contours, key=cv2.contourArea)
        return largest_contour

    @staticmethod
    def warp_perspective(img, contour):
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) == 4:
            points = approx.reshape(4, 2)
            rect = np.zeros((4, 2), dtype="float32")
            s = points.sum(axis=1)
            rect[0] = points[np.argmin(s)]
            rect[2] = points[np.argmax(s)]
            diff = np.diff(points, axis=1)
            rect[1] = points[np.argmin(diff)]
            rect[3] = points[np.argmax(diff)]
            (tl, tr, br, bl) = rect
            width = max(np.linalg.norm(br - bl), np.linalg.norm(tr - tl))
            height = max(np.linalg.norm(tr - br), np.linalg.norm(tl - bl))
            dst = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype="float32")
            M = cv2.getPerspectiveTransform(rect, dst)
            warped = cv2.warpPerspective(img, M, (int(width), int(height)))
            return warped
        else:
            raise Exception("La grille n'a pas été détectée correctement.")

    @staticmethod
    def extract_cells(warped, grid_size=9):
        cells = []
        cell_height, cell_width = warped.shape[0] // grid_size, warped.shape[1] // grid_size
        for i in range(grid_size):
            row = []
            for j in range(grid_size):
                cell = warped[i * cell_height:(i + 1) * cell_height, j * cell_width:(j + 1) * cell_width]
                row.append(cell)
            cells.append(row)
        return cells