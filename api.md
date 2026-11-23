Esta api sirve para ver el horario de pistas de padel de un club, se podra hacer reservas y cancelarlas, ver si las pistas estan libres u ocupadas...


## Criterios
- Datos mal rellenados (falta un campo, formato incorrecto): 422, lo pone FastAPI solo.
- Datos bien rellenados pero que rompen una regla del club: 422.
- Choque con algo que ya existe (hueco ocupado, reserva ya cancelada): 409.
- Fechas en formato AAAA-MM-DD.
- Cancelar una reserva = se borra la reserva.

GET /pistas
- 200: devuelve las pistas / te devuelve una lista vacia (no hay pistas)

GET /pistas/{id}
- 200: devuelve los datos de la pista (id, nombre, tipo)
- 404: la pista no existe

GET /pistas/{id}/horas?fecha=x
- 404: no se encuentra la pista
- 200: devuelve las horas libres para una pista de una fecha (horas)

POST /reservas
- 201: crea la reserva (id reserva, nombre, fecha, hora, pista)
- 422: has puesto algun dato mal (fuera del horario / fecha ya pasada)
- 409: has intentado una reserva en una hora ocupada
- 404: has reservado en una pista que no existe

GET /reservas?fecha=x
- 422: has puesto un campo mal (fecha)
- 200: devuelve las reservas de x fecha

DELETE /reservas/{id}
- 204: cancelas la reserva
- 404: no se encuentra la reserva
- 422: no cumple los criterios para cancelar la reserva (plazo de 24h pasado)