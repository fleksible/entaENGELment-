# Android-App-Erstellung für FractalSense EntaENGELment

Dieses Dokument beschreibt den Prozess zur Erstellung einer Android-APK für die FractalSense EntaENGELment-Anwendung.

## Voraussetzungen

- Android Studio (neueste Version)
- Python 3.8 oder höher
- Kivy Framework
- Buildozer (für die APK-Erstellung)

## Schritt 1: Vorbereitung der Entwicklungsumgebung

1. **Python-Umgebung einrichten**
   ```bash
   # Virtuelle Umgebung erstellen
   python -m venv fractal_env
   
   # Umgebung aktivieren (Windows)
   fractal_env\Scripts\activate
   
   # Umgebung aktivieren (Linux/Mac)
   source fractal_env/bin/activate
   
   # Abhängigkeiten installieren
   pip install kivy kivymd numpy matplotlib pygame hypernetx buildozer
   ```

2. **Buildozer initialisieren**
   ```bash
   # Im Projektverzeichnis
   buildozer init
   ```

3. **buildozer.spec anpassen**
   Öffnen Sie die Datei `buildozer.spec` und passen Sie folgende Einstellungen an:
   
   ```
   [app]
   title = FractalSense EntaENGELment
   package.name = fractalsense
   package.domain = org.fractalsense
   source.dir = .
   source.include_exts = py,png,jpg,kv,atlas,json,md
   version = 1.0
   requirements = python3,kivy,kivymd,numpy,matplotlib,pygame,requests
   orientation = portrait
   fullscreen = 0
   android.permissions = INTERNET,ACCESS_NETWORK_STATE,VIBRATE,CAMERA,RECORD_AUDIO
   android.api = 30
   android.minapi = 26
   android.ndk = 21e
   ```

## Schritt 2: Anpassung der Projektstruktur für Android

1. **Hauptdatei erstellen (main.py)**
   Erstellen Sie eine `main.py` Datei im Hauptverzeichnis:
   
   ```python
   from kivy.app import App
   from kivy.uix.screenmanager import ScreenManager, Screen
   from kivy.uix.boxlayout import BoxLayout
   from kivy.uix.button import Button
   from kivy.uix.label import Label
   from kivy.core.window import Window
   from kivy.clock import Clock
   
   # Import der Modulklassen
   from modules.fractal_visualization.kivy_interface import FractalVisualizationWidget
   from modules.sensor_integration.kivy_interface import SensorIntegrationWidget
   from modules.resonance_enhancer.kivy_interface import ResonanceEnhancerWidget
   from modules.hypergraph_visualization.kivy_interface import HypergraphVisualizationWidget
   
   # Import des Event-Systems
   from modular_app_structure import EventSystem, ConfigManager
   
   class MainScreen(Screen):
       def __init__(self, **kwargs):
           super(MainScreen, self).__init__(**kwargs)
           self.layout = BoxLayout(orientation='vertical')
           
           # Titel
           self.title = Label(text='FractalSense EntaENGELment', 
                             font_size=24, 
                             size_hint=(1, 0.1))
           self.layout.add_widget(self.title)
           
           # Hauptbereich für Module
           self.content_area = BoxLayout(orientation='vertical', 
                                        size_hint=(1, 0.8))
           self.layout.add_widget(self.content_area)
           
           # Navigationsleiste
           self.nav_bar = BoxLayout(orientation='horizontal', 
                                   size_hint=(1, 0.1))
           
           # Buttons für Module
           self.fractal_btn = Button(text='Fraktal')
           self.fractal_btn.bind(on_press=self.show_fractal)
           self.nav_bar.add_widget(self.fractal_btn)
           
           self.sensor_btn = Button(text='Sensoren')
           self.sensor_btn.bind(on_press=self.show_sensor)
           self.nav_bar.add_widget(self.sensor_btn)
           
           self.resonance_btn = Button(text='Resonanz')
           self.resonance_btn.bind(on_press=self.show_resonance)
           self.nav_bar.add_widget(self.resonance_btn)
           
           self.hypergraph_btn = Button(text='Hypergraph')
           self.hypergraph_btn.bind(on_press=self.show_hypergraph)
           self.nav_bar.add_widget(self.hypergraph_btn)
           
           self.layout.add_widget(self.nav_bar)
           self.add_widget(self.layout)
           
           # Module initialisieren
           self.event_system = EventSystem()
           self.config_manager = ConfigManager('config.json')
           
           self.app_context = {
               'event_system': self.event_system,
               'config_manager': self.config_manager
           }
           
           # Widgets erstellen
           self.fractal_widget = FractalVisualizationWidget(self.app_context)
           self.sensor_widget = SensorIntegrationWidget(self.app_context)
           self.resonance_widget = ResonanceEnhancerWidget(self.app_context)
           self.hypergraph_widget = HypergraphVisualizationWidget(self.app_context)
           
           # Standard-Widget anzeigen
           self.current_widget = None
           Clock.schedule_once(lambda dt: self.show_fractal(None), 0.1)
       
       def show_fractal(self, instance):
           self.update_content(self.fractal_widget)
       
       def show_sensor(self, instance):
           self.update_content(self.sensor_widget)
       
       def show_resonance(self, instance):
           self.update_content(self.resonance_widget)
       
       def show_hypergraph(self, instance):
           self.update_content(self.hypergraph_widget)
       
       def update_content(self, widget):
           self.content_area.clear_widgets()
           if self.current_widget:
               self.current_widget.pause()
           self.content_area.add_widget(widget)
           widget.resume()
           self.current_widget = widget

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        # Einstellungen-UI hier implementieren

class PresentationScreen(Screen):
    def __init__(self, **kwargs):
        super(PresentationScreen, self).__init__(**kwargs)
        # Präsentationsmodus-UI hier implementieren

class FractalSenseApp(App):
    def build(self):
        # Fenstergröße für Mobilgeräte optimieren
        Window.size = (360, 640)
        
        # Screen Manager erstellen
        self.sm = ScreenManager()
        
        # Screens hinzufügen
        self.main_screen = MainScreen(name='main')
        self.sm.add_widget(self.main_screen)
        
        self.settings_screen = SettingsScreen(name='settings')
        self.sm.add_widget(self.settings_screen)
        
        self.presentation_screen = PresentationScreen(name='presentation')
        self.sm.add_widget(self.presentation_screen)
        
        return self.sm

if __name__ == '__main__':
    FractalSenseApp().run()
   ```

2. **Kivy-Interface-Dateien für Module erstellen**
   
   Erstellen Sie für jedes Modul eine `kivy_interface.py` Datei:
   
   Beispiel für `modules/fractal_visualization/kivy_interface.py`:
   ```python
   from kivy.uix.boxlayout import BoxLayout
   from kivy.uix.label import Label
   from kivy.uix.button import Button
   from kivy.graphics.texture import Texture
   from kivy.uix.image import Image
   import numpy as np
   import matplotlib.pyplot as plt
   from io import BytesIO

   class FractalVisualizationWidget(BoxLayout):
       def __init__(self, app_context, **kwargs):
           super(FractalVisualizationWidget, self).__init__(**kwargs)
           self.orientation = 'vertical'
           self.app_context = app_context
           
           # UI-Elemente erstellen
           self.title = Label(text='Fraktal-Visualisierung', 
                             font_size=20, 
                             size_hint=(1, 0.1))
           self.add_widget(self.title)
           
           # Fraktal-Bild
           self.image = Image(size_hint=(1, 0.7))
           self.add_widget(self.image)
           
           # Steuerelemente
           self.controls = BoxLayout(orientation='horizontal', 
                                    size_hint=(1, 0.2))
           
           self.zoom_in_btn = Button(text='Zoom +')
           self.zoom_in_btn.bind(on_press=self.zoom_in)
           self.controls.add_widget(self.zoom_in_btn)
           
           self.zoom_out_btn = Button(text='Zoom -')
           self.zoom_out_btn.bind(on_press=self.zoom_out)
           self.controls.add_widget(self.zoom_out_btn)
           
           self.reset_btn = Button(text='Reset')
           self.reset_btn.bind(on_press=self.reset)
           self.controls.add_widget(self.reset_btn)
           
           self.add_widget(self.controls)
           
           # Fraktal-Parameter
           self.center = complex(-0.75, 0)
           self.zoom = 1.0
           self.max_iter = 100
           
           # Initialisierung
           self.is_active = False
       
       def resume(self):
           self.is_active = True
           self.update_fractal()
       
       def pause(self):
           self.is_active = False
       
       def update_fractal(self):
           if not self.is_active:
               return
               
           # Fraktal berechnen
           fractal = self.calculate_mandelbrot(400, 400, self.max_iter, 
                                              self.center, self.zoom)
           
           # In Textur umwandeln
           buf = BytesIO()
           plt.imsave(buf, fractal, format='png', cmap='viridis')
           buf.seek(0)
           
           # Textur erstellen und anwenden
           texture = Texture.create(size=(400, 400))
           texture.blit_buffer(buf.read(), colorfmt='rgba', bufferfmt='ubyte')
           self.image.texture = texture
           
           # Event senden
           self.app_context['event_system'].emit_event('fractal_updated', {
               'center': self.center,
               'zoom': self.zoom
           })
       
       def calculate_mandelbrot(self, width, height, max_iter, center, zoom):
           # Implementierung der Mandelbrot-Berechnung
           x_min, x_max = center.real - 1.5/zoom, center.real + 1.5/zoom
           y_min, y_max = center.imag - 1.5/zoom, center.imag + 1.5/zoom
           
           x, y = np.meshgrid(np.linspace(x_min, x_max, width),
                             np.linspace(y_min, y_max, height))
           c = x + y * 1j
           z = c.copy()
           
           fractal = np.zeros(z.shape, dtype=np.float32)
           
           for i in range(max_iter):
               mask = np.abs(z) < 2.0
               fractal[mask] = i
               z[mask] = z[mask]**2 + c[mask]
           
           fractal = fractal / max_iter
           return fractal
       
       def zoom_in(self, instance):
           self.zoom *= 1.5
           self.update_fractal()
       
       def zoom_out(self, instance):
           self.zoom /= 1.5
           self.update_fractal()
       
       def reset(self, instance):
           self.center = complex(-0.75, 0)
           self.zoom = 1.0
           self.update_fractal()
   ```

   Ähnliche Interface-Dateien für die anderen Module erstellen.

## Schritt 3: APK erstellen

1. **Buildozer-Konfiguration anpassen**
   Stellen Sie sicher, dass alle erforderlichen Berechtigungen in der `buildozer.spec` Datei konfiguriert sind.

2. **APK bauen**
   ```bash
   # Für Debug-APK
   buildozer android debug
   
   # Für Release-APK
   buildozer android release
   ```

3. **APK signieren (für Release)**
   ```bash
   # Keystore erstellen (einmalig)
   keytool -genkey -v -keystore fractalsense.keystore -alias fractalsense -keyalg RSA -keysize 2048 -validity 10000
   
   # APK signieren
   jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore fractalsense.keystore bin/FractalSense-*-release-unsigned.apk fractalsense
   
   # APK optimieren
   zipalign -v 4 bin/FractalSense-*-release-unsigned.apk bin/FractalSense.apk
   ```

## Schritt 4: APK testen

1. **Auf Emulator testen**
   ```bash
   # Android-Emulator starten
   emulator -avd <emulator_name>
   
   # APK installieren
   adb install bin/FractalSense-*-debug.apk
   ```

2. **Auf physischem Gerät testen**
   - Verbinden Sie Ihr Android-Gerät per USB
   - Aktivieren Sie USB-Debugging in den Entwickleroptionen
   - Führen Sie aus:
     ```bash
     adb install bin/FractalSense-*-debug.apk
     ```

## Schritt 5: APK verteilen

1. **Direkte Verteilung**
   - Kopieren Sie die APK-Datei auf einen USB-Stick oder senden Sie sie per E-Mail
   - Benutzer müssen "Installation aus unbekannten Quellen" aktivieren

2. **Google Play Store (optional)**
   - Erstellen Sie ein Entwicklerkonto im Google Play Store
   - Folgen Sie den Anweisungen zum Hochladen Ihrer App

3. **Alternative App-Stores**
   - F-Droid
   - Amazon App Store
   - Samsung Galaxy Store

## Fehlerbehebung

- **Buildozer-Fehler**: Überprüfen Sie die Logdateien in `.buildozer/logs/`
- **Abhängigkeitsprobleme**: Stellen Sie sicher, dass alle erforderlichen Bibliotheken in `requirements` aufgeführt sind
- **Berechtigungsprobleme**: Überprüfen Sie die Android-Berechtigungen in `buildozer.spec`
- **Kompatibilitätsprobleme**: Testen Sie auf verschiedenen Android-Versionen
