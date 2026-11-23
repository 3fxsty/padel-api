# padel-api

API REST para gestionar las reservas de las pistas de un club de pádel, hecha con Python y FastAPI.

Es un proyecto de aprendizaje: la he diseñado y programado desde cero para practicar los fundamentos del desarrollo backend (HTTP, diseño de APIs REST, códigos de estado, validación de datos y reglas de negocio).

## Qué se puede hacer

- Ver todas las pistas del club y los datos de una pista concreta.
- Consultar las horas libres de una pista en una fecha.
- Reservar una pista a una hora.
- Ver todas las reservas de un día.
- Cancelar una reserva.

## Reglas del club

- Hay 3 pistas, cada una con nombre y tipo (interior o exterior).
- El club abre de 9:00 a 22:00. Las reservas son de 1 hora y empiezan en punto (la última, a las 21:00).
- No se puede reservar un hueco ocupado, fuera de horario, en el pasado ni en una pista que no existe.
- Una reserva no se puede cancelar si faltan menos de 24 horas. Al cancelarla, se borra.
- Las fechas y horas se envían sin zona horaria y se entienden en hora de Madrid (Europe/Madrid).

## Endpoints

| Método | Ruta | Qué hace |
| --- | --- | --- |
| GET | `/pistas` | Lista todas las pistas |
| GET | `/pistas/{pista_id}` | Devuelve una pista |
| GET | `/pistas/{pista_id}/horas?fecha=AAAA-MM-DD` | Horas libres de una pista en una fecha |
| POST | `/reservas` | Crea una reserva |
| GET | `/reservas?fecha=AAAA-MM-DD` | Reservas de un día |
| DELETE | `/reservas/{reserva_id}` | Cancela una reserva |

El detalle de cada ruta (qué recibe, qué devuelve y sus errores) está en [api.md](api.md).

## Cómo arrancarla

Necesitas Python 3.13 o superior y [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run fastapi dev main.py
```

Con el servidor en marcha, abre http://127.0.0.1:8000/docs para ver y probar la API desde el navegador.

## Limitaciones

- Los datos se guardan en memoria: al reiniciar el servidor se pierden las reservas.
- No hay usuarios ni login: cualquiera puede cancelar cualquier reserva si conoce su id.

## Próximos pasos

- Guardar los datos en una base de datos.
- Tests automáticos.
- Usuarios y login.
- Docker.