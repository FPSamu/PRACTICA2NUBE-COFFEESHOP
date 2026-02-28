# ☕ CoffeeOrder AWS Integrator

Este proyecto implementa una **arquitectura desacoplada** para la gestión de pedidos en una cafetería utilizando los servicios de **Amazon Web Services (AWS)**. El objetivo es evitar la pérdida de órdenes durante picos de tráfico mediante el uso de colas de mensajería y procesamiento asíncrono.

## 🚀 Arquitectura del Sistema

La solución se basa en el patrón **Productor-Consumidor**:

1.  **Productor (AWS CLI):** Simula la entrada de pedidos enviando mensajes a una cola.
2.  **Mensajería (Amazon SQS):** Actúa como buffer para almacenar los pedidos de forma segura.
3.  **Consumidor (EC2 + Python):** Una instancia de computación que realiza *polling* a la cola, parsea los datos y los procesa.
4.  **Almacenamiento (Amazon RDS):** Base de datos PostgreSQL que persiste las órdenes para su posterior gestión.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Librerías:** `boto3` (AWS SDK), `psycopg2` (PostgreSQL adapter)
* **Infraestructura:** * Amazon EC2 (Amazon Linux 2023)
    * Amazon SQS (Standard Queue)
    * Amazon RDS (PostgreSQL Engine)

## 📋 Requisitos Previos

Antes de ejecutar el consumidor, asegúrate de tener:
1. Una cola SQS creada y su URL a la mano.
2. Una instancia de RDS configurada con la tabla `coffee_orders`.
3. El rol de IAM `LabRole` (en AWS Academy) asignado a la instancia EC2.

### Esquema de la Base de Datos
```sql
CREATE TABLE coffee_orders (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    coffee_type VARCHAR(50) NOT NULL,
    order_status VARCHAR(20) NOT NULL DEFAULT 'created'
);
```

## ⚙️ Configuración e Instalación

### 1. Clonar el repositorio:
```bash
git clone https://github.com/FPSamu/PRACTICA2NUBE-COFFEESHOP.git
```

### 2. Instalar dependencias en la EC2:
```bash
pip install boto3 psycopg2-binary
```

### 3. Configurar credenciales:
El script está diseñado para usar el perfil de instancia (IAM Role), por lo que no es necesario configurar aws configure manualmente dentro de la EC2 si el rol está asignado.

## 🖥️ Uso

### 1. Iniciar el Consumidor
Ejecuta el script en tu instancia EC2 para comenzar a escuchar la cola:
```bash
python3 consumer.py
```

### 2. Simular Pedidos (Productor)
Desde cualquier terminal con AWS CLI configurado, envía un mensaje con el formato `Tipo de cafe|timestamp`:
```bash
aws sqs send-message --queue-url TU_URL_AQUI --message-body "Latte|2026-02-27 10:00:00"
```

## 🔍 Formato de Datos
El sistema espera mensajes con la siguiente estructura:
`Nombre del Café | YYYY-MM-DD HH:MM:SS`

Desarrollado por __Samuel Pia Figueroa__ - 2026
