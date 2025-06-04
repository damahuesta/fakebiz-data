import pandas as pd
import numpy as np
import random
import string
from faker import Faker
from datetime import datetime, timedelta

class ClientesFaker:
    def __init__(self, n_clientes=100, exclude_ids=None):
        print("Generando clientes...")
        self.n_clientes = n_clientes
        self.exclude_ids = set(exclude_ids) if exclude_ids else set()
        self.fake = Faker(['es_ES', 'en_US', 'fr_FR', 'de_DE'])
        self.fake_global = Faker()
        self.hoy = datetime.today()
        self.clientes = self._generar_clientes(n_clientes)
        print(f"Clientes generados: {len(self.clientes)}")
        
    def letra_dni(self, numero):
        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        return letras[int(numero) % 23]

    def gen_cod_docum(self, tipo):
        if tipo == "DNI":
            return self.fake.nif()
        elif tipo == "NIE":
            return self.fake.nie()
        elif tipo == "PASAPORTE":
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
        else:  # OTRO
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    def random_fecha_nacimiento(self):
        max_years = 120
        start_date = self.hoy - timedelta(days=365.25 * max_years)
        nacimiento = self.fake.date_between(start_date=start_date, end_date=self.hoy)
        return nacimiento

    def random_fecha_cliente(self, fecha_nac):
        cliente = self.fake.date_between(start_date=fecha_nac, end_date=self.hoy)
        return cliente

    def _generar_clientes(self, n_clientes):
        # Definir valores y pesos para tipo_docum
        tipos = ["DNI", "NIE", "PASAPORTE", "OTRO"]
        pesos = [0.6, 0.15, 0.2, 0.05]
        
        # Generar n_clientes números únicos de 9 dígitos que no estén en exclude_ids
        ids_generados = set()
        while len(ids_generados) < n_clientes:
            num = random.randint(0, 999999999)
            id_str = str(num).zfill(9)
            if id_str not in self.exclude_ids:
                ids_generados.add(id_str)

        cliente_ids = list(ids_generados)

        tipo_docum = random.choices(tipos, weights=pesos, k=n_clientes)
        cod_docum = [self.gen_cod_docum(t) for t in tipo_docum]

        # Generar nombres y apellidos separados, y a veces dejar apellido2 vacío
        nombres, apellidos1, apellidos2 = [], [], []
        for _ in range(n_clientes):
            nombre = self.fake.first_name()
            apellido1 = self.fake.last_name()
            # 25% de los casos sin apellido2
            if random.random() < 0.25:
                apellido2 = ''
            else:
                apellido2 = self.fake.last_name()
            nombres.append(nombre)
            apellidos1.append(apellido1)
            apellidos2.append(apellido2)

        pais_nacionalidad = [
            "España" if t in ["DNI", "NIE"] else self.fake_global.country()
            for t in tipo_docum
        ]

        fechas_nac, fechas_cliente = [], []
        for _ in range(n_clientes):
            f_nac = self.random_fecha_nacimiento()
            f_cli = self.random_fecha_cliente(f_nac)
            fechas_nac.append(f_nac.strftime("%Y-%m-%d"))
            fechas_cliente.append(f_cli.strftime("%Y-%m-%d"))
            
        generos = random.choices(["M", "F"], weights=[0.49, 0.51], k=n_clientes)  # M: masculino, F: femenino

        # Estado civil: ponderado (aprox España INE)
        estados = ["Soltero/a", "Casado/a", "Divorciado/a", "Viudo/a", "Separado/a", "Pareja de hecho"]
        pesos_estados = [0.4, 0.45, 0.06, 0.05, 0.02, 0.02]
        estado_civil = random.choices(estados, weights=pesos_estados, k=n_clientes)

        # 7. NIVEL DE ESTUDIOS (códigos: 01-06)
        niveles = ["01", "02", "03", "04", "05", "06"]
        pesos_niveles = [0.15, 0.2, 0.3, 0.2, 0.1, 0.05]
        nivel_estudios = random.choices(niveles, weights=pesos_niveles, k=n_clientes)

        # 8. CÓDIGO DE IDIOMA
        idiomas = ["E", "C", "G", "H", "A", "F"]  # Español, Catalán, Gallego, Euskera, Alemán, Francés
        pesos_idiomas = [0.85, 0.05, 0.03, 0.03, 0.02, 0.02]
        codigo_idioma = random.choices(idiomas, weights=pesos_idiomas, k=n_clientes)

        clientes = pd.DataFrame({
            "cliente_id": cliente_ids,
            "tipo_docum": tipo_docum,
            "cod_docum": cod_docum,
            "nombre": nombres,
            "apellido1": apellidos1,
            "apellido2": apellidos2,
            "pais_nacionalidad": pais_nacionalidad,
            "fecha_nacimiento": fechas_nac,
            "fecha_cliente": fechas_cliente,
            "genero": generos,
            "estado_civil": estado_civil,
            "nivel_estudios": nivel_estudios,
            "codigo_idioma": codigo_idioma
        })
        clientes = clientes.sample(frac=1).reset_index(drop=True)  # Desordenar
        return clientes
    
    def get_clientes(self):
        print("Obteniendo DataFrame de clientes")
        return self.clientes
