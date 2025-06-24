import os
import datetime
from typing import List, Dict, Any, Optional
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from bson import ObjectId

class MongoDBClient:
    """
    A client for interacting with MongoDB.
    Provides methods for connecting to the database and performing CRUD operations.
    """
    
    def __init__(self, connection_string: Optional[str] = None):
        """
        Initialize the MongoDB client.
        
        Args:
            connection_string: MongoDB connection string. If not provided, it will be read from the environment variable.
        """
        self.connection_string = connection_string or os.environ.get("MDB_MCP_CONNECTION_STRING")
        if not self.connection_string:
            raise ValueError("MongoDB connection string not provided and not found in environment variables")
        
        self.client = None
        self.db = None
        self.messages_collection = None
    
    def connect(self, db_name: str = "giter_users", collection_name: str = "chat") -> None:
        """
        Connect to the MongoDB database and initialize the messages collection.

        Args:
            db_name: Name of the database to connect to
            collection_name: Name of the collection to use for messages
        """
        self.client = MongoClient(self.connection_string)
        self.db = self.client[db_name]
        self.messages_collection = self.db[collection_name]
        
        # Create indexes if they don't exist
        self.messages_collection.create_index("date", background=True)
    
    def close(self) -> None:
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()
    
    def add_message(self, role: str, text: str) -> str:
        """
        Add a new message to the database.
        
        Args:
            role: The role of the message sender (user or system)
            text: The message text
            
        Returns:
            The ID of the inserted message
        """
        # if not self.messages_collection:
        #     raise RuntimeError("Not connected to MongoDB. Call connect() first.")
        
        # Validate role
        if role not in ["user", "system"]:
            raise ValueError("Role must be either 'user' or 'system'")
        
        # Create message document
        message = {
            "role": role,
            "text": text,
            "date": datetime.datetime.utcnow()
        }
        
        # Insert the message
        result = self.messages_collection.insert_one(message)
        return str(result.inserted_id)
    
    def get_recent_messages(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get the most recent messages from the database.
        
        Args:
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of message documents
        """
        if not self.messages_collection:
            raise RuntimeError("Not connected to MongoDB. Call connect() first.")
        
        # Query for the most recent messages
        cursor = self.messages_collection.find().sort("date", -1).limit(limit)
        
        # Convert ObjectId to string for JSON serialization
        messages = []
        for message in cursor:
            message["id"] = str(message.pop("_id"))
            messages.append(message)
        
        # Return messages in chronological order (oldest first)
        return list(reversed(messages))
    
    @property
    def is_connected(self) -> bool:
        """Check if the client is connected to MongoDB."""
        return self.client is not None and self.db is not None and self.messages_collection is not None