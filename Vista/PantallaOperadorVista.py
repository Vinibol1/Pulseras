from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QGridLayout, QLabel, QSizePolicy, QSpacerItem, QHBoxLayout
from PySide6.QtCore import Qt

class PantallaOperadorVista(QWidget):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        self.setWindowTitle("Pantalla Operador")
        self.resize(800, 600)  

        layout = QVBoxLayout()
        layout.setSpacing(20)  # Menos espacio
        layout.setContentsMargins(40, 50, 40, 30)

        self.label = QLabel("Ingrese el NOMBRE Y APELLIDO:")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 30px; font-weight: bold;")
        layout.addWidget(self.label)

        self.nombre_edit = QLineEdit()
        self.nombre_edit.setAlignment(Qt.AlignCenter)
        self.nombre_edit.setStyleSheet("font-size: 25px; min-height: 80px;")
        self.nombre_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.nombre_edit)

        # Quitar el spacer entre input y teclado
        # layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Contenedor para el teclado
        teclado_widget = QWidget()
        teclado_layout = self.crear_teclado()
        teclado_widget.setLayout(teclado_layout)
        teclado_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(teclado_widget)

        # Botón OK grande abajo a la derecha
        ok_layout = QHBoxLayout()
        ok_layout.addStretch()
        self.btn_ok = QPushButton("OK")
        self.btn_ok.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_ok.setStyleSheet("font-size: 35px; min-width: 150px; min-height: 100px; background-color: #388e3c; color: white; border-radius: 16px;")
        self.btn_ok.clicked.connect(self.enviar_nombre)
        ok_layout.addWidget(self.btn_ok)
        layout.addLayout(ok_layout)

        # layout.addSpacerItem(QSpacerItem(10, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)
        self.set_dark_theme()  

    def crear_teclado(self):
        grid = QGridLayout()
        grid.setSpacing(20)
        filas = [
            "1234567890",
            "QWERTYUIOP'",
            "ASDFGHJKLÑ",
            "ZXCVBNM"
        ]
        # Fila de números (sin desplazamiento)
        for col, numero in enumerate(filas[0]):
            btn = QPushButton(numero)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setStyleSheet("font-size: 30px; min-width: 70px; min-height: 80px;")  
            btn.clicked.connect(lambda _, n=numero: self.nombre_edit.insert(n))
            grid.addWidget(btn, 0, col)
        # Primera fila de letras 
        for col, letra in enumerate(filas[1]):
            btn = QPushButton(letra)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setStyleSheet("font-size: 30px; min-width: 70px; min-height: 80px;")  
            btn.clicked.connect(lambda _, l=letra: self.nombre_edit.insert(l))
            grid.addWidget(btn, 1, col)
        # Segunda fila de letras (desplazada una columna)
        for col, letra in enumerate(filas[2]):
            btn = QPushButton(letra)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setStyleSheet("font-size: 30px; min-width: 70px; min-height: 80px;")  
            btn.clicked.connect(lambda _, l=letra: self.nombre_edit.insert(l))
            grid.addWidget(btn, 2, col + 1)
        # Tercera fila de letras (desplazada dos columnas)
        for col, letra in enumerate(filas[3]):
            btn = QPushButton(letra)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setStyleSheet("font-size: 30px; min-width: 70px; min-height: 80px;")  
            btn.clicked.connect(lambda _, l=letra: self.nombre_edit.insert(l))
            grid.addWidget(btn, 3, col + 2)
        # Botón espacio
        btn_espacio = QPushButton("Espacio")
        btn_espacio.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn_espacio.setStyleSheet("font-size: 25px; min-width: 150px; min-height: 80px;")  
        btn_espacio.clicked.connect(lambda: self.nombre_edit.insert(" "))
        grid.addWidget(btn_espacio, 4, 4, 1, 4)  # Ajustado a fila 4
        # Botón borrar una letra (Backspace)
        btn_borrar = QPushButton("←")
        btn_borrar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn_borrar.setStyleSheet("font-size: 30px; min-width: 70px; min-height: 80px;")  
        btn_borrar.clicked.connect(self.borrar_una_letra)
        grid.addWidget(btn_borrar, 0, 10)
        # Botón limpiar todo
        btn_limpiar = QPushButton("Limpiar")
        btn_limpiar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn_limpiar.setStyleSheet("font-size: 20px; min-width: 65px; min-height: 80px;")  # Aumentado a 80px
        btn_limpiar.clicked.connect(self.nombre_edit.clear)
        grid.addWidget(btn_limpiar, 0, 11)
        # Elimina el botón OK del teclado
        # btn_ok = QPushButton("OK")
        # btn_ok.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # btn_ok.setStyleSheet("font-size: 30px; min-width: 65px; min-height: 170px;")
        # btn_ok.clicked.connect(self.enviar_nombre)
        # grid.addWidget(btn_ok, 1, 11, 3, 1)  # Ajustado para abarcar 3 filas
        return grid

    def borrar_una_letra(self):
        texto = self.nombre_edit.text()
        self.nombre_edit.setText(texto[:-1])

    def enviar_nombre(self):
        nombre = self.nombre_edit.text()
        self.controlador.agregar_persona(nombre)
        self.nombre_edit.clear()
        # Llama a asociar_pulsera en la vista de administrador
        self.controlador.vista_admin.asociar_pulsera()

    def set_dark_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #232629;
                color: #f0f0f0;
            }
            QLineEdit {
                background-color: #31363b;
                color: #f0f0f0;
                border: 2px solid #555;
                border-radius: 8px;
            }
            QPushButton {
                background-color: #31363b;
                color: #f0f0f0;
                border: 1px solid #555;
                border-radius: 8px;
            }
            QPushButton:pressed {
                background-color: #232629;
            }
            QLabel {
                color: #f0f0f0;
            }
        """)