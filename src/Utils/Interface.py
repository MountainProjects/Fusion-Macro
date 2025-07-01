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
        self.window.geometry("500x400")  # increased height for scrollable stock tab
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

        # LabelFrame for Play controls in the Field tab
        playFrame = ttk.LabelFrame(fieldTab, text="Play")
        playFrame.pack(fill="x", pady=5, padx=10)

        self.playStopButton = tk.Button(
            playFrame,
            text="Play (F5)",
            height=1,
            width=15,
            bg="#4CAF50",
            fg="white",
            command=self.toggleMacro
        )
        self.playStopButton.pack(ipady=5, pady=5)

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

        saved_time_record = self.settings_db.getByQuery({"key": "max_farming_repeat"})
        if saved_time_record:
            saved_max_time = saved_time_record[0]["value"]
            var.max_farming_repeat = saved_max_time
        else:
            saved_max_time = getattr(var, "max_farming_repeat", var.max_farming_repeat)
            var.max_farming_repeat = saved_max_time

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
                self.maxFarmingTimeVar.set(str(var.max_farming_repeat))
            else:
                val_int = int(val)
                self.maxFarmingTimeVar.set(str(val_int))
                var.max_farming_repeat = val_int

                existing = self.settings_db.getByQuery({"key": "max_farming_repeat"})
                if existing:
                    self.settings_db.updateById(existing[0]["id"], {"key": "max_farming_repeat", "value": val_int})
                else:
                    self.settings_db.add({"key": "max_farming_repeat", "value": val_int})

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

        ttk.Label(settingsFrame, text="Max Farming Repeat (times)").grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Load saved parachute setting or fallback to default "None"
        saved_parachute_record = self.settings_db.getByQuery({"key": "parachute"})
        if saved_parachute_record:
            saved_parachute = saved_parachute_record[0]["value"]
        else:
            saved_parachute = "None"

        self.parachuteVar = tk.StringVar(value=saved_parachute)

        def on_parachute_selected(event):
            val = self.parachuteVar.get()
            var.parachuteType = val  # Update var with current selection

            existing = self.settings_db.getByQuery({"key": "parachute"})
            if existing:
                self.settings_db.updateById(existing[0]["id"], {"key": "parachute", "value": val})
            else:
                self.settings_db.add({"key": "parachute", "value": val})

        parachuteDropdown = ttk.Combobox(
            settingsFrame,
            textvariable=self.parachuteVar,
            values=["None", "Leaf", "Maple Leaf"],
            state="readonly",
            width=15
        )
        parachuteDropdown.grid(row=2, column=0, padx=5, pady=5)
        parachuteDropdown.bind("<<ComboboxSelected>>", on_parachute_selected)

        ttk.Label(settingsFrame, text="Parachute").grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # Load saved movement path setting or fallback to default "Cannon"
        saved_movement_path_record = self.settings_db.getByQuery({"key": "movement_path"})
        if saved_movement_path_record:
            saved_movement_path = saved_movement_path_record[0]["value"]
        else:
            saved_movement_path = "Cannon"

        self.movementPathVar = tk.StringVar(value=saved_movement_path)

        def on_movement_path_selected(event):
            val = self.movementPathVar.get()
            existing = self.settings_db.getByQuery({"key": "movement_path"})

            var.movementPath = val # Update var with current selection
            if existing:
                self.settings_db.updateById(existing[0]["id"], {"key": "movement_path", "value": val})
            else:
                self.settings_db.add({"key": "movement_path", "value": val})

            # Auto-select path based on selected field and movement path
            selectedFieldName = self.selectedField.get()
            if not selectedFieldName:
                self.selectedPath.set("")
                return

            fieldDataList = self.macro.field.database.getByQuery({"name": selectedFieldName})
            if not fieldDataList:
                self.selectedPath.set("")
                return

            fieldData = fieldDataList[0]

            # Map dropdown value to field-id values (you may want to normalize)
            movementPathMap = {
                "Cannon": "cannon",
                "Walk": "walk",
                # Add more if needed
            }
            desiredFieldId = movementPathMap.get(val.lower().capitalize(), val.lower())

            # Find matching path
            matchingPath = None
            for path in fieldData.get("paths", []):
                if path.get("type", "").lower() == desiredFieldId.lower():
                    matchingPath = path
                    break

            if matchingPath:
                self.selectedPath.set(matchingPath["id"])
                # Optionally, update the macro's internal path variable, e.g.:
                
                self.macro.path.set(matchingPath["id"])
            else:
                self.selectedPath.set("")

        movementPathDropdown = ttk.Combobox(
            settingsFrame,
            textvariable=self.movementPathVar,
            values=["Cannon", "Walk"],
            state="readonly",
            width=15
        )
        movementPathDropdown.grid(row=3, column=0, padx=5, pady=5)
        movementPathDropdown.bind("<<ComboboxSelected>>", on_movement_path_selected)

        ttk.Label(settingsFrame, text="Movement Type").grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # --- Stock Tab ---
        stockTab = ttk.Frame(notebook, padding=10)
        notebook.add(stockTab, text="Stock")

        stockFrame = ttk.LabelFrame(stockTab, text="Stock Items")
        stockFrame.pack(fill="both", expand=True, pady=10, padx=10)

        # Canvas + scrollbar for scrolling stock checkboxes
        canvas = tk.Canvas(stockFrame)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(stockFrame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        checkboxFrame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=checkboxFrame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        checkboxFrame.bind("<Configure>", on_frame_configure)

        # Load saved stock enabled and stock settings
        saved_stock_enabled = self.settings_db.getByQuery({"key": "stock-enabled"})
        if saved_stock_enabled:
            stockEnabled = saved_stock_enabled[0]["value"]
            var.stockEnabled = stockEnabled
        else:
            var.stockEnabled = False  # default off

        saved_stocks_record = self.settings_db.getByQuery({"key": "Stocks"})
        stockItems = [
            "Strawberry",
            "Blueberry",
            "Sunflower Seed",
            "Honeycomb",
            "Honey Jar",
            "Blueberry Jam",
            "Strawberry Jam",
            "Bottomless Bag"
        ]

        if saved_stocks_record:
            savedStocks = saved_stocks_record[0]["value"]
        else:
            savedStocks = {item: False for item in stockItems}

        var.stockSettings = savedStocks.copy()

        self.stockEnabledVar = tk.BooleanVar(value=var.stockEnabled)
        self.stockVars = {}
        self.stockCheckboxes = []

        def on_stock_enabled_toggle():
            var.stockEnabled = self.stockEnabledVar.get()
            existing = self.settings_db.getByQuery({"key": "stock-enabled"})
            if existing:
                self.settings_db.updateById(existing[0]["id"], {"key": "stock-enabled", "value": var.stockEnabled})
            else:
                self.settings_db.add({"key": "stock-enabled", "value": var.stockEnabled})

            for chk in self.stockCheckboxes:
                chk.config(state="normal" if var.stockEnabled else "disabled")

        def on_stock_check():
            for item, varBool in self.stockVars.items():
                var.stockSettings[item] = varBool.get()
            existing = self.settings_db.getByQuery({"key": "Stocks"})
            if existing:
                self.settings_db.updateById(existing[0]["id"], {"key": "Stocks", "value": var.stockSettings})
            else:
                self.settings_db.add({"key": "Stocks", "value": var.stockSettings})

        # Enable Stock checkbox
        stockEnabledCheckbox = ttk.Checkbutton(
            checkboxFrame,
            text="Enable Stock",
            variable=self.stockEnabledVar,
            command=on_stock_enabled_toggle
        )
        stockEnabledCheckbox.grid(row=0, column=0, sticky="w", pady=5)

        # Stock item checkboxes
        for i, item in enumerate(stockItems, start=1):
            varBool = tk.BooleanVar(value=savedStocks.get(item, False))
            chk = ttk.Checkbutton(
                checkboxFrame,
                text=item,
                variable=varBool,
                command=on_stock_check
            )
            chk.grid(row=i, column=0, sticky="w", pady=2)
            self.stockVars[item] = varBool
            self.stockCheckboxes.append(chk)

        # Disable stock checkboxes if stockEnabled is False
        if not var.stockEnabled:
            for chk in self.stockCheckboxes:
                chk.config(state="disabled")

        # --- End of Tabs ---

        # Load last saved selected field, pattern, and path
        saved_field_record = self.settings_db.getByQuery({"key": "selected-field"})
        if saved_field_record:
            saved_field = saved_field_record[0]["value"]
            self.selectedField.set(saved_field)

        saved_pattern_record = self.settings_db.getByQuery({"key": "selected-pattern"})
        if saved_pattern_record:
            saved_pattern_id = saved_pattern_record[0]["value"]
            self.selectedPattern.set(saved_pattern_id)
        else:
            self.selectedPattern.set("")

        self.updatePatternDropdown()

        if self.selectedPattern.get():
            fieldDataList = self.macro.field.database.getByQuery({"name": fieldName})
            if fieldDataList:
                fieldData = fieldDataList[0]
                patternName = self.selectedPattern.get()
                patternId = None
                for pattern in fieldData.get("patterns", []):
                    if pattern["name"] == patternName:
                        patternId = pattern["id"]
                        break

                self.macro.pattern.set(patternId)

        if self.selectedPath.get():
            self.macro.path.set(self.selectedPath.get())

        self.window.mainloop()

    def updatePlayStopButton(self):
        if self.macro.started:
            self.playStopButton.config(text="Stop (F5)", bg="#E53935")
        else:
            self.playStopButton.config(text="Play (F5)", bg="#4CAF50")

    def toggleMacro(self):
        if self.macro.started:
            self.macro.end()
        else:
            if not self.selectedField.get() or not self.selectedPattern.get():
                messagebox.showerror("Error", "Please select Field, Pattern before starting.")
                return
            self.macro.restart()
        self.updatePlayStopButton()

    def onFieldSelected(self, event):
        selected = self.selectedField.get()
        # Save selection to db
        existing = self.settings_db.getByQuery({"key": "selected-field"})
        if existing:
            self.settings_db.updateById(existing[0]["id"], {"key": "selected-field", "value": selected})
        else:
            self.settings_db.add({"key": "selected-field", "value": selected})

        # Update patterns and paths based on selected field
        self.updatePatternDropdown()

    def updatePatternDropdown(self):
        fieldName = self.selectedField.get()
        if not fieldName:
            self.patternDropdown.config(state="disabled")
            self.patternDropdown["values"] = []
            self.selectedPattern.set("")
            self.selectedPath.set("")
            return

        fieldDataList = self.macro.field.database.getByQuery({"name": fieldName})
        if not fieldDataList:
            self.patternDropdown.config(state="disabled")
            self.patternDropdown["values"] = []
            self.selectedPattern.set("")
            self.selectedPath.set("")
            return

        fieldData = fieldDataList[0]

        # Extract pattern names and build id->name map
        patterns = fieldData.get("patterns", [])
        patternNames = [p["name"] for p in patterns]
        patternIdToName = {p["id"]: p["name"] for p in patterns}

        self.patternDropdown.config(state="readonly")
        self.patternDropdown["values"] = patternNames

        savedPatternId = self.selectedPattern.get()

        # If savedPatternId is in our map, select corresponding name in dropdown
        if savedPatternId in patternIdToName:
            patternName = patternIdToName[savedPatternId]
            self.patternDropdown.set(patternName)
        else:
            self.patternDropdown.set("")
            self.selectedPattern.set("")

    def onPatternSelected(self, event):
        fieldName = self.selectedField.get()
        selectedPatternName = self.patternDropdown.get()  # get pattern name from dropdown

        if not fieldName or not selectedPatternName:
            self.selectedPattern.set("")
            return

        # Find pattern id by name in the selected field
        fieldDataList = self.macro.field.database.getByQuery({"name": fieldName})
        if not fieldDataList:
            self.selectedPattern.set("")
            return
        fieldData = fieldDataList[0]

        patternId = None
        for pattern in fieldData.get("patterns", []):
            if pattern["name"] == selectedPatternName:
                patternId = pattern["id"]
                break

        if patternId is None:
            self.selectedPattern.set("")
            return

        self.selectedPattern.set(patternId)  # Store ID here
        self.macro.pattern.set(patternId)   # Update macro with ID

        # Save pattern ID to db
        existing = self.settings_db.getByQuery({"key": "selected-pattern"})
        if existing:
            self.settings_db.updateById(existing[0]["id"], {"key": "selected-pattern", "value": patternId})
        else:
            self.settings_db.add({"key": "selected-pattern", "value": patternId})