import tkinter as tk

class Interface():
    def __init__(self, macro):
        self.macro = macro

    def start(self):
        self.window = tk.Tk()
        self.window.title("Macro Interface")
        self.window.geometry("300x200")
        
        self.path_label = tk.Label(self.window, text="Current Path: None")
        self.path_label.pack()

        # Create buttons for each macro function
        tk.Button(self.window, text="Start", command=self.macro.start).pack()
        tk.Button(self.window, text="Restart", command=self.macro.restart).pack()