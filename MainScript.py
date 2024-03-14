import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class ParSuitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ParSuit")
        self.sliders = []
        self.setup_ui()
    
    def setup_ui(self):
        self.root.geometry("650x700")  # Set initial size
        
        container = ttk.Frame(self.root)
        container.pack(side='top', fill='both', expand=True)

        self.canvas = tk.Canvas(container)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Save the window ID for later reference
        self.scrollable_frame_window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.load_and_display_image()
        self.create_sliders()

        self.total_label = tk.Label(self.root, text="Total: 0/100")
        self.total_label.pack(side='bottom')

        # Bind the resize event to dynamically adjust the scrollable frame position
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

    def create_sliders(self):
        for i in range(8):  # Assuming you have 8 sliders
            frame = tk.Frame(self.scrollable_frame)
            frame.pack(fill='x', pady=2)
            label = tk.Label(frame, text=f"Slider {i + 1}")
            label.pack(side='left', padx=(0, 10))
            slider = tk.Scale(frame, from_=0, to=100, orient='horizontal', command=lambda value, i=i: self.slider_moved(i, value))
            slider.pack(side='left', fill='x', expand=True)
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
