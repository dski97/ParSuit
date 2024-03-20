import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from PIL import Image, ImageTk
import threading

class Configuration:
    SLIDER_NAMES = [
        'Away from Brownfields', 'Buildable Soil', 'Away from Floodzones',
        'Proximity to Hospitals', 'Proximity to Police Stations',
        'Proximity to Roads', 'Proximity to Schools', 'Public Sewer',
        'Low Grade Slope', 'Away from Wetlands', 'Appropriate Land Use'
    ]
    IMAGE_PATH = r"C:\Users\cwalinskid\Desktop\CRCOG Project\ParSuit\CRCOG.jpg"
    TITLE_TEXT = "Suitability Analysis for Hartford Capitol Region"
    GEOGRAPHIC_ANALYSIS_TEXT = "Explore the Hartford Capitol Region with ParSuit, your guide to informed land suitability analysis. This tool empowers you to prioritize geographic and environmental factors with simple slider adjustments. From safeguarding against environmental risks to enhancing access to essential services, your input directly shapes the analysis. Once you've set your preferences, a single click reveals a comprehensive map, visualizing the most suitable parcels according to your criteria. ParSuit combines precision with simplicity, offering a clear path to insightful, actionable data for your projects."
    PRESETS = ["Balanced", "Urban-Intensified", "Rural Favorite", "Community-Based", "Lone Star Ranger"]
    PRESET_VALUES = {
        "Balanced": [9] * 10 + [10],
        "Urban-Intensified": [3, 3, 3, 14, 14, 14, 8, 14, 3, 3, 21],
        "Rural Favorite": [14, 14, 14, 3, 3, 3, 9, 3, 14, 14, 9],
        "Community-Based": [3, 9, 3, 16, 16, 11, 16, 9, 3, 2, 12],
        "Lone Star Ranger": [16, 12, 16, 3, 3, 3, 3, 3, 12, 16, 13]
    }
    NUM_SLIDERS = len(SLIDER_NAMES)

class ParSuitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ParSuit")
        self.sliders = []
        self.setup_ui()
        self.center_window()

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

    def create_title(self):
        title_font = Font(family="Helvetica", size=16, weight="bold")
        tk.Label(self.root, text=Configuration.TITLE_TEXT, font=title_font).pack(side='top', pady=(10, 20))

    def create_main_container(self):
        container = ttk.Frame(self.root)
        container.pack(side='top', fill='both', expand=True)
        self.canvas = tk.Canvas(container)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.scrollable_frame_window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

    def load_and_display_image(self):
        image = Image.open(Configuration.IMAGE_PATH)
        resized_image = image.resize((650, 500), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized_image)
        image_label = tk.Label(self.scrollable_frame, image=photo)
        image_label.image = photo
        image_label.pack(pady=20)

    def create_info_text(self):
        heading_font = Font(family="Helvetica", size=14, weight="bold")
        tk.Label(self.scrollable_frame, text="Welcome to the ParSuit Application!", font=heading_font).pack(pady=(10, 2))
        tk.Label(self.scrollable_frame, text=Configuration.GEOGRAPHIC_ANALYSIS_TEXT, wraplength=600, justify="center").pack(pady=(0, 20))
        self.create_presets_combobox()

    def create_presets_combobox(self):
        tk.Label(self.scrollable_frame, text="Adjust the criteria based on your needs or select custom presets made for certain scenarios").pack(pady=(10, 2))
        self.preset_combobox = ttk.Combobox(self.scrollable_frame, values=Configuration.PRESETS, state="readonly")
        self.preset_combobox.set("Custom Presets")
        self.preset_combobox.pack(pady=(0, 20))
        self.preset_combobox.bind("<<ComboboxSelected>>", self.on_preset_selected)

    def create_importance_key(self):
        key_frame = tk.Frame(self.scrollable_frame)
        key_frame.pack(fill='x', pady=(10, 0), expand=False)

        less_important_label = tk.Label(key_frame, text="Less Important", fg="red", anchor='w', padx=120)
        less_important_label.pack(side='left')

        more_important_label = tk.Label(key_frame, text="More Important", fg="red", anchor='e')
        more_important_label.pack(side='right')

    def create_sliders(self):
        for index, name in enumerate(Configuration.SLIDER_NAMES):
            self.create_slider(name, index)

    def create_slider(self, name, index):
        frame = tk.Frame(self.scrollable_frame)
        frame.pack(fill='x', pady=2, expand=False)
        label = tk.Label(frame, text=name, anchor='w', width=20)
        label.grid(row=0, column=0, sticky='w')
        slider = tk.Scale(frame, from_=0, to=100, orient='horizontal', length=400,
                          command=lambda value, index=index: self.update_total(index, value))
        slider.grid(row=0, column=1, sticky='ew')
        frame.grid_columnconfigure(1, weight=1)
        self.sliders.append(slider)

    def update_total(self, moved_index, value):
        total = sum(slider.get() for i, slider in enumerate(self.sliders) if i != moved_index)
        moved_value = int(value)
        if total + moved_value > 100:
            excess = total + moved_value - 100
            new_value = moved_value - excess
            self.sliders[moved_index].set(new_value)
            total = 100
        else:
            total += moved_value

        self.total_label.config(text=f"Total: {total}/100")

        # Enable or disable the process button based on the total value
        if self.is_total_valid():
            self.process_button.config(state='normal')
        else:
            self.process_button.config(state='disabled')

    def on_preset_selected(self, event):
        selected_preset = self.preset_combobox.get()
        self.apply_preset_values(selected_preset)

    def apply_preset_values(self, preset):
        selected_values = Configuration.PRESET_VALUES.get(preset, [0] * Configuration.NUM_SLIDERS)
        for slider, value in zip(self.sliders, selected_values):
            slider.set(value)

    def create_total_label(self):
        total_label_font = Font(family="Times New Roman", size=16, weight="bold")
        self.total_label = tk.Label(self.root, text="Total: 0/100", font=total_label_font)
        self.total_label.pack(side='bottom')

    def create_glossary(self):
        glossary_frame = tk.Frame(self.scrollable_frame)
        glossary_frame.pack(fill='x', pady=20)

        glossary_title_font = Font(family="Arial", size=14, weight="bold")
        glossary_title = tk.Label(glossary_frame, text="Glossary", font=glossary_title_font)
        glossary_title.pack(side='top')

        term_font = Font(family="Arial", size=12, weight="bold", slant="italic")

        glossary_terms = {
            'Away from Brownfields': 'Indicates the degree to which the land is inclined, affecting construction and drainage.',
            'Buildable Soil': 'Refers to soil with properties conducive to agriculture or construction.',
            'Away from Flood Zones': 'Areas less likely to experience flooding, reducing risk of water damage.',
            'Proximity to Hospitals': 'Distance from medical facilities, affecting emergency response times.',
            'Proximity to Police Stations': 'Distance from law enforcement, affecting crime rates and safety.',
            'Proximity to Roads': 'Distance from roads, affecting accessibility and noise pollution.',
            'Proximity to Schools': 'Distance from educational institutions, affecting property values and child safety.',
            'Public Sewer': 'Availability of immediate access to public sewer systems.',
            'Low Grade Slope': 'Indicates the degree to which the land is flat and suitable for construction.',
            'Away from Wetlands': 'Distance from wetlands, affecting environmental impact and land use.',
            'Appropriate Land Use': 'Refers to the suitability of the land for specific purposes such as residential, commercial, or industrial.'
        }

        glossary_text = tk.Text(glossary_frame, wrap=tk.WORD, width=70, height=20)
        glossary_scrollbar = tk.Scrollbar(glossary_frame, command=glossary_text.yview, width=22)
        glossary_text.configure(yscrollcommand=glossary_scrollbar.set)

        for term, explanation in glossary_terms.items():
            glossary_text.insert(tk.END, f"{term} - ", 'term')
            glossary_text.insert(tk.END, f"{explanation}\n\n")

        glossary_text.tag_configure('term', font=term_font)

        glossary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        glossary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def on_window_resize(self, event=None):
        canvas_width = self.canvas.winfo_width()
        frame_width = self.scrollable_frame.winfo_reqwidth()
        new_x_position = max((canvas_width - frame_width) / 2, 0)
        self.canvas.coords(self.scrollable_frame_window_id, new_x_position, 0)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')

    def update_scroll(self):
        self.root.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_processing_button(self):
        button_frame = tk.Frame(self.scrollable_frame)
        button_frame.pack(fill='x', pady=20)

        self.process_button = tk.Button(button_frame, text="Process Weighted Overlay",
                                        command=self.process_weighted_overlay,
                                        bg='green', fg='white',
                                        font=Font(family="Arial", size=12, weight="bold"),
                                        state='disabled')  # Initially disable the button
        self.process_button.pack(pady=10, padx=20, ipadx=20, ipady=10)

    def process_weighted_overlay(self):
        self.processing_window = tk.Toplevel(self.root)
        self.processing_window.title("Processing")

        # Calculate the center coordinates of the main window
        main_window_width = self.root.winfo_width()
        main_window_height = self.root.winfo_height()
        main_window_x = self.root.winfo_x()
        main_window_y = self.root.winfo_y()
        center_x = main_window_x + (main_window_width // 2)
        center_y = main_window_y + (main_window_height // 2)

        # Set the dimensions and position of the popup window
        popup_width = 400
        popup_height = 150
        popup_x = center_x - (popup_width // 2)
        popup_y = center_y - (popup_height // 2)
        self.processing_window.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")

        processing_message = tk.Label(self.processing_window, text="Script working... please be patient!")
        processing_message.pack(pady=10)

        button_frame = tk.Frame(self.processing_window, background='red', bd=1, relief='solid', padx=1, pady=1)
        button_frame.pack(pady=20)

        self.process_completed_button = tk.Button(self.processing_window, text="OK", state='disabled',
                                                command=self.processing_window.destroy,
                                                padx=16, pady=7,
                                                font=('Helvetica', 14, 'bold'),
                                                bg='red', fg='white',
                                                activebackground='dark red', activeforeground='white',
                                                relief='raised', borderwidth=2)
        self.process_completed_button.pack(ipadx=6, ipady=3)

        threading.Thread(target=self.run_weighted_overlay).start()

    def run_weighted_overlay(self):
        # Simulate a long-running task
        # Replace this with your actual function to perform the weighted overlay
        # time.sleep(5) or any long-running task

        # After completing the task, enable the OK button
        self.process_completed_button.config(state='normal')

    
    def is_total_valid(self):
        total = sum(slider.get() for slider in self.sliders)
        return total == 100

if __name__ == "__main__":
    root = tk.Tk()
    app = ParSuitApp(root)
    root.mainloop()