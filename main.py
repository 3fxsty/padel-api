import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

pistas = {1: {"id": 1, "nombre": "Alpha", "tipo": "Interior"}, 2: {"id": 2, "nombre": "Beta", "tipo": "Exterior"}, 3: {"id": 3, "nombre": "Cabo", "tipo": "Interior"}}

reservas = {}

class Reserva(BaseModel):
    username: str
    day: datetime.date
    hour: datetime.time
    pista: int

contador_reservas: int = 0

@app.get("/pistas")
async def root():
    list_pistas = list(pistas.values())
    return list_pistas

@app.get("/pistas/{pista_id}")
async def get_pista_id(pista_id: int):
    if pistas.get(pista_id) is None:
        raise HTTPException(status_code=404, detail=("No se ha encontrado la pista que buscas."))

    return pistas.get(pista_id)

app.get("/reservas")
async def get_reservas():
    list_resrvas = list(reservas.values())
    return list_resrvas

@app.post("/reservas", status_code=201)
async def crear_reserva(reserva: Reserva):
    datos = reserva.model_dump()

    if datos["pista"] in pistas:
        global contador_reservas
        contador_reservas += 1
        datos["id"] = contador_reservas
        reservas[contador_reservas] = datos

        return datos

    else:
        raise HTTPException(status_code=404, detail="No encontramos esa pista.")


# @app.get("/reservas/")