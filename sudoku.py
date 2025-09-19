import tkinter as tk
from tkinter import messagebox

class SudokuSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.grid = [[0] * 9 for _ in range(9)]
        self.entries = [[None] * 9 for _ in range(9)]
        self.create_grid()
        self.create_buttons()

    def create_grid(self):
        canvas = tk.Canvas(self.root, width=450, height=450)
        canvas.grid(row=0, column=0, columnspan=9)

        # Draw main boundary
        for i in range(0, 451, 150):  # Main grid lines (thicker)
            canvas.create_line(i, 0, i, 450, width=3)
            canvas.create_line(0, i, 450, i, width=3)

        # Draw subgrid boundaries
        for i in range(50, 451, 50):  # Subgrid lines (less thick)
            if i % 150 != 0:  # Avoid overlapping with main grid lines
                canvas.create_line(i, 0, i, 450, width=1.5)
                canvas.create_line(0, i, 450, i, width=1.5)

        # Create entry widgets
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(self.root, width=2, font=('Arial', 18), justify='center', fg='black')
                entry_window = canvas.create_window(25 + col * 50, 25 + row * 50, window=entry)
                self.entries[row][col] = entry

    def create_buttons(self):
        solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        solve_button.grid(row=10, column=3, columnspan=2, pady=10)

        clear_button = tk.Button(self.root, text="Clear", command=self.clear)
        clear_button.grid(row=10, column=5, columnspan=2, pady=10)

    def get_grid(self):
        for row in range(9):
            for col in range(9):
                val = self.entries[row][col].get()
                self.grid[row][col] = int(val) if val.isdigit() else 0

    def set_grid(self):
        for row in range(9):
            for col in range(9):
                if self.entries[row][col].get() == '':
                    self.entries[row][col].insert(0, str(self.grid[row][col]))
                    self.entries[row][col].config(fg='blue')  # Solved numbers in blue

    def is_valid_move(self, row, col, num):
        if num in self.grid[row]:
            return False
        if num in (self.grid[i][col] for i in range(9)):
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.grid[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve_sudoku(self):
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid_move(row, col, num):
                            self.grid[row][col] = num
                            if self.solve_sudoku():
                                return True
                            self.grid[row][col] = 0
                    return False
        return True

    def solve(self):
        self.get_grid()
        if self.solve_sudoku():
            self.set_grid()
            messagebox.showinfo("Sudoku Solver", "Sudoku solved successfully!")
        else:
            messagebox.showwarning("Sudoku Solver", "No solution exists for the provided Sudoku puzzle.")

    def clear(self):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
                self.entries[row][col].config(fg='black')  # Reset text color to black

root = tk.Tk()
app = SudokuSolver(root)
root.mainloop()
