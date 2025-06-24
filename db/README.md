# MongoDB Integration Module

This module provides a simple interface for interacting with MongoDB in the AI Bootcamp project.

## Features

- Connect to MongoDB using a connection string
- Add messages to the database with role, text, and timestamp
- Retrieve the most recent messages from the database
- Automatic connection management in the FastAPI server

## Usage

### Initialization

```python
from db import MongoDBClient

# Initialize with connection string from environment variable
client = MongoDBClient()

# Or provide a connection string directly
client = MongoDBClient(connection_string="mongodb://username:password@host:port/database")
```

### Connecting to the Database

```python
# Connect to the default database (chat_db) and collection (messages)
client.connect()

# Or specify a custom database and collection
client.connect(db_name="my_database", collection_name="my_collection")
```

### Adding Messages

```python
# Add a user message
message_id = client.add_message(role="user", text="Hello, how are you?")

# Add a system message
message_id = client.add_message(role="system", text="I'm doing well, thank you!")
```

### Retrieving Messages

```python
# Get the 10 most recent messages
messages = client.get_recent_messages()

# Or specify a custom limit
messages = client.get_recent_messages(limit=20)
```

### Closing the Connection

```python
# Close the connection when done
client.close()
```

## Message Schema

Each message in the database has the following fields:

- `_id`: MongoDB ObjectId (converted to string as `id` in the API response)
- `role`: String, either "user" or "system"
- `text`: String, the message content
- `date`: DateTime, when the message was created

## Integration with FastAPI

The MongoDB client is integrated with the FastAPI server in `server.py`. The server:

1. Initializes the MongoDB client at startup
2. Connects to the database
3. Provides endpoints for adding and retrieving messages
4. Closes the connection on shutdown

### API Endpoints

- `GET /api/chat`: Retrieves the 10 most recent messages
- `POST /api/chat/message`: Adds a new message to the chat

## Error Handling

The MongoDB client includes error handling for:

- Missing connection string
- Invalid role values
- Connection failures
- Database operation failures

## Testing

Tests for the MongoDB client are available in `tests/test_mongodb.py`. Run the tests with:

```bash
python -m unittest tests/test_mongodb.py
```