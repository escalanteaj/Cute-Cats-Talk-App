import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import requests
import io
from PIL import Image, ImageTk
import threading  # For handling image loading in a separate thread

# Create a function to fetch cat images from the API
def fetch_cat_image(event=None):
    # Display loading message or animation
    loading_label.config(text="Loading...")
    
    user_input = user_input_entry.get()
    url = f"https://cataas.com/cat/cute/says/{user_input}"
    
    # Create a separate thread to fetch and display the image
    def fetch_image():
        response = requests.get(url)
        if response.status_code == 200:
            image_data = response.content
            # Resize the image to a maximum size of 300px
            img = Image.open(io.BytesIO(image_data))
            img.thumbnail((300, 300))
            img = ImageTk.PhotoImage(img)
            cat_image_label.config(image=img)
            cat_image_label.image = img  # Keep a reference
            loading_label.config(text="")  # Clear loading message
        else:
            loading_label.config(text="Error: Cat couldn't talk. Try again!")

    # Start the thread for image loading
    image_thread = threading.Thread(target=fetch_image)
    image_thread.start()

# Create a function to reset the app
def reset_app():
    user_input_entry.delete(0, tk.END)
    cat_image_label.config(image="")
    cat_image_label.config(text="")
    user_input_entry.focus()

# Create the main application window
app = tk.Tk()
app.title("Cute Cats Talk")
app.geometry("500x600")

# Apply the Radiance (Ubuntu) theme
style = ThemedStyle(app)
style.set_theme("radiance")

# Create a frame for padding and alignment
frame = ttk.Frame(app)
frame.pack(expand=True, fill="both")

# Create a label for the app name
app_name_label = ttk.Label(frame, text="Cute Cats Talk")
app_name_label.pack(fill="x", padx=10, pady=10)

# Create an entry for user input
user_input_label = ttk.Label(frame, text="What does the cat say?")
user_input_label.pack(anchor="w", padx=10, pady=10)
user_input_entry = ttk.Entry(frame)
user_input_entry.pack(fill="x", padx=10, pady=10)

# Bind the <Return> event to the fetch_cat_image function
user_input_entry.bind("<Return>", fetch_cat_image)

# Create a button to fetch cat image
fetch_button = ttk.Button(frame, text="Enter", command=fetch_cat_image)
fetch_button.pack(fill="x", padx=10, pady=10)

# Create a label for displaying loading message or animation
loading_label = ttk.Label(frame, text="")
loading_label.pack(expand=True, fill="both", padx=10, pady=10)

# Create a label for the cat image
cat_image_label = ttk.Label(frame, text="")
cat_image_label.pack(expand=True, fill="both", padx=10, pady=10)

# Create a button to reset the app
reset_button = ttk.Button(frame, text="Reset", command=reset_app)
reset_button.pack(fill="x", padx=10, pady=10)

app.mainloop()
