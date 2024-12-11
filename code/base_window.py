import tkinter as tk
from PIL import Image, ImageTk

class BaseWindow:

    def __init__(self):
        self.root = tk.Tk()
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.bg_image = None
        self.setup_window()
        self.create_grid()
        self.create_exit_button()
        self.create_zoom_buttons()

    def setup_window(self):
        self.root.attributes("-fullscreen", True)
        self.root.bind('<Escape>', self.close_window)

        self.root.geometry(f"{self.width}x{self.height}")
        self.root.title("Flatland")
        self.root.configure(bg="#000000")

    def close_window(self, event=None):
        self.root.quit()  # Close the Tkinter window

    def run(self):
        self.root.mainloop()

    def create_grid(self):
        width = self.width // 2
        height = self.height
        canvas = tk.Canvas(self.root, width=height, height=height)
        canvas.grid(row=0, column=0)

        cells_per_row = 40
        cells_per_column = 40
        cell_size = height // cells_per_column

        # Create a grid of cells inside the canvas
        for row in range(cells_per_row):
            for col in range(cells_per_column):
                canvas.create_rectangle(col * cell_size, row * cell_size,
                                        (col + 1) * cell_size, (row + 1) * cell_size,
                                        outline="black", width=1)  # Grid lines

    def create_exit_button(self):
        close = tk.Button(self.root, command=self.close_window, text="X",
                          font=("Arial", 20, "bold"),
                          fg="#FF0000", bg="#000000", bd=0,
                          width=2, height=1)
        close.place(x=self.width-45, y=0)

    def create_zoom_buttons(self):
        zoom_in = tk.Button(self.root, command=self.zoom_in_grid,
                            text="+", font=("Arial", 20, "bold"),
                            fg="#00FF00", bg="#000000", bd=0,
                            width=2, height=1)
        zoom_in.place(x=self.height + 7, y=self.height - 120)

        zoom_out = tk.Button(self.root, command=self.zoom_out_grid,
                             text="-", font=("Arial", 20, "bold"),
                             fg="#00FF00", bg="#000000", bd=0,
                             width=2, height=1)
        zoom_out.place(x=self.height + 7, y=self.height - 60)

    def zoom_in_grid(self):
        print("ZOOM IN")
        return

    def zoom_out_grid(self):
        print("ZOOM OUT")
        return


if __name__ == "__main__":
    test = BaseWindow()
    test.run()
