# filepath: /home/tobias/Documentos/Pulseras/src/main.py

from Vista.PantallaOperadorVista import PantallaOperadorVista
from Vista.PantallaAdministradorVista import PantallaAdministradorVista
from Controlador.FlujoPrograma import FlujoPrograma

def main():
    flujo = FlujoPrograma()
    flujo.iniciar()

if __name__ == "__main__":
    main()