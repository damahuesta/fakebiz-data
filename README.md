# Generador de Datos Falsos para Clientes

Este proyecto genera datos sintéticos realistas para clientes, contratos, contactos, direcciones, exclientes y envíos, simulando un entorno empresarial. Todos los módulos muestran mensajes por consola para seguir la ejecución y el progreso de la generación de datos.

## Módulos

### 1. `fake_clientes.py`
Genera un DataFrame de clientes con los siguientes campos:

- **cliente_id**: Identificador único de 9 dígitos, no repetido.
- **tipo_docum**: Tipo de documento de identificación. Valores posibles: `DNI`, `NIE`, `PASAPORTE`, `OTRO`. Distribución configurable.
- **cod_docum**: Código del documento, generado según el tipo.
- **nombre**: Nombre propio, realista según el país.
- **apellido1**: Primer apellido.
- **apellido2**: Segundo apellido (25% de los casos vacío).
- **pais_nacionalidad**: País de nacionalidad. `España` para DNI/NIE, aleatorio para otros.
- **fecha_nacimiento**: Fecha de nacimiento, entre hoy y hace 120 años.
- **fecha_cliente**: Fecha de alta como cliente, posterior a la fecha de nacimiento y anterior a hoy.
- **genero**: `M` o `F`, distribución realista.
- **estado_civil**: Estado civil, ponderado según estadísticas reales.
- **nivel_estudios**: Código de nivel de estudios (`01` a `06`), ponderado.
- **codigo_idioma**: Código de idioma (`E`, `C`, `G`, `H`, `A`, `F`), ponderado.

#### Requisitos funcionales:
- Los identificadores son únicos y no se repiten.
- Los campos de fechas son coherentes (fecha de cliente ≥ fecha de nacimiento).
- Los apellidos pueden estar vacíos según la probabilidad definida.
- Se muestran mensajes por consola durante la generación y obtención de datos.

---

### 2. `fake_contratos.py`
Genera contratos asociados a clientes.

- **cliente_id**: Referencia a un cliente existente.
- **empresa**: Código de empresa (ej: `EMP01`).
- **centro**: Código de centro asociado a la empresa.
- **codigo_producto**: Código de producto.
- **codigo_subproducto**: Subproducto (solo para ciertos productos).
- **identificador**: Identificador único de contrato.
- **rel_contra**: Rol del cliente en el contrato (ej: Titular, Cotitular, etc.), ponderado.
- **fecha_alta_contrato**: Fecha de alta del contrato (últimos 10 años).
- **fecha_baja_contrato**: Fecha de baja (`9999-12-31` si activo).
- **situacion_actividad**: Estado del contrato (`Activa`, `Cancelada`, etc.), ponderado.

#### Requisitos funcionales:
- Cada cliente tiene un número aleatorio de contratos entre 3 y 15, con probabilidad decreciente a medida que aumenta el número.
- Fechas de baja coherentes con fechas de alta y situación.
- Se muestran mensajes por consola durante la generación y obtención de datos.

---

### 3. `fake_contactos.py`
Genera contactos (email, teléfono, etc.) para cada cliente.

- **cliente_id**: Referencia a cliente.
- **tipo_contacto**: Tipo (`email`, `telefono`, `fax`, `web`), ponderado.
- **valor_contacto**: Valor realista según el tipo.
- **fecha_alta_contacto**: Entre la fecha de alta del cliente y hoy.
- **fecha_baja_contacto**: `9999-12-31` si activo, o fecha real de baja.

#### Requisitos funcionales:
- Cada cliente tiene entre 1 y 4 contactos, número aleatorio.
- Fechas de alta y baja coherentes.
- Se muestran mensajes por consola durante la generación y obtención de datos.

---

### 4. `fake_direcciones.py`
Genera una o varias direcciones por cliente.

- **cliente_id**: Referencia a cliente.
- **numero_domicilio**: Número secuencial de domicilio para el cliente.
- **direccion**: Calle y número.
- **ciudad**: Ciudad (realista para España, aleatoria para otros países).
- **provincia**: Provincia (para España) o estado/región.
- **codigo_postal**: Código postal.
- **pais**: País (`España`, `Francia`, `Alemania`, `Estados Unidos`).

#### Requisitos funcionales:
- 75% de domicilios en España, 25% en otros países.
- Cada cliente tiene entre 1 y 5 domicilios, número aleatorio ponderado.
- Se muestran mensajes por consola durante la generación y obtención de datos.

---

### 5. `fake_exclientes.py`
Genera exclientes (clientes dados de baja).

- **cliente_id**: Identificador único.
- **tipo_docum**, **cod_docum**, **nombre**, **apellido1**, **apellido2**, **pais_nacionalidad**, **fecha_nacimiento**, **fecha_cliente**, **genero**, **estado_civil**, **nivel_estudios**, **codigo_idioma**: Igual que en clientes.
- **motivo_baja**: Motivo de baja (`Voluntaria`, `Incumplimiento`, `Fallecimiento`).
- **fecha_inclusion_excliente**: Fecha de inclusión como excliente.
- **fecha_recuperacion_excliente**: Fecha en la que el excliente vuelve a ser cliente (20% de los casos), o vacío si no ha sido recuperado.

#### Requisitos funcionales:
- El número de exclientes se pasa como parámetro.
- Fechas de inclusión y recuperación coherentes.
- Motivo de baja aleatorio entre los posibles.
- Se muestran mensajes por consola durante la generación y obtención de datos.

---

### 6. `fake_envios.py`
Genera registros de envíos realizados entre clientes.

- **cliente_origen_id**: Referencia al cliente que realiza el envío.
- **cliente_destino_id**: Referencia al cliente que recibe el envío (distinto del origen).
- **valor_envio**: Valor monetario del envío.
- **fecha_hora_envio**: Fecha y hora del envío (últimos 5 años).
- **motivo_envio**: Motivo del envío (`Pago`, `Regalo`, `Transferencia`, `Devolución`, `Otro`).

#### Requisitos funcionales:
- Cada cliente realiza entre 2 y 20 envíos, número aleatorio.
- Ambos clientes deben existir y ser distintos.
- El valor del envío es positivo y realista.
- La fecha y hora es coherente (últimos 5 años).
- El motivo se elige aleatoriamente entre las opciones posibles.
- Se muestran mensajes por consola durante la generación y obtención de datos.

---

## Ejecución

El archivo principal es `main_fake_data.py`. Al ejecutarlo, se generan los ficheros CSV en la carpeta `./data/out/`.

```bash
python main_fake_data.py
```

## Dependencias

- pandas
- numpy
- faker

Instalar con:

```bash
pip install pandas numpy faker
```

---

## Notas

- El generador utiliza ponderaciones y reglas realistas para simular datos verosímiles.
- Los datos generados son sintéticos y no corresponden a personas reales.
