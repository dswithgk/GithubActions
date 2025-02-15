from fastapi import FastAPI
import socket
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

@app.get("/ip")
def read_ip():
    return {"ip": socket.gethostbyname(socket.gethostname())}