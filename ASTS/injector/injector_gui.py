import tkinter as tk
from tkinter import messagebox

def spoof_hwid():
    # Simulate HWID spoofing
    messagebox.showinfo("HWID Spoofing", "New HWID set successfully.")
    inject_button.config(state=tk.NORMAL)

def inject():
    # Simulate DLL injection
    messagebox.showinfo("Injection", "Injection successful. You can now remove the flash drive and load the game.")
    root.destroy()

root = tk.Tk()
root.title("ASTS Injector")

spoof_button = tk.Button(root, text="Spoof HWID", command=spoof_hwid)
spoof_button.pack(pady=10)

inject_button = tk.Button(root, text="Inject", command=inject, state=tk.DISABLED)
inject_button.pack(pady=10)

root.mainloop()
