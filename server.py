# server.py
from fastapi import FastAPI, HTTPException, Response
from pymongo import MongoClient
import pika
import json
import threading
from config import RABBITMQ_CONFIG, MONGODB_CONFIG
from dateutil import parser

app = FastAPI()

# MongoDB setup
client = MongoClient(MONGODB_CONFIG['host'], MONGODB_CONFIG['port'])
db = client[MONGODB_CONFIG['db_name']]
collection = db[MONGODB_CONFIG['collection_name']]

def process_message(ch, method, properties, body):
    """
    This function processes a message received from RabbitMQ.
    """
    message = json.loads(body)
    
    # Store in MongoDB
    collection.insert_one({
        'status': message['status'],
        'timestamp': parser.parse(message['timestamp'])
    })
    
    print(f"Processed and stored status: {message['status']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_rabbitmq_consumer():
    """
    This function is likely intended to start a RabbitMQ consumer.
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_CONFIG['host'])
    )
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_CONFIG['queue_name'])
    
    channel.basic_consume(
        queue=RABBITMQ_CONFIG['queue_name'],
        on_message_callback=process_message
    )
    
    print("Started consuming messages...")
    channel.start_consuming()

#Get api to fetch messages
@app.get("/status-count")
async def get_status_count(start_time: str, end_time: str, respone: Response):
    try:
        start_dt = parser.parse(start_time)
        end_dt = parser.parse(end_time)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid datetime format. Use ISO format (e.g., 2024-01-01T00:00:00Z)"
        )
    
    pipeline = [
        {
            "$match": {
                "timestamp": {
                    "$gte": start_dt,
                    "$lte": end_dt
                }
            }
        },
        {
            "$group": {
                "_id": "$status",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"_id": 1}
        }
    ]
    
    results = list(collection.aggregate(pipeline))
    
    # Format results as a dictionary
    status_counts = {str(result["_id"]): result["count"] for result in results}
    print(status_counts)
    
    # Ensure all status values (0-6) are present in response
    for status in range(7):
        if str(status) not in status_counts:
            status_counts[str(status)] = 0
    respone.status_code = 200
    return {
        "success": True,
        "message": "Status counts retrieved successfully",
        "data": status_counts
    }

def start_server():
    # Start RabbitMQ consumer in a separate thread
    consumer_thread = threading.Thread(target=start_rabbitmq_consumer)
    consumer_thread.daemon = True
    consumer_thread.start()
    
    # Start FastAPI server
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start_server()