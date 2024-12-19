import tkinter as tk
from tkinter import filedialog
import cv2
import sys
import os
from ultralytics import YOLO

# Ajouter le chemin du répertoire 'py' au sys.path pour importer les modules locaux
sys.path.append(os.path.join(os.path.dirname(__file__), 'py'))

from solve import SudokuSolver
from image_processing import ImageProcessor
from sudoku_detection import SudokuDetector
from utils import plot_image

class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        
        # Création du canevas pour afficher la grille de Sudoku
        self.canvas = tk.Canvas(root, width=450, height=450, bg='white')
        self.canvas.grid(row=0, column=0, columnspan=3)

        # Boutons pour charger, résoudre et sauvegarder le Sudoku
        self.load_button = tk.Button(root, text="Load Sudoku", command=self.load_sudoku)
        self.load_button.grid(row=1, column=0)

        self.solve_button = tk.Button(root, text="Solve Sudoku", command=self.solve_sudoku)
        self.solve_button.grid(row=1, column=1)

        self.save_button = tk.Button(root, text="Save Sudoku", command=self.save_sudoku)
        self.save_button.grid(row=1, column=2)

        # Initialiser les variables pour l'image et les grilles détectées
        self.image = None
        self.detected_grid = None
        self.original_grid = None  # Pour stocker la grille détectée initiale

    def load_sudoku(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            # Charger et ajuster l'exposition de l'image
            self.image = cv2.imread(file_path)
            self.image = ImageProcessor.adjust_exposure(self.image, 260)

            # Pré-traiter l'image et détecter la grille
            edges = ImageProcessor.preprocess_image(self.image)
            largest_contour = SudokuDetector.find_largest_contour(edges)
            binary_image = ImageProcessor.binary(self.image)
            warped = SudokuDetector.warp_perspective(binary_image, largest_contour)

            # Extraire les cellules de la grille
            cells = SudokuDetector.extract_cells(warped)
            self.detected_grid = [[0 for _ in range(9)] for _ in range(9)]
            self.original_grid = [[0 for _ in range(9)] for _ in range(9)]
            for i in range(9):
                for j in range(9):
                    cells_crop = ImageProcessor.crop_image(cells[i][j])
                    if ImageProcessor.is_mostly_white(cells_crop):
                        self.detected_grid[i][j] = 0
                        self.original_grid[i][j] = 0
                    else:
                        # Convertir la cellule en RGB pour le modèle YOLO
                        cells_rgb = cv2.cvtColor(cells_crop, cv2.COLOR_GRAY2BGR)
                        results = YOLO('models/yolov8n_number.pt')(cells_rgb)
                        for result in results:
                            if result.boxes:
                                for box in result.boxes:
                                    detected_class = int(box.cls.item())
                                    self.detected_grid[i][j] = detected_class
                                    self.original_grid[i][j] = detected_class

            # Afficher la grille détectée
            self.display_grid(self.detected_grid)

    def solve_sudoku(self):
        if self.detected_grid:
            solver = SudokuSolver()
            solver.genere(self.detected_grid)
            # Afficher la grille résolue
            self.display_grid(self.detected_grid, solved=True)

    def save_sudoku(self):
        if self.detected_grid:
            # Ouvrir une boîte de dialogue pour choisir l'emplacement de sauvegarde
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                solver = SudokuSolver()
                solver.sauvegarde(self.detected_grid, file_path)

    def display_grid(self, grid, solved=False):
        self.canvas.delete("all")
        cell_size = 450 // 9
        for i in range(9):
            for j in range(9):
                x1 = j * cell_size
                y1 = i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                self.canvas.create_rectangle(x1, y1, x2, y2)
                
                # Épaissir les lignes des sous-grilles 3x3
                if i % 3 == 0 and i != 0:
                    self.canvas.create_line(x1, y1, x2, y1, width=2)
                if j % 3 == 0 and j != 0:
                    self.canvas.create_line(x1, y1, x1, y2, width=2)
                
                if grid[i][j] != 0:
                    # Afficher les chiffres en bleu si résolus, en noir sinon
                    color = 'blue' if solved and self.original_grid[i][j] == 0 else 'black'
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(grid[i][j]), fill=color, font=("Helvetica", 18))

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()