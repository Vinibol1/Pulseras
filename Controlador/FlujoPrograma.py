import pickle
import os
from PySide6.QtWidgets import QApplication
from Modelo.Persona import Persona
from Vista.PantallaOperadorVista import PantallaOperadorVista
from Vista.PantallaAdministradorVista import PantallaAdministradorVista

#ruta = os.path.join(os.environ["LOCALAPPDATA"], "Pulseras")
#os.makedirs(ruta, exist_ok=True)
archivo = os.path.join("personas.pkl")

class FlujoPrograma:
    def __init__(self):
        self.app = QApplication([])
        self.personas = []
        self.cargar_personas() 
        self.vista_operador = PantallaOperadorVista(self)
        self.vista_admin = PantallaAdministradorVista(self)

    def iniciar(self):
        self.vista_operador.show()
        self.vista_admin.show()
        self.app.exec()

    def agregar_persona(self, nombre):
        if nombre:
            self.personas.append(Persona(nombre))
            self.vista_admin.actualizar_tabla(seleccionar_fila=len(self.personas) - 1, seleccionar_columna=1)  # 1 es la columna "Unidad"
            self.guardar_personas()

    def obtener_personas(self):
        return self.personas

    def asociar_pulsera(self, idx, pulsera):
        if 0 <= idx < len(self.personas):
            self.personas[idx].pulsera = pulsera
            self.guardar_personas()

    def eliminar_persona(self, idx):
        if 0 <= idx < len(self.personas):
            del self.personas[idx]
            self.guardar_personas()

    def guardar_personas(self):
        with open(archivo, "wb") as f:
            pickle.dump(self.personas, f)

    def cargar_personas(self):
        try:
            with open(archivo, "rb") as f:
                self.personas = pickle.load(f)
        except FileNotFoundError:
            self.personas = []

    def reestablecer_todo(self):
        self.personas = []
        self.guardar_personas()
        self.vista_admin.actualizar_tabla()
        self.vista_operador.actualizar_tabla()