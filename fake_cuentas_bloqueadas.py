import pandas as pd
import numpy as np
from faker import Faker
from typing import Optional, Union
import logging

from fake_clientes import ClientesFaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CuentasBloqueadasFaker:
    """
    Generador de cuentas bloqueadas por fraude.
    """
    TIPOS_FRAUDE = [
        'Phishing',
        'Robo de identidad',
        'Transacciones sospechosas',
        'Fraude con tarjeta',
        'Lavado de dinero',
        'Acceso no autorizado'
    ]

    def __init__(self, clientes: Union[pd.DataFrame, 'ClientesFaker'], seed: Optional[int] = None):
        """
        clientes: DataFrame con columna 'cliente_id' o instancia de ClientesFaker.
        seed: semilla para reproducibilidad (opcional).
        """
        logger.info("Generando cuentas bloqueadas por fraude...")
        self.seed = seed
        if seed is not None:
            np.random.seed(seed)
            Faker.seed(seed)
        self.fake = Faker('es_ES')
        if hasattr(clientes, "get_clientes"):
            self.clientes_df = clientes.get_clientes()
        else:
            self.clientes_df = clientes
        self.cuentas_bloqueadas = self._generar_cuentas_bloqueadas()
        logger.info(f"Cuentas bloqueadas generadas: {len(self.cuentas_bloqueadas)}")

    def _generar_cuentas_bloqueadas(self) -> pd.DataFrame:
        """
        Genera el DataFrame de cuentas bloqueadas.
        """
        cliente_ids = self.clientes_df['cliente_id'].tolist()
        n_clientes = len(cliente_ids)
        n_bloqueadas = max(1, int(np.floor(n_clientes * 0.01)))
        bloqueados = np.random.choice(cliente_ids, n_bloqueadas, replace=False)
        cuentas = []
        for cid in bloqueados:
            tipo_fraude = np.random.choice(self.TIPOS_FRAUDE)
            estado_fraude = np.random.choice(['Investigación', 'Bloqueado'])
            fecha_inclusion = self.fake.date_time_between(start_date='-3y', end_date='now')
            if estado_fraude == 'Bloqueado':
                fecha_bloqueo = self.fake.date_time_between(
                    start_date=fecha_inclusion, end_date='now'
                ).strftime('%Y-%m-%d %H:%M:%S')
            else:
                fecha_bloqueo = None
            motivo = self.fake.sentence(nb_words=8)
            cuentas.append({
                'cliente_id': cid,
                'tipo_fraude': tipo_fraude,
                'estado_fraude': estado_fraude,
                'fecha_inclusion': fecha_inclusion.strftime('%Y-%m-%d %H:%M:%S'),
                'fecha_bloqueo': fecha_bloqueo,
                'motivo': motivo
            })
        return pd.DataFrame(cuentas)

    def get_cuentas_bloqueadas(self) -> pd.DataFrame:
        """
        Devuelve el DataFrame de cuentas bloqueadas.
        """
        logger.info("Obteniendo DataFrame de cuentas bloqueadas")
        return self.cuentas_bloqueadas
