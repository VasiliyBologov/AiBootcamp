# AI Bootcamp Project Guidelines

This document provides guidelines and information for developers working on the AI Bootcamp project.

## Build/Configuration Instructions

### Prerequisites
- Python 3.10 or higher
- Docker (for containerized deployment)
- MongoDB (for the MCP server)

### Environment Setup
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root with the following variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   MDB_MCP_CONNECTION_STRING=your_mongodb_connection_string
   ```

### Running the Application
#### Local Development
1. Start the FastAPI server:
   ```bash
   python server.py
   ```
   This will start the server on http://localhost:8080

2. To run the AI agent with MongoDB integration:
   ```bash
   python main.py
   ```

#### Docker Deployment
1. Build the Docker image:
   ```bash
   docker build -t aibootcamp:latest .
   ```

2. Run the container:
   ```bash
   docker run -p 8080:8080 -e OPENAI_API_KEY=your_key -e MDB_MCP_CONNECTION_STRING=your_connection_string aibootcamp:latest
   ```

## Testing Information

### Test Structure
- Tests are located in the `tests` directory
- The project uses FastAPI's TestClient for API testing

### Running Tests
To run all tests:
```bash
python -m pytest tests/
```

To run a specific test file:
```bash
python tests/test_server.py
```

### Adding New Tests
1. Create a new test file in the `tests` directory
2. Import the necessary modules and the application:
   ```python
   from fastapi.testclient import TestClient
   import sys
   import os
   
   # Add the parent directory to the path so we can import the server module
   sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
   
   from server import app
   
   client = TestClient(app)
   ```
3. Write test functions that use the TestClient to make requests to the API:
   ```python
   def test_example():
       response = client.get("/example-endpoint")
       assert response.status_code == 200
       assert response.json() == {"expected": "response"}
   ```

### Test Example
Here's an example of testing the server endpoints:

```python
def test_root_endpoint():
    """Test that the root endpoint returns a 200 status code and HTML content."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<h1>Welcome to the Simple FastAPI Server</h1>" in response.text

def test_ask_endpoint():
    """Test that the /ask endpoint returns a 200 status code and the expected JSON response."""
    response = client.get("/ask")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

## Additional Development Information

### Project Structure
- `client/` - Frontend web application (HTML, CSS, JavaScript)
- `mcps/` - Model Control Protocol (MCP) servers for integrating with MongoDB
- `tests/` - Test files
- `main.py` - Entry point for the AI agent application
- `server.py` - FastAPI server for the web application
- `Dockerfile` - Container configuration for deployment

### AI Agent Integration
The project uses OpenAI's agent framework to create an AI assistant that can interact with MongoDB. The agent is configured in `main.py` and uses the MCP server to communicate with MongoDB.

### Client-Server Communication
The client communicates with the server through two API endpoints:
- `GET /api/chat` - Fetch conversation history
- `POST /api/chat/message` - Send new message

### Code Style Guidelines
- Follow PEP 8 for Python code
- Use docstrings for functions and classes
- Keep functions small and focused on a single responsibility
- Use type hints for function parameters and return values

### Debugging
- For FastAPI server issues, check the server logs
- For AI agent issues, check the trace ID and view the trace in the OpenAI platform
- For MongoDB issues, check the MCP server logs

### Adding New Features
1. For new API endpoints, add them to `server.py`
2. For new client features, modify the files in the `client/` directory
3. For new AI agent capabilities, modify `main.py` or add new MCP servers in the `mcps/` directory
4. Always add tests for new features