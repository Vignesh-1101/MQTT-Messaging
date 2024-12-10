# config.py
RABBITMQ_CONFIG = {
    'host': 'localhost',
    'port': 5672,
    'queue_name': 'status_queue'
}

MONGODB_CONFIG = {
    'host': 'localhost',
    'port': 27017,
    'db_name': 'monitoring_db',
    'collection_name': 'status_records'
}