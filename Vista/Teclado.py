class Teclado(QWidget):
        def __init__(self, controlador):
        super().__init__()



        def crear_teclado(self):
                grid = QGridLayout()
                # Distribución tipo teclado QWERTY
                filas = [
                "QWERTYUIOP",
                "ASDFGHJKLÑ",
                "ZXCVBNM"
                ]
                # Primera fila
                for col, letra in enumerate(filas[0]):
                btn = QPushButton(letra)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                btn.setStyleSheet("font-size: 3vw; min-width: 90px; min-height: 90px;")
                btn.clicked.connect(lambda _, l=letra: self.nombre_edit.insert(l))
                grid.addWidget(btn, 0, col)
                # Segunda fila (ligero desplazamiento)
                for col, letra in enumerate(filas[1]):
                btn = QPushButton(letra)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                btn.setStyleSheet("font-size: 3vw; min-width: 90px; min-height: 90px;")
                btn.clicked.connect(lambda _, l=letra: self.nombre_edit.insert(l))
                grid.addWidget(btn, 1, col + 1)
                # Tercera fila (más desplazada)
                for col, letra in enumerate(filas[2]):
                btn = QPushButton(letra)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                btn.setStyleSheet("font-size: 3vw; min-width: 90px; min-height: 90px;")
                btn.clicked.connect(lambda _, l=letra: self.nombre_edit.insert(l))
                grid.addWidget(btn, 2, col + 2)

                # Botón borrar una letra (Backspace)
                btn_borrar = QPushButton("←")
                btn_borrar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                btn_borrar.setStyleSheet("font-size: 3vw; min-width: 120px; min-height: 90px;")
                btn_borrar.clicked.connect(self.borrar_una_letra)
                grid.addWidget(btn_borrar, 2, 10)

                # Botón limpiar todo
                btn_limpiar = QPushButton("Limpiar")
                btn_limpiar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                btn_limpiar.setStyleSheet("font-size: 2vw; min-width: 120px; min-height: 90px;")
                btn_limpiar.clicked.connect(self.nombre_edit.clear)
                grid.addWidget(btn_limpiar, 0, 11, 1, 1)

                # Botón OK grande
                btn_ok = QPushButton("OK")
                btn_ok.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                btn_ok.setStyleSheet("font-size: 3vw; min-width: 120px; min-height: 180px;")
                btn_ok.clicked.connect(self.enviar_nombre)
                grid.addWidget(btn_ok, 1, 11, 2, 1)

        return grid