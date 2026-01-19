"""
FractalSense EntaENGELment - Hauptanwendung

Diese Datei implementiert die Hauptanwendung, die das modulare Framework und die Module zusammenführt.
"""

import os
import sys
import logging
import argparse
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import threading
import time

# Importiere das modulare Framework
from modular_app_structure import FractalSenseApp, EventSystem

class FractalSenseGUI:
    """Grafische Benutzeroberfläche für die FractalSense EntaENGELment App."""
    
    def __init__(self, app: FractalSenseApp):
        self.app = app
        self.event_system = app.event_system
        
        # Hauptfenster erstellen
        self.root = tk.Tk()
        self.root.title("FractalSense EntaENGELment")
        self.root.geometry("1200x800")
        
        # Hauptframe erstellen
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Linke Seite für Module-Liste und Steuerelemente
        self.left_frame = ttk.Frame(self.main_frame, width=300)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Rechte Seite für Visualisierung
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Module-Liste
        self.module_frame = ttk.LabelFrame(self.left_frame, text="Module")
        self.module_frame.pack(fill=tk.X, pady=5)
        
        self.module_listbox = tk.Listbox(self.module_frame, height=6)
        self.module_listbox.pack(fill=tk.X, padx=5, pady=5)
        self.module_listbox.bind('<<ListboxSelect>>', self.on_module_select)
        
        # Steuerelemente-Frame
        self.controls_frame = ttk.LabelFrame(self.left_frame, text="Steuerelemente")
        self.controls_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Statusleiste
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(self.status_frame, text="Bereit")
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Visualisierungsbereich
        self.canvas_frame = ttk.Frame(self.right_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Event-Handler registrieren
        self.event_system.register_handler("fractal_updated", self.on_fractal_updated)
        self.event_system.register_handler("sensor_data_updated", self.on_sensor_data_updated)
        
        # Beim Schließen des Fensters aufräumen
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Module laden
        self.load_modules()
    
    def load_modules(self):
        """Lädt die Module in die GUI."""
        # Module-Liste leeren
        self.module_listbox.delete(0, tk.END)
        
        # Module aus der App holen
        modules = self.app.get_all_modules()
        
        # Module zur Liste hinzufügen
        for name, module in modules.items():
            self.module_listbox.insert(tk.END, f"{name} (v{module.version})")
        
        # Wenn Module vorhanden sind, das erste auswählen
        if modules:
            self.module_listbox.selection_set(0)
            self.on_module_select(None)
    
    def on_module_select(self, event):
        """Handler für die Auswahl eines Moduls in der Liste."""
        # Ausgewählten Index holen
        selection = self.module_listbox.curselection()
        if not selection:
            return
        
        # Ausgewähltes Modul holen
        modules = list(self.app.get_all_modules().items())
        if selection[0] < len(modules):
            name, module = modules[selection[0]]
            
            # Steuerelemente des Moduls anzeigen
            self.show_module_controls(name, module)
    
    def show_module_controls(self, module_name, module):
        """Zeigt die Steuerelemente eines Moduls an."""
        # Bestehende Steuerelemente entfernen
        for widget in self.controls_frame.winfo_children():
            widget.destroy()
        
        # UI-Komponenten des Moduls holen
        ui_components = module.get_ui_components()
        
        # Wenn keine UI-Komponenten vorhanden sind, Hinweis anzeigen
        if not ui_components or not ui_components.get("controls"):
            ttk.Label(self.controls_frame, text=f"Keine Steuerelemente für Modul '{module_name}'").pack(padx=5, pady=5)
            return
        
        # Steuerelemente anzeigen
        controls = ui_components.get("controls", {})
        for control_name, control_info in controls.items():
            control_type = control_info.get("type", "")
            control_label = control_info.get("label", control_name)
            control_value = control_info.get("value", "")
            control_event = control_info.get("event", "")
            
            # Label für das Steuerelement
            label_frame = ttk.Frame(self.controls_frame)
            label_frame.pack(fill=tk.X, padx=5, pady=2)
            
            ttk.Label(label_frame, text=control_label).pack(side=tk.LEFT)
            
            # Je nach Typ des Steuerelements
            if control_type == "button":
                # Button
                button = ttk.Button(
                    label_frame, 
                    text=control_label,
                    command=lambda e=control_event: self.event_system.emit_event(e, {})
                )
                button.pack(side=tk.RIGHT)
            
            elif control_type == "text":
                # Textfeld
                var = tk.StringVar(value=control_value)
                entry = ttk.Entry(label_frame, textvariable=var)
                entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
                
                # Funktion zum Aktualisieren des Werts
                def update_value(event=None, name=control_name, var=var):
                    self.event_system.emit_event(
                        f"ui_update_{module_name}_{name}",
                        {name: var.get()}
                    )
                
                entry.bind("<Return>", update_value)
                entry.bind("<FocusOut>", update_value)
            
            elif control_type == "number":
                # Zahlenfeld
                var = tk.StringVar(value=str(control_value))
                spinbox = ttk.Spinbox(
                    label_frame, 
                    from_=control_info.get("min", 0),
                    to=control_info.get("max", 100),
                    textvariable=var
                )
                spinbox.pack(side=tk.RIGHT)
                
                # Funktion zum Aktualisieren des Werts
                def update_value(event=None, name=control_name, var=var):
                    try:
                        value = int(var.get())
                        self.event_system.emit_event(
                            f"ui_update_{module_name}_{name}",
                            {name: value}
                        )
                    except ValueError:
                        pass
                
                spinbox.bind("<Return>", update_value)
                spinbox.bind("<FocusOut>", update_value)
            
            elif control_type == "dropdown":
                # Dropdown-Menü
                var = tk.StringVar(value=control_value)
                combobox = ttk.Combobox(
                    label_frame,
                    textvariable=var,
                    values=control_info.get("options", [])
                )
                combobox.pack(side=tk.RIGHT)
                
                # Funktion zum Aktualisieren des Werts
                def update_value(event=None, name=control_name, var=var):
                    self.event_system.emit_event(
                        f"ui_update_{module_name}_{name}",
                        {name: var.get()}
                    )
                
                combobox.bind("<<ComboboxSelected>>", update_value)
        
        # Wenn das Modul eine Figur hat, diese anzeigen
        if "figure" in ui_components:
            self.show_figure(ui_components["figure"])
    
    def show_figure(self, figure):
        """Zeigt eine Matplotlib-Figur im Canvas-Frame an."""
        # Bestehende Widgets entfernen
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        
        # Canvas erstellen
        canvas = FigureCanvasTkAgg(figure, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def on_fractal_updated(self, event_type, event_data):
        """Handler für das Fractal-Updated-Event."""
        # Status aktualisieren
        zoom = event_data.get("zoom", 0)
        self.status_label.config(text=f"Fraktal aktualisiert - Zoom: {zoom:.2f}")
    
    def on_sensor_data_updated(self, event_type, event_data):
        """Handler für das Sensor-Data-Updated-Event."""
        # Status aktualisieren
        timestamp = event_data.get("timestamp", 0)
        formatted_time = time.strftime("%H:%M:%S", time.localtime(timestamp))
        self.status_label.config(text=f"Sensordaten aktualisiert - {formatted_time}")
    
    def on_close(self):
        """Handler für das Schließen des Fensters."""
        # App stoppen
        self.app.stop()
        
        # Fenster schließen
        self.root.destroy()
    
    def run(self):
        """Startet die GUI."""
        # App starten
        self.app.run()
        
        # Tkinter-Hauptschleife starten
        self.root.mainloop()

def main():
    """Hauptfunktion der Anwendung."""
    # Kommandozeilenargumente parsen
    parser = argparse.ArgumentParser(description="FractalSense EntaENGELment App")
    parser.add_argument("--config", default="config.json", help="Pfad zur Konfigurationsdatei")
    parser.add_argument("--modules-dir", default="modules", help="Verzeichnis mit Modulen")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Log-Level")
    args = parser.parse_args()
    
    # Logging konfigurieren
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # App erstellen und initialisieren
    app = FractalSenseApp(config_file=args.config)
    
    # Modulverzeichnis überschreiben, falls angegeben
    if args.modules_dir:
        app.config_manager.set_config("app", "modules_dir", args.modules_dir)
    
    # App initialisieren
    if not app.initialize():
        logging.error("Initialisierung der App fehlgeschlagen.")
        return 1
    
    # GUI erstellen und starten
    gui = FractalSenseGUI(app)
    gui.run()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
