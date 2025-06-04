import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime

class EnviosFaker:
    def __init__(self, clientes, seed=None):
        """
        clientes: instancia de ClientesFaker o DataFrame con columna 'cliente_id'
        """
        print("Generando envíos...")
        self.seed = seed
        self.fake = Faker('es_ES')
        if seed is not None:
            np.random.seed(seed)
            Faker.seed(seed)
        # Permitir tanto instancia como DataFrame
        if hasattr(clientes, "get_clientes"):
            self.clientes_df = clientes.get_clientes()
        else:
            self.clientes_df = clientes
        self.envios = self._generar_envios()
        print(f"Envíos generados: {len(self.envios)}")

    def _generar_envios(self):
        MOTIVOS_ENVIO = ['Pago', 'Regalo', 'Transferencia', 'Devolución', 'Otro']
        cliente_ids = self.clientes_df['cliente_id'].tolist()
        n_clientes = len(cliente_ids)
        if n_clientes < 2:
            raise ValueError("Se requieren al menos dos clientes para generar envíos.")
        envios = []
        for origen in cliente_ids:
            n_envios = np.random.randint(2, 21)  # Entre 2 y 20 envíos por cliente
            posibles_destinos = [cid for cid in cliente_ids if cid != origen]
            for _ in range(n_envios):
                destino = np.random.choice(posibles_destinos)
                valor_envio = round(np.random.uniform(10, 5000), 2)
                fecha_hora_envio = self.fake.date_time_between(
                    start_date='-5y', end_date='now'
                ).strftime('%Y-%m-%d %H:%M:%S')
                motivo_envio = np.random.choice(MOTIVOS_ENVIO)
                envios.append({
                    'cliente_origen_id': origen,
                    'cliente_destino_id': destino,
                    'valor_envio': valor_envio,
                    'fecha_hora_envio': fecha_hora_envio,
                    'motivo_envio': motivo_envio
                })
        df = pd.DataFrame(envios)
        df = df.sample(frac=1).reset_index(drop=True)  # Desordenar
        return df

    def get_envios(self):
        print("Obteniendo DataFrame de envíos")
        return self.envios
