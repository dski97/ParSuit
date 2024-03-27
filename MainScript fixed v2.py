import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from PIL import Image, ImageTk
import threading
import subprocess
import os
import webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer

# Configuration class to store the constants
class Configuration:
    SLIDER_NAMES = [
        "Away from Brownfields",
        "Buildable Soil",
        "Away from Floodzones",
        "Proximity to Hospitals",
        "Proximity to Police Stations",
        "Proximity to Roads",
        "Proximity to Schools",
        "Public Sewer",
        "Low Grade Slope",
        "Away from Wetlands",
        "Appropriate Land Use",
    ]
    IMAGE_PATH = "icons/CRCOG.jpg"
    TITLE_TEXT = "Suitability Analysis for Hartford Capitol Region"
    GEOGRAPHIC_ANALYSIS_TEXT = "Explore the Hartford Capitol Region with ParSuit, your guide to informed land suitability analysis. This tool empowers you to prioritize geographic and environmental factors with simple slider adjustments. From safeguarding against environmental risks to enhancing access to essential services, your input directly shapes the analysis. Once you've set your preferences, a single click reveals a comprehensive map, visualizing the most suitable parcels according to your criteria. ParSuit combines precision with simplicity, offering a clear path to insightful, actionable data for your projects."
    PRESETS = [
        "Balanced",
        "Urban-Intensified",
        "Rural Favorite",
        "Community-Based",
        "Lone Star Ranger",
        "Reset",
    ]
    PRESET_VALUES = {
        "Balanced": [9] * 10 + [10],
        "Urban-Intensified": [3, 3, 3, 14, 14, 14, 8, 14, 3, 3, 21],
        "Rural Favorite": [14, 14, 14, 3, 3, 3, 9, 3, 14, 14, 9],
        "Community-Based": [3, 9, 3, 16, 16, 11, 16, 9, 3, 2, 12],
        "Lone Star Ranger": [16, 12, 16, 3, 3, 3, 3, 3, 12, 16, 13],
        "Reset": [0] * 11,
    }
    NUM_SLIDERS = len(SLIDER_NAMES)


# Main class for the ParSuit application
class ParSuitApp:
    # Constructor for the ParSuitApp class
    def __init__(self, root):
        self.root = root
        self.root.title("ParSuit")
        self.sliders = []
        self.slider_values = []
        self.setup_ui()
        self.center_window()
        self.start_server()
        self.is_browser_open = False
        self.root.protocol(
            "WM_DELETE_WINDOW", self.stop_server
        )  # Stop the server when the window is closed

    # Method to set up the user interface
    def setup_ui(self):
        self.root.geometry("800x800")
        self.root.resizable(False, False)
        self.create_title()
        self.create_main_container()
        self.load_and_display_image()
        self.create_info_text()
        self.create_importance_key()
        self.create_sliders()
        self.create_total_label()
        self.create_glossary()
        self.update_scroll()
        self.create_processing_button()
        self.root.bind_all("<MouseWheel>", self.on_mousewheel)
        self.root.bind("<Configure>", self.on_window_resize)

    # Method to start the server
    def start_server(self):

        # Change the current directory to the script directory
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Start the server in the script directory
        os.chdir(current_dir)

        # Start the server on port 8000
        self.port = 8000

        # Create the server
        server_address = ("", self.port)

        # Create the HTTP server
        self.httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

        # Start the server in a separate thread
        print(f"Server running on http://localhost:{self.port}")

        # Create a thread for the server
        self.server_thread = threading.Thread(target=self.httpd.serve_forever)

        # Set the thread as a daemon
        self.server_thread.daemon = True

        # Start the server thread
        self.server_thread.start()

    # Method to create the title
    def create_title(self):
        # Create the title font
        title_font = Font(family="Helvetica", size=16, weight="bold")
        # Create the title label
        tk.Label(self.root, text=Configuration.TITLE_TEXT, font=title_font).pack(
            side="top", pady=(10, 20)
        )

    # Method to create the main container
    def create_main_container(self):
        # Create the container
        container = ttk.Frame(self.root)

        # Pack the container
        container.pack(side="top", fill="both", expand=True)

        # Create the canvas
        self.canvas = tk.Canvas(container)

        # Create the scrollbar
        self.scrollbar = ttk.Scrollbar(
            container, orient="vertical", command=self.canvas.yview
        )

        # Create the scrollable frame
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Bind the scrollable frame to the canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        # Create the window id for the scrollable frame
        self.scrollable_frame_window_id = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )

        # Configure the canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack the canvas and scrollbar
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Bind the canvas to the mousewheel event
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Configure the grid
        container.grid_rowconfigure(0, weight=1)

        # Configure the grid
        container.grid_columnconfigure(0, weight=1)

        # Bind the mousewheel event to the on_mousewheel method
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def load_and_display_image(self):
        # Open the image file
        image = Image.open(Configuration.IMAGE_PATH)

        # Resize the image to fit the application window
        resized_image = image.resize((650, 500), Image.LANCZOS)

        # Create a PhotoImage object from the resized image
        photo = ImageTk.PhotoImage(resized_image)

        # Create a label to display the image
        image_label = tk.Label(self.scrollable_frame, image=photo)
        image_label.image = photo

        # Pack the image label with vertical padding
        image_label.pack(pady=20)

    def create_info_text(self):
        # Create a custom font for the heading
        heading_font = Font(family="Helvetica", size=14, weight="bold")

        # Create a label for the heading and pack it with vertical padding
        tk.Label(
            self.scrollable_frame,
            text="Welcome to the ParSuit Application!",
            font=heading_font,
        ).pack(pady=(10, 2))

        # Create a label for the geographic analysis text and pack it with vertical padding
        tk.Label(
            self.scrollable_frame,
            text=Configuration.GEOGRAPHIC_ANALYSIS_TEXT,
            wraplength=600,
            justify="center",
        ).pack(pady=(0, 20))

        # Call the method to create the presets combobox
        self.create_presets_combobox()

    # Method to create the presets combobox
    def create_presets_combobox(self):
        # Create a label for the presets combobox and pack it with vertical padding
        tk.Label(
            self.scrollable_frame,
            text="Adjust the criteria based on your needs or select custom presets made for certain scenarios",
        ).pack(pady=(10, 2))

        # Create the presets combobox with the values from Configuration.PRESETS
        self.preset_combobox = ttk.Combobox(
            self.scrollable_frame, values=Configuration.PRESETS, state="readonly"
        )

        # Set the default value of the presets combobox
        self.preset_combobox.set("Custom Presets")

        # Pack the presets combobox with vertical padding
        self.preset_combobox.pack(pady=(0, 20))

        # Bind the <<ComboboxSelected>> event to the on_preset_selected method
        self.preset_combobox.bind("<<ComboboxSelected>>", self.on_preset_selected)

    # Method to create the importance key
    def create_importance_key(self):
        # Create a frame for the importance key
        key_frame = tk.Frame(self.scrollable_frame)

        # Pack the key frame with horizontal fill and vertical padding
        key_frame.pack(fill="x", pady=(10, 0), expand=False)

        # Create a label for "Less Important" and pack it on the left side of the key frame
        tk.Label(key_frame, text="Less Important", fg="red", anchor="w", padx=120).pack(
            side="left"
        )

        # Create a label for "More Important" and pack it on the right side of the key frame
        tk.Label(key_frame, text="More Important", fg="red", anchor="e").pack(
            side="right"
        )

    # Method to create the sliders
    def create_sliders(self):
        # Iterate over the slider names from Configuration.SLIDER_NAMES
        for index, name in enumerate(Configuration.SLIDER_NAMES):
            # Call the create_slider method for each slider name and index
            self.create_slider(name, index)

    # Method to create a slider
    def create_slider(self, name, index):

        # Create a frame for the slider
        frame = tk.Frame(self.scrollable_frame)

        # Pack the frame with horizontal fill, 2 pixels of vertical padding, and no expansion
        frame.pack(fill="x", pady=2, expand=False)

        # Create a label for the slider with the given name and pack it on the left side of the frame
        label = tk.Label(frame, text=name, anchor="w", width=20)

        # Pack the label with horizontal fill and no expansion
        label.grid(row=0, column=0, sticky="w")

        # Create a slider with values from 0 to 100, horizontal orientation, and a length of 400 pixels
        slider = tk.Scale(
            frame,
            from_=0,
            to=100,
            orient="horizontal",
            length=400,
            command=lambda value, index=index: self.update_total(index, value),
        )

        # Set the initial value of the slider to 0
        slider.grid(row=0, column=1, sticky="ew")
        frame.grid_columnconfigure(1, weight=1)
        self.sliders.append(slider)

    # Method to update the total value and enable/disable the process button
    def update_total(self, moved_index, value):
        # Calculate the total value of all sliders except the one that was moved
        total = sum(
            slider.get() for i, slider in enumerate(self.sliders) if i != moved_index
        )
        moved_value = int(value)
        if total + moved_value > 100:
            excess = total + moved_value - 100
            new_value = moved_value - excess
            self.sliders[moved_index].set(new_value)
            total = 100
        else:
            total += moved_value

        # Update the total label text with the new total value
        self.total_label.config(text=f"Total: {total}/100")
        self.process_button.config(
            state="normal" if self.is_total_valid() else "disabled"
        )

    # Method to handle the selection of a preset
    def on_preset_selected(self, event):

        # Get the selected preset from the combobox
        selected_preset = self.preset_combobox.get()

        # Apply the preset values to the sliders
        self.apply_preset_values(selected_preset)

    # Method to apply the preset values to the sliders
    def apply_preset_values(self, preset):

        # Get the selected values from the Configuration.PRESET_VALUES dictionary
        selected_values = Configuration.PRESET_VALUES.get(
            preset, [0] * Configuration.NUM_SLIDERS
        )
        # Iterate over the sliders and set the values from the selected values list
        for slider, value in zip(self.sliders, selected_values):
            slider.set(value)

    # Method to create the total label
    def create_total_label(self):

        # Create a font for the total label
        total_label_font = Font(family="Times New Roman", size=16, weight="bold")

        # Create the total label with the initial text "Total: 0/100"
        self.total_label = tk.Label(
            self.root, text="Total: 0/100", font=total_label_font
        )

        # Pack the total label with vertical padding
        self.total_label.pack(side="bottom")

    # Method to create the glossary
    def create_glossary(self):
        # Create a frame for the glossary
        glossary_frame = tk.Frame(self.scrollable_frame)

        # Pack the glossary frame with horizontal fill and 20 pixels of vertical padding
        glossary_frame.pack(fill="x", pady=20)

        # Create a font for the glossary title
        glossary_title_font = Font(family="Arial", size=14, weight="bold")
        glossary_title = tk.Label(
            glossary_frame, text="Glossary", font=glossary_title_font
        )
        glossary_title.pack(side="top")
        term_font = Font(family="Arial", size=12, weight="bold", slant="italic")

        # Create a dictionary of glossary terms and their explanations
        glossary_terms = {
            "Away from Brownfields": "Indicates the degree to which the land is inclined, affecting construction and drainage.",
            "Buildable Soil": "Refers to soil with properties conducive to agriculture or construction.",
            "Away from Flood Zones": "Areas less likely to experience flooding, reducing risk of water damage.",
            "Proximity to Hospitals": "Distance from medical facilities, affecting emergency response times.",
            "Proximity to Police Stations": "Distance from law enforcement, affecting crime rates and safety.",
            "Proximity to Roads": "Distance from roads, affecting accessibility and noise pollution.",
            "Proximity to Schools": "Distance from educational institutions, affecting property values and child safety.",
            "Public Sewer": "Availability of immediate access to public sewer systems.",
            "Low Grade Slope": "Indicates the degree to which the land is flat and suitable for construction.",
            "Away from Wetlands": "Distance from wetlands, affecting environmental impact and land use.",
            "Appropriate Land Use": "Refers to the suitability of the land for specific purposes such as residential, commercial, or industrial.",
        }

        # Create a text widget for the glossary terms
        glossary_text = tk.Text(glossary_frame, wrap=tk.WORD, width=70, height=20)
        glossary_scrollbar = tk.Scrollbar(
            glossary_frame, command=glossary_text.yview, width=22
        )
        glossary_text.configure(yscrollcommand=glossary_scrollbar.set)

        # Insert the glossary terms into the text widget
        for term, explanation in glossary_terms.items():
            glossary_text.insert(tk.END, f"{term} - ", "term")
            glossary_text.insert(tk.END, f"{explanation}\n\n")
        glossary_text.tag_configure("term", font=term_font)
        glossary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        glossary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Method to handle the window resize event
    def on_window_resize(self, event=None):

        # Update the scrollable frame window position
        canvas_width = self.canvas.winfo_width()
        frame_width = self.scrollable_frame.winfo_reqwidth()
        new_x_position = max((canvas_width - frame_width) / 2, 0)
        self.canvas.coords(self.scrollable_frame_window_id, new_x_position, 0)

    # Method to center the window on the screen
    def center_window(self):
        # Update the window idletasks
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"+{x}+{y}")

    # Method to update the scroll region of the canvas
    def update_scroll(self):

        # Update the window idletasks
        self.root.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Method to handle the mousewheel event
    def on_mousewheel(self, event):

        # Scroll the canvas vertically based on the mousewheel event
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Method to create the processing button
    def create_processing_button(self):

        # Create a frame for the button
        button_frame = tk.Frame(self.scrollable_frame)
        button_frame.pack(fill="x", pady=20)

        # Create the process button with the text "Process Weighted Overlay"
        self.process_button = tk.Button(
            button_frame,
            text="Process Weighted Overlay",
            command=self.process_weighted_overlay,
            bg="green",
            fg="white",
            font=Font(family="Arial", size=12, weight="bold"),
            state="disabled",
        )

        # Initially disable the button
        self.process_button.pack(pady=10, padx=20, ipadx=20, ipady=10)

    # Method to process the weighted overlay
    def process_weighted_overlay(self):

        # Create a processing window
        self.processing_window = tk.Toplevel(self.root)
        self.processing_window.title("Processing")
        main_window_width = self.root.winfo_width()
        main_window_height = self.root.winfo_height()
        main_window_x = self.root.winfo_x()
        main_window_y = self.root.winfo_y()
        center_x = main_window_x + (main_window_width // 2)
        center_y = main_window_y + (main_window_height // 2)
        popup_width = 400
        popup_height = 150
        popup_x = center_x - (popup_width // 2)
        popup_y = center_y - (popup_height // 2)

        # Set the geometry of the processing window
        self.processing_window.geometry(
            f"{popup_width}x{popup_height}+{popup_x}+{popup_y}"
        )
        processing_message = tk.Label(
            self.processing_window, text="Script working... please be patient!"
        )
        processing_message.pack(pady=10)
        button_frame = tk.Frame(
            self.processing_window,
            background="red",
            bd=1,
            relief="solid",
            padx=1,
            pady=1,
        )
        button_frame.pack(pady=20)
        self.process_completed_button = tk.Button(
            self.processing_window,
            text="OK",
            state="disabled",
            command=self.processing_window.destroy,
            padx=16,
            pady=7,
            font=("Helvetica", 14, "bold"),
            bg="red",
            fg="white",
            activebackground="dark red",
            activeforeground="white",
            relief="raised",
            borderwidth=2,
        )

        # Pack the process completed button with internal padding
        self.process_completed_button.pack(ipadx=6, ipady=3)
        self.slider_values = self.get_slider_values()

        # Start the weighted overlay in a separate thread
        threading.Thread(target=self.run_weighted_overlay).start()

    # Method to get the slider values
    def get_slider_values(self):
        return [slider.get() for slider in self.sliders]

    # Method to run the weighted overlay
    def run_weighted_overlay(self):

        # Write the slider values to a file
        with open("slider_values.txt", "w") as file:
            file.write(",".join(str(value) for value in self.slider_values))

        # Execute the WeightedOverlayScript.py script
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            subprocess.run(
                ["python", "WeightedOverlayScript.py"], cwd=script_dir, check=True
            )
        except subprocess.CalledProcessError as e:
            print("An error occurred while executing WeightedOverlayScript.py")

        # Enable the process completed button
        self.process_completed_button.config(state="normal")

        # Open the browser window
        if not self.is_browser_open:
            webbrowser.open_new_tab(f"http://localhost:{self.port}/index.html")
            self.is_browser_open = True
        else:
            self.reload_page()

    # Method to check if the total value is valid
    def is_total_valid(self):

        # Calculate the total value of all sliders
        total = sum(slider.get() for slider in self.sliders)
        return total == 100

    # Method to stop the server
    def stop_server(self):

        # Shutdown the server
        self.httpd.shutdown()

        # Join the server thread
        self.server_thread.join()

        # Quit and destroy the Tkinter application
        self.root.quit() 
        self.root.destroy()
        print("Server stopped successfully")

    # Method to refresh the page
    def refresh_page(self):

        # Refresh the page using JavaScript
        refresh_script = (
            f'window.open("http://localhost:{self.port}/index.html", "_self");'
        )
        webbrowser.open(f"javascript:{refresh_script}")

    # Method to reload the page
    def reload_page(self):
        webbrowser.open(f"http://localhost:{self.port}/index.html", new=0)


# Main method to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ParSuitApp(root)
    root.mainloop()
