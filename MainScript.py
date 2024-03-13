import tkinter as tk
from PIL import Image, ImageTk

def slider_moved(slider_index, value):
    global sliders, total_label
    # Convert value to integer
    value = int(value)
    # Calculate the current total excluding the moved slider
    current_total = sum(slider.get() for i, slider in enumerate(sliders) if i != slider_index)
    max_allowed = 100 - current_total
    if value > max_allowed:
        # Set the slider to the maximum allowed value if the new value is too high
        sliders[slider_index].set(max_allowed)
        # Update the total display
        total_label.config(text=f"Total: 100/100")
    else:
        # Update the total display normally
        total_label.config(text=f"Total: {current_total + value}/100")

root = tk.Tk()
root.title("ParSuit")  # Main title

# Subtitle label with styling
subtitle_label = tk.Label(root, text="Suitability Analysis for the Hartford Capitol Region",
                          font=("Arial", 18, "bold")) 
subtitle_label.pack()

# Load the image (we'll resize later)
image = Image.open(r"C:\Users\cwalinskid\Desktop\CRCOG Project\ParSuit\CRCOG.jpg")

# Resize the image
resized_image = image.resize((650, 500), Image.ANTIALIAS)  # Adjust width and height as desired

# Convert to PhotoImage
photo = ImageTk.PhotoImage(resized_image)

# Create the label with the resized image
image_label = tk.Label(root, image=photo)
image_label.pack()


sliders = []
for i in range(8):
    # Create a frame to hold the label and the slider
    frame = tk.Frame(root)
    frame.pack(fill='x')

    # Create and pack the label to the left side of the frame
    label = tk.Label(frame, text=f"Slider {i + 1}")
    label.pack(side='left')

    # Create and pack the slider to fill the rest of the frame
    slider = tk.Scale(frame, from_=0, to=100, orient='horizontal', command=lambda value, i=i: slider_moved(i, value))
    slider.pack(side='left', fill='x', expand=True)
    sliders.append(slider)

total_label = tk.Label(root, text="Total: 0/100")
total_label.pack()

root.mainloop()
