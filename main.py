from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"mensaje": "API funcionando correctamente"}

@app.get("/usuarios")
def usuarios():
    return [{"id": 1, "nombre": "Ariel"}]