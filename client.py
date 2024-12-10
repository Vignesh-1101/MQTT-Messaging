# client.py
import pika
import json
import random
import time
from datetime import datetime
from config import RABBITMQ_CONFIG

def setup_rabbitmq_connection():
    """
    This function sets up a connection to a RabbitMQ server.
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_CONFIG['host'])
    )
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_CONFIG['queue_name'])
    return connection, channel

def emit_status():
    """
    This function is named emit_status and its purpose is not specified in the code snippet provided.
    """
    connection, channel = setup_rabbitmq_connection()
    
    try:
        while True:
            status = random.randint(0, 6)
            message = {
                'status': status,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            channel.basic_publish(
                exchange='',
                routing_key=RABBITMQ_CONFIG['queue_name'],
                body=json.dumps(message)
            )
            print(f"Emitted status: {status}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping client...")
    finally:
        connection.close()
        
if __name__ == "__main__":
    emit_status()

