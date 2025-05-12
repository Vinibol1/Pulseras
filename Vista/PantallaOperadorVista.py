from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QGridLayout, QLabel, QSizePolicy, QSpacerItem
from PySide6.QtCore import Qt

class PantallaOperadorVista(QWidget):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        self.setWindowTitle("Pantalla Operador")
        self.setFixedSize(1024, 768)  # <-- Fijar resolución

        layout = QVBoxLayout()
        layout.setSpacing(40)
        layout.setContentsMargins(70, 80, 70, 80)

        self.label = QLabel("Ingrese el nombre y apellido:")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 30px; font-weight: bold;")
        layout.addWidget(self.label)

        self.nombre_edit = QLineEdit()
        self.nombre_edit.setAlignment(Qt.AlignCenter)
        self.nombre_edit.setStyleSheet("font-size: 25px; min-height: 80px;")
        self.nombre_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.nombre_edit)

        layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Contenedor para el teclado
        teclado_widget = QWidget()
        teclado_layout = self.crear_teclado()
        teclado_widget.setLayout(teclado_layout)
        teclado_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(teclado_widget)

        layout.addSpacerItem(QSpacerItem(30, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def crear_teclado(self):
        grid = QGridLayout()
        grid.setSpacing(10)
        filas = [
            "QWERTYUIOP",
            "ASDFGHJKLÑ",
            "ZXCVBNM"
        ]
        # Primera fila (desplazada una columna)
        for col, letra in enumerate(filas[0]):
            btn = QPushButton(letra)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setStyleSheet("font-size: 30px; min-width: 70px; min-height: 70px;")
            btn.clicked.connect(lambda _, l=letra: self.nombre_edit.insert(l))
            grid.addWidget(btn, 0, col + 1)
        # Segunda fila (desplazada dos columnas)
        for col, letra in enumerate(filas[1]):
            btn = QPushButton(letra)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setStyleSheet("font-size: 30px; min-width: 70px; min-height: 70px;")
            btn.clicked.connect(lambda _, l=letra: self.nombre_edit.insert(l))
            grid.addWidget(btn, 1, col + 2)
        # Tercera fila (desplazada tres columnas)
        for col, letra in enumerate(filas[2]):
            btn = QPushButton(letra)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setStyleSheet("font-size: 30px; min-width: 70px; min-height: 70px;")
            btn.clicked.connect(lambda _, l=letra: self.nombre_edit.insert(l))
            grid.addWidget(btn, 2, col + 3)

        # Botón espacio
        btn_espacio = QPushButton("Espacio")
        btn_espacio.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn_espacio.setStyleSheet("font-size: 25px; min-width: 150px; min-height: 70px;")
        btn_espacio.clicked.connect(lambda: self.nombre_edit.insert(" "))
        grid.addWidget(btn_espacio, 3, 5, 1, 3)  # Ajusta la posición y el tamaño según lo necesites

        # Botón borrar una letra (Backspace)
        btn_borrar = QPushButton("←")
        btn_borrar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn_borrar.setStyleSheet("font-size: 30px; min-width: 70px; min-height: 70px;")
        btn_borrar.clicked.connect(self.borrar_una_letra)
        grid.addWidget(btn_borrar, 0, 11)

        # Botón limpiar todo
        btn_limpiar = QPushButton("Limpiar")
        btn_limpiar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn_limpiar.setStyleSheet("font-size: 20px; min-width: 70px; min-height: 70px;")
        btn_limpiar.clicked.connect(self.nombre_edit.clear)
        grid.addWidget(btn_limpiar, 0, 12, 1, 1)

        # Botón OK grande
        btn_ok = QPushButton("OK")
        btn_ok.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn_ok.setStyleSheet("font-size: 30px; min-width: 70px; min-height: 170px;")
        btn_ok.clicked.connect(self.enviar_nombre)
        grid.addWidget(btn_ok, 1, 12, 2, 1)

        return grid

    def borrar_una_letra(self):
        texto = self.nombre_edit.text()
        self.nombre_edit.setText(texto[:-1])

    def enviar_nombre(self):
        nombre = self.nombre_edit.text()
        self.controlador.agregar_persona(nombre)
        self.nombre_edit.clear()