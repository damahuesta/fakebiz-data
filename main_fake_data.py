from fake_clientes import ClientesFaker
from fake_contratos import ContratosFaker
from fake_contactos import ContactosFaker
from fake_direcciones import DireccionesFaker
from fake_exclientes import ExClientesFaker  # Nueva importación
from fake_envios import EnviosFaker  # Importar el módulo de envíos

class Main:
    def read(self):
        self.clientes = ClientesFaker(n_clientes=10000)
        self.contratos = ContratosFaker(self.clientes)  # Quitar n_contratos
        self.contactos = ContactosFaker(self.clientes)
        self.direcciones = DireccionesFaker(self.clientes)
        self.exclientes = ExClientesFaker(n_exclientes=2000)  # Nueva línea
        self.envios = EnviosFaker(self.clientes)  # Generar envíos

    def write(self):
        self.clientes.get_clientes().to_csv("./data/out/clientes.csv", index=False)
        self.contratos.get_contratos().to_csv("./data/out/contratos.csv", index=False)
        self.contactos.get_contactos().to_csv("./data/out/contactos.csv", index=False)
        self.direcciones.get_direcciones().to_csv("./data/out/direcciones.csv", index=False)
        self.exclientes.get_exclientes().to_csv("./data/out/exclientes.csv", index=False)  # Nueva línea
        self.envios.get_envios().to_csv("./data/out/envios.csv", index=False)  # Guardar envíos

        
    
if __name__ == "__main__":
    main = Main()
    main.read()
    main.write()