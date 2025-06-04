import pandas as pd
import random
import string
from faker import Faker
from datetime import datetime, timedelta

class ExClientesFaker:
    def __init__(self, n_exclientes=None, exclude_ids=None):
        print("Generando exclientes...")
        self.n_exclientes = n_exclientes
        self.exclude_ids = set(exclude_ids) if exclude_ids else set()
        self.fake = Faker(['es_ES', 'en_US', 'fr_FR', 'de_DE'])
        self.fake_global = Faker()
        self.hoy = datetime.today()
        self._exclientes = self.__generar_exclientes()
        print(f"Exclientes generados: {len(self._exclientes)}")

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

    def __generar_exclientes(self):
        tipos = ["DNI", "NIE", "PASAPORTE", "OTRO"]
        pesos = [0.6, 0.15, 0.2, 0.05]
        motivos = ("Voluntaria", "Incumplimiento", "Fallecimiento")

        # Generar n_exclientes números únicos de 9 dígitos que no estén en exclude_ids
        ids_generados = set()
        while len(ids_generados) < self.n_exclientes:
            num = random.randint(0, 999999999)
            id_str = str(num).zfill(9)
            if id_str not in self.exclude_ids:
                ids_generados.add(id_str)
        cliente_ids = list(ids_generados)

        tipo_docum = random.choices(tipos, weights=pesos, k=self.n_exclientes)
        cod_docum = [self.gen_cod_docum(t) for t in tipo_docum]

        nombres, apellidos1, apellidos2 = [], [], []
        for _ in range(self.n_exclientes):
            nombre = self.fake.first_name()
            apellido1 = self.fake.last_name()
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
        for _ in range(self.n_exclientes):
            f_nac = self.random_fecha_nacimiento()
            f_cli = self.random_fecha_cliente(f_nac)
            fechas_nac.append(f_nac.strftime("%Y-%m-%d"))
            fechas_cliente.append(f_cli.strftime("%Y-%m-%d"))

        generos = random.choices(["M", "F"], weights=[0.49, 0.51], k=self.n_exclientes)
        estados = ["Soltero/a", "Casado/a", "Divorciado/a", "Viudo/a", "Separado/a", "Pareja de hecho"]
        pesos_estados = [0.4, 0.45, 0.06, 0.05, 0.02, 0.02]
        estado_civil = random.choices(estados, weights=pesos_estados, k=self.n_exclientes)

        niveles = ["01", "02", "03", "04", "05", "06"]
        pesos_niveles = [0.15, 0.2, 0.3, 0.2, 0.1, 0.05]
        nivel_estudios = random.choices(niveles, weights=pesos_niveles, k=self.n_exclientes)

        idiomas = ["E", "C", "G", "H", "A", "F"]
        pesos_idiomas = [0.85, 0.05, 0.03, 0.03, 0.02, 0.02]
        codigo_idioma = random.choices(idiomas, weights=pesos_idiomas, k=self.n_exclientes)

        motivo_baja = [random.choice(motivos) for _ in range(self.n_exclientes)]
        fecha_inclusion_excliente = []
        fecha_recuperacion_excliente = []  # Fecha en la que el excliente vuelve a ser cliente
        for fc in fechas_cliente:
            # Convertir string a objeto datetime
            if isinstance(fc, str):
                fecha_cliente_dt = datetime.strptime(fc, "%Y-%m-%d")
            else:
                fecha_cliente_dt = fc
            fecha_incl = self.fake.date_between(start_date=fecha_cliente_dt, end_date=self.hoy)
            fecha_inclusion_excliente.append(fecha_incl.strftime("%Y-%m-%d"))
            # 20% tienen fecha de recuperación (vuelven a ser clientes)
            if random.random() < 0.2:
                fecha_recuperacion = self.fake.date_between(start_date=fecha_incl, end_date=self.hoy)
                fecha_recuperacion_excliente.append(fecha_recuperacion.strftime("%Y-%m-%d"))
            else:
                fecha_recuperacion_excliente.append(None)

        exclientes = pd.DataFrame({
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
            "codigo_idioma": codigo_idioma,
            "motivo_baja": motivo_baja,
            "fecha_inclusion_excliente": fecha_inclusion_excliente,
            # Fecha en la que el excliente vuelve a ser cliente (recuperación)
            "fecha_recuperacion_excliente": fecha_recuperacion_excliente
        })
        exclientes = exclientes.sample(frac=1).reset_index(drop=True)
        return exclientes

    def get_exclientes(self):
        print("Obteniendo DataFrame de exclientes")
        """
        Devuelve el DataFrame de exclientes.
        La columna 'fecha_recuperacion_excliente' indica la fecha en la que el excliente vuelve a ser cliente.
        Si es None, el excliente no ha sido recuperado.
        """
        return self._exclientes
