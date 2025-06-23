from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Simple FastAPI Server</title>
        </head>
        <body>
            <h1>Welcome to the Simple FastAPI Server</h1>
            <p>This is a simple HTML page served by FastAPI.</p>
        </body>
    </html>
    """
    return html_content

@app.get("/ask")
async def ask():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)