import tkinter as tk
from tkinter import Label, Entry, Button


def save_keys():
    api_key = api_key_entry.get()
    api_secret = api_secret_entry.get()
    # You can save these keys to a file, a database, or use them as needed.
    print("API Key:", api_key)
    print("API Secret:", api_secret)
    # Optionally, save the keys to a file or perform any other action.


root = tk.Tk()
root.title("Binance API Key Setup")
root.geometry("300x150")


api_key_label = Label(root, text="Binance API Key:")
api_key_label.pack()
api_key_entry = Entry(root)
api_key_entry.pack()

api_secret_label = Label(root, text="API Secret Key:")
api_secret_label.pack()
api_secret_entry = Entry(root, show="*")  # The show option hides the entered text
api_secret_entry.pack()

save_button = Button(root, text="Save Keys", command=save_keys)
save_button.pack()

root.mainloop()



