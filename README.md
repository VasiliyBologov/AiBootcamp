# How run docker mongodb mcp

    for use "mongodb_mcp_server:latest"

* go to `/mcps/mcp-mongj/mongodb-mcp-server`
* open in terminal
* git clone https://github.com/mongodb-js/mongodb-mcp-server
* run: `sudo docker build -t mongodb_mcp_server . -f Dockerfile`

------------------------

# Simple FastAPI Server

A simple REST server built with FastAPI that includes two endpoints:
- `/`: Returns a simple HTML page
- `/ask`: Returns a JSON response with status "ok"

## Setup without Docker

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Run the server:
   ```
   python server.py
   ```

   Alternatively, you can use uvicorn directly:
   ```
   uvicorn server:app --reload
   ```

3. Access the endpoints:
   - Open your browser and navigate to `http://localhost:8080/` for the HTML page
   - Navigate to `http://localhost:8080/ask` for the JSON response

## Docker Setup

### Building the Docker Image

To build the Docker image, run the following command in the project directory:

```bash
docker build -t fastapi-server .
```

### Running the Docker Container

To run the Docker container:

```bash
docker run -p 8080:8080 fastapi-server
```

This will start the server and map port 8080 from the container to port 8080 on your host machine.

### Accessing the Server

Once the container is running, you can access the server at:
- `http://localhost:8080/` for the HTML page
- `http://localhost:8080/ask` for the JSON response
