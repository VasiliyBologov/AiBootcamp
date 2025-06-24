import os
import sys
import unittest
from datetime import datetime

# Add the parent directory to the path so we can import the db module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import MongoDBClient

class TestMongoDBClient(unittest.TestCase):
    """Test the MongoDBClient class"""
    
    def setUp(self):
        """Set up the test environment"""
        # Create a test database name with timestamp to avoid conflicts
        self.test_db_name = f"test_db_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.client = MongoDBClient()
        self.client.connect(db_name=self.test_db_name)
    
    def tearDown(self):
        """Clean up after the tests"""
        if self.client.is_connected:
            # Drop the test database
            self.client.db.drop_collection("messages")
            self.client.close()
    
    def test_connection(self):
        """Test that the client can connect to MongoDB"""
        self.assertTrue(self.client.is_connected)
        self.assertIsNotNone(self.client.db)
        self.assertIsNotNone(self.client.messages_collection)
    
    def test_add_message(self):
        """Test adding a message to the database"""
        # Add a test message
        message_id = self.client.add_message(role="user", text="Test message")
        
        # Verify that the message was added
        self.assertIsNotNone(message_id)
        
        # Retrieve the message directly from the collection
        message = self.client.messages_collection.find_one({"_id": self.client.messages_collection.database.command('convertToBSON', {'$oid': message_id})["_id"]})
        
        # Verify the message fields
        self.assertIsNotNone(message)
        self.assertEqual(message["role"], "user")
        self.assertEqual(message["text"], "Test message")
        self.assertIsNotNone(message["date"])
    
    def test_get_recent_messages(self):
        """Test retrieving recent messages"""
        # Add some test messages
        for i in range(15):
            role = "user" if i % 2 == 0 else "system"
            self.client.add_message(role=role, text=f"Test message {i}")
        
        # Retrieve the most recent messages (default limit is 10)
        messages = self.client.get_recent_messages()
        
        # Verify that we got the expected number of messages
        self.assertEqual(len(messages), 10)
        
        # Verify that the messages are in chronological order (oldest first)
        for i in range(1, len(messages)):
            self.assertLessEqual(messages[i-1]["date"], messages[i]["date"])
        
        # Verify that each message has the expected fields
        for message in messages:
            self.assertIn("id", message)
            self.assertIn("role", message)
            self.assertIn("text", message)
            self.assertIn("date", message)
            self.assertIn(message["role"], ["user", "system"])
            self.assertTrue(message["text"].startswith("Test message"))

if __name__ == "__main__":
    unittest.main()