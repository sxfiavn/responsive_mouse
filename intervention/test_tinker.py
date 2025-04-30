import tkinter as tk

def show_ui():
    root = tk.Tk()
    root.title("Test Popup")
    root.geometry("400x300")

    label = tk.Label(root, text="You seem stressed.\nTake a deep breath.", font=("Arial", 16))
    label.pack(pady=60)

    button = tk.Button(root, text="Start Breathing", command=root.destroy)
    button.pack(pady=20)

    root.mainloop()

show_ui()
# This code creates a simple Tkinter UI with a label and a button.