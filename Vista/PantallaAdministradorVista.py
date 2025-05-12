from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QInputDialog, QHeaderView, QLineEdit
)
from PySide6.QtGui import QFont, Qt, QIcon

class PantallaAdministradorVista(QWidget):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        self.setWindowTitle("Pantalla Administrador")
        self.resize(1400, 1000)
        layout = QVBoxLayout()
        # Barra de búsqueda
        self.buscador = QLineEdit()
        self.buscador.setPlaceholderText("Buscar por nombre...")
        self.buscador.textChanged.connect(self.actualizar_tabla)
        layout.addWidget(self.buscador)
        # Tabla con 3 columnas
        self.tabla = QTableWidget(0, 3)
        self.tabla.setHorizontalHeaderLabels(["Nombre", "Pulsera", "Eliminar"])
        self.tabla.setFont(QFont("Arial", 15))
        self.tabla.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tabla.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.tabla.setColumnWidth(2, 60)  # Ajusta el ancho de la columna "Eliminar"
        self.tabla.verticalHeader().setVisible(True)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.tabla)
        self.btn_asociar = QPushButton("Asociar Pulsera")
        self.btn_asociar.setFont(QFont("Arial", 18))
        self.btn_asociar.setFixedHeight(100)
        self.btn_asociar.clicked.connect(self.asociar_pulsera)
        layout.addWidget(self.btn_asociar)

        # Botón de restablecer en la esquina inferior derecha
        h_layout = QHBoxLayout()
        h_layout.addStretch()  
        self.btn_reset = QPushButton("Restablecer Todo")
        self.btn_reset.setFont(QFont("Arial", 18))
        self.btn_reset.setStyleSheet("background-color: darkred; color: white;")
        self.btn_reset.setFixedHeight(50)
        self.btn_reset.clicked.connect(self.reestablecer_todo)
        h_layout.addWidget(self.btn_reset)
        layout.addLayout(h_layout)

        self.setLayout(layout)
        self.tabla.cellChanged.connect(self.pulsera_editada)
        self.actualizar_tabla()
        self.set_dark_theme()  

    def set_dark_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #232629;
                color: #f0f0f0;
            }
            QLineEdit {
                background-color: #232629;
                color: #f0f0f0;
                border: 2px solid #555;
                border-radius: 8px;
            }
            QTableWidget {
                background-color: #232629;
                color: #f0f0f0;
                border: 2px solid #555;
                border-radius: 8px;
                gridline-color: #555;
            }
            QHeaderView::section {
                background-color: #232629;
                color: #f0f0f0;
                font-weight: bold;
                border: 1px solid #555;
            }
                QTableCornerButton::section {
                background-color: #232629;
                border: 1px solid #555;
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

    def mensaje_confirmacion(self, titulo, texto):
        msg = QMessageBox(self)
        msg.setWindowTitle(titulo)
        msg.setText(texto)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setButtonText(QMessageBox.Yes, "Sí")
        msg.setFont(QFont("Arial", 32))
        msg.setStyleSheet(
            "QLabel{min-width: 600px; min-height: 120px;} "
            "QPushButton{font-size: 32px; min-width: 200px; min-height: 100px;}"
        )
        return msg.exec()

    def actualizar_tabla(self):
        filtro = self.buscador.text().lower() if hasattr(self, 'buscador') else ""
        personas = [p for p in self.controlador.obtener_personas() if p is not None]  
        personas_filtradas = [
            p for p in personas
            if filtro in p.nombre.lower() or filtro in (p.pulsera or "").lower()
        ]
        self.tabla.blockSignals(True)
        self.tabla.setRowCount(len(personas_filtradas))
        for i, persona in enumerate(personas_filtradas):
            nombre_item = QTableWidgetItem(persona.nombre)
            nombre_item.setFlags(nombre_item.flags())
            nombre_item.setFont(QFont("Arial", 15))
            self.tabla.setItem(i, 0, nombre_item)
            pulsera_item = QTableWidgetItem(persona.pulsera or "")
            pulsera_item.setFont(QFont("Arial", 15))
            self.tabla.setItem(i, 1, pulsera_item)
            # Botón eliminar centrado
            btn_eliminar = QPushButton("✖")
            btn_eliminar.setFixedSize(30, 30)
            btn_eliminar.setStyleSheet(
                "background-color: darkred; color: white; font-size: 20px;"
            )
            btn_eliminar.clicked.connect(lambda _, row=i: self.eliminar_persona(row))
            widget_centro = QWidget()
            layout_centro = QHBoxLayout(widget_centro)
            layout_centro.addStretch()
            layout_centro.addWidget(btn_eliminar)
            layout_centro.addStretch()
            layout_centro.setContentsMargins(0, 0, 0, 0)
            self.tabla.setCellWidget(i, 2, widget_centro)
        self.tabla.blockSignals(False)
        if personas_filtradas:
            self.tabla.selectRow(len(personas_filtradas) - 1)

    def validar_pulsera(self, row, pulsera):
        persona = self.controlador.obtener_personas()[row]
        valor_anterior = persona.pulsera or ""
        if self.pulsera_ya_asignada(pulsera, exclude_row=row):
            respuesta = self.mensaje_confirmacion(
                "Pulsera ya asignada",
                "Esa pulsera ya está asignada a otra persona.\n¿Está seguro de que desea reasignarla?"
            )
            if respuesta != QMessageBox.Yes:
                self.tabla.blockSignals(True)
                self.tabla.setItem(row, 1, QTableWidgetItem(persona.pulsera or ""))
                self.tabla.blockSignals(False)
                return 0
        if valor_anterior != "" and pulsera != valor_anterior:
            respuesta = self.mensaje_confirmacion(
                "Cambiar pulsera",
                "Esta seguro que desea cambiar la pulsera de esta persona?"
            )
            if respuesta != QMessageBox.Yes:
                self.tabla.blockSignals(True)
                self.tabla.setItem(row, 1, QTableWidgetItem(valor_anterior))
                self.tabla.blockSignals(False)
                return 0
        return 1

    def asociar_pulsera(self):
        personas = self.controlador.obtener_personas()
        if not personas:
            return
        fila = len(personas) - 1  # Siempre la última persona
        self.tabla.selectRow(fila)

        # QInputDialog personalizado para pantalla táctil
        dialog = QInputDialog(self)
        dialog.setCancelButtonText("Cancelar")
        dialog.setOkButtonText("Aceptar")
        dialog.setWindowTitle("Pulsera")
        dialog.setLabelText("Ingrese el código de la pulsera:")
        dialog.setFont(QFont("Arial", 32))
        dialog.setStyleSheet(
            "QLabel{min-width: 600px; min-height: 120px; font-size: 32px;} "
            "QLineEdit{font-size: 32px; min-height: 80px;} "
            "QPushButton{font-size: 32px; min-width: 200px; min-height: 100px;}"
        )
        dialog.resize(800, 300)
        if dialog.exec() == QInputDialog.Accepted:
            pulsera = dialog.textValue()
            if self.validar_pulsera(fila, pulsera) == 0:
                return
            self.controlador.asociar_pulsera(fila, pulsera)
            self.actualizar_tabla()

    def pulsera_editada(self, row, column):
        if column == 1:
            pulsera = self.tabla.item(row, column).text()
            if self.validar_pulsera(row, pulsera) == 0:
                return
            self.controlador.asociar_pulsera(row, pulsera)

    def pulsera_ya_asignada(self, pulsera, exclude_row=None):
        if not pulsera:
            return False
        personas = self.controlador.obtener_personas()
        for idx, persona in enumerate(personas):
            if idx == exclude_row:
                continue
            if persona.pulsera == pulsera:
                return True
        return False

    def closeEvent(self, event):
        """Guardar datos al cerrar la ventana."""
        self.controlador.guardar_personas()  # Debes implementar este método en el controlador
        event.accept()

    def reestablecer_todo(self):
        respuesta = self.mensaje_confirmacion(
            "Restablecer todo",
            "¿Está seguro de que desea restablecer todas las personas y pulseras a 0? Esta acción no se puede deshacer."
        )
        if respuesta == QMessageBox.Yes:
            self.controlador.reestablecer_todo()  # Debes implementar este método en el controlador
            self.actualizar_tabla()

    def eliminar_persona(self, row):
        respuesta = self.mensaje_confirmacion(
            "Eliminar persona",
            "¿Está seguro de que desea eliminar a esta persona?"
        )
        if respuesta == QMessageBox.Yes:
            self.controlador.eliminar_persona(row)
            self.actualizar_tabla()