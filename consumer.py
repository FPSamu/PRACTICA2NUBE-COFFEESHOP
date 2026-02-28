import boto3
import psycopg2
import time

# Configuración - Reemplaza con tus datos
QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/123456789/example'
DB_HOST = 'example.jag83bv09a.us-east-1.rds.amazonaws.com'
DB_NAME = 'EXAMPLE'
DB_USER = 'EXAMPLE'
DB_PASS = 'EXAMPLE'

# Conexión a SQS
sqs = boto3.client('sqs', region_name='us-east-1')

def process_message(body):
    try:
        # Parsing: "Latte|2026-02-16 13:39:45"
        coffee_type, timestamp = body.split('|')
        
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = conn.cursor()
        
        query = """INSERT INTO coffee_orders (timestamp, coffee_type, order_status) 
                   VALUES (%s, %s, 'created')"""
        cur.execute(query, (timestamp, coffee_type))
        
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error procesando: {e}")
        return False

print("Esperando pedidos en la cafetería...")

while True:
    # Polling infinito
    response = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=20  # Long Polling
    )

    if 'Messages' in response:
        for msg in response['Messages']:
            receipt_handle = msg['ReceiptHandle']
            body = msg['Body']
            
            print(f"Nuevo pedido recibido: {body}")
            
            if process_message(body):
                # Borrar de la cola si se guardó en DB
                sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=receipt_handle)
                print("Pedido guardado y borrado de la cola.")
    
    time.sleep(1)
