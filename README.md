# proyecto-uni-python


Proyecto "Hotel California"

![image](https://user-images.githubusercontent.com/103605757/211127311-48a10d94-011c-45e3-bf91-f003cc185e2d.png)
Versión del proyecto dado a los alumnos de la materia Fundamentos de la Programación, de la carrera de LSI de los alumnos
Consignas
1. Para ser huésped del hotel debe ser mayor de edad (>18 años).
Cada huésped puede venir solo o acompañado por varias personas.
2. Un huésped puede solicitar la reserva de una o varias habitaciones.
Al momento de hacer una reserva, se debe verificar la disponibilidad de habitaciones para un rango de fecha determinado y para la cantidad de personas solicitadas, mostrando al usuario una lista de habitaciones disponibles en caso de que lo hubiera

El usuario seleccionará de la lista aquellas habitaciones que desea reservar.

3. Se toman los datos necesarios para la reserva, como las fechas desde y hasta, el tipo de cada habitación y los datos del huésped.
En caso de no haber disponibilidad del tipo de habitación solicitado se puede:

Verificar si no se cuenta con una habitación de un tipo superior disponible.
En ese caso, se procede a la reserva. Por ejemplo: Se solicita una habitación doble y no se cuenta con disponibilidad de habitaciones dobles, se procede a reservar una habitación triple.

En caso de que no haya más habitaciones disponibles, se debe generar una cola de espera.
Esta cola debe contener el DNI del huésped, el tipo de habitación solicitado y las fechas de la reserva.

4. Las reservas pueden ser canceladas en cualquier momento.
En caso de cancelarse una reserva, se debe verificar la cola de reservas.
5. Cuándo el huésped se presenta en el hotel (check-in), se toman los datos de todos sus acompañantes y se marca la habitación como ocupada.
6. Durante la estadía los huéspedes pueden cargar a la habitación una serie de servicios ofrecidos por el hotel (frigobar, room-service, lavandería, bar, spa, gimnasio) los cuales serán cobrados al momento del retiro.
7. Cuando un huésped se retira del hotel (check-out), se procede a emitir la factura de la estadía.
Para eso se debe calcular los días que se hospedó en el hotel y verificar el precio de la/s habitación/es ocupadas.

Para esto se debe usar el módulo días_de_estadía provisto por la cátedra.

La factura debe contener los datos del huésped (nombre, apellido, DNI, domicilio), los datos de la estadía y servicios utilizados con su precio total, según se detalla en el modelo a continuación.

8. Todos los días se debe contar con:
Un listado de los huéspedes que tienen reservas para ese día, ordenado por número de habitación

Un listado de todos los menores de edad que están ocupando el hotel en ese momento, junto con los datos del huésped a cargo y el número de habitación que ocupan, ordenado por Apellido y Nombre. Este listado se presenta en la policía para control de personas desaparecidas.

Un mapa de ocupación de todas las habitaciones del hotel.

Un proceso que permita facturar un día de estadía para las reservas no efectivizadas.

Se debe aplicar Caja Negra en las altas de datos
