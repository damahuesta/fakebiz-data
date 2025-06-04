from fake_clientes import ClientesFaker
from fake_contratos import ContratosFaker
from fake_contactos import ContactosFaker
from fake_direcciones import DireccionesFaker
from fake_exclientes import ExClientesFaker
from fake_envios import EnviosFaker
from fake_cuentas_bloqueadas import CuentasBloqueadasFaker

class Main:
    """
    Clase principal para generar y guardar los datos falsos.
    """
    def read(self):
        """
        Genera los datos falsos.
        """
        self.clientes = ClientesFaker(n_clientes=10000)
        self.contratos = ContratosFaker(self.clientes)
        self.contactos = ContactosFaker(self.clientes)
        self.direcciones = DireccionesFaker(self.clientes)
        self.exclientes = ExClientesFaker(n_exclientes=2000)
        self.envios = EnviosFaker(self.clientes)
        self.cuentas_bloqueadas = CuentasBloqueadasFaker(self.clientes)

    def write(self):
        """
        Guarda los datos generados en archivos CSV.
        """
        self.clientes.get_clientes().to_csv("./data/out/clientes.csv", index=False)
        self.contratos.get_contratos().to_csv("./data/out/contratos.csv", index=False)
        self.contactos.get_contactos().to_csv("./data/out/contactos.csv", index=False)
        self.direcciones.get_direcciones().to_csv("./data/out/direcciones.csv", index=False)
        self.exclientes.get_exclientes().to_csv("./data/out/exclientes.csv", index=False)
        self.envios.get_envios().to_csv("./data/out/envios.csv", index=False)
        self.cuentas_bloqueadas.get_cuentas_bloqueadas().to_csv("./data/out/cuentas_bloqueadas.csv", index=False)

if __name__ == "__main__":
    main = Main()
    main.read()
    main.write()