import os
from PIL import Image, ImageOps
import tkinter as tk
from tkinter import filedialog, messagebox


def convert_image(input_path, output_path):
    with Image.open(input_path) as im:
        # Crop naar 64 x 48 aspect ratio
        aspect_ratio = 5 / 3
        width, height = im.size
        current_ratio = width / height
        if current_ratio > aspect_ratio:
            new_width = int(height * aspect_ratio)
            left = (width - new_width) // 2
            right = left + new_width
            box = (left, 0, right, height)
        else:
            new_height = int(width / aspect_ratio)
            top = (height - new_height) // 2
            bottom = top + new_height
            box = (0, top, width, bottom)
        im = im.crop(box)

        # Schaal de afbeelding naar 400 x 240 zonder vervorming
        target_size = (400, 240)
        im = ImageOps.fit(im, target_size, method=Image.LANCZOS)

        # Opslaan als JPG
        if im.format != "JPEG":
            im = im.convert("RGB")
        im.save(output_path, format="JPEG", quality=20, optimize=True)


def main(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png") or filename.endswith(".webp"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".jpg")
            convert_image(input_path, output_path)

# Functie om de totale aantal bestanden te tellen
def count_files(files):
    count = 0
    for file in files:
        if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png') or file.endswith('.webp'):
            count += 1
    return count

# Functie om de conversie uit te voeren
def convert(input_folder, output_folder):
    try:
        main(input_folder, output_folder)

        messagebox.showinfo("Succesvol geconverteerd", "De bestanden zijn succesvol geconverteerd!")
    except:
        messagebox.showerror("Fout", "Er is een fout opgetreden tijdens de conversie.")

# Functie voor het selecteren van de map en bijwerken van de teller
def select_folder(folder_type, label):
    folder = filedialog.askdirectory()
    if folder:
        files = os.listdir(folder)
        if folder_type == "input":
            count = count_files(files)
            label.config(text="Bestanden gevonden: " + str(count))
            input_var.set(folder)
        elif folder_type == "output":
            output_var.set(folder)

# Maak het venster aan
root = tk.Tk()
root.title("Converteer afbeeldingen")

# Maak de widgets aan
input_label = tk.Label(root, text="Selecteer de invoermap:")
input_var = tk.StringVar()
input_entry = tk.Entry(root, textvariable=input_var, width=50)
input_button = tk.Button(root, text="Bladeren...", command=lambda: select_folder("input", file_count_label))

output_label = tk.Label(root, text="Selecteer de uitvoermap:")
output_var = tk.StringVar()
output_entry = tk.Entry(root, textvariable=output_var, width=50)
output_button = tk.Button(root, text="Bladeren...", command=lambda: select_folder("output", file_count_label))

file_count_label = tk.Label(root, text="Bestanden gevonden: 0")

convert_button = tk.Button(root, text="Converteren", command=lambda: convert(input_var.get(), output_var.get()))

status_label = tk.Label(root, text="")

# Plaats de widgets in het venster
input_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
input_entry.grid(row=1, column=0, padx=5, pady=5)
input_button.grid(row=1, column=1, padx=5, pady=5)

output_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
output_entry.grid(row=3, column=0, padx=5, pady=5)
output_button.grid(row=3, column=1, padx=5, pady=5)

file_count_label.grid(row=4, column=0, padx=5, pady=5)

convert_button.grid(row=5, column=0, padx=5, pady=5)

status_label.grid(row=6, column=0, padx=5, pady=5)

# Start het venster
root.mainloop()