import tkinter as tk
from PIL import Image, ImageTk

class Window:

    def __init__(self, fullscreen=False):
        self.root = tk.Tk()
        self.fullscreen = fullscreen
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.bg_image = None
        self.setup_window()
        self.create_grid()

    def setup_window(self):
        # Set window size
        if self.fullscreen:
            self.root.attributes("-fullscreen", True)

            # Bind the Escape key to exit full-screen
            self.root.bind("<Return>", self.exit_fullscreen)

        self.root.bind('<Escape>', self.close_window)

        self.root.geometry(f"{self.width}x{self.height}")
        self.root.title("Flatland")
        self.root.configure(bg="#000000")

    def exit_fullscreen(self, event=None):
        # Exit full-screen mode
        self.root.attributes("-fullscreen", False)

    def close_window(self, event=None):
        self.root.quit()  # Close the Tkinter window

    def run(self):
        self.root.mainloop()

    def create_grid(self):
        # Create a frame for the smaller grid area
        width = self.width // 2
        height = self.height - 50

        frame = tk.Frame(self.root, width=height, height=height)
        frame.grid(row=0, column=0, padx=10, pady=10)

        # Load the image using PIL
        image = Image.open("../png/env_001--4_2.png")
        img_width, img_height = image.size
        crop_amount = 4
        image = image.crop((0, 0, img_width-crop_amount, img_height - crop_amount))
        image = image.resize((height, height))
        self.bg_image = ImageTk.PhotoImage(image)

        # Create a Label to hold the background image and add it to the frame
        bg_label = tk.Label(frame, image=self.bg_image)
        bg_label.place(relwidth=1, relheight=1)  # Make the image fill the frame

        # cells_per_row = 40
        # cells_per_column = 40
        # cell_size = height // cells_per_column
        #
        # # Create a grid inside the frame
        # for row in range(cells_per_row):
        #     for col in range(cells_per_column):
        #         empty_cell = tk.Frame(frame, borderwidth=1, relief="solid",
        #                               width=cell_size,height=cell_size)
        #         empty_cell.grid(row=row, column=col)


if __name__ == "__main__":
    test = Window(fullscreen=True)
    test.run()
