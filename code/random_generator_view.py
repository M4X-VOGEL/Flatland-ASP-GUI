from base_window import BaseWindow

from PIL import Image, ImageTk
import tkinter as tk

class RandomGeneratorView(BaseWindow):
    def __init__(self):
        super().__init__()

        # Initialize variables
        self.image_scale = 1

        # None initialized vars
        self.original_image = None
        self.display_image = None
        self.image_on_canvas = None
        self.pan_start = None
        self.text_label = None

        # Grid settings
        self.grid_rows = 40
        self.grid_cols = 40
        self.grid_color = "#000000"
        self.grid_thickness = 1

        # Entry fields
        self.env_width = None
        self.env_height = None
        self.num_agents = None
        self.max_num_cities = None
        self.seed = None
        self.grid_mode = None
        self.rails_between_cities = None
        self.rail_pairs = None
        self.remove_agents = None
        self.speed_ratio = None
        self.malfunction_rate = None
        self.malfunction_min = None
        self.malfunction_max = None

        # Function calls
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
        self.create_seed_entry()
        self.create_grid_mode_entry()
        self.create_rails_between_cities_entry()
        self.create_rail_pairs_entry()
        self.create_remove_agents_entry()
        self.create_speed_ratio_entry()
        self.create_malfunction_rate_entry()
        self.create_malfunction_min_entry()
        self.create_malfunction_max_entry()



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
        self.canvas.bind("<Leave>", self.remove_coordinates_display)
        self.canvas.bind("<Motion>", self.update_grid_coordinates)
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
                50, 50, anchor="nw", image=self.display_image
            )
        else:
            # Update the image
            self.canvas.itemconfig(self.image_on_canvas,
                                   image=self.display_image)

        # Update canvas scroll region to match the current image size
        self.canvas.config(scrollregion=(0, 0, new_width, new_height))

        # Redraw the grid
        self.draw_grid(new_width, new_height)

    def draw_grid(self, img_width, img_height):
        """Draw a grid with numerical labels fixed to the image."""
        # Clear existing grid lines and labels
        self.canvas.delete("grid_line")
        self.canvas.delete("grid_label")

        # Calculate grid spacing
        row_spacing = img_height / self.grid_rows
        col_spacing = img_width / self.grid_cols

        # Get the current position of the image
        x0, y0 = self.canvas.coords(self.image_on_canvas)

        # Draw horizontal lines and row labels
        for i in range(self.grid_rows + 1):
            y = y0 + i * row_spacing
            # Draw horizontal grid line
            self.canvas.create_line(
                x0, y, x0 + img_width, y,
                fill=self.grid_color,
                width=self.grid_thickness,
                tags="grid_line"
            )
            # Add row labels
            if i < self.grid_rows:
                label_y = y + row_spacing / 2  # Center label between grid lines
                self.canvas.create_text(
                    x0 - 20, label_y,  # Position relative to the image
                    text=str(i),
                    anchor="e",  # Align text to the right
                    font=("Arial", 10),
                    fill=self.grid_color,
                    tags="grid_label"
                )

        # Draw vertical lines and column labels
        for i in range(self.grid_cols + 1):
            x = x0 + i * col_spacing
            # Draw vertical grid line
            self.canvas.create_line(
                x, y0, x, y0 + img_height,
                fill=self.grid_color,
                width=self.grid_thickness,
                tags="grid_line"
            )
            # Add column labels
            if i < self.grid_cols:
                label_x = x + col_spacing / 2  # Center label between grid lines
                self.canvas.create_text(
                    label_x, y0 - 20,  # Position relative to the image
                    text=str(i),
                    anchor="e",  # Align text to the bottom
                    angle=90,
                    font=("Arial", 10),
                    fill=self.grid_color,
                    tags="grid_label"
                )

    def update_grid_coordinates(self, event):
        """Update the grid coordinates and display the current cell under the cursor."""
        # Get the position of the mouse on the canvas
        mouse_x = event.x
        mouse_y = event.y

        # Get the current position of the image on the canvas
        image_coords = self.canvas.coords(self.image_on_canvas)
        if not image_coords:
            return  # Image not loaded yet

        x0, y0 = image_coords

        # Adjust for panning and scaling
        adjusted_x = (mouse_x - x0) / self.image_scale
        adjusted_y = (mouse_y - y0) / self.image_scale

        # Check if the cursor is within the bounds of the image
        img_width = self.original_image.width
        img_height = self.original_image.height
        if 0 <= adjusted_x < img_width and 0 <= adjusted_y < img_height:
            # Calculate the grid cell row and column
            row_spacing = img_height / self.grid_rows
            col_spacing = img_width / self.grid_cols

            row = int(adjusted_y / row_spacing)
            col = int(adjusted_x / col_spacing)

            # Format the row and column to be displayed
            coords_text = f"[{row}, {col}]"

            # If the text label doesn't exist, create it
            if self.text_label is None:
                self.text_label = self.canvas.create_text(
                    mouse_x + 10, mouse_y + 10,  # Position next to the cursor
                    text=coords_text,
                    font=("Arial", 12),
                    fill="#662266", # Text color
                    anchor="nw"
                )
            else:
                # Update the text and position of the label
                self.canvas.itemconfig(self.text_label, text=coords_text)
                self.canvas.coords(self.text_label, mouse_x + 10, mouse_y + 10)
        else:
            # Remove the label if the cursor is not over the image
            if self.text_label is not None:
                self.canvas.delete(self.text_label)
                self.text_label = None

    def remove_coordinates_display(self, event):
        """Clear the coordinates label when the mouse leaves the canvas."""
        if self.text_label is not None:
            self.canvas.delete(self.text_label)
            self.text_label = None

    def zoom(self, event):
        """Zoom the image in or out."""
        scale_factor = 1.1 if event.delta > 0 else 0.9
        self.image_scale *= scale_factor
        self.image_scale = max(0.1,
                               self.image_scale)  # Prevent negative or zero scale
        self.update_display_image()

    def start_pan(self, event):
        """Start the pan operation."""
        self.pan_start = (event.x, event.y)

    def pan(self, event):
        """Pan the image and grid together."""
        if self.pan_start:
            dx = event.x - self.pan_start[0]
            dy = event.y - self.pan_start[1]
            self.canvas.move(self.image_on_canvas, dx, dy)
            self.canvas.move("grid_line", dx, dy)
            self.canvas.move("grid_label", dx, dy)
            self.pan_start = (event.x, event.y)

    def create_run_button(self):
        button = tk.Button(
            self.root, command=self.stub,
            text="Run", font=("Arial", 20, "bold"),
            fg="#000000", bg="#55AA55", bd=0,
            width=4, height=1
        )
        button.place(
            x=int(self.width*0.9), y=int(self.height*0.85)
        )

    def create_save_button(self):
        button = tk.Button(
            self.root, command=self.stub,
            text="Save Environment", font=("Arial", 20, "bold"),
            fg="#000000", bg="#AAAA55", bd=0,
            width=15, height=1
        )
        button.place(
            x=int(self.width*0.55), y=int(self.height*0.85)
        )

    def create_load_button(self):
        button = tk.Button(
            self.root, command=self.stub,
            text="Load Environment", font=("Arial", 20, "bold"),
            fg="#000000", bg="#5555AA", bd=0,
            width=15, height=1
        )
        button.place(
            x=int(self.width*0.7), y=int(self.height*0.85)
        )

    def create_generate_button(self):
        button = tk.Button(
            self.root, command=self.get_entered_params,
            text="Generate Random Environment", font=("Arial", 20, "bold"),
            fg="#000000", bg="#AAAAAA", bd=0,
            width=25, height=1
        )
        button.place(
            x=int(self.width*0.55), y=int(self.height*0.08)
        )

    def create_create_button(self):
        button = tk.Button(
            self.root, command=self.stub,
            text="Create", font=("Arial", 20, "bold"),
            fg="#000000", bg="#AAAAAA", bd=0,
            width=10, height=1
        )
        button.place(
            x=int(self.width*0.80), y=int(self.height*0.08)
        )

    def create_modify_button(self):
        button = tk.Button(
            self.root, command=self.stub,
            text="Modify", font=("Arial", 20, "bold"),
            fg="#000000", bg="#AAAAAA", bd=0,
            width=10, height=1
        )
        button.place(
            x=int(self.width*0.90), y=int(self.height*0.08)
        )

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
        label.place(
            x=int(self.width*0.55), y=int(self.height*0.15)
        )

        text = "e.g: 40"
        self.env_width = tk.Entry(
            self.root,
            font=("Arial", 15), fg="#AAAAAA", bg="#FFFFFF",
            width=10
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
        self.env_width.place(
            x=int(self.width*0.70), y=int(self.height*0.15)
        )

    def create_env_height_entry(self):
        label = tk.Label(
            self.root,
            text="Environment height:", font=("Arial", 15),
            fg="#FFFFFF", bg="#000000"
        )
        label.place(
            x=int(self.width*0.55), y=int(self.height*0.2)
        )

        text = "e.g.: 40"
        self.env_height = tk.Entry(
            self.root,
            font=("Arial", 15), fg="#AAAAAA", bg="#FFFFFF",
            width=10
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
        self.env_height.place(
            x=int(self.width*0.70), y=int(self.height*0.2)
        )

    def create_number_of_agents_entry(self):
        label = tk.Label(
            self.root,
            text="Number of agents:", font=("Arial", 15),
            fg="#FFFFFF", bg="#000000"
        )
        label.place(
            x=int(self.width*0.55), y=int(self.height*0.25)
        )

        text = "e.g: 4"
        self.num_agents = tk.Entry(
            self.root,
            font=("Arial", 15), fg="#AAAAAA", bg="#FFFFFF",
            width=10
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
        self.num_agents.place(
            x=int(self.width*0.70), y=int(self.height*0.25)
        )

    def create_max_number_of_cities_entry(self):
        label = tk.Label(
            self.root,
            text="Max. number of cities:", font=("Arial", 15),
            fg="#FFFFFF", bg="#000000"
        )
        label.place(
            x=int(self.width*0.55), y=int(self.height*0.3)
        )

        text = "e.g: 2"
        self.max_num_cities = tk.Entry(
            self.root,
            font=("Arial", 15), fg="#AAAAAA", bg="#FFFFFF",
            width=10
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
        self.max_num_cities.place(
            x=int(self.width*0.70), y=int(self.height*0.3)
        )

    def create_seed_entry(self):
        label = tk.Label(
            self.root,
            text="Seed:", font=("Arial", 15),
            fg="#FFFFFF", bg="#000000"
        )
        label.place(
            x=int(self.width*0.55), y=int(self.height*0.35)
        )

        text = "e.g: 1"
        self.seed = tk.Entry(
            self.root,
            font=("Arial", 15), fg="#AAAAAA", bg="#FFFFFF",
            width=10
        )
        self.seed.insert(0, text)
        self.seed.bind(
            "<FocusIn>",
            lambda event: self.on_entry_click(event, self.seed, text)
        )
        self.seed.bind(
            "<FocusOut>",
            lambda event: self.on_focusout(event, self.seed, text)
        )
        self.seed.place(
            x=int(self.width*0.70), y=int(self.height*0.35)
        )

    def create_grid_mode_entry(self):
        label = tk.Label(
            self.root,
            text="Grid mode:", font=("Arial", 15),
            fg="#FFFFFF", bg="#000000"
        )
        label.place(
            x=int(self.width*0.55), y=int(self.height*0.4)
        )

        text = "e.g: False"
        self.grid_mode = tk.Entry(
            self.root,
            font=("Arial", 15), fg="#AAAAAA", bg="#FFFFFF",
            width=10
        )
        self.grid_mode.insert(0, text)
        self.grid_mode.bind(
            "<FocusIn>",
            lambda event: self.on_entry_click(event, self.grid_mode, text)
        )
        self.grid_mode.bind(
            "<FocusOut>",
            lambda event: self.on_focusout(event, self.grid_mode, text)
        )
        self.grid_mode.place(
            x=int(self.width*0.70), y=int(self.height*0.4)
        )

    def create_rails_between_cities_entry(self):
        label = tk.Label(
            self.root,
            text="Max. rails between cities:", font=("Arial", 15),
            fg="#FFFFFF", bg="#000000"
        )
        label.place(
            x=int(self.width*0.55), y=int(self.height*0.45)
        )

        text = "e.g: 2"
        self.rails_between_cities = tk.Entry(
            self.root,
            font=("Arial", 15), fg="#AAAAAA", bg="#FFFFFF",
            width=10
        )
        self.rails_between_cities.insert(0, text)
        self.rails_between_cities.bind(
            "<FocusIn>",
            lambda event: self.on_entry_click(
                event, self.rails_between_cities, text
            )
        )
        self.rails_between_cities.bind(
            "<FocusOut>",
            lambda event: self.on_focusout(
                event, self.rails_between_cities, text
            )
        )
        self.rails_between_cities.place(
            x=int(self.width*0.70), y=int(self.height*0.45)
        )

    def create_rail_pairs_entry(self):
        label = tk.Label(
            self.root,
            text="Max. rail pairs in cities:", font=("Arial", 15),
            fg="#FFFFFF", bg="#000000"
        )
        label.place(
            x=int(self.width*0.55), y=int(self.height*0.5)
        )

        text = "e.g: 2"
        self.rail_pairs = tk.Entry(
            self.root,
            font=("Arial", 15), fg="#AAAAAA", bg="#FFFFFF",
            width=10
        )
        self.rail_pairs.insert(0, text)
        self.rail_pairs.bind(
            "<FocusIn>",
            lambda event: self.on_entry_click(event, self.rail_pairs, text)
        )
        self.rail_pairs.bind(
            "<FocusOut>",
            lambda event: self.on_focusout(event, self.rail_pairs, text)
        )
        self.rail_pairs.place(
            x=int(self.width*0.70), y=int(self.height*0.5)
        )

    def create_remove_agents_entry(self):
        label = tk.Label(
            self.root,
            text="Remove agents on arrival:", font=("Arial", 15),
            fg="#FFFFFF", bg="#000000"
        )
        label.place(
            x=int(self.width*0.55), y=int(self.height*0.55)
        )

        text = "e.g: True"
        self.remove_agents = tk.Entry(
            self.root,
            font=("Arial", 15), fg="#AAAAAA", bg="#FFFFFF",
            width=10
        )
        self.remove_agents.insert(0, text)
        self.remove_agents.bind(
            "<FocusIn>",
            lambda event: self.on_entry_click(event, self.remove_agents, text)
        )
        self.remove_agents.bind(
            "<FocusOut>",
            lambda event: self.on_focusout(event, self.remove_agents, text)
        )
        self.remove_agents.place(
            x=int(self.width*0.70), y=int(self.height*0.55)
        )

    def create_speed_ratio_entry(self):
        label = tk.Label(
            self.root,
            text="Speed ration map:", font=("Arial", 15),
            fg="#FFFFFF", bg="#000000"
        )
        label.place(
            x=int(self.width*0.55), y=int(self.height*0.6)
        )

        text = "e.g: {1:1}"
        self.speed_ratio = tk.Entry(
            self.root,
            font=("Arial", 15), fg="#AAAAAA", bg="#FFFFFF",
            width=10
        )
        self.speed_ratio.insert(0, text)
        self.speed_ratio.bind(
            "<FocusIn>",
            lambda event: self.on_entry_click(event, self.speed_ratio, text)
        )
        self.speed_ratio.bind(
            "<FocusOut>",
            lambda event: self.on_focusout(event, self.speed_ratio, text)
        )
        self.speed_ratio.place(
            x=int(self.width*0.70), y=int(self.height*0.6)
        )

    def create_malfunction_rate_entry(self):
        label = tk.Label(
            self.root,
            text="Malfunction rate:", font=("Arial", 15),
            fg="#FFFFFF", bg="#000000"
        )
        label.place(
            x=int(self.width*0.55), y=int(self.height*0.65)
        )

        text = "e.g: 0/30"
        self.malfunction_rate = tk.Entry(
            self.root,
            font=("Arial", 15), fg="#AAAAAA", bg="#FFFFFF",
            width=10
        )
        self.malfunction_rate.insert(0, text)
        self.malfunction_rate.bind(
            "<FocusIn>",
            lambda event: self.on_entry_click(
                event, self.malfunction_rate, text
            )
        )
        self.malfunction_rate.bind(
            "<FocusOut>",
            lambda event: self.on_focusout(
                event, self.malfunction_rate, text
            )
        )
        self.malfunction_rate.place(
            x=int(self.width*0.70), y=int(self.height*0.65)
        )

    def create_malfunction_min_entry(self):
        label = tk.Label(
            self.root,
            text="Min. malfunction duration:", font=("Arial", 15),
            fg="#FFFFFF", bg="#000000"
        )
        label.place(
            x=int(self.width*0.55), y=int(self.height*0.7)
        )

        text = "e.g: 2"
        self.malfunction_min = tk.Entry(
            self.root,
            font=("Arial", 15), fg="#AAAAAA", bg="#FFFFFF",
            width=10
        )
        self.malfunction_min.insert(0, text)
        self.malfunction_min.bind(
            "<FocusIn>",
            lambda event: self.on_entry_click(event, self.malfunction_min, text)
        )
        self.malfunction_min.bind(
            "<FocusOut>",
            lambda event: self.on_focusout(event, self.malfunction_min, text)
        )
        self.malfunction_min.place(
            x=int(self.width*0.70), y=int(self.height*0.7)
        )

    def create_malfunction_max_entry(self):
        label = tk.Label(
            self.root,
            text="Max. malfunction duration:", font=("Arial", 15),
            fg="#FFFFFF", bg="#000000"
        )
        label.place(
            x=int(self.width*0.55), y=int(self.height*0.75)
        )

        text = "e.g: 6"
        self.malfunction_max = tk.Entry(
            self.root,
            font=("Arial", 15), fg="#AAAAAA", bg="#FFFFFF",
            width=10
        )
        self.malfunction_max.insert(0, text)
        self.malfunction_max.bind(
            "<FocusIn>",
            lambda event: self.on_entry_click(event, self.malfunction_max, text)
        )
        self.malfunction_max.bind(
            "<FocusOut>",
            lambda event: self.on_focusout(event, self.malfunction_max, text)
        )
        self.malfunction_max.place(
            x=int(self.width*0.70), y=int(self.height*0.75)
        )

    def get_entered_params(self):
        # STUB FUNCTION FOR NOW
        entries = {
            "Environment width": self.env_width.get(),
            "Environment height": self.env_height.get(),
            "Number of agents": self.num_agents.get(),
            "Max. number of cities": self.max_num_cities.get(),
            "Seed": self.seed.get(),
            "Grid mode": self.grid_mode.get(),
            "Max. rails between cities": self.rails_between_cities.get(),
            "Max. rail pairs in cities": self.rail_pairs.get(),
            "Remove agent on arrival": self.remove_agents.get(),
            "Speed ration map": self.speed_ratio.get(),
            "Malfunction rate": self.malfunction_rate.get(),
            "Min. malfunction duration": self.malfunction_min.get(),
            "Max. malfunction duration": self.malfunction_max.get(),
        }
        print(entries)
        return

    def stub(self):
        # PLACE HOLDER FOR BUTTON FUNCTIONS
        return

if __name__ == "__main__":
    test = RandomGeneratorView()
    test.run()
