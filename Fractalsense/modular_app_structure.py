"""
FractalSense EntaENGELment - Modulare App-Struktur

Diese Datei implementiert ein modulares Framework für die FractalSense EntaENGELment App,
das eine einfache Integration neuer Module ermöglicht.
"""

import importlib
import inspect
import os
import sys
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Type, Callable

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("FractalSense")

class ModuleInterface(ABC):
    """Basis-Interface für alle Module."""
    
    @abstractmethod
    def initialize(self, app_context: Dict[str, Any]) -> bool:
        """Initialisiert das Modul mit dem App-Kontext.
        
        Args:
            app_context: Dictionary mit dem App-Kontext
            
        Returns:
            bool: True, wenn die Initialisierung erfolgreich war, sonst False
        """
        pass
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verarbeitet Eingabedaten und gibt Ergebnisse zurück.
        
        Args:
            input_data: Eingabedaten für die Verarbeitung
            
        Returns:
            Dict[str, Any]: Ergebnisse der Verarbeitung
        """
        pass
    
    @abstractmethod
    def get_ui_components(self) -> Dict[str, Any]:
        """Gibt UI-Komponenten des Moduls zurück.
        
        Returns:
            Dict[str, Any]: UI-Komponenten des Moduls
        """
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Bereinigt Ressourcen des Moduls."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Gibt den Namen des Moduls zurück."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Gibt die Version des Moduls zurück."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Gibt die Beschreibung des Moduls zurück."""
        pass
    
    @property
    @abstractmethod
    def dependencies(self) -> List[str]:
        """Gibt die Abhängigkeiten des Moduls zurück."""
        pass

class ModuleRegistry:
    """Verwaltet die Registrierung und Verwaltung von Modulen."""
    
    def __init__(self):
        self._modules: Dict[str, ModuleInterface] = {}
        self._module_classes: Dict[str, Type[ModuleInterface]] = {}
        self._module_paths: Dict[str, str] = {}
        self._module_dependencies: Dict[str, List[str]] = {}
        self._module_load_order: List[str] = []
    
    def register_module_class(self, module_class: Type[ModuleInterface], module_path: str) -> bool:
        """Registriert eine Modulklasse.
        
        Args:
            module_class: Die Modulklasse
            module_path: Der Pfad zum Modul
            
        Returns:
            bool: True, wenn die Registrierung erfolgreich war, sonst False
        """
        try:
            # Erstelle temporäre Instanz zur Überprüfung
            temp_instance = module_class()
            module_name = temp_instance.name
            
            if module_name in self._module_classes:
                logger.warning(f"Modul '{module_name}' ist bereits registriert.")
                return False
            
            self._module_classes[module_name] = module_class
            self._module_paths[module_name] = module_path
            self._module_dependencies[module_name] = temp_instance.dependencies
            
            logger.info(f"Modul '{module_name}' (v{temp_instance.version}) erfolgreich registriert.")
            return True
        except Exception as e:
            logger.error(f"Fehler bei der Registrierung des Moduls: {str(e)}")
            return False
    
    def discover_modules(self, modules_dir: str) -> int:
        """Entdeckt Module im angegebenen Verzeichnis.
        
        Args:
            modules_dir: Verzeichnis, in dem Module gesucht werden sollen
            
        Returns:
            int: Anzahl der gefundenen Module
        """
        if not os.path.exists(modules_dir):
            logger.error(f"Modulverzeichnis '{modules_dir}' existiert nicht.")
            return 0
        
        # Füge Modulverzeichnis zum Pfad hinzu
        if modules_dir not in sys.path:
            sys.path.append(modules_dir)
        
        count = 0
        for item in os.listdir(modules_dir):
            module_path = os.path.join(modules_dir, item)
            
            # Überprüfe, ob es sich um ein Verzeichnis mit einer __init__.py handelt
            if os.path.isdir(module_path) and os.path.exists(os.path.join(module_path, "__init__.py")):
                try:
                    module_name = item
                    module = importlib.import_module(module_name)
                    
                    # Suche nach Klassen, die ModuleInterface implementieren
                    for name, obj in inspect.getmembers(module):
                        if (inspect.isclass(obj) and 
                            issubclass(obj, ModuleInterface) and 
                            obj != ModuleInterface):
                            if self.register_module_class(obj, module_path):
                                count += 1
                except Exception as e:
                    logger.error(f"Fehler beim Laden des Moduls '{item}': {str(e)}")
        
        logger.info(f"{count} Module gefunden und registriert.")
        return count
    
    def initialize_modules(self, app_context: Dict[str, Any]) -> bool:
        """Initialisiert alle registrierten Module in der richtigen Reihenfolge.
        
        Args:
            app_context: Dictionary mit dem App-Kontext
            
        Returns:
            bool: True, wenn alle Module erfolgreich initialisiert wurden, sonst False
        """
        # Bestimme Ladereihenfolge basierend auf Abhängigkeiten
        self._determine_load_order()
        
        # Initialisiere Module in der richtigen Reihenfolge
        for module_name in self._module_load_order:
            if module_name not in self._modules:
                try:
                    module_class = self._module_classes[module_name]
                    module_instance = module_class()
                    
                    logger.info(f"Initialisiere Modul '{module_name}'...")
                    if not module_instance.initialize(app_context):
                        logger.error(f"Initialisierung des Moduls '{module_name}' fehlgeschlagen.")
                        return False
                    
                    self._modules[module_name] = module_instance
                    logger.info(f"Modul '{module_name}' erfolgreich initialisiert.")
                except Exception as e:
                    logger.error(f"Fehler bei der Initialisierung des Moduls '{module_name}': {str(e)}")
                    return False
        
        return True
    
    def _determine_load_order(self) -> None:
        """Bestimmt die Ladereihenfolge der Module basierend auf Abhängigkeiten."""
        # Zurücksetzen der Ladereihenfolge
        self._module_load_order = []
        
        # Temporäre Datenstrukturen für die topologische Sortierung
        visited = set()
        temp_visited = set()
        
        def visit(module_name):
            """Rekursive Hilfsfunktion für die topologische Sortierung."""
            if module_name in temp_visited:
                # Zyklische Abhängigkeit erkannt
                cycle = " -> ".join(list(temp_visited) + [module_name])
                logger.error(f"Zyklische Abhängigkeit erkannt: {cycle}")
                raise ValueError(f"Zyklische Abhängigkeit erkannt: {cycle}")
            
            if module_name not in visited:
                temp_visited.add(module_name)
                
                # Besuche alle Abhängigkeiten
                for dependency in self._module_dependencies.get(module_name, []):
                    if dependency in self._module_classes:
                        visit(dependency)
                    else:
                        logger.warning(f"Abhängigkeit '{dependency}' für Modul '{module_name}' nicht gefunden.")
                
                temp_visited.remove(module_name)
                visited.add(module_name)
                self._module_load_order.append(module_name)
        
        # Führe topologische Sortierung für alle Module durch
        for module_name in self._module_classes:
            if module_name not in visited:
                visit(module_name)
    
    def get_module(self, module_name: str) -> Optional[ModuleInterface]:
        """Gibt eine Instanz eines Moduls zurück.
        
        Args:
            module_name: Name des Moduls
            
        Returns:
            Optional[ModuleInterface]: Modulinstanz oder None, wenn nicht gefunden
        """
        return self._modules.get(module_name)
    
    def get_all_modules(self) -> Dict[str, ModuleInterface]:
        """Gibt alle initialisierten Module zurück.
        
        Returns:
            Dict[str, ModuleInterface]: Dictionary mit allen Modulen
        """
        return self._modules.copy()
    
    def cleanup_modules(self) -> None:
        """Bereinigt alle Module."""
        # Bereinige Module in umgekehrter Ladereihenfolge
        for module_name in reversed(self._module_load_order):
            if module_name in self._modules:
                try:
                    logger.info(f"Bereinige Modul '{module_name}'...")
                    self._modules[module_name].cleanup()
                except Exception as e:
                    logger.error(f"Fehler bei der Bereinigung des Moduls '{module_name}': {str(e)}")
        
        # Zurücksetzen der Module
        self._modules = {}

class EventSystem:
    """Implementiert ein Event-System für die Kommunikation zwischen Modulen."""
    
    def __init__(self):
        self._event_handlers: Dict[str, List[Callable]] = {}
    
    def register_handler(self, event_type: str, handler: Callable) -> None:
        """Registriert einen Event-Handler.
        
        Args:
            event_type: Typ des Events
            handler: Handler-Funktion
        """
        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = []
        
        self._event_handlers[event_type].append(handler)
        logger.debug(f"Event-Handler für '{event_type}' registriert.")
    
    def unregister_handler(self, event_type: str, handler: Callable) -> bool:
        """Entfernt einen Event-Handler.
        
        Args:
            event_type: Typ des Events
            handler: Handler-Funktion
            
        Returns:
            bool: True, wenn der Handler entfernt wurde, sonst False
        """
        if event_type in self._event_handlers and handler in self._event_handlers[event_type]:
            self._event_handlers[event_type].remove(handler)
            logger.debug(f"Event-Handler für '{event_type}' entfernt.")
            return True
        return False
    
    def emit_event(self, event_type: str, event_data: Dict[str, Any] = None) -> None:
        """Sendet ein Event an alle registrierten Handler.
        
        Args:
            event_type: Typ des Events
            event_data: Event-Daten
        """
        if event_data is None:
            event_data = {}
        
        logger.debug(f"Event '{event_type}' emittiert.")
        
        if event_type in self._event_handlers:
            for handler in self._event_handlers[event_type]:
                try:
                    handler(event_type, event_data)
                except Exception as e:
                    logger.error(f"Fehler im Event-Handler für '{event_type}': {str(e)}")

class ConfigManager:
    """Verwaltet die Konfiguration der App und der Module."""
    
    def __init__(self, config_file: str):
        self._config_file = config_file
        self._config: Dict[str, Any] = {
            "app": {
                "name": "FractalSense EntaENGELment",
                "version": "1.0.0",
                "modules_dir": "modules"
            },
            "modules": {}
        }
        self.load_config()
    
    def load_config(self) -> bool:
        """Lädt die Konfiguration aus der Datei.
        
        Returns:
            bool: True, wenn die Konfiguration erfolgreich geladen wurde, sonst False
        """
        try:
            if os.path.exists(self._config_file):
                with open(self._config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    self._update_config(self._config, loaded_config)
                logger.info(f"Konfiguration aus '{self._config_file}' geladen.")
                return True
            else:
                logger.warning(f"Konfigurationsdatei '{self._config_file}' nicht gefunden. Verwende Standardkonfiguration.")
                return False
        except Exception as e:
            logger.error(f"Fehler beim Laden der Konfiguration: {str(e)}")
            return False
    
    def _update_config(self, target: Dict[str, Any], source: Dict[str, Any]) -> None:
        """Aktualisiert die Konfiguration rekursiv.
        
        Args:
            target: Ziel-Dictionary
            source: Quell-Dictionary
        """
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._update_config(target[key], value)
            else:
                target[key] = value
    
    def save_config(self) -> bool:
        """Speichert die Konfiguration in der Datei.
        
        Returns:
            bool: True, wenn die Konfiguration erfolgreich gespeichert wurde, sonst False
        """
        try:
            with open(self._config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=4)
            logger.info(f"Konfiguration in '{self._config_file}' gespeichert.")
            return True
        except Exception as e:
            logger.error(f"Fehler beim Speichern der Konfiguration: {str(e)}")
            return False
    
    def get_config(self, section: str = None, key: str = None) -> Any:
        """Gibt die Konfiguration oder einen Teil davon zurück.
        
        Args:
            section: Abschnitt der Konfiguration
            key: Schlüssel innerhalb des Abschnitts
            
        Returns:
            Any: Konfigurationswert oder None, wenn nicht gefunden
        """
        if section is None:
            return self._config
        
        if section in self._config:
            if key is None:
                return self._config[section]
            elif key in self._config[section]:
                return self._config[section][key]
        
        return None
    
    def set_config(self, section: str, key: str, value: Any) -> None:
        """Setzt einen Konfigurationswert.
        
        Args:
            section: Abschnitt der Konfiguration
            key: Schlüssel innerhalb des Abschnitts
            value: Zu setzender Wert
        """
        if section not in self._config:
            self._config[section] = {}
        
        self._config[section][key] = value
    
    def get_module_config(self, module_name: str) -> Dict[str, Any]:
        """Gibt die Konfiguration eines Moduls zurück.
        
        Args:
            module_name: Name des Moduls
            
        Returns:
            Dict[str, Any]: Modulkonfiguration oder leeres Dictionary, wenn nicht gefunden
        """
        if "modules" in self._config and module_name in self._config["modules"]:
            return self._config["modules"][module_name]
        return {}
    
    def set_module_config(self, module_name: str, config: Dict[str, Any]) -> None:
        """Setzt die Konfiguration eines Moduls.

        Args:
            module_name: Name des Moduls
            config: Konfigurationsdictionary
        """
        if "modules" not in self._config:
            self._config["modules"] = {}
        self._config["modules"][module_name] = config
