# MQTT Status Monitoring System

A Python-based monitoring system that uses RabbitMQ for MQTT messaging and MongoDB for data storage. The system consists of a client that emits status messages and a server that processes and stores these messages, providing an API endpoint for status analysis.

## Prerequisites

- Python 3.8 or higher
- RabbitMQ Server
- MongoDB Server
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mqtt-monitoring-system
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

The system configuration is stored in `config.py`. Default settings:

```python
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
```

Modify these settings according to your environment.

## Project Structure

```
mqtt-monitoring-system/
├── requirements.txt
├── config.py
├── client.py
├── server.py
└── README.md
```

## Running the Application

1. Start the server:
```bash
python server.py
```
This will:
- Start the FastAPI server on port 8000
- Begin consuming messages from RabbitMQ
- Store messages in MongoDB

2. In a separate terminal, start the client:
```bash
python client.py
```
This will start emitting status messages every second.

## API Usage

The server provides an endpoint to query status counts within a specified time range.

### Endpoint: GET /status-count

**Parameters:**
- `start_time`: Start timestamp in ISO format
- `end_time`: End timestamp in ISO format

**Example Request:**
```bash
curl "http://localhost:8000/status-count?start_time=2024-12-10T10:21:45Z&end_time=2024-12-10T11:21:45Z"
```

**Example Response:**
```json
{
    "0": 180,
    "1": 165,
    "2": 170,
    "3": 175,
    "4": 160,
    "5": 150,
    "6": 155
}
```

## Message Format

The client emits messages in the following format:
```json
{
    "status": <integer 0-6>,
    "timestamp": <ISO format timestamp>
}
```

## Features

- Random status generation (0-6) every second
- Real-time message processing
- Message persistence in MongoDB
- RESTful API for data retrieval
- Time-range based status count aggregation
- Proper error handling and connection management

## Error Handling

The API will return appropriate error messages for:
- Invalid datetime formats
- Connection issues
- Processing errors

Example error response:
```json
{
    "detail": "Invalid datetime format. Use ISO format (e.g., 2024-01-01T00:00:00Z)"
}
```
