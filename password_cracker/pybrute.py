import itertools
import hashlib
import tkinter as tk
from tkinter import ttk
import logging
import threading
from PIL import Image, ImageTk

# Set up logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def brute_force_attack(target_hash, result_callback):
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    found = False
    for length in range(1, 8):  # Adjust the range as needed
        logging.debug(f"Trying length {length}")
        for guess in itertools.product(chars, repeat=length):
            guess = ''.join(guess)
            guess_hash = hashlib.sha256(guess.encode()).hexdigest()
            logging.debug(f"Trying password {guess}")
            if guess_hash == target_hash:
                logging.info(f"Password found: {guess}")
                result_callback(guess)
                found = True
                break
        if found:
            break
    if not found:
        result_callback(None)

def on_crack_click():
    target_hash = hash_entry.get()
    if not target_hash:
        show_custom_message("Error", "Please enter a hash to crack.")
        return

    def run_brute_force():
        try:
            logging.info("Starting brute force attack")
            brute_force_attack(target_hash, result_callback)
            logging.info("Brute force attack completed")
        except Exception as e:
            logging.error(f"Error during brute force attack: {e}")
            show_custom_message("Error", f"An error occurred: {e}")

    def result_callback(result):
        if result:
            show_custom_message("Success", f"Password found: {result}")
        else:
            show_custom_message("Failure", "Password not found.")

    thread = threading.Thread(target=run_brute_force)
    thread.start()

def show_custom_message(title, message):
    custom_msg = tk.Toplevel(root)
    custom_msg.title(title)
    custom_msg.geometry("300x150")
    custom_msg.resizable(False, False)
    
    msg_frame = ttk.Frame(custom_msg, padding="10")
    msg_frame.pack(fill='both', expand=True)
    
    msg_label = ttk.Label(msg_frame, text=message, wraplength=280, justify="center")
    msg_label.pack(pady=20)
    
    ok_button = ttk.Button(msg_frame, text="OK", command=custom_msg.destroy)
    ok_button.pack(pady=10)

# Initialize the GUI
root = tk.Tk()
root.title("Password Cracking Suite")
root.geometry("500x400")
root.resizable(False, False)

# Set up style
style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#2e3f4f")
style.configure("TLabel", background="#2e3f4f", foreground="#ffffff", font=("Helvetica", 12))
style.configure("TEntry", padding=5)
style.configure("TButton", background="#4a7a8c", foreground="#ffffff", font=("Helvetica", 12))

# Set background image
bg_image = Image.open("background.jpg")
bg_image = bg_image.resize((500, 400), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = ttk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create and place widgets
frame = ttk.Frame(root, padding="10")
frame.place(relx=0.5, rely=0.5, anchor="center")

hash_label = ttk.Label(frame, text="Enter Hash:")
hash_label.grid(row=0, column=0, pady=5, sticky=tk.W)

hash_entry = ttk.Entry(frame, width=50)
hash_entry.grid(row=1, column=0, pady=5, sticky=(tk.W, tk.E))

crack_button = ttk.Button(frame, text="Crack Password", command=on_crack_click)
crack_button.grid(row=2, column=0, pady=20)

# Run the GUI event loop
root.mainloop()
