import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import tkinter.messagebox as messagebox

import threading
from pynput.keyboard import Key, Listener

import var

from pysondb import db

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

        # Initialize pysondb database for settings
        self.settings_db = db.getDb("settings.json")

    def on_key_press(self, key):
        if key == Key.f5:
            self.toggleMacro()

    def to_async(self):
        with Listener(on_press = lambda key: self.on_key_press(key)) as listener:
            listener.join()

    def start(self):
        threading.Thread(target=self.to_async, daemon=True).start()

        self.window = tk.Tk()
        self.window.title("Fusion Macro")
        self.window.geometry("500x300")
        self.window.resizable(False, False)

        self.window.bind("<F5>", lambda event: self.toggleMacro())
        self.window.iconbitmap("src/assets/Icon.ico")

        self.selectedField = tk.StringVar()
        self.selectedPattern = tk.StringVar()
        self.selectedPath = tk.StringVar()

        buttonFont = tkFont.Font(size=14, weight="bold")

        notebook = ttk.Notebook(self.window)
        notebook.pack(expand=True, fill="both")

        # --- Field Tab ---
        fieldTab = ttk.Frame(notebook, padding=10)
        notebook.add(fieldTab, text="Field")

        # LabelFrame for Field selection
        fieldFrame = ttk.LabelFrame(fieldTab, text="Field")
        fieldFrame.pack(fill="x", pady=10, padx=10)

        ttk.Label(fieldFrame, text="Select Field:").grid(row=0, column=0, sticky="w", padx=5, pady=(5, 2))
        fieldNames = [f["name"] for f in self.macro.field.database.getAll()]

        self.fieldDropdown = ttk.Combobox(
            fieldFrame,
            textvariable=self.selectedField,
            values=fieldNames,
            state="readonly",
            width=30
        )
        self.fieldDropdown.grid(row=0, column=1, padx=5, pady=(5, 2))
        self.fieldDropdown.bind("<<ComboboxSelected>>", self.onFieldSelected)

        ttk.Label(fieldFrame, text="Select Pattern:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.patternDropdown = ttk.Combobox(
            fieldFrame,
            textvariable=self.selectedPattern,
            values=["Select field first"],
            state="disabled",
            width=30
        )
        self.patternDropdown.grid(row=1, column=1, padx=5, pady=2)
        self.patternDropdown.bind("<<ComboboxSelected>>", self.onPatternSelected)

        ttk.Label(fieldFrame, text="Select Path:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.pathDropdown = ttk.Combobox(
            fieldFrame,
            textvariable=self.selectedPath,
            values=["Select field first"],
            state="disabled",
            width=30
        )
        self.pathDropdown.grid(row=2, column=1, padx=5, pady=2)
        self.pathDropdown.bind("<<ComboboxSelected>>", self.onPathSelected)

        # LabelFrame for Play controls in the Field tab
        playFrame = ttk.LabelFrame(fieldTab, text="Play")
        playFrame.pack(fill="x", pady=5, padx=10)  # reduced vertical padding

        self.playStopButton = tk.Button(
            playFrame,
            text="Play (F5)",
            height=1,
            width=15,
            bg="#4CAF50",
            fg="white",
            command=self.toggleMacro
        )
        self.playStopButton.pack(ipady=5, pady=5)  # smaller vertical internal padding and pady

        self.updatePlayStopButton()

        # --- Settings Tab ---
        settingsTab = ttk.Frame(notebook, padding=10)
        notebook.add(settingsTab, text="Settings")

        settingsFrame = ttk.LabelFrame(settingsTab, text="Settings")
        settingsFrame.pack(fill="x", pady=10, padx=10)

        # Load saved walkspeed and max farming time from db or fallback to var values
        saved_speed_record = self.settings_db.getByQuery({"key": "walkspeed"})
        if saved_speed_record:
            saved_speed = saved_speed_record[0]["value"]
            var.movespeed = saved_speed
        else:
            saved_speed = var.movespeed

        saved_time_record = self.settings_db.getByQuery({"key": "max_farming_time"})
        if saved_time_record:
            saved_max_time = saved_time_record[0]["value"]
            var.max_farming_time = saved_max_time
        else:
            saved_max_time = getattr(var, "max_farming_time", 60)
            var.max_farming_time = saved_max_time

        self.walkspeedVar = tk.StringVar(value=str(saved_speed))
        self.maxFarmingTimeVar = tk.StringVar(value=str(saved_max_time))

        def validate_positive_int(new_value):
            if new_value == "":
                return True
            try:
                val = int(new_value)
                return val >= 0
            except ValueError:
                return False

        def on_walkspeed_focus_out(event):
            val = self.walkspeedVar.get()
            if val == "":
                self.walkspeedVar.set(str(var.movespeed))
            else:
                val_int = int(val)
                self.walkspeedVar.set(str(val_int))
                var.movespeed = val_int

                existing = self.settings_db.getByQuery({"key": "walkspeed"})
                if existing:
                    self.settings_db.updateById(existing[0]["id"], {"key": "walkspeed", "value": val_int})
                else:
                    self.settings_db.add({"key": "walkspeed", "value": val_int})

        def on_max_time_focus_out(event):
            val = self.maxFarmingTimeVar.get()
            if val == "":
                self.maxFarmingTimeVar.set(str(var.max_farming_time))
            else:
                val_int = int(val)
                self.maxFarmingTimeVar.set(str(val_int))
                var.max_farming_time = val_int

                existing = self.settings_db.getByQuery({"key": "max_farming_time"})
                if existing:
                    self.settings_db.updateById(existing[0]["id"], {"key": "max_farming_time", "value": val_int})
                else:
                    self.settings_db.add({"key": "max_farming_time", "value": val_int})

        vcmd = (self.window.register(validate_positive_int), '%P')

        walkspeedEntry = tk.Entry(
            settingsFrame,
            textvariable=self.walkspeedVar,
            width=5,
            justify="center",
            font=tkFont.Font(size=12, weight="bold"),
            validate='key',
            validatecommand=vcmd
        )
        walkspeedEntry.grid(row=0, column=0, padx=5)
        walkspeedEntry.bind("<FocusOut>", on_walkspeed_focus_out)

        ttk.Label(settingsFrame, text="Walkspeed").grid(row=0, column=1, sticky="w", padx=5, pady=5)

        maxTimeEntry = tk.Entry(
            settingsFrame,
            textvariable=self.maxFarmingTimeVar,
            width=5,
            justify="center",
            font=tkFont.Font(size=12, weight="bold"),
            validate='key',
            validatecommand=vcmd
        )
        maxTimeEntry.grid(row=1, column=0, padx=5)
        maxTimeEntry.bind("<FocusOut>", on_max_time_focus_out)

        ttk.Label(settingsFrame, text="Max Farming Time (min)").grid(row=1, column=1, sticky="w", padx=5, pady=5)

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.window.after(200, self.pollMacroState)
        self.window.mainloop()

    def on_close(self):
        # Save current walkspeed before closing
        val = self.walkspeedVar.get()
        if val:
            try:
                val_int = int(val)
                existing = self.settings_db.getByQuery({"key": "walkspeed"})
                if existing:
                    self.settings_db.updateById(existing[0]["id"], {"key": "walkspeed", "value": val_int})
                else:
                    self.settings_db.add({"key": "walkspeed", "value": val_int})
            except Exception:
                pass

        # Save max farming time before closing
        val = self.maxFarmingTimeVar.get()
        if val:
            try:
                val_int = int(val)
                existing = self.settings_db.getByQuery({"key": "max_farming_time"})
                if existing:
                    self.settings_db.updateById(existing[0]["id"], {"key": "max_farming_time", "value": val_int})
                else:
                    self.settings_db.add({"key": "max_farming_time", "value": val_int})
            except Exception:
                pass

        self.window.destroy()

    def onFieldSelected(self, event):
        fieldName = self.selectedField.get()
        fieldData = self.macro.field.get(fieldName)
        if fieldData:
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
            self.patternDropdown["values"] = ["Select field first"]
            self.patternDropdown.config(state="disabled")
            self.selectedPattern.set("")
            self.macro.pattern.set(None)

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
