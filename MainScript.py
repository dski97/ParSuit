import tkinter as tk
from tkinter import ttk
from tkinter.font import Font  # Import for font customization
from PIL import Image, ImageTk

class ParSuitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ParSuit")
        self.sliders = []
        self.setup_ui()
    
    def setup_ui(self):
        self.root.geometry("650x700")  # Set initial size
        
        # Define a bold font for the title
        title_font = Font(family="Helvetica", size=16, weight="bold")
        
        # Create a title label with the bold font
        title_label = tk.Label(self.root, text="Suitability Analysis for Hartford Capitol Region", font=title_font)
        title_label.pack(side='top', pady=(10, 20))  # Adjust padding as needed
        
        container = ttk.Frame(self.root)
        container.pack(side='top', fill='both', expand=True)

        self.canvas = tk.Canvas(container)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.scrollable_frame_window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.load_and_display_image()
        self.create_info_text()
        self.create_sliders()

        self.total_label = tk.Label(self.root, text="Total: 0/100")
        self.total_label.pack(side='bottom')

        self.root.bind("<Configure>", self.on_window_resize)

    def on_window_resize(self, event=None):
        # Dynamically adjust the position of the scrollable frame to remain centered
        canvas_width = self.canvas.winfo_width()
        frame_width = self.scrollable_frame.winfo_reqwidth()
        new_x_position = max((canvas_width - frame_width) / 2, 0)  # Ensure the position is not negative

        self.canvas.coords(self.scrollable_frame_window_id, new_x_position, 0)

    def load_and_display_image(self):
        image_path = r"C:\Users\cwalinskid\Desktop\CRCOG Project\ParSuit\CRCOG.jpg"  # Ensure this path is accessible
        image = Image.open(image_path)
        resized_image = image.resize((650, 500), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized_image)
        self.image_label = tk.Label(self.scrollable_frame, image=photo)
        self.image_label.image = photo  # Keep a reference to avoid garbage collection
        self.image_label.pack(pady=20)

    def create_info_text(self):
        # Define a font for the heading
        heading_font = Font(family="Helvetica", size=14, weight="bold")

        # Create a heading label with the custom font
        heading_label = tk.Label(self.scrollable_frame, text="Geographic Analysis", font=heading_font)
        heading_label.pack(pady=(10, 2))  # Adjust vertical padding as needed

        # Create a paragraph label. No custom font needed, but you can customize if desired
        paragraph_text = "This analysis explores various geographic and environmental factors influencing the Hartford Capitol Region. It provides insights into land use, demographics, and infrastructure, assisting in strategic planning and decision-making."
        paragraph_label = tk.Label(self.scrollable_frame, text=paragraph_text, wraplength=600, justify="center")
        paragraph_label.pack(pady=(0, 20))  # Adjust vertical padding as needed

          # Add a label for the combobox
        preset_label = tk.Label(self.scrollable_frame, text="Adjust the criteria based on your needs or select custom presets made for certain scenarios")
        preset_label.pack(pady=(10, 2))  # Adjust vertical padding as needed

        # Create a Combobox for custom presets
        self.preset_combobox = ttk.Combobox(self.scrollable_frame, 
                                            values=["Balanced", "Urban-Intensified", "Rural Favorite", "Community-Based", "Lone Star Ranger"],
                                            state="readonly")  # state="readonly" to prevent user typing
        self.preset_combobox.set("Custom Presets")  # Placeholder text
        self.preset_combobox.pack(pady=(0, 20))

        # Bind the selection event to a method if needed
        self.preset_combobox.bind("<<ComboboxSelected>>", self.on_preset_selected)

    def on_preset_selected(self, event):
        selected_preset = self.preset_combobox.get()
        # Update sliders or perform other actions based on the selected preset
        # For example:
        if selected_preset == "Balanced":
            # Set sliders to balanced positions
            pass
        # Handle other presets similarly...

    def create_sliders(self):

        # Define the bold font
        bold_font = Font(family="Helvetica", size=10, weight="bold")

        # Create a frame for the importance labels
        importance_frame = tk.Frame(self.scrollable_frame)
        importance_frame.pack(fill='x', pady=(0, 2))

        # Label for "Less Important" on the left with bold font
        less_important_label = tk.Label(importance_frame, text="Less Important", anchor='w', font=bold_font)
        less_important_label.pack(side='left', fill='x', expand=True)

        # Label for "More Important" on the right with bold font
        more_important_label = tk.Label(importance_frame, text="More Important", anchor='e', font=bold_font)
        more_important_label.pack(side='left', fill='x', expand=True)

        # Define a fixed width for labels to ensure sliders align
        label_width = 20  # Adjust this value as needed

        #List of slider names
        slider_names = [
            'Away from Brownfields',
            'Buildable Soil',
            'Away from Floodzones',
            'Proximity to Hospitals',
            'Proximity to Police Stations',
            'Proximity to Roads',
            'Proximity to Schools',
            'Public Sewer',
            'Low Grade Slope',
            'Away from Wetlands',
            'Appropriate Land Use'
        ]

        for name in slider_names:
            frame = tk.Frame(self.scrollable_frame)
            frame.pack(fill='x', pady=2, expand=False)

            # Label for the criteria with a fixed width
            label = tk.Label(frame, text=name, anchor='w', width=label_width)
            label.pack(side='left')

            # Slider with a fixed length
            slider_length = 500  # Adjust this value as needed to fit your layout
            slider = tk.Scale(frame, from_=0, to=100, orient='horizontal', length=slider_length)
            slider.pack(side='left', fill='x', padx=(0, 10))

            self.sliders.append(slider)

    def slider_moved(self, slider_index, value):
        value = int(value)
        current_total = sum(slider.get() for i, slider in enumerate(self.sliders) if i != slider_index)
        max_allowed = 100 - current_total
        if value > max_allowed:
            self.sliders[slider_index].set(max_allowed)
            self.total_label.config(text="Total: 100/100")
        else:
            self.total_label.config(text=f"Total: {current_total + value}/100")

if __name__ == "__main__":
    root = tk.Tk()
    app = ParSuitApp(root)
    root.mainloop()
