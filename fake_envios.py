import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime
from typing import Optional, Union
import logging

from fake_clientes import ClientesFaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnviosFaker:
    """
    Generador de envíos falsos entre clientes.
    """
    def __init__(self, clientes: Union['ClientesFaker', pd.DataFrame], seed: Optional[int] = None):
        """
        clientes: instancia de ClientesFaker o DataFrame con columna 'cliente_id'.
        seed: semilla para reproducibilidad (opcional).
        """
        logger.info("Generando envíos...")
        self.seed = seed
        if seed is not None:
            np.random.seed(seed)
            Faker.seed(seed)
        self.fake = Faker('es_ES')
        # Permitir tanto instancia como DataFrame
        if hasattr(clientes, "get_clientes"):
            self.clientes_df = clientes.get_clientes()
        else:
            self.clientes_df = clientes
        self.envios = self._generar_envios()
        logger.info(f"Envíos generados: {len(self.envios)}")

    def _generar_envios(self) -> pd.DataFrame:
        """
        Genera el DataFrame de envíos.
        """
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

    def get_envios(self) -> pd.DataFrame:
        """
        Devuelve el DataFrame de envíos.
        """
        logger.info("Obteniendo DataFrame de envíos")
        return self.envios
