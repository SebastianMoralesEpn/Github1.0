# gui/main_window.py
"""
Clase principal de la ventana de la interfaz gráfica (PyQt5) - Rediseñada.
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QSlider, QGroupBox,
    QTextEdit, QMessageBox, QProgressBar, QFrame, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette

from core.terrain_data import TerrainDataLoader
from core.viewer_3d import Horizon3DViewer
from config import (
    PRESET_LOCATIONS, DEFAULT_VIEW_RADIUS_KM, DEFAULT_FIELD_OF_VIEW,
    EQUATOR_LAT_RANGE, EQUATOR_LON_RANGE, OBSERVER_HEIGHT_M,
    MSG_LOADING_TERRAIN, MSG_GENERATING_VIEW, MSG_READY,
    MSG_ERROR_COORDS, MSG_ERROR_NO_DATA, MSG_ERROR_PYVISTA
)

class ViewGenerationWorker(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    progress = pyqtSignal(str)

    def __init__(self, viewer: Horizon3DViewer, lat: float, lon: float, azimut: int, location_name: str = "Ubicación Personalizada", parent=None):
        super().__init__(parent)
        self.viewer = viewer
        self.lat = lat
        self.lon = lon
        self.azimut = azimut
        self.location_name = location_name

    def run(self):
        try:
            self.progress.emit(MSG_LOADING_TERRAIN)
            if self.viewer.terrain_loader.full_terrain_matrix is None:
                self.viewer.terrain_loader.load_full_terrain_matrix()
            self.progress.emit(MSG_GENERATING_VIEW)
            view_info = self.viewer.generate_3d_view(
                self.lat, self.lon, self.azimut,
                DEFAULT_FIELD_OF_VIEW, DEFAULT_VIEW_RADIUS_KM,
                location_name=self.location_name
            )
            self.finished.emit(view_info)
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualizador del Horizonte - Ecuador")
        self.setGeometry(80, 80, 800, 600)
        self.setWindowIcon(QIcon('assets/icon.png'))

        self.terrain_loader = TerrainDataLoader()
        self.viewer_3d = Horizon3DViewer(self.terrain_loader)
        self.view_thread = None

        self._create_ui()
        self._load_initial_data()

    def _create_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Paleta personalizada para fondo (tonos morados y azules)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#2c003e"))
        main_widget.setAutoFillBackground(True)
        main_widget.setPalette(palette)

        # Header
        header = QLabel("Explorador de Horizontes Geográficos")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Arial", 28, QFont.Bold))
        header.setStyleSheet("color: #FFD700; background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 20px;")
        main_layout.addWidget(header)

        # Subtitle
        subtitle = QLabel("Sistema Avanzado de Visualización Topográfica")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Arial", 16))
        subtitle.setStyleSheet("color: #00ff88; background: linear-gradient(90deg, #0f3460, #16213e); border-radius: 10px; padding: 10px;")
        main_layout.addWidget(subtitle)

        # Horizontal layout for main controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(20)

        # Left panel: Locations & Coordinates
        left_panel = QVBoxLayout()
        left_panel.addWidget(self._create_preset_locations_group())
        left_panel.addWidget(self._create_custom_coordinates_group())
        controls_layout.addLayout(left_panel)

        # Middle panel: Direction
        controls_layout.addWidget(self._create_view_direction_group())

        # Right panel: Info & Status
        right_panel = QVBoxLayout()
        right_panel.addWidget(self._create_info_status_group())
        controls_layout.addLayout(right_panel)

        main_layout.addLayout(controls_layout)

        # Separator line
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        sep.setStyleSheet("color: #21e6c1;")
        main_layout.addWidget(sep)

        # Bottom controls
        bottom_controls = QHBoxLayout()
        bottom_controls.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        bottom_controls.addWidget(self._create_controls_group())
        bottom_controls.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        main_layout.addLayout(bottom_controls)

        main_layout.addStretch(1)
        self._update_info_panel()

    def _create_preset_locations_group(self):
        group_box = QGroupBox("🗺️ Destinos Turísticos")
        group_box.setStyleSheet("""
            QGroupBox { 
                font-weight: bold; 
                color: #FFD700; 
                background: linear-gradient(135deg, #0f3460, #16213e); 
                border-radius: 12px; 
                padding: 15px; 
                border: 2px solid #FFD700;
            }
        """)
        layout = QVBoxLayout()
        self.preset_combo = QComboBox()
        self.preset_combo.setStyleSheet("""
            background: #FFD700; 
            color: #16213e; 
            font-weight: bold; 
            font-size: 12px;
            border-radius: 8px;
            padding: 8px;
        """)
        self.preset_combo.addItem("🎯 Seleccione un destino...")
        for name in PRESET_LOCATIONS.keys():
            self.preset_combo.addItem(name)
        self.preset_combo.currentIndexChanged.connect(self._load_preset_location)
        layout.addWidget(self.preset_combo)
        group_box.setLayout(layout)
        return group_box

    def _create_custom_coordinates_group(self):
        group_box = QGroupBox("📍 Coordenadas Personalizadas")
        group_box.setStyleSheet("""
            QGroupBox { 
                font-weight: bold; 
                color: #00ff88; 
                background: linear-gradient(135deg, #16213e, #0f3460); 
                border-radius: 12px; 
                padding: 15px;
                border: 2px solid #00ff88;
            }
        """)
        layout = QVBoxLayout()

        lat_layout = QHBoxLayout()
        lat_label = QLabel("🌍 Latitud:")
        lat_label.setStyleSheet("color: #FFD700; font-weight: bold;")
        lat_layout.addWidget(lat_label)
        first_location = list(PRESET_LOCATIONS.keys())[0]
        self.lat_input = QLineEdit(str(PRESET_LOCATIONS[first_location][0]))
        self.lat_input.setPlaceholderText(f"{EQUATOR_LAT_RANGE[0]}° a {EQUATOR_LAT_RANGE[1]}°")
        self.lat_input.setStyleSheet("""
            background: #FFD700; 
            color: #16213e; 
            font-weight: bold;
            border-radius: 8px;
            padding: 5px;
        """)
        self.lat_input.textChanged.connect(self._update_info_panel)
        lat_layout.addWidget(self.lat_input)
        layout.addLayout(lat_layout)

        lon_layout = QHBoxLayout()
        lon_label = QLabel("🌎 Longitud:")
        lon_label.setStyleSheet("color: #FFD700; font-weight: bold;")
        lon_layout.addWidget(lon_label)
        self.lon_input = QLineEdit(str(PRESET_LOCATIONS[first_location][1]))
        self.lon_input.setPlaceholderText(f"{EQUATOR_LON_RANGE[0]}° a {EQUATOR_LON_RANGE[1]}°")
        self.lon_input.setStyleSheet("""
            background: #FFD700; 
            color: #16213e; 
            font-weight: bold;
            border-radius: 8px;
            padding: 5px;
        """)
        self.lon_input.textChanged.connect(self._update_info_panel)
        lon_layout.addWidget(self.lon_input)
        layout.addLayout(lon_layout)

        group_box.setLayout(layout)
        return group_box

    def _create_view_direction_group(self):
        group_box = QGroupBox("Dirección")
        group_box.setStyleSheet("""
            QGroupBox { font-weight: bold; color: #21e6c1; background: #16213e; border-radius: 8px; padding: 10px; }
        """)
        layout = QVBoxLayout()

        azimut_layout = QHBoxLayout()
        azimut_label = QLabel("Azimut:")
        azimut_label.setStyleSheet("color: #e94560;")
        azimut_layout.addWidget(azimut_label)
        self.azimut_slider = QSlider(Qt.Vertical)
        self.azimut_slider.setRange(0, 359)
        self.azimut_slider.setValue(90)
        self.azimut_slider.setTickInterval(30)
        self.azimut_slider.setTickPosition(QSlider.TicksRight)
        self.azimut_slider.setStyleSheet("""
            QSlider::groove:vertical { background: #21e6c1; height: 8px; border-radius: 4px; }
            QSlider::handle:vertical { background: #e94560; border: 2px solid #21e6c1; height: 20px; margin: -2px 0; border-radius: 10px; }
        """)
        self.azimut_slider.valueChanged.connect(self._update_azimut_display)
        self.azimut_slider.valueChanged.connect(self._update_info_panel)
        azimut_layout.addWidget(self.azimut_slider)

        self.azimut_value_label = QLabel("90° (Este)")
        self.azimut_value_label.setStyleSheet("color: #21e6c1; font-weight: bold;")
        azimut_layout.addWidget(self.azimut_value_label)
        layout.addLayout(azimut_layout)

        # Direction buttons (circle layout)
        button_layout = QHBoxLayout()
        for text, value, color in [
            ("N", 0, "#21e6c1"), ("E", 90, "#e94560"),
            ("S", 180, "#21e6c1"), ("O", 270, "#e94560")
        ]:
            btn = QPushButton(text)
            btn.setStyleSheet(f"background: {color}; color: #16213e; font-weight: bold; border-radius: 15px; padding: 10px;")
            btn.clicked.connect(lambda checked, v=value: self.azimut_slider.setValue(v))
            button_layout.addWidget(btn)
        layout.addLayout(button_layout)

        group_box.setLayout(layout)
        return group_box

    def _create_controls_group(self):
        group_box = QGroupBox()
        group_box.setStyleSheet("background: #0f3460; border-radius: 8px; padding: 10px;")
        layout = QHBoxLayout()

        self.generate_button = QPushButton("Generar el horizonte")
        self.generate_button.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #21e6c1, stop:1 #e94560);
            color: #16213e; font-size: 18px; font-weight: bold; border-radius: 10px; padding: 15px;
        """)
        self.generate_button.clicked.connect(self._start_view_generation)
        layout.addWidget(self.generate_button)

        exit_button = QPushButton("Salir de la aplicación")
        exit_button.setStyleSheet("""
            background: #e94560; color: white; font-size: 16px; border-radius: 10px; padding: 12px;
        """)
        exit_button.clicked.connect(self.close)
        layout.addWidget(exit_button)

        group_box.setLayout(layout)
        return group_box

    def _create_info_status_group(self):
        group_box = QGroupBox("📊 Información Detallada")
        group_box.setStyleSheet("""
            QGroupBox { 
                font-weight: bold; 
                color: #ffcc00; 
                background: linear-gradient(135deg, #3a0ca3, #720026); 
                border-radius: 15px; 
                padding: 20px;
                border: 3px solid #ffcc00;
            }
        """)
        layout = QVBoxLayout()

        self.info_text_edit = QTextEdit()
        self.info_text_edit.setReadOnly(True)
        self.info_text_edit.setFixedHeight(150)
        self.info_text_edit.setStyleSheet("""
            background: #ffcc00; 
            color: #1a1a1a; 
            font-family: 'Consolas'; 
            font-size: 16px; 
            border-radius: 10px;
            padding: 10px;
        """)
        layout.addWidget(self.info_text_edit)

        self.status_bar_label = QLabel(MSG_READY)
        self.status_bar_label.setStyleSheet("""
            font-size: 15px; 
            color: #ffcc00; 
            background: #720026; 
            border-radius: 10px; 
            padding: 10px;
            font-weight: bold;
        """)
        layout.addWidget(self.status_bar_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setStyleSheet("""
            QProgressBar { background: #720026; color: #ffcc00; border-radius: 10px; }
            QProgressBar::chunk { background: #ffcc00; }
        """)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        group_box.setLayout(layout)
        return group_box


    def _load_initial_data(self):
        self.status_bar_label.setText("Cargando datos de terreno...")
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        self.initial_load_thread = QThread()
        self.terrain_loader.moveToThread(self.initial_load_thread)
        self.initial_load_thread.started.connect(self.terrain_loader.load_full_terrain_matrix)
        self.terrain_loader.full_terrain_matrix_loaded.connect(self._on_initial_terrain_loaded)
        self.terrain_loader.error_loading_matrix.connect(self._on_initial_terrain_error)
        self.initial_load_thread.start()

    def _on_initial_terrain_loaded(self):
        self.status_bar_label.setText(MSG_READY)
        self.progress_bar.hide()
        self.initial_load_thread.quit()
        self.initial_load_thread.wait()
        QMessageBox.information(self, "Carga Completa", "Datos de terreno cargados exitosamente.")

    def _on_initial_terrain_error(self, error_msg):
        self.status_bar_label.setText(f"Error al cargar datos: {error_msg}")
        self.progress_bar.hide()
        self.initial_load_thread.quit()
        self.initial_load_thread.wait()
        QMessageBox.critical(self, "Error de Carga", f"No se pudieron cargar los datos de terreno:\n{error_msg}")
        self.generate_button.setEnabled(False)

    def _load_preset_location(self):
        selected_text = self.preset_combo.currentText()
        if selected_text in PRESET_LOCATIONS:
            lat, lon = PRESET_LOCATIONS[selected_text]
            self.lat_input.setText(str(lat))
            self.lon_input.setText(str(lon))
            self.status_bar_label.setText(f"Ubicación: {selected_text}")
        self._update_info_panel()

    def _update_azimut_display(self, value):
        direction = self.viewer_3d._get_cardinal_direction(value)
        self.azimut_value_label.setText(f"{value}° ({direction})")

    def _update_info_panel(self):
        try:
            lat = float(self.lat_input.text())
            lon = float(self.lon_input.text())
            azimut = self.azimut_slider.value()
            direction = self.viewer_3d._get_cardinal_direction(azimut)
            
            # Find location name
            location_name = "📍 Ubicación Personalizada"
            for name, coords in PRESET_LOCATIONS.items():
                if abs(coords[0] - lat) < 0.01 and abs(coords[1] - lon) < 0.01:
                    location_name = name
                    break
            
            info = (
                f"📍 Lugar: {location_name}\n"
                f"🌍 Latitud: {lat:.6f}°\n"
                f"🌎 Longitud: {lon:.6f}°\n"
                f"🧭 Dirección: {azimut}° ({direction})\n"
                f"📏 Radio: {DEFAULT_VIEW_RADIUS_KM}km | Campo: {DEFAULT_FIELD_OF_VIEW}° | Altura: Terreno+{OBSERVER_HEIGHT_M}m"
            )
            self.info_text_edit.setText(info)
        except ValueError:
            self.info_text_edit.setText("⚠️ Coordenadas inválidas")

    def _validate_coordinates(self) -> bool:
        try:
            lat = float(self.lat_input.text())
            lon = float(self.lon_input.text())
            if not (EQUATOR_LAT_RANGE[0] <= lat <= EQUATOR_LAT_RANGE[1] and
                    EQUATOR_LON_RANGE[0] <= lon <= EQUATOR_LON_RANGE[1]):
                QMessageBox.warning(self, "Coordenadas Fuera de Rango", MSG_ERROR_COORDS)
                return False
            return True
        except ValueError:
            QMessageBox.warning(self, "Entrada Inválida", "Latitud y Longitud deben ser números.")
            return False

    def _start_view_generation(self):
        if not self._validate_coordinates():
            return
        lat = float(self.lat_input.text())
        lon = float(self.lon_input.text())
        azimut = self.azimut_slider.value()

        # Obtener nombre de ubicación
        location_name = "Ubicación Personalizada"
        for name, coords in PRESET_LOCATIONS.items():
            if abs(coords[0] - lat) < 0.01 and abs(coords[1] - lon) < 0.01:
                location_name = name
                break

        reply = QMessageBox.question(self, "Confirmación de Vista",
                                     f"¿Seguro quiere denerar la vista para?:\n\n"
                                     f"\nLatitud: {lat:.6f}°\n"
                                     f"Longitud: {lon:.6f}°\n"
                                     f"Dirección: {azimut}° ({self.viewer_3d._get_cardinal_direction(azimut)})\n"
                                     f"Lugar: {location_name}\n\n"
                                     f"Esto abrirá una ventana separada.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.generate_button.setEnabled(False)
            self.status_bar_label.setText(MSG_GENERATING_VIEW)
            self.progress_bar.show()
            self.progress_bar.setValue(0)
            # Pasar nombre de ubicación al worker
            self.view_thread = ViewGenerationWorker(self.viewer_3d, lat, lon, azimut, location_name)
            self.view_thread.finished.connect(self._on_view_generated)
            self.view_thread.error.connect(self._on_view_error)
            self.view_thread.progress.connect(self.status_bar_label.setText)
            self.view_thread.start()

    def _on_view_generated(self, view_info: dict):
        self.status_bar_label.setText(MSG_READY)
        self.generate_button.setEnabled(True)
        self.progress_bar.hide()
        QMessageBox.information(self, "Vista Generada", "La vista ha sido generada exitosamente. La ventana de visualización se abrirá.")
        self.viewer_3d.show_view()

    def _on_view_error(self, error_msg: str):
        self.status_bar_label.setText(f"Error: {error_msg}")
        self.generate_button.setEnabled(True)
        self.progress_bar.hide()
        QMessageBox.critical(self, "Error de Visualización", f"No se pudo generar la vista:\n{error_msg}")
        if "PyVista no está instalado" in error_msg:
            QMessageBox.information(self, "Instalación Requerida", "Por favor, instale PyVista: pip install pyvista")

    def closeEvent(self, event):
        if self.view_thread and self.view_thread.isRunning():
            self.view_thread.quit()
            self.view_thread.wait()
        if self.viewer_3d.plotter:
            self.viewer_3d.plotter.close()
        super().closeEvent(event)
