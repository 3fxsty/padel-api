from fastapi import FastAPI, HTTPException

app = FastAPI()

pistas = {1: {"id": 1, "nombre": "Alpha", "tipo": "Interior"}, 2: {"id": 2, "nombre": "Beta", "tipo": "Exterior"}, 3: {"id": 3, "nombre": "Cabo", "tipo": "Interior"}}


@app.get("/pistas")
async def root():
    list_pistas = list(pistas.values())
    return list_pistas

@app.get("/pistas/{pista_id}")
async def pista_id(pista_id: int):
    if pistas.get(pista_id) is None:
        raise HTTPException(status_code=404, detail=("No se ha encontrado la pista que buscas."))

    return pistas.get(pista_id)
