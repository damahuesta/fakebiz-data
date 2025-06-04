import pandas as pd
import random
from faker import Faker
from datetime import datetime

class ContactosFaker:
    def __init__(self, clientes, n_contactos_por_cliente=None):
        print("Generando contactos...")
        self.clientes = clientes
        self.n_contactos_por_cliente = n_contactos_por_cliente  # Puede ser None
        self.fake_locales = {
            "España": Faker('es_ES'),
            "France": Faker('fr_FR'),
            "Germany": Faker('de_DE'),
            "United States": Faker('en_US'),
            # ...puedes añadir más países/locales si es necesario...
        }
        self.default_fake = Faker(['es_ES', 'en_US', 'fr_FR', 'de_DE'])
        self.contactos = self._generar_contactos()
        print(f"Contactos generados: {len(self.contactos)}")

    def get_faker_for_pais(self, pais):
        # Normaliza nombres de país
        if pais.lower() in ["españa", "spain"]:
            return self.fake_locales["España"]
        elif pais.lower() in ["francia", "france"]:
            return self.fake_locales["France"]
        elif pais.lower() in ["alemania", "germany"]:
            return self.fake_locales["Germany"]
        elif pais.lower() in ["estados unidos", "united states", "usa"]:
            return self.fake_locales["United States"]
        else:
            return self.default_fake

    def _generar_contactos(self):
        contactos_list = []
        tipos = ["email", "telefono", "fax", "web"]
        pesos = [0.45, 0.4, 0.08, 0.07]  # Más peso para email y teléfono
        hoy = datetime.today()
        for idx, row in self.clientes.get_clientes().iterrows():
            cliente_id = row["cliente_id"]
            fecha_alta_cliente = pd.to_datetime(row["fecha_cliente"])
            pais = row.get("pais", "España")  # Ajusta si el campo tiene otro nombre
            fake = self.get_faker_for_pais(pais)
            if self.n_contactos_por_cliente is None:
                n_contactos = random.randint(1, 4)
            else:
                n_contactos = self.n_contactos_por_cliente
            for _ in range(n_contactos):
                tipo = random.choices(tipos, weights=pesos, k=1)[0]
                if tipo == "email":
                    valor = fake.email()
                elif tipo == "telefono":
                    valor = fake.phone_number()
                elif tipo == "fax":
                    valor = fake.phone_number()
                elif tipo == "web":
                    valor = fake.url()
                # Fecha alta contacto entre fecha alta cliente y hoy
                fecha_alta_contacto = fake.date_between_dates(
                    date_start=fecha_alta_cliente, date_end=hoy
                )
                # 80% de contactos activos (baja 9999-12-31), 20% baja real
                if random.random() < 0.8:
                    fecha_baja_contacto = "9999-12-31"
                else:
                    fecha_baja_contacto = fake.date_between_dates(
                        date_start=fecha_alta_contacto, date_end=hoy
                    ).strftime("%Y-%m-%d")
                contactos_list.append({
                    "cliente_id": cliente_id,
                    "tipo_contacto": tipo,
                    "valor_contacto": valor,
                    "fecha_alta_contacto": fecha_alta_contacto.strftime("%Y-%m-%d"),
                    "fecha_baja_contacto": fecha_baja_contacto
                })
        df = pd.DataFrame(contactos_list)
        df = df.sample(frac=1).reset_index(drop=True)  # Desordenar
        return df

    def get_contactos(self):
        print("Obteniendo DataFrame de contactos")
        return self.contactos
