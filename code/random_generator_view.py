from base_window import BaseWindow

from PIL import Image, ImageTk
import tkinter as tk

class RandomGeneratorView(BaseWindow):

    def __init__(self):
        super().__init__()

        # initialized vars
        self.image_scale = 1

        # None initialized vars
        self.original_image = None
        self.display_image = None
        self.image_on_canvas = None
        self.pan_start = None

        # Entry fields
        self.env_width = None
        self.env_height = None
        self.num_agents = None
        self.max_num_cities = None

        # function calls
        super().setup_window()
        super().create_exit_button()
        super().create_help_button()
        super().create_canvas()

        self.add_image_to_canvas()
        self.create_run_button()
        self.create_save_button()
        self.create_load_button()
        self.create_generate_button()
        self.create_create_button()
        self.create_modify_button()

        self.create_env_width_entry()
        self.create_env_height_entry()
        self.create_number_of_agents_entry()
        self.create_max_number_of_cities_entry()

    def get_entered_params(self):
        entries = {
            "Environment Width": self.env_width.get(),
            "Environment Height": self.env_height.get(),
            "Number of Agents": self.num_agents.get(),
            "Max Number of Cities": self.max_num_cities.get(),
        }
        print(entries)
        return

    def add_image_to_canvas(self):
        # Load the image
        # TODO: change so created image is displayed
        image = Image.open("../png/env_001--4_2.png")

        # Crop the image
        crop_box = (0, 0, image.width - 4, image.height - 4)
        image = image.crop(crop_box)

        self.original_image = image
        self.display_image = image  # Image to be displayed

        # Display the initial image
        self.update_display_image()

        # Bind mouse events for zoom and pan
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<ButtonPress-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.pan)

    def update_display_image(self):
        """Update the image displayed on the canvas based on the current scale."""
        new_width = int(self.original_image.width * self.image_scale)
        new_height = int(self.original_image.height * self.image_scale)
        resized_image = self.original_image.resize((new_width, new_height))
        self.display_image = ImageTk.PhotoImage(resized_image)

        if self.image_on_canvas is None:
            # Display the image initially
            self.image_on_canvas = self.canvas.create_image(
                0, 0, anchor="nw", image=self.display_image
            )
        else:
            # Update the image
            self.canvas.itemconfig(self.image_on_canvas, image=self.display_image)

        # Update canvas scroll region to match the current image size
        self.canvas.config(scrollregion=(0, 0, new_width, new_height))

    def zoom(self, event):
        """Zoom the image in or out."""
        scale_factor = 1.1 if event.delta > 0 else 0.9
        self.image_scale *= scale_factor
        self.image_scale = max(0.1, self.image_scale)  # Prevent negative or zero scale
        self.update_display_image()

    def start_pan(self, event):
        """Start the pan operation."""
        self.pan_start = (event.x, event.y)

    def pan(self, event):
        """Pan the image within the fixed canvas."""
        if self.pan_start:
            dx = event.x - self.pan_start[0]
            dy = event.y - self.pan_start[1]
            self.canvas.move(self.image_on_canvas, dx, dy)
            self.pan_start = (event.x, event.y)

    def create_run_button(self):
        button = tk.Button(
            self.root, command=self.stub,
            text="Run", font=("Arial", 20, "bold"),
            fg="#000000", bg="#55AA55", bd=0, width=4, height=1
        )
        button.place(x=self.height + 100, y=self.height - 100)

    def create_save_button(self):
        button = tk.Button(
            self.root, command=self.stub,
            text="Save", font=("Arial", 20, "bold"),
            fg="#000000", bg="#AAAA55", bd=0, width=4, height=1
        )
        button.place(x=self.height + 100, y=self.height - 200)

    def create_load_button(self):
        button = tk.Button(
            self.root, command=self.stub,
            text="Load", font=("Arial", 20, "bold"),
            fg="#000000", bg="#5555AA", bd=0, width=4, height=1
        )
        button.place(x=self.height + 300, y=self.height - 200)

    def create_generate_button(self):
        button = tk.Button(
            self.root, command=self.get_entered_params,
            text="Generate Random Environment", font=("Arial", 20, "bold"),
            fg="#000000", bg="#AAAAAA", bd=0, width=25, height=1
        )
        button.place(x=self.height + 100, y=300)

    def create_create_button(self):
        button = tk.Button(
            self.root, command=self.stub,
            text="Create", font=("Arial", 20, "bold"),
            fg="#000000", bg="#AAAAAA", bd=0, width=10, height=1
        )
        button.place(x=self.height + 100, y=400)

    def create_modify_button(self):
        button = tk.Button(
            self.root, command=self.stub,
            text="Modify", font=("Arial", 20, "bold"),
            fg="#000000", bg="#AAAAAA", bd=0, width=10, height=1
        )
        button.place(x=self.height + 300, y=400)

    @staticmethod
    def on_entry_click(event, entry_field, text):
        if entry_field.get() == text:
            entry_field.delete(0, tk.END)  # Delete the placeholder text
            entry_field.config(fg="#000000")  # Change text color to black

    @staticmethod
    def on_focusout(event, entry_field, text):
        if entry_field.get() == '':
            entry_field.insert(0, text)  # Restore placeholder text if empty
            entry_field.config(fg="#AAAAAA")  # Change text color to grey

    def create_env_width_entry(self):
        label = tk.Label(
            self.root,
            text="Environment width:", font=("Arial", 15),
            fg="#FFFFFF", bg="#000000"
        )
        label.place(x=self.height + 100, y=170)

        text = "e.g: 30"
        self.env_width = tk.Entry(
            self.root,
            font=("Arial", 15), fg="#AAAAAA", bg="#FFFFFF", width=15
        )
        self.env_width.insert(0, text)
        self.env_width.bind(
            "<FocusIn>",
            lambda event: self.on_entry_click(event, self.env_width, text)
        )
        self.env_width.bind(
            "<FocusOut>",
            lambda event: self.on_focusout(event, self.env_width, text)
        )
        self.env_width.place(x=self.height + 100, y=200)

    def create_env_height_entry(self):
        label = tk.Label(
            self.root,
            text="Environment height:", font=("Arial", 15),
            fg="#FFFFFF", bg="#000000"
        )
        label.place(x=self.height + 300, y=170)

        text = "e.g: 30"
        self.env_height = tk.Entry(
            self.root,
            font=("Arial", 15), fg="#AAAAAA", bg="#FFFFFF", width=15
        )
        self.env_height.insert(0, text)
        self.env_height.bind(
            "<FocusIn>",
            lambda event: self.on_entry_click(event, self.env_height, text)
        )
        self.env_height.bind(
            "<FocusOut>",
            lambda event: self.on_focusout(event, self.env_height, text)
        )
        self.env_height.place(x=self.height + 300, y=200)

    def create_number_of_agents_entry(self):
        label = tk.Label(
            self.root,
            text="Number of Agents:", font=("Arial", 15),
            fg="#FFFFFF", bg="#000000"
        )
        label.place(x=self.height + 100, y=570)

        text = "e.g: 3"
        self.num_agents = tk.Entry(
            self.root,
            font=("Arial", 15), fg="#AAAAAA", bg="#FFFFFF", width=15
        )
        self.num_agents.insert(0, text)
        self.num_agents.bind(
            "<FocusIn>",
            lambda event: self.on_entry_click(event, self.num_agents, text)
        )
        self.num_agents.bind(
            "<FocusOut>",
            lambda event: self.on_focusout(event, self.num_agents, text)
        )
        self.num_agents.place(x=self.height + 100, y=600)

    def create_max_number_of_cities_entry(self):
        label = tk.Label(
            self.root,
            text="Max. Number of Cities:", font=("Arial", 15),
            fg="#FFFFFF", bg="#000000"
        )
        label.place(x=self.height + 300, y=570)

        text = "e.g: 3"
        self.max_num_cities = tk.Entry(
            self.root,
            font=("Arial", 15), fg="#AAAAAA", bg="#FFFFFF", width=15
        )
        self.max_num_cities.insert(0, text)
        self.max_num_cities.bind(
            "<FocusIn>",
            lambda event: self.on_entry_click(event, self.max_num_cities, text)
        )
        self.max_num_cities.bind(
            "<FocusOut>",
            lambda event: self.on_focusout(event, self.max_num_cities, text)
        )
        self.max_num_cities.place(x=self.height + 300, y=600)

    def stub(self):
        return

if __name__ == "__main__":
    test = RandomGeneratorView()
    test.run()
