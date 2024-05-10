import tkinter as tk
from tkinter import scrolledtext
from agents import MAS
import os
from dotenv import load_dotenv
load_dotenv()  # Loads from a '.env' file in the project directory

class Interface:
    def __init__(self, master, mas):
        self.master = master
        self.mas = mas  # MAS instance

        self.master.title("Task Manager Interface")

        # Set up the input field
        self.input_entry = tk.Entry(self.master, width=100)
        self.input_entry.grid(row=0, column=0, padx=10, pady=20, sticky='ew')

        # Set up the button
        self.run_button = tk.Button(self.master, text="Run Manager", command=self.run_manager)
        self.run_button.grid(row=1, column=0, pady=10, sticky='ew')

        # Set up the scrollable output text area
        self.output_text = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, state='disabled')
        self.output_text.grid(row=2, column=0, padx=10, pady=20, sticky='nsew')

        # Configure grid expansion properties
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def run_manager(self):
        user_input = self.input_entry.get()
        output = self.mas.manager(user_input)
        self.output_text.configure(state='normal')
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, output)
        self.output_text.configure(state='disabled')

def main():
    root = tk.Tk()
    api_key = os.getenv("Agent1")  # Ensure you have a default or ensure the key is set
    mas = MAS(api_key)  # Create an instance of MAS
    app = Interface(root, mas)  # Create an instance of the Interface with MAS
    root.mainloop()

if __name__ == "__main__":
    main()