import uvicorn


if __name__ == '__main__':
    uvicorn.run("server:app", reload=False,
                    host="localhost", port=8000, log_level="info")
