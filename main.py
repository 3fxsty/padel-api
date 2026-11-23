from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

pistas = {1: {"id": 1, "nombre": "Alpha", "tipo": "Interior"}, 2: {"id": 2, "nombre": "Beta", "tipo": "Exterior"}, 3: {"id": 3, "nombre": "Cabo", "tipo": "Interior"}}

reservas = {}

apertura = time(9, 0)
cierre = time(22, 0)
hoy = date.today()
zona = ZoneInfo("Europe/Madrid")

class Reserva(BaseModel):
    username: str
    date: datetime = Field(
        examples=["2026-11-23T16:00:00"]
    )
    pista: int = 1

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

@app.get("/pistas/{pista_id}/horas")
async def get_horas_libres_fecha(pista_id: int, fecha: date):
    horas_ocupadas = []
    horas_libres = []

    if pistas.get(pista_id) is None:
        raise HTTPException(status_code=404, detail=("No se ha encontrado la pista que buscas."))

    if fecha < date.today():
        raise HTTPException(status_code=422, detail="La fecha introducida ha pasado ya.")

    for r in reservas.values():
        if r["pista"] == pista_id and r["date"].date() == fecha:
            horas_ocupadas.append(r["date"].hour)
    
    for hora in range(apertura.hour, cierre.hour):
        if hora not in horas_ocupadas:
            horas_libres.append(hora)

    return horas_libres

@app.get("/reservas")
async def get_reservas_fecha(fecha: date):

    reservas_fecha = []

    for r in reservas.values():
        if fecha == r["date"].date():
            reservas_fecha.append(r)

    return reservas_fecha


@app.post("/reservas", status_code=201)
async def crear_reserva(reserva: Reserva):
    datos = reserva.model_dump()
    pista = reserva.pista
    hora = reserva.date.time()
    fecha = reserva.date
    fecha = fecha.replace(tzinfo=zona)

    if pista not in pistas:
        raise HTTPException(status_code=404, detail="No encontramos esa pista.")

    if hora >= cierre or hora < apertura:
        raise HTTPException(status_code=422, detail="Hora fuera del horario permitido.")

    if hora.minute != 0 or hora.second != 0 or hora.microsecond != 0:
        raise HTTPException(status_code=422, detail="Solo se pueden hacer reservas en punto. (16:00, 17:00, 18:00 ...)")

    if fecha < datetime.now(zona):
        raise HTTPException(status_code=422, detail="No se puede hacer una reserva en pasado.")

    for r in reservas.values():
        if fecha == r["date"] and pista == r["pista"]:
            raise HTTPException(status_code=409, detail="No se puede hacer una reserva en un hueco ocupado.")

    global contador_reservas
    contador_reservas += 1
    datos["id"] = contador_reservas
    reservas[contador_reservas] = datos
    datos["date"] = fecha

    return datos

@app.delete("/reservas/{reserva_id}", status_code=204)
async def delete_reserva(reserva_id: int):
    now = datetime.now(zona)
    r = reservas.get(reserva_id)

    if r is None:
        raise HTTPException(status_code=404, detail="No se ha encontrado ninguna reserva con ese id.")

    if (r["date"] - now) < timedelta(hours=24):
        raise HTTPException(status_code=422, detail="Quedan menos de 24h para la reserva.")

    reservas.pop(reserva_id)