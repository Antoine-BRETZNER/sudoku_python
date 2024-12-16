import sys
import os
import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO

sys.path.append(os.path.join(os.path.dirname(__file__), 'py'))

from image_processing import ImageProcessor
from sudoku_detection import SudokuDetector
from utils import plot_image
from solve import SudokuSolver

if __name__ == "__main__":
    # Vérification et traitement des arguments de la ligne de commande
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

    # Vérifiez s'il y a un nombre correct d'arguments
    if len(args) < 1 or len(args) > 2 or (len(opts) > 0 and opts[0] != "-g"):
        print(f"Usage: {sys.argv[0]} path_to_sudoku_image.jpg [-g path_to_sudoku_csv.csv]")
        sys.exit(1)

    image_path = args[0]
    save_path = None

    # Si l'option -g est utilisée, vérifiez qu'un chemin de sauvegarde est fourni
    if "-g" in opts:
        save_index = sys.argv.index("-g") + 1
        if save_index < len(sys.argv):
            save_path = sys.argv[save_index]
        else:
            print(f"Usage: {sys.argv[0]} path_to_sudoku_image.jpg [-g path_to_sudoku_csv.csv]")
            sys.exit(1)

    # Chargement et pré-traitement de l'image
    image = cv2.imread(image_path)
    image = ImageProcessor.adjust_exposure(image, 260)

    edges = ImageProcessor.preprocess_image(image)
    largest_contour = SudokuDetector.find_largest_contour(edges)
    binary_image = ImageProcessor.binary(image)
    warped = SudokuDetector.warp_perspective(binary_image, largest_contour)

    cells = SudokuDetector.extract_cells(warped)

    cells_crop = [[None for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            cells_crop[i][j] = ImageProcessor.crop_image(cells[i][j])

    model = YOLO('models/yolov8n_number.pt')
    detected_grid = [[0 for _ in range(9)] for _ in range(9)]

    for i in range(9):
        for j in range(9):
            if ImageProcessor.is_mostly_white(cells_crop[i][j]):
                detected_grid[i][j] = 0
                continue
            
            cells_rgb = cv2.cvtColor(cells_crop[i][j], cv2.COLOR_GRAY2BGR)
            results = model(cells_rgb)

            for result in results:
                if result.boxes:
                    for box in result.boxes:
                        detected_class = int(box.cls.item())
                        detected_grid[i][j] = detected_class

    print("La grille ci-dessous a été chargée :")
    solver = SudokuSolver()
    solver.affiche(detected_grid)

    if solver.genere(detected_grid):
        print("La grille résolue est :")
        solver.affiche(detected_grid)
    else:
        print("Cette grille n'est pas résolvable !")

    if save_path:
        solver.sauvegarde(detected_grid, save_path)
        print(f"La grille résolue a été sauvegardée dans le fichier {save_path}")