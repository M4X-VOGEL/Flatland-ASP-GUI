import tkinter as tk

class BaseWindow:

    def __init__(self):
        # initialized vars
        self.root = tk.Tk()
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        # None initialized vars
        self.canvas = None

    def run(self):
        self.root.mainloop()

    def close_window(self, event=None):
        self.root.quit()  # Close the window

    def setup_window(self):
        self.root.title("Flatland")
        self.root.configure(bg="#000000")
        self.root.attributes("-fullscreen", True)
        self.root.bind('<Escape>', self.close_window)

    def create_exit_button(self):
        close_button = tk.Button(
            self.root, command=self.close_window,
            text="X", font=("Arial", 20, "bold"),
            fg="#FF0000", bg="#000000", bd=0, width=2, height=1
        )
        close_button.place(x=self.width-45, y=0)

    def create_help_button(self):
        help_button = tk.Button(
            self.root, command=self.open_help_window,
            text="Help", font=("Arial", 20, "bold"),
            fg="#FFFFFF", bg="#000000", bd=0, width=4, height=1
        )
        help_button.place(x=self.height + 10, y=0)

    def create_canvas(self):
        self.canvas = tk.Canvas(self.root, width=self.height, height=self.height)
        self.canvas.place(x=0, y=0)

    def open_help_window(self):
        # Create a new popup window
        popup = tk.Toplevel(self.root, bg="#000000")
        popup.title("Help")
        popup.geometry("500x500")

        # Add a label with text inside the popup
        with open("help_text.txt", "r") as file:
            # TODO: change help text
            help_text = file.read()

        label = tk.Label(
            popup,
            text=help_text,font=("Arial", 20),
            fg="#FFFFFF", bg="#000000"
        )
        label.pack(pady=20)


if __name__ == "__main__":
    test = BaseWindow()
    test.run()
