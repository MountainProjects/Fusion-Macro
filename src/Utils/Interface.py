import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import tkinter.messagebox as messagebox

import threading
from pynput.keyboard import Key, Listener

class Interface():
    def __init__(self, macro):
        self.macro = macro
        self.window = None
        self.fieldDropdown = None
        self.patternDropdown = None
        self.pathDropdown = None
        self.selectedField = None
        self.selectedPattern = None
        self.selectedPath = None
        self.playStopButton = None

    def on_key_press(self, key):
        if key == Key.f5:
            self.toggleMacro()

    def to_async(self):
        with Listener(on_press = lambda key: self.on_key_press(key)) as listener:
            listener.join()

    def start(self):
        threading.Thread(target=self.to_async).start()

        self.window = tk.Tk()
        self.window.title("Fusion Macro")
        self.window.geometry("400x300")  # slightly taller for path selector
        self.window.resizable(False, False)

        self.window.bind("<F5>", lambda event: self.toggleMacro())
        self.window.iconbitmap("src/assets/Icon.ico")

        self.selectedField = tk.StringVar()
        self.selectedPattern = tk.StringVar()
        self.selectedPath = tk.StringVar()

        buttonFont = tkFont.Font(size=14, weight="bold")

        mainFrame = tk.Frame(self.window, padx=20, pady=20)
        mainFrame.pack(expand=True)

        fieldFrame = ttk.LabelFrame(mainFrame, text="Field Selection", padding=(10, 10))
        fieldFrame.pack(fill="x", pady=10)

        # Field selector
        ttk.Label(fieldFrame, text="Select Field:").pack(anchor="w")
        fieldNames = [f["name"] for f in self.macro.field.database.getAll()]
        print(self.macro.field.database.getAll())

        self.fieldDropdown = ttk.Combobox(
            fieldFrame,
            textvariable=self.selectedField,
            values=fieldNames,
            state="readonly",
            width=30
        )
        self.fieldDropdown.pack(pady=5)
        self.fieldDropdown.bind("<<ComboboxSelected>>", self.onFieldSelected)

        # Pattern selector (initially disabled)
        ttk.Label(fieldFrame, text="Select Pattern:").pack(anchor="w", pady=(10, 0))
        self.patternDropdown = ttk.Combobox(
            fieldFrame,
            textvariable=self.selectedPattern,
            values=["Select field first"],
            state="disabled",
            width=30
        )
        self.patternDropdown.pack(pady=5)
        self.patternDropdown.bind("<<ComboboxSelected>>", self.onPatternSelected)

        # Path selector (initially disabled)
        ttk.Label(fieldFrame, text="Select Path:").pack(anchor="w", pady=(10, 0))
        self.pathDropdown = ttk.Combobox(
            fieldFrame,
            textvariable=self.selectedPath,
            values=["Select field first"],
            state="disabled",
            width=30
        )
        self.pathDropdown.pack(pady=5)
        self.pathDropdown.bind("<<ComboboxSelected>>", self.onPathSelected)

        # Controls frame
        controlFrame = tk.Frame(mainFrame)
        controlFrame.pack(pady=5)

        self.playStopButton = tk.Button(
            controlFrame,
            text="Play (F5)",
            height=3,
            width=20,
            bg="#4CAF50",
            fg="white",
            command=self.toggleMacro
        )
        self.playStopButton.pack(ipady=10)

        self.updatePlayStopButton()

        self.window.after(200, self.pollMacroState)
        self.window.mainloop()

    def onFieldSelected(self, event):
        fieldName = self.selectedField.get()
        fieldData = self.macro.field.get(fieldName)
        if fieldData:
            # Enable and update patterns dropdown
            patterns = fieldData.get("patterns", [])
            patternNames = [p["name"] for p in patterns]
            if patternNames:
                self.patternDropdown["values"] = patternNames
                self.patternDropdown.config(state="readonly")
                self.selectedPattern.set(patternNames[0])
                self.macro.pattern.set(patterns[0]["id"])
            else:
                self.patternDropdown["values"] = []
                self.patternDropdown.config(state="disabled")
                self.selectedPattern.set("")
                self.macro.pattern.set(None)

            # Enable and update paths dropdown
            paths = fieldData.get("paths", [])
            pathNames = [p["name"] for p in paths]
            if pathNames:
                self.pathDropdown["values"] = pathNames
                self.pathDropdown.config(state="readonly")
                self.selectedPath.set(pathNames[0])
                self.macro.path.set(paths[0]["id"])
            else:
                self.pathDropdown["values"] = []
                self.pathDropdown.config(state="disabled")
                self.selectedPath.set("")
                self.macro.path.set(None)
        else:
            # No field selected: reset and disable pattern dropdown
            self.patternDropdown["values"] = ["Select field first"]
            self.patternDropdown.config(state="disabled")
            self.selectedPattern.set("")
            self.macro.pattern.set(None)

            # Reset and disable path dropdown
            self.pathDropdown["values"] = ["Select field first"]
            self.pathDropdown.config(state="disabled")
            self.selectedPath.set("")
            self.macro.path.set(None)

    def onPatternSelected(self, event):
        fieldName = self.selectedField.get()
        fieldData = self.macro.field.get(fieldName)
        if not fieldData:
            return

        selectedPatternName = self.selectedPattern.get()
        for pattern in fieldData.get("patterns", []):
            if pattern["name"] == selectedPatternName:
                self.macro.pattern.set(pattern["id"])
                break

    def onPathSelected(self, event):
        fieldName = self.selectedField.get()
        fieldData = self.macro.field.get(fieldName)
        if not fieldData:
            return

        selectedPathName = self.selectedPath.get()
        for path in fieldData.get("paths", []):
            if path["name"] == selectedPathName:
                self.macro.path.set(path["id"])
                break

    def toggleMacro(self):
        if self.macro.started:
            self.macro.end()
        else:
            if not self.selectedField.get():
                messagebox.showwarning("Warning", "Please select a field first.")
                return
            
            self.macro.restart()

        self.updatePlayStopButton()

    def updatePlayStopButton(self):
        label = "Stop (F5)" if self.macro.started else "Play (F5)"
        color = "#F44336" if self.macro.started else "#4CAF50"
        self.playStopButton.config(text=label, bg=color)

    def pollMacroState(self):
        self.updatePlayStopButton()
        self.window.after(200, self.pollMacroState)
