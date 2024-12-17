import random

class SudokuSolver:
    @staticmethod
    def valide(grille):
        # Valeurs permises dans une grille
        autorisees = range(1, 10)

        # Test des lignes
        for line in grille:
            if not len(set(line)) == 9:
                return False

        # Test des colonnes
        for i in range(9):
            column = [grille[j][i] for j in range(9)]
            if not len(set(column)) == 9:
                return False

        # On teste les sous-grilles 3x3
        for y0 in [0, 3, 6]:
            for x0 in [0, 3, 6]:
                subgrid = []
                for i in range(0, 3):
                    for j in range(0, 3):
                        if grille[y0+i][x0+j] in subgrid or grille[y0+i][x0+j] not in autorisees:
                            return False
                        subgrid.append(grille[y0+i][x0+j])

        return True

    @staticmethod
    def n_valide(y, x, n, grid):
        # Détermine si un nombre n peut être mis sur une case à la colonne x et à la ligne y
        for x0 in range(len(grid)):
            if grid[y][x0] == n:
                return False

        for y0 in range(len(grid)):
            if grid[y0][x] == n:
                return False

        x0, y0 = (x // 3) * 3, (y // 3) * 3
        for i in range(0, 3):
            for j in range(0, 3):
                if grid[y0+i][x0+j] == n:
                    return False
        return True

    def genere(self, grid):
        if self.valide(grid):
            return True

        for y in range(9):
            for x in range(9):
                if grid[y][x] == 0:
                    r = list(range(1, 10))
                    random.shuffle(r)
                    for n in r:
                        if self.n_valide(y, x, n, grid):
                            grid[y][x] = n
                            if self.genere(grid):
                                return True
                            grid[y][x] = 0
                    return False

    @staticmethod
    def affiche(grille):
        horizontal_sep = "─" * 7
        middle_sep = "├" + "┼".join([horizontal_sep]*3) + "┤"
        top_border = "┌" + "┬".join([horizontal_sep]*3) + "┐"
        bottom_border = "└" + "┴".join([horizontal_sep]*3) + "┘"
        
        print(top_border)
        
        for i in range(9):
            row = ""
            for j in range(9):
                val = str(grille[i][j]) if grille[i][j] != 0 else " "
                if j % 3 == 0:
                    row += "│ "
                row += val + " "
            row += "│"
            print(row)
            
            if i % 3 == 2 and i != 8:
                print(middle_sep)
        
        print(bottom_border)
        print()

    @staticmethod
    def sauvegarde(grid, fichier):
        with open(fichier, 'w') as f:
            for line in grid:
                f.write(";".join(map(str, line)) + "\n")