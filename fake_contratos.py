import pandas as pd
import numpy as np
import random
import string
from faker import Faker
from datetime import datetime, timedelta

class ContratosFaker:
    def __init__(self, clientes):
        print("Generando contratos...")
        self.fake = Faker(['es_ES', 'en_US', 'fr_FR', 'de_DE'])
        self.clientes = clientes
        self.hoy = datetime.today()
        self.contratos = self._generar_contratos()
        print(f"Contratos generados: {len(self.contratos)}")

    def _generar_contratos(self):
        empresas = [f"EMP{str(i+1).zfill(2)}" for i in range(5)]
        centros_por_empresa = {e: [f"CEN{str(j+1).zfill(2)}" for j in range(7)] for e in empresas}
        productos = [f"PRD{str(i+1).zfill(2)}" for i in range(25)]

        productos_con_sub = np.random.choice(productos, 10, replace=False)
        subproductos = [f"SB{str(i+1).zfill(2)}" for i in range(5)]

        tipos_interventor = [
            "Titular",
            "Cotitular",
            "Autorizado",
            "Representante",
            "Apoderado",
            "Tutor",
            "Interventor judicial",
            "Administrador",
            "Heredero"
        ]
        pesos_interventor = [0.6, 0.15, 0.1, 0.05, 0.03, 0.02, 0.02, 0.02, 0.01]

        situaciones = ["Activa", "Cancelada", "Vencida", "Rescindida"]
        pesos = [0.7, 0.15, 0.1, 0.05]

        contratos_list = []
        cliente_ids = self.clientes.clientes["cliente_id"]
        # El número de contratos por cliente es aleatorio y decreciente
        posibles = list(range(3, 16))
        pesos_contratos = [0.25, 0.20, 0.15, 0.10, 0.08, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01, 0.01, 0.01]
        pesos_contratos = [p / sum(pesos_contratos) for p in pesos_contratos]
        for cliente_id in cliente_ids:
            # Selección aleatoria ponderada del número de contratos por cliente
            n = random.choices(posibles, weights=pesos_contratos, k=1)[0]
            for _ in range(n):
                empresa = random.choice(empresas)
                centro = random.choice(centros_por_empresa[empresa])
                codigo_producto = random.choice(productos)
                if codigo_producto in productos_con_sub:
                    codigo_subproducto = random.choice(subproductos)
                else:
                    codigo_subproducto = "SB00"
                identificador = str(random.randint(0, 10**7-1)).zfill(7)
                rel_contra = random.choices(tipos_interventor, weights=pesos_interventor, k=1)[0]
                fecha_alta_contrato = self.fake.date_between(start_date='-10y', end_date='today')
                situacion_actividad = random.choices(situaciones, weights=pesos, k=1)[0]
                if situacion_actividad == "Activa":
                    fecha_baja_contrato = "9999-12-31"
                else:
                    fecha_baja_contrato = str(self.fake.date_between(start_date=fecha_alta_contrato, end_date=self.hoy))
                contratos_list.append({
                    "cliente_id": cliente_id,
                    "empresa": empresa,
                    "centro": centro,
                    "codigo_producto": codigo_producto,
                    "codigo_subproducto": codigo_subproducto,
                    "identificador": identificador,
                    "rel_contra": rel_contra,
                    "fecha_alta_contrato": fecha_alta_contrato,
                    "fecha_baja_contrato": fecha_baja_contrato,
                    "situacion_actividad": situacion_actividad
                })
        contratos = pd.DataFrame(contratos_list)
        column_order = [
            "cliente_id", "empresa", "centro", "codigo_producto", "codigo_subproducto",
            "identificador", "rel_contra", "fecha_alta_contrato",
            "fecha_baja_contrato", "situacion_actividad"
        ]
        contratos = contratos[column_order]
        contratos = contratos.sample(frac=1).reset_index(drop=True)  # Desordenar
        return contratos

    def get_contratos(self):
        print("Obteniendo DataFrame de contratos")
        return self.contratos