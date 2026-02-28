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
