import pandas as pd
import random
from faker import Faker

class DireccionesFaker:
    def __init__(self, clientes):
        print("Generando direcciones...")
        self.clientes = clientes
        self.fake_locales = {
            "España": Faker('es_ES'),
            "France": Faker('fr_FR'),
            "Germany": Faker('de_DE'),
            "United States": Faker('en_US'),
            # ...puedes añadir más países/locales si es necesario...
        }
        self.default_fake = Faker(['es_ES', 'en_US', 'fr_FR', 'de_DE'])
        # Cargamos el mapeo de ciudades/provincias desde un CSV externo
        self.ciudades_provincias_es = self._cargar_ciudades_provincias_es()
        self.direcciones = self._generar_direcciones()
        print(f"Direcciones generadas: {len(self.direcciones)}")

    def _cargar_ciudades_provincias_es(self):
        df = pd.read_csv('./data/in/ciudades_provincias_es.csv')
        # Espera columnas: ciudad,provincia
        return list(df.itertuples(index=False, name=None))

    def _generar_direcciones(self):
        direcciones_list = []
        # Pesos: mayoría 1 o 2 domicilios
        pesos_domicilios = [0.6, 0.3, 0.07, 0.02, 0.01]
        for idx, row in self.clientes.get_clientes().iterrows():
            cliente_id = row["cliente_id"]
            n_domicilios = random.choices([1,2,3,4,5], weights=pesos_domicilios, k=1)[0]
            for num_dom in range(1, n_domicilios + 1):
                # 75% domicilios españoles, 25% otros países
                if random.random() < 0.75:
                    fake = self.fake_locales["España"]
                    direccion = fake.street_address()
                    ciudad, provincia = random.choice(self.ciudades_provincias_es)
                    codigo_postal = fake.postcode()
                    pais = "España"
                else:
                    pais_opciones = ["France", "Germany", "United States"]
                    pais_elegido = random.choice(pais_opciones)
                    fake = self.fake_locales.get(pais_elegido, self.default_fake)
                    direccion = fake.street_address()
                    # Para otros países, usamos city y state coherentes
                    ciudad = fake.city()
                    provincia = fake.state() if hasattr(fake, "state") else ""
                    codigo_postal = fake.postcode()
                    pais = {
                        "France": "Francia",
                        "Germany": "Alemania",
                        "United States": "Estados Unidos"
                    }.get(pais_elegido, pais_elegido)
                direcciones_list.append({
                    "cliente_id": cliente_id,
                    "numero_domicilio": num_dom,
                    "direccion": direccion,
                    "ciudad": ciudad,
                    "provincia": provincia,
                    "codigo_postal": codigo_postal,
                    "pais": pais
                })
        df = pd.DataFrame(direcciones_list)
        df = df.sample(frac=1).reset_index(drop=True)  # Desordenar
        return df

    def get_direcciones(self):
        print("Obteniendo DataFrame de direcciones")
        return self.direcciones
