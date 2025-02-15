"""
=======================================
Project Title: Image Processing System
Author: Sasarman Darius-Eric
Date: 2025-02-15
Version: 1.0

Description:
    This program processes images and converts them into ASCII art representation.
    It allows the user to upload an image and specify dimensions for the ASCII output.
=======================================
"""
import os.path
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np

# ----------------- Processing functions ----------------- #

# Function to get the directory of the running executable
def get_executable_directory():
    if getattr(sys, 'frozen', False):  # Check if running as a bundled exe
        return os.path.dirname(sys.executable)  # Returns the folder where the exe is extracted
    else:
        return os.path.abspath(os.path.dirname(__file__))  # Script directory if running as a script


def process_image_to_text(path: str, width: str, height: str):
    # The characters used in writing out the final text image
    draw_string = "  `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"  # 92 characters

    result_width = int(width)
    result_height = int(height)
    text = []

    # Opening the image in gray-scale
    img = Image.open(path).convert('L')
    img_width, img_height = img.size

    # Dividing the image in multiple pieces
    sector_width = max(1, img_width // result_width)
    sector_height = max(1, img_height // result_height)

    for i in range(0, img_height, sector_height):
        line = ""
        for j in range(0, img_width, sector_width):
            # Getting the coordinates of the image section
            left = j
            upper = i
            right = min(j + sector_width, img_width)
            lower = min(i + sector_height, img_height)

            # Calculating the average grayscale value
            sector = np.array(img.crop((left, upper, right, lower)))
            avg = np.average(sector)

            # Converting it on our 0-91 scale
            darkness_score = int((1 - avg / 255) * 92)

            line += draw_string[min(darkness_score, 91)]  # Ensuring index is within range
        text.append(line + "\n")

    return "".join(text)

# Adds the text to memory
def append_text_to_memory(text) :
    # Get the file location
    file_path = os.path.join(get_executable_directory(), "history.txt")
    with open(file_path, "a") as file:
        for row in text:
            # Write out each line
            file.write("".join(row))
        # Secure space in between other processed images
        file.write("\n")

# Retrieves the saved text
def get_text_from_memory():
    text = ""
    file_path = os.path.join(get_executable_directory(), "history.txt") # Get the file location
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            for line in file:# Building the string inside the saved, exisitng file
                text = text + line
    return text

# Deletes the file from memory
def delete_memory():
    file_path = os.path.join(get_executable_directory(), "history.txt")
    if os.path.exists(file_path):
        with open(file_path, "w") as file:
            pass

# ----------------- UI ----------------- #
# Create main window
root = tk.Tk()
root.title("Image to text processor")
root.state('zoomed')
root.resizable(True, True)

# Create a Notebook (tab container)
notebook = ttk.Notebook(root)

# Create two separate frames (each acts as a parent for widgets)
tab1 = tk.Frame(notebook)
tab2 = tk.Frame(notebook)

# Add tabs to the Notebook
notebook.add(tab1, text="Image processing")
notebook.add(tab2, text="Text history")

style = ttk.Style()
style.configure("TNotebook.Tab",
                width=root.winfo_screenwidth() // 2,  # Make each tab half the screen width
                anchor="center",  # Ensures text is centered
                padding=(10, 5))  # Adds padding for better centering
notebook.pack(expand=True, fill="both")

# Variables to hold the image path and dimensions
selected_image_path = ""
width_var = ""
length_var = ""

# ----------------- Tab 1 ----------------- #
tab1.grid_columnconfigure(0, weight=1)
tab1.grid_columnconfigure(1, weight=1)
tab1.grid_rowconfigure(0, weight=0)  # Row 0 is for the image, no stretching
tab1.grid_rowconfigure(1, weight=0)  # Row 1 is for the "Select Image" and "Process Image" button
tab1.grid_rowconfigure(2, weight=0)  # Row 2 is for width and length inputs

# Left Half: Image Previewer (reserved space)
image_label = tk.Label(tab1, text="Image will appear here, please select one first")
image_label.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

# Function to update the image preview
def update_image_preview(image_path):
    image = Image.open(image_path)
    image.thumbnail((700, 700))  # Resize to fit within the allocated space
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo, text="")  # Remove default text when image is shown
    image_label.image = photo  # Keep a reference to avoid garbage collection

# Right Half: Controls
# Button to select image
def select_image():
    global selected_image_path
    selected_image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
    if selected_image_path:
        update_image_preview(selected_image_path)

select_image_button = tk.Button(tab1, text="Select Image", command=select_image)
select_image_button.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
select_image_button.grid_propagate(False)
select_image_button.configure(height=1)  # Set desired height

def on_focus_in(event, var_name):
    widget = event.widget
    if widget.get() == var_name:
        widget.delete(0, tk.END)

def on_focus_out(event, var_name):
    widget = event.widget
    if widget.get() == "":
        widget.insert(0, var_name)

# Width Text Field
width_text = tk.Entry(tab1)
width_text.insert(0, "Please insert the width")
width_text.bind("<FocusIn>", lambda event: on_focus_in(event, "Please insert the width"))
width_text.bind("<FocusOut>", lambda event: on_focus_out(event, "Please insert the width"))
width_text.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

# Length Text Field
length_text = tk.Entry(tab1)
length_text.insert(0, "Please insert the height")
length_text.bind("<FocusIn>", lambda event: on_focus_in(event, "Please insert the height"))
length_text.bind("<FocusOut>", lambda event: on_focus_out(event, "Please insert the height"))
length_text.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

# Function to store the width and length values
def store_dimensions():
    global width_var, length_var
    width_var = width_text.get()
    length_var = length_text.get()

# Process Image Button
def process_image():
    store_dimensions()
    if selected_image_path == "":
        messagebox.showerror("Error","No image selected")
    elif width_var == "" or width_var.isdigit() == 0:
        messagebox.showerror("Error","Invalid width")
    elif length_var == "" or length_var.isdigit() == 0:
        messagebox.showerror("Error","Invalid length")
    else:
        # Create result window
        result = tk.Tk()
        result.resizable(True, True)
        result.title("Image Processing Result")

        # Configure grid for the root window
        result.grid_columnconfigure(0, weight=1)
        result.grid_rowconfigure(0, weight=1)

        # Create frame to hold text area and scrollbars
        frame = tk.Frame(result)
        frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

        # Configure frame layout
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Create text widget with scrollbars
        result_scrollbar = tk.Scrollbar(frame, orient="vertical")
        result_scrollbar2 = tk.Scrollbar(frame, orient="horizontal")
        text_area_result = tk.Text(frame, wrap="none", state="disabled", yscrollcommand=result_scrollbar.set, xscrollcommand=result_scrollbar2.set)

        # Link scrollbars to text widget
        result_scrollbar.config(command=text_area_result.yview)
        result_scrollbar2.config(command=text_area_result.xview)

        # Grid the text widget and scrollbars
        text_area_result.grid(row=0, column=0, sticky="nsew")
        result_scrollbar.grid(row=0, column=1, sticky="ns")
        result_scrollbar2.grid(row=1, column=0, sticky="ew")

        # Insert processed image text
        text_area_result.configure(state="normal")
        text_area_result.delete(1.0, tk.END)
        processed_text = process_image_to_text(selected_image_path, width_var, length_var)
        text_area_result.insert(1.0, processed_text)
        text_area_result.configure(state="disabled")

        # Save button (with corrected command)
        save_button = tk.Button(result, text="Save Image", command=lambda:append_text_to_memory(processed_text))
        save_button.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        # Close button
        close_button = tk.Button(result, text="Close Window", command=result.destroy)
        close_button.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

        result.mainloop()


process_button = tk.Button(tab1, text="Process Image", command=process_image)
process_button.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
process_button.grid_propagate(False)
process_button.configure(height=1)  # Set desired height

# Make the right half take up the necessary space
tab1.grid_columnconfigure(1, weight=1)

# ----------------- Tab 2 ----------------- #
# Create a frame to hold the text widget and button
tab2.grid_rowconfigure(0, weight=1)
tab2.grid_columnconfigure(0, weight=1)

# Create a Scrollbar and Text widget
scrollbar = tk.Scrollbar(tab2,orient="vertical")
scrollbar2= tk.Scrollbar(tab2, orient="horizontal")
text_area = tk.Text(tab2, wrap="none", state="disabled", yscrollcommand=scrollbar.set, xscrollcommand=scrollbar2.set,width=50, height=20)
text_area.grid(row=0, column=0, sticky="nsew")

# Configure the scrollbar
scrollbar.config(command=text_area.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

scrollbar2.config(command=text_area.xview)
scrollbar2.grid(row=1, column=0, sticky="ew")
#get text from file

# Delete Button (spanning the full width at the bottom)
def on_delete_click():
    delete_memory()
    text_area.config(state="normal")  # Enable text for modification
    text_area.delete("1.0", tk.END)   # Clear the content
    text_area.config(state="disabled")  # Disable editing again

delete_button = tk.Button(tab2, text="Delete History", command=on_delete_click)
delete_button.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

# Function to write a string into the text area
def write_text():
    string = get_text_from_memory()
    text_area.config(state="normal")  # Enable text for writing
    text_area.delete("1.0", tk.END)   # Clear any existing text
    text_area.insert("1.0", string)   # Insert new text
    text_area.config(state="disabled")  # Disable editing again

# Make the button take up only the necessary space
tab2.grid_columnconfigure(1, weight=0)

def on_tab_selected(event):
    selected_tab = event.widget.index(event.widget.select())  # Get the index of the selected tab
    if selected_tab == 1:  # Tab 2 is at index 1
        write_text()

notebook.bind("<<NotebookTabChanged>>", on_tab_selected)

root.mainloop()
